from django.forms import ModelForm, IntegerField, BooleanField, Form, ModelChoiceField
from .models import Word, WordList
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

    def save(self, *args, **kwargs):
        self.instance.creator = kwargs.pop('creator', None)
        instance = super(WordForm, self).save(*args, **kwargs)
        return instance

    def clean(self):
        super().clean()
        if 'pinyin' in self.cleaned_data:
            self.cleaned_data['pinyin'] = mark_text(
                self.cleaned_data['pinyin']
                )


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
        self.cleaned_data['options'] = max(2, self.cleaned_data.get('options', 3))
        if self.cleaned_data['timer']:
            self.cleaned_data['timer'] = max(0, self.cleaned_data.get('timer', 0))


class TestForm(Form):
    question = ModelChoiceField(queryset=Word.objects.all())
    answer = ModelChoiceField(queryset=Word.objects.all())
