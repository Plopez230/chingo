import re
from .models import Word

tone_mark_order = ['a', 'o', 'e', 'i', 'u', 'ü']
tone_marks = {
	'a': "aāáǎà",
	'o': "oōóǒò",
	'e': "eēéěè",
	'i': "iīíǐì",
	'u': "uūúǔù",
	'ü': "üǖǘǚǜ"
}
consonants = "([BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz]*)"
vowels = "([aeiouü]+)"
tone_mark =  "([1-4])"
unmarked_word = re.compile(consonants + vowels + consonants + tone_mark)

def tone_mark_position(vowels, tone):
	for order in tone_mark_order:
		position = re.search(order, vowels)
		if position:
			return position.span()[0]
		
def mark_syllable(syllable):
	print (syllable)
	syllable = unmarked_word.findall(syllable[0])[0]
	vowels = syllable[1]
	tone = int(syllable[3])
	position = tone_mark_position(vowels, tone)
	vowels = vowels.replace(
		vowels[position], 
		tone_marks[vowels[position]][tone]
		)
	return syllable[0] + vowels + syllable[2]

def mark_text(text):
	return unmarked_word.sub(mark_syllable, text)

def mark_database():
	words = Word.objects.all()
	for word in words:
		word.pinyin = mark_text(word.pinyin)
		word.save()