from .models import *
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

def score_test(user):
    user.tests_passed += 1
    user.save()

def search_words(keyword):
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
    kw = {}
    for k, v in keywords.items():
        if v == '':
            kw[k] = 'No keyword provided'
        else:
            kw[k] = v
    suggestions = Word.objects.filter(
        Q(simplified__icontains=kw['simplified'])
        | Q(traditional__icontains=kw['traditional'])
        | Q(pinyin__icontains=kw['pinyin'])
        | Q(translation__icontains=kw['translation'])
        | Q(part_of_speech__exact=kw['part_of_speech'])
        | Q(classifier__icontains=kw['classifier'])
    )
    return [{'label':str(word) , 'id':word.id} for word in suggestions]

game_config = {
    'words': [],
    'game_modes': [],
    'number_of_options': 5
}

test = {
    'question': {
        'word': 0,
        'label': '',
    },
    'options': []
}


def timestamp_question(user, word):
    if user.is_authenticated():
        score = Score.objects.filter(
            Q()
        ) 

def timestamp_answer(user, word):
    if user.is_authenticated():
        pass 

def get_option_list(word, max_options=5):
    if max_options < 2:
        max_options = 2
    queryset = Word.objects.filter(
        ~Q(simplified__icontains=word.simplified)
        & ~Q(pinyin__icontains=word.pinyin)
    ).order_by("?")[0:max_options - 1]
    options = list(queryset)
    options.append(word)
    random.shuffle(options)
    return options 

class GameModes(Enum):
    SIMP_PINY = 1
    SIMP_TRAN = 2
    PINY_SIMP = 3
    PINY_TRAN = 4
    TRAN_SIMP = 5
    TRAN_PINY = 6

def get_game_mode(game_config):
    modes = game_config.get('game_modes', None)
    if not modes or not isinstance(modes, list) or len(modes) == 0:
        modes = [game_mode.value for game_modes in GameModes]
    random.shuffle(modes)
    return modes[0]

def get_next_word(game_config):
    words = game_config.get('words', None)
    word = None
    if words and isinstance(words, list) and len(words) > 0:
        word = words[0]
        words.pop(0)
    return word

def generate_test(user, game_config):
    question = get_next_word(game_config)
    mode = get_game_mode(game_config)
    options = get_option_list(question)
    timestamp_question(user, question)
    test = {
        'question': question, 'mode': mode, 'options': options
    }
    return test

def check_test(user, game_config, question, option):
    pass
    #()read game_config
    #()check the answer from post parameters
    #(Authenticated)checks answer timestamp:
    #(Authenticated)    save results
    #(Authenticated)else:
    #(Authenticated)    +1000 points?