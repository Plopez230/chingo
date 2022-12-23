from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
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
    template = loader.get_template('chingo/test.html')
    context = {}
    return HttpResponse(template.render(context, request))

def test_check_view(request):
    template = loader.get_template('chingo/check_test.html')
    context = {"wrong": True}
    return HttpResponse(template.render(context, request))

def word_add_from_database_view(request, list_id, word_id):
    if request.method == "POST":
        word = get_object_or_404(Word, id=word_id)
        list = get_object_or_404(WordList, id=list_id)
        list.words.add(word)
    response = redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    return response

def word_add_view(request, list_id):
    word_list = get_object_or_404(WordList, pk=list_id)
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            new_word = form.save()
            word_list.words.add(new_word)
            game.score_word(request.user)
    response = redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    return response

def list_add_view(request):
    if request.method == "POST":
        form = WordListForm(request.POST)
        if form.is_valid():
            new_list = form.save()
            game.score_list(request.user, new_list)
    response = redirect(reverse('chingo:list', kwargs={'list_id':new_list.id}))
    return response

def word_remove_view(request, list_id, word_id):
    if request.method == "POST":
        word = get_object_or_404(Word, id=word_id)
        list = get_object_or_404(WordList, id=list_id)
        if list.words.contains(word):
            list.words.remove(word)
    response = redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    return response

def list_edit_view(request, list_id):
    word_list = get_object_or_404(WordList, pk=list_id)
    if request.method == "POST":
        form = WordListForm(request.POST, instance=word_list)
        if form.is_valid():
            new_word = form.save()
    response = redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    return response

def word_edit_view(request, list_id):
    if request.method == "POST":
        word_list = get_object_or_404(WordList, pk=list_id)
        word_id = request.POST.get("word_id")
        word = get_object_or_404(Word, pk=word_id)
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
    response = redirect(reverse('chingo:list', kwargs={'list_id':list_id}))
    return response