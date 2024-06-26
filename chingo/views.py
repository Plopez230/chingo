from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from .forms import *
from .utils import split_columns, sing
from . import chingo_game as game
from .pinyin_marker import mark_text
from django.db.models import Count, Sum, Prefetch, Q

# Create your views here.
def index_view(request):
    template = loader.get_template('chingo/index.html')
    context = {
        'lists': split_columns(WordList.objects.with_word_count()),
        'worst_scores': Score.objects.worst_scores(request.user)[:6],
        }
    return HttpResponse(template.render(context, request))

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect(reverse('chingo:index'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
        })

def sing_view(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    filename = sing(word)
    file = None
    file = open(filename, "rb").read()
    response = HttpResponse(file, content_type="audio/mpeg")
    response['Content-Disposition'] = 'attachment; filename=espeak.mp3' 
    return response

def search_view(request):
    template = loader.get_template('chingo/search.html')
    keyword = request.GET.get("keyword")
    keyword = mark_text(keyword)
    user = request.user
    context = {
        'lists': WordList.objects.search(keyword),
        'words': Word.objects.search(keyword),
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
    if not game.has_next_question(request):
        return redirect(reverse('chingo:index'))
    template = loader.get_template('chingo/test.html')
    question = game.next_question(request)
    context = {
        'question': question,
        'score': Score.objects.by_user_and_word(request.user, question['word'])
    }
    return HttpResponse(template.render(context, request))

@require_http_methods(["POST"])
def practice(request):
    config_form = GameConfigForm(request.POST)
    config_form.is_valid()
    game.game_init(request, config_form.cleaned_data)
    return redirect(reverse('chingo:test'))

@require_http_methods(["POST"])
def test_check_view(request):
    template = loader.get_template('chingo/test_check.html')
    test_form = TestForm(request.POST)
    test_form.is_valid()
    grade = game.check(request, **test_form.cleaned_data)
    context = {
        'grade': grade,
        'question': test_form.cleaned_data['question'],
        'score': Score.objects.by_user_and_word(
            request.user, 
            test_form.cleaned_data['question']
            )
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
        new_word = form.save(creator=request.user)
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
        'lists': split_columns(WordList.objects.all()),
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
    wordform.is_valid()
    suggestions = [
        {'label':str(word) , 'id':word.id} 
        for word in Word.objects.suggestions(**wordform.cleaned_data)
        ] 
    return JsonResponse(suggestions, safe=False)