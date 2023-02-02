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
    answers = list(Word.objects.question_options(word, wordlist)[:options-1])
    answers.append(word)
    random.shuffle(answers)
    return answers

def has_next_question(request):
    if request.session['game']:
        return request.session['game'][0]
    return 0

def next_question(request):
    list_id = request.session['game_config']['list_id']
    question = get_object_or_404(Word, id=has_next_question(request))
    word_list = get_object_or_404(WordList, id=list_id)
    score = Score.objects.by_user_and_word(request.user, question)
    if score:
        score.shown += 1
        score.save()
    option_c = request.session['game_config']['options']
    game_mode = get_game_mode(request)
    question = {
        'word': question,
        'label': get_word_label(question, game_mode[0]),
        'answers': [
            {'label': get_word_label(answer, game_mode[1]), 'word': answer} 
            for answer in get_answers(question, word_list, option_c)
            ]
    }
    if 'timer' in request.session['game_config']:
        question['timer'] = request.session['game_config'].get('timer','')
    return question

def score_test(request, question, grade):
    if request.user.is_authenticated:
        score = Score.objects.by_user_and_word(request.user, question)
        if grade=='correct':
            score.correct += 1
            request.user.tests_passed += 1
        else:
            score.wrong += 1
        score.save()
        request.user.save()

def remove_first_question(request):
    new_list = request.session['game']
    del new_list[0]
    request.session['game'] = new_list

def check(request, question, answer):
    expected = request.session['game'][0]
    if question.id != expected:
        return 'cheat'
    if question.id != getattr(answer, 'id', 0):
        grade = 'wrong'
    else:
        grade = 'correct'
    score_test(request, question, grade)
    remove_first_question(request)
    return grade
    