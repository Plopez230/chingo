from django.conf import settings
import math
import pyttsx3
import os

def split_columns(lst):
    chunk1 = math.ceil(len(lst)/3)
    remainder = len(lst)-chunk1
    chunk2 = chunk1+math.ceil(remainder/2)
    return [
        lst[0:chunk1],
        lst[chunk1:chunk2],
        lst[chunk2:],
        ]

def sing(word):
    espeak_path = os.path.join(settings.BASE_DIR, 'espeak')
    if not os.path.exists(espeak_path):
        os.makedirs(espeak_path)
    filename = os.path.join(espeak_path, str(word.id)+'_espeak.mp3')
    mandarin = pyttsx3.init()
    mandarin.setProperty('voice', 'zh')
    mandarin.setProperty('rate', 130)
    mandarin.save_to_file(word.pinyin, filename)
    mandarin.runAndWait()
    mandarin.stop()
    del(mandarin)
    while not os.path.exists(filename) or os.path.getsize(filename) == 0:
        pass
    return filename