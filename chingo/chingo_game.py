from .models import *
from .pinyin_marker import mark_text
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from enum import Enum
import random

def score_word(user, word):
    user.words_included += 1
    word.creator = user
    word.save()
    user.save()

def score_list(user, wordlist):
    user.lists_created += 1
    wordlist.owner = user
    wordlist.save()
    user.save()

def search_words(keyword, user):
    if not keyword or keyword == "":
        return []
    queryset = Word.objects.filter(
        Q(simplified__icontains=keyword)
        | Q(traditional__icontains=keyword)
        | Q(pinyin__icontains=keyword)
        | Q(translation__icontains=keyword)
        )
    return queryset

def search_lists(keyword):
    if not keyword or keyword == "":
        return []
    queryset = WordList.objects.filter(
        Q(name__icontains=keyword)
        | Q(description__icontains=keyword)
        )
    return queryset

def word_suggestions(keywords):
    q = Q(pk=None)
    if keywords['simplified']:
        q = q | Q(simplified__icontains=keywords['simplified'])
    if keywords['traditional']:
        q = q | Q(traditional__icontains=keywords['traditional'])
    if keywords['pinyin']:
        q = q | Q(pinyin__icontains=mark_text(keywords['pinyin']))
    if keywords['translation']:
        q = q | Q(translation__icontains=keywords['translation'])
    if keywords['classifier']:
        q = q | Q(classifier__icontains=keywords['classifier'])
    suggestions = Word.objects.filter(q)
    return [{'label':str(word) , 'id':word.id} for word in suggestions]

def game_init(request, game_config):
    list_id = game_config.get('list_id', '')
    wordlist = get_object_or_404(WordList, id=list_id)
    questions = [word.id for word in wordlist.words.all()]
    random.shuffle(questions)
    request.session['game'] = questions
    request.session['game_config'] = game_config

game_modes = {
    'simplified_translation': ('s', 't'),
    'simplified_pinyin': ('s', 'p'),
    'pinyin_translation': ('p', 't'),
    'pinyin_simplified': ('p', 's'),
    'translation_simplified': ('t', 's'),
    'translation_pinyin': ('t', 'p')
}

def get_game_mode(request):
    game_config = request.session['game_config']
    selected_modes = [
        key for key, value in game_config.items() if (value == True and not key in ['list_id', 'timer'])
    ]
    if selected_modes:
        game_mode = random.choice(selected_modes)
    else:
        game_mode = random.choice(list(game_modes.items()))[0]
    return game_modes[game_mode]

def get_word_label(word, mode):
    if mode == 's':
        return word.simplified
    if mode == 'p':
        return word.pinyin
    if mode == 't':
        return word.translation

def get_answers(word, wordlist, options):
    queryset = wordlist.words.exclude(
        Q(id__exact=word.id)
        | Q(translation__icontains=word.translation)
        | Q(pinyin__icontains=word.pinyin)
        ).order_by('?')[:options-1]
    answers = list(queryset)
    answers.append(word)
    random.shuffle(answers)
    return answers

def next_question(request):
    question_id = request.session['game'][0]
    list_id = request.session['game_config']['list_id']
    question = get_object_or_404(Word, id=question_id)
    if request.user.is_authenticated:
        score, created = Score.objects.get_or_create(
            player=request.user,
            word=question,
        )
        score.shown += 1
        score.save()
    word_list = get_object_or_404(WordList, id=list_id)
    option_c = request.session['game_config'].get('options','')
    game_mode = get_game_mode(request)
    question = {
        'word': question,
        'label': get_word_label(question, game_mode[0]),
        'answers': [
            {'label': get_word_label(answer, game_mode[1]), 'word': answer} 
            for answer in get_answers(question, word_list, option_c)
            ]
    }
    if request.session['game_config'].get('timer',''):
        question['timer'] = request.session['game_config'].get('timer','')
    return question

def score_test(request, question, grade):
    question = get_object_or_404(Word, id=question)
    if request.user.is_authenticated:
        score = question.scores.filter(player=request.user)[0]
        if grade=='correct':
            score.correct += 1
            request.user.tests_passed += 1
        else:
            score.wrong += 1
        score.save()
        request.user.save()

def check(request, question, answer):
    question = int(request.POST.get('question_id', -1))
    answer = int(request.POST.get('answer_id', -1))
    expected = request.session['game'][0]
    if question != expected:
        return 'cheat'
    if question != answer:
        grade = 'wrong'
    else:
        grade = 'correct'
    score_test(request, question, grade)
    new_list = request.session['game']
    del new_list[0]
    request.session['game'] = new_list
    return grade
    