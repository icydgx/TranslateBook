import httpx
import json
import re
import time
import sys
import os

# URL for the DeeplXL translation API
deeplxl_api = "http://127.0.0.1:1188/translate"

# Function to translate a sentence from English to Chinese using the DeeplXL API
def translate(sentence):
    data = {
        "text": sentence,
        "source_lang": "EN",
        "target_lang": "ZH"
    }

    # Convert data to JSON format
    post_data = json.dumps(data)

    # Send a POST request to the DeeplXL API and retrieve the translated text
    response = httpx.post(url=deeplxl_api, data=post_data).json()
    translated_text = response["data"]

    # Replace all English letters with '#' in the translated text
    translated_text = re.sub(r"[a-zA-Z]", "#", translated_text)

    return translated_text

# Function to translate and add a line to the text based on a keyword match
def translate_and_add_line(text, keywords):
    lines = text.split('\n')
    matchCheck = True

    # Iterate over each line in the text
    for i, line in enumerate(lines):
        sentences = re.split(r'(?<=[.!?])\s+', line)

        # Iterate over each sentence in the line
        for sentence in sentences:
            for keyword in keywords:
                pattern = r"\b" + re.escape(keyword) + r"\b"

                # Check if the sentence contains the keyword
                match = re.search(pattern, sentence)
                if match:
                    try:
                        # Pause for 5 seconds before making a translation request
                        time.sleep(5)

                        # Translate the sentence using the translate function
                        translated_line = translate(sentence)
                        print(sentence + '\n' + translated_line)
                        matchCheck = True
                    except Exception as e:
                        print(e)
                        pass

                    # If the translation is successful, insert the translated line after the current line
                    if matchCheck is True:
                        lines.insert(i + 1, translated_line)
                        matchCheck = False
                    break

    # Reconstruct the text with the translated lines
    translated_text = '\n'.join(lines)
    return translated_text

# Folder containing text files
text_folder = 'raw_word'

# Selecting the first text file in the folder
text_file = os.listdir(text_folder)[0]
print("book name " + text_file)

# File containing the list of keywords
word_list_file = "word_file.txt"

# Construct the path to the text file
text_file = os.path.join(text_folder, text_file)

# Read the contents of the text file
with open(text_file, 'r', encoding='utf-8') as file:
    book_text = file.read()

# Read the keywords from the word list file
with open(word_list_file, 'r', encoding='utf-8') as file:
    keywords = file.read().lower().splitlines()

# Translate and add lines based on the keywords in the text
result = translate_and_add_line(book_text, keywords)

# Create an output file with the translated text
output_file = 'zh-en_' + str(os.listdir(text_folder)[0]) + '.txt'
with open(output_file, 'w+', encoding='utf-8') as f:
    f.write(result)
