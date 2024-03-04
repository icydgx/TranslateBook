import httpx
import json
import re
import time
import sys

import os

from types import NoneType
import stardict
import sys
import re

import stardict
import sys
import re

sys.path.append('.')
dict = stardict.StarDict('C:/python/ECDICT-master/stardict.db', verbose = True)
# word = sys.argv[1]
# word = word.strip().lower()

def translate(word):
    try:
        result = dict.query(word)
        # print(result)
        # phonetic= result['phonetic']
        translation = result['translation']
        translation='\t'.join(translation.split('\n'))
        return translation
    except TypeError as e:pass


def translate_and_add_line(text, keyword):
    lines = text.split('\n')
    translated_book_text=''
    for line in lines:
        matchCheck=False
        sentences = re.split(r'(?<=[.!?])\s+', line)
        word = ''

        for sentence in sentences:
            # print(sentence+'$$$4')
            for keyword in keywords:
                pattern = r"\b" + re.escape(keyword) + r"\s"
                match = re.search(pattern, sentence)
                if match:

                    if not matchCheck:
                        translated_book_text += '\n'
                    # time.sleep(5)
                    # word += keyword
                    if keyword not in word:
                        word += keyword+' '
                        translated_word = keyword+': '+translate(keyword)
                        # print(translated_word)
                        # print("translate success")
                        # print()
                        # matchCheck=True

                    # if matchCheck is True:
                        # print("kkkkkkk")
                        translated_book_text += '\n'+translated_word
                        print(translated_book_text)
                        matchCheck=True
                    # break

        # if word not in ' ':
        #     print(word)

        if matchCheck:
            translated_book_text += '\n'

        translated_book_text += '\n'+line
    return translated_book_text

text_folder = 'raw_word'
text_file = os.listdir(text_folder)[0]
print("book name "+text_file)
word_list_file = "word_file.txt"
text_file = os.path.join(text_folder, text_file)

with open(text_file, 'r', encoding='utf-8') as file:
    book_text = file.read()

with open(word_list_file, 'r', encoding='utf-8') as file:
    keywords = file.read().lower().splitlines()

result = translate_and_add_line(book_text, keywords)

output_file = 'zh-en_'+str(os.listdir(text_folder)[0])+'.txt'
with open(output_file, 'w+', encoding='utf-8') as f:
        f.write(result)
