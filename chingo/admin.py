from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ChingoUser)
admin.site.register(Word)
admin.site.register(WordList)
admin.site.register(Score)