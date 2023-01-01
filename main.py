# pythonProject6

# Парсим рецепты с сайта
# Видео в You Tube от Хауди-Хо "Парсинг в Python за 10 минут!"
# Парсит рецепты со страницы и выводит в виде списка строк
# Парсит несколько страниц

import requests
from bs4 import BeautifulSoup as BS
from config import site_adress, sel_title, sel_ingredient, sel_recipe

# парсим первые 20 страниц
# page_list = range(1, 0 + 1)
recipe_list = []


# for page in page_list:
# Получаем содержимое страницы ("ее адрес") через библиотеку requests
r = requests.get(site_adress)  # + str(page)
# скачанное обрабатываем через библиотеку BeautifulSoup
html = BS(r.content, 'html.parser')

recipe =[]  # весь рецепт
# Скачиваем весь текст со страницы (с мусором)
# скачиваем название
title = html.select(sel_title)
recipe += title
recipe.append("\nИНГРЕДИЕНТЫ:\n")
print(recipe)
# скачиваем ингредиенты
ingredient = html.select(sel_ingredient)
recipe += ingredient
# скачиваем рецепт
rec = html.select(sel_recipe)
recipe += rec


# чистим текст строки и формируем анекдот
def clean_text(text):
    """
    Удаляем все символы в спарсенном тексте между скобками < и >
    :param text: вводим текст
    :return: чистый текст
    """
    cl_text = str(text)
    if cl_text == '':
        return None
    while '<' in cl_text:
        cl_text = cl_text[:cl_text.find('<')] + cl_text[cl_text.find('>') + 1:]
    while '\r\n' in cl_text:
        cl_text = cl_text[:cl_text.find('\r')] + cl_text[cl_text.find('\n') + 1:]
    while '\n' in cl_text:
        cl_text = cl_text.replace('\n', ' ')
    return cl_text


# print(html)
file2 = open("secondText.txt", 'w', encoding='utf-8')  # создается файл, 'w' - запись файла

# Очищеная страница записывается в список 'recipe_text' и в текстовый файл 'secondText.txt'
recipe_text = []

for rcp in recipe:
    # убираем пустые строки
    if clean_text(rcp) == '':
        continue
    if clean_text(rcp) == ' ':
        continue
    recipe_text.append(clean_text(rcp))
    file2.write(clean_text(rcp) + '\n')

file2.close()  # закрывает файл
print(recipe_text)
