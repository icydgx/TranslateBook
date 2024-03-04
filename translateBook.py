import httpx
import json
import re
import time
import sys

import os

deeplxl_api = "http://127.0.0.1:1188/translate"


def translate(sentence):
    data = {
        "text": sentence,
        "source_lang": "EN",
        "target_lang": "ZH"
    }

    post_data = json.dumps(data)
    response = httpx.post(url=deeplxl_api, data=post_data).json()
    translated_text = response["data"]
    translated_text = re.sub(r"[a-zA-Z]", "#", translated_text)
    return translated_text


def translate_and_add_line(text, keyword):
    lines = text.split('\n')

    matchCheck = True
    for i, line in enumerate(lines):
        sentences = re.split(r'(?<=[.!?])\s+', line)
        for sentence in sentences:
            # print(sentence+'$$$4')
            for keyword in keywords:
                pattern = r"\b" + re.escape(keyword) + r"\b"
                match = re.search(pattern, sentence)
                if match:

                    try:
                        time.sleep(5)
                        translated_line = translate(sentence)
                        # print("translate success")
                        print(sentence + '\n' + translated_line)
                        matchCheck = True
                    except Exception as e:
                        print(e)
                        pass

                    if matchCheck is True:
                        # print("kkkkkkk")
                        lines.insert(i + 1, translated_line)
                        matchCheck = False
                    break

    translated_text = '\n'.join(lines)
    return translated_text


text_folder = 'raw_word'
text_file = os.listdir(text_folder)[0]
print("book name " + text_file)
word_list_file = "word_file.txt"
text_file = os.path.join(text_folder, text_file)

with open(text_file, 'r', encoding='utf-8') as file:
    book_text = file.read()

with open(word_list_file, 'r', encoding='utf-8') as file:
    keywords = file.read().lower().splitlines()

result = translate_and_add_line(book_text, keywords)

output_file = 'zh-en_' + str(os.listdir(text_folder)[0]) + '.txt'
with open(output_file, 'w+', encoding='utf-8') as f:
    f.write(result)
