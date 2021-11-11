import json
from string import punctuation, digits, ascii_lowercase
from collections import defaultdict
import csv
from pymystem3 import Mystem
from bs4 import BeautifulSoup
import requests


def read_file(file_name):
    file = open(file_name, 'r')
    content = file.read()
    file.close()
    return content


def text_cleaning(text):
    text = text.lower().translate(str.maketrans('', '', punctuation + digits + ascii_lowercase + '–\t«»…”—“№'))

    while '\n' in text or '  ' in text:
        text = text.replace('\n', ' ')
        text = text.replace('  ', ' ')

    text = ' '.join([word for word in text.split(' ') if len(word) > 2])

    return text

    # text = ''.join([text[i] for i in range(len(text) - 1) if not (text[i] == '\n' and text[i + 1] == '\n')])


def freq_dict(text):
    tokens = defaultdict(lambda: 0)
    for word in text.split(' '):
        tokens[word] += 1

    tokens = dict(tokens)
    tokens = {k: v for k, v in sorted(tokens.items(), key=lambda item: item[1], reverse=True)}

    return tokens


def make_lemmas(text):
    mystem = Mystem()
    lemmas = mystem.lemmatize(text)

    return lemmas


if __name__ == '__main__':
    # 1. Открывает файл dom.txt с диска и читает текст.
    text = read_file('dom.txt')
    # 2. Приводит текст к нижнему регистру.
    # и
    # 3. Удаляет знаки препинания и прочие ненужные символы, а также слова длинной меньше 3-х символов.
    text = text_cleaning(text)
    # 4. Создаёт частотный словарь и записывает в CSV.
    frequency_dict = freq_dict(text)
    with open('file_frequency_dict.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        for key, value in frequency_dict.items():
            writer.writerow([key, value])
    # 5. Лемматизирует текст с помощью Mystem.
    lemmas = make_lemmas(text)
    # 6. Находит леммы, в которых ровно две буквы "о"
    lemmas_with2o = [word for word in lemmas if str(word).count('о') == 2]
    # print(f"Леммы с двумя буквами о:\n {' '.join(lemmas_with2o)}")
    # 7. Обращается к http://lib.ru/POEZIQ/PESSOA/lirika.txt.
    url = 'http://lib.ru/POEZIQ/PESSOA/lirika.txt'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    # Вытаскивает весь нужный текст со страницы.
    page_text = soup.body.pre.pre.text
    page_text = text_cleaning(page_text)
    # 8. Составляет частотный словарь для текста, который размещен на этой странице.
    frequency_dict = freq_dict(page_text)
    # 9. Записывает файл в формате JSON.
    with open('page_frequency_dict.json', 'w+') as file:
        json.dump(frequency_dict, file, ensure_ascii=False)
