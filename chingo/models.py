from django.db import models
from django.contrib.auth.models import AbstractUser

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