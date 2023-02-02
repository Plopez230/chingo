from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum, Prefetch, Q

# Create your models here.
class ChingoUser(AbstractUser):
	dictionary_points = models.IntegerField(
		verbose_name = _('points'),
		default = 0
		)
	lists_created = models.IntegerField(
		verbose_name = _('lists created'),
		default = 0
		)
	words_included = models.IntegerField(
		verbose_name = _('words included'),
		default = 0
		)
	tests_passed = models.IntegerField(
		verbose_name = _('tests passed'),
		default = 0
		)
	class Meta:
		verbose_name = _("chingo user")
		verbose_name_plural = _("chingo users")

	@property
	def stars(self):
		return int(
			self.tests_passed * 1/50 
			+ self.words_included * 1/5 
			+ self.lists_created * 1/20
			)

	@property
	def rank(self):
		stars = self.stars
		if stars < 10:
			return _('newcomer')
		elif stars < 100:
			return _('apprentice')
		elif stars < 1000:
			return _('nerd')
		elif stars < 10000:
			return _('master')
		else:
			return _('donnish')

class Word(models.Model):
	class PartOfSpeech(models.TextChoices):
		NOUN = 'NOUN', _('noun')
		PRONOUN = 'PRON', _('pronoun')
		VERB = 'VERB', _('verb')
		ADJECTIVE = 'ADJE', _('adjective')
		ADVERB = 'ADVE', _('adverb')
		NUMBER = 'NUMB', _('number')
		CLASSIFIER = 'CLAS', _('classifier')
		INTERJECTION = 'INTE', _('interjection')
		ONOMATOPEIA = 'ONOM', _('onomatopeia')
		CONJUNCTION = 'CONJ', _('conjunction')
		PREPOSITION = 'PREP', _('preposition')
		PARTICLE = 'PART', _('particle')
		EXPRESSION = 'EXPR', _('expression')

	simplified = models.TextField(
		verbose_name = _('simplified character')
		)
	traditional = models.TextField(
		verbose_name = _('traditional character'),
		null = True,
		blank = True
		)
	pinyin = models.TextField(
		verbose_name = _('pinyin transcription')
		)
	classifier = models.TextField(
		verbose_name = _('classifiers (if needed)'),
		default = '',
		blank = True
		)
	translation = models.TextField(
		verbose_name = _('translated text')
		)
	part_of_speech = models.CharField(
		max_length=4,
		choices=PartOfSpeech.choices,
		default=PartOfSpeech.NOUN,
	)
	creator = models.ForeignKey(
		ChingoUser,
		verbose_name = _('creator of this character'),
		on_delete = models.SET_NULL,
		null = True
		)
	creation_date = models.DateTimeField(
		verbose_name = _('date of creation'),
		auto_now_add = True
		)
	class Meta:
		verbose_name = _("character")
		verbose_name_plural = _("characters")
		
	def __str__(self):
		return '{} ({}) {}'.format(
			self.simplified, 
			self.pinyin, 
			self.translation
			)

class WordListManager(models.Manager):

	def with_word_count(self):
		queryset = self.get_queryset().annotate(word_count=Count('words'))
		return queryset

class WordList(models.Model):
	objects = WordListManager()
	name = models.TextField(
		verbose_name = _('name of the list')
		)
	description = models.TextField(
		verbose_name = _('brief description of the contents of the list'),
		default = ''
		)
	words = models.ManyToManyField(
		Word, 
		verbose_name = _('words in this list'),
		related_name = 'lists'
		)
	owner = models.ForeignKey(
		ChingoUser,
		verbose_name = _('owner of the list'),
		on_delete = models.SET_NULL,
		null = True
		)
	creation_date = models.DateTimeField(
		verbose_name = _('date of creation'),
		auto_now_add = True
		)
	image = models.TextField(
		verbose_name = _('image'),
		max_length=500, 
		default = '',
		blank = True,
		null = True
		)
	class Meta:
		verbose_name = _("word list")
		verbose_name_plural = _("word lists")
		
	def __str__(self):
		return '{} ({})'.format(self.name, self.owner.username)

class ScoreManager(models.Manager):

	def worst_scores(self, user):
		queryset = self.none()
		if user.is_authenticated:
			queryset = self.get_queryset().filter(player=user).order_by('-wrong')
		return queryset
	
	def by_user_and_word(self, user, word):
		score = None
		if user.is_authenticated:
			score, created = self.get_or_create(player=user.id, word=word.id)
		return score

class Score(models.Model):
	objects = ScoreManager()
	word = models.ForeignKey(
		Word, 
		verbose_name = _('the word whose score is stored'),
		related_name = "scores",
		on_delete = models.SET_NULL,
		null = True
		)
	player = models.ForeignKey(
		ChingoUser, 
		verbose_name = _('player who scores'),
		related_name = "scores",
		on_delete = models.SET_NULL,
		null = True
		)
	shown = models.IntegerField(
		verbose_name = _('number of times shown'),
		default = 0
		)
	correct = models.IntegerField(
		verbose_name = _('number of times correct'),
		default = 0
		)
	wrong = models.IntegerField(
		verbose_name = _('number of times wrong'),
		default = 0
		)
	next_reminder = models.DateTimeField(
		verbose_name = _('next reminder date'),
		auto_now_add = True,
		null = True
		)
	class Meta:
		verbose_name = _("score")
		verbose_name_plural = _("scores")
		
	def __str__(self):
		return '{}, {}'.format(self.player.username, self.word)