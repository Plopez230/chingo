from .models import *
from django.db.models import Prefetch, Q


def score_word(user):
    user.words_included += 1
    user.save()

def score_list(user, list):
    user.lists_created += 1
    list.owner = user
    list.save()
    user.save()

def score_test(user):
    user.tests_passed += 1
    user.save()

def search_characters(keyword):
    if keyword == "":
        return []
    queryset = Word.objects.filter(
        Q(simplified__icontains=keyword)
        | Q(traditional__icontains=keyword)
        | Q(pinyin__icontains=keyword)
        | Q(translation__icontains=keyword)
        )
    return queryset

def search_lists(keyword):
    if keyword == "":
        return []
    queryset = WordList.objects.filter(
        Q(name__icontains=keyword)
        | Q(description__icontains=keyword)
        )
    return queryset