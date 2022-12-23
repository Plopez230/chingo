from django.forms import ModelForm
from .models import Word, WordList

class WordForm(ModelForm):
    class Meta:
        model = Word
        fields = [
            'simplified',
            'traditional',
            'pinyin',
            'classifier',
            'translation',
            'part_of_speech'
            ]

class WordListForm(ModelForm):
    class Meta:
        model = WordList
        fields = [
            'name',
            'description',
            'image'
            ]