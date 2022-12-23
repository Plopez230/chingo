from django.contrib import admin
from .models import *

# Register your models here.
admin.register(ChingoUser)
admin.register(Word)
admin.register(WordList)
admin.register(Score)