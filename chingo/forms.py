from django.forms import ModelForm, IntegerField, BooleanField, Form
from .models import Word, WordList
from django.core import validators

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


class GameConfigForm(Form):
    list_id = IntegerField()
    options = IntegerField()
    simplified_pinyin = BooleanField(required=False)
    simplified_translation = BooleanField(required=False)
    translation_pinyin = BooleanField(required=False)
    translation_simplified = BooleanField(required=False)
    pinyin_simplified = BooleanField(required=False)
    pinyin_translation = BooleanField(required=False)

    def clean(self):
        super().clean()
        try:
            options = int(self.cleaned_data['options'])
        except:
            options = 4
        if options < 2:
            options = 2
        self.cleaned_data['options'] = options