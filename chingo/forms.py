from django.forms import ModelForm, IntegerField, BooleanField, Form
from .models import Word, WordList
from django.core import validators
from .pinyin_marker import mark_text

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

    def clean(self):
        super().clean()
        pinyin = self.cleaned_data['pinyin']
        self.cleaned_data['pinyin'] = mark_text(pinyin)

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
    timer = IntegerField(required=False)
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
        if self.cleaned_data['timer'] and self.cleaned_data['timer'] < 0:
            self.cleaned_data['timer'] = 0
        self.cleaned_data['options'] = options