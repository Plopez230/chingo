from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import *
from .forms import *
from . import chingo_game as game

# Create your views here.
def index_view(request):
    template = loader.get_template('chingo/index.html')
    context = {
        'lists': WordList.objects.all(),
        'user': request.user,
        }
    return HttpResponse(template.render(context, request))

def search_view(request):
    template = loader.get_template('chingo/search.html')
    keyword = request.GET.get("keyword")
    context = {
        'lists': game.search_lists(keyword),
        'words': game.search_words(keyword),
        'user': request.user,
        }
    return HttpResponse(template.render(context, request))

def list_view(request, list_id):
    template = loader.get_template('chingo/list.html')
    current_list = get_object_or_404(WordList, id=list_id)
    context = {
        'list': current_list,
        'parts_of_speech': Word.PartOfSpeech.choices,
        'words': Word.objects.all()
    }
    return HttpResponse(template.render(context, request))

def test_view(request):
    if not request.session['game']:
        return redirect(reverse('chingo:index'))
    template = loader.get_template('chingo/test.html')
    question = game.next_question(request)
    score = question['word'].scores.filter(player=request.user)[0]
    context = {
        'question': question,
        'score': score
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def practice(request):
    config_form = GameConfigForm(request.POST)
    print(request.POST.keys())
    config_form.is_valid()
    game.game_init(request, config_form.cleaned_data)
    return redirect(reverse('chingo:test'))

@require_http_methods(["POST"])
def test_check_view(request):
    template = loader.get_template('chingo/test_check.html')
    question_id = request.POST.get('question_id', -1)
    question = get_object_or_404(Word, id=question_id)
    answer_id = request.POST.get('answer_id', -1)
    answer = get_object_or_404(Word, id=answer_id)
    grade = game.check(request, question, answer)
    context = {
        'grade': grade,
        'question': question,
        'answer': answer,
        'score': question.scores.filter(player=request.user)[0]
        }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def word_add_from_database_view(request, list_id, word_id):
    word = get_object_or_404(Word, id=word_id)
    list = get_object_or_404(WordList, id=list_id)
    list.words.add(word)
    response = redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    return response

@require_http_methods(["POST"])
def word_add_view(request, list_id):
    template = loader.get_template('chingo/list.html')
    word_list = get_object_or_404(WordList, pk=list_id)
    form = WordForm(request.POST)
    if form.is_valid():
        new_word = form.save()
        word_list.words.add(new_word)
        game.score_word(request.user, new_word)
        return redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    context = {
        'list': word_list,
        'parts_of_speech': Word.PartOfSpeech.choices,
        'words': Word.objects.all(),
        'word_add_form': form
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def list_add_view(request):
    template = loader.get_template('chingo/index.html')
    form = WordListForm(request.POST)
    if form.is_valid():
        new_list = form.save()
        game.score_list(request.user, new_list)
        return redirect(reverse('chingo:list', kwargs={'list_id':new_list.id}))
    context = {
        'lists': WordList.objects.all(),
        'user': request.user,
        'list_form': form,
        }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def word_remove_view(request, list_id, word_id):
    word = get_object_or_404(Word, id=word_id)
    list = get_object_or_404(WordList, id=list_id)
    if list.words.contains(word):
        list.words.remove(word)
    response = redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    return response

@require_http_methods(["POST"])
def list_edit_view(request, list_id):
    template = loader.get_template('chingo/list.html')
    word_list = get_object_or_404(WordList, pk=list_id)
    form = WordListForm(request.POST, instance=word_list)
    if form.is_valid():
        new_word = form.save()
        return redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    context = {
        'list': word_list,
        'parts_of_speech': Word.PartOfSpeech.choices,
        'words': Word.objects.all(),
        'list_edit_form': form
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def word_edit_view(request, list_id):
    template = loader.get_template('chingo/list.html')
    word_list = get_object_or_404(WordList, pk=list_id)
    word_id = request.POST.get("word_id")
    word = get_object_or_404(Word, pk=word_id)
    form = WordForm(request.POST, instance=word)
    if form.is_valid():
        form.save()
        return redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    context = {
        'list': word_list,
        'parts_of_speech': Word.PartOfSpeech.choices,
        'words': Word.objects.all(),
        'word_edit_form': form,
        'word_id': word_id
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def word_suggest_view(request):
    wordform = WordForm(request.POST)
    suggestions = game.word_suggestions(wordform.data)
    return JsonResponse(suggestions, safe=False)