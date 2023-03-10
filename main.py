# pythonProject6

# Парсим рецепты с сайта
# Видео в You Tube от Хауди-Хо "Парсинг в Python за 10 минут!"
# Парсит рецепты со страницы и выводит в виде списка строк
# Парсит несколько страниц

import requests
from bs4 import BeautifulSoup as BS
from config import site_adress, sel_title, sel_ingredient, sel_recipe

# парсим нужные страницы
# ВАЖНО! Python не обрабатывает текстовые файлы весом более 2.56мб!
page_list = range(26001, 26500)
recipe_list = []

for page in page_list:
    # Получаем содержимое страницы ("ее адрес") через библиотеку requests
    r = requests.get(site_adress + str(page))  #
    # скачанное обрабатываем через библиотеку BeautifulSoup
    html = BS(r.content, 'html.parser')

    recipe = []  # весь рецепт
    # Скачиваем нужный текст со страницы (с мусором)
    # скачиваем название
    title = html.select(sel_title)
    recipe += title
    recipe.append("ИНГРЕДИЕНТЫ:")
    # скачиваем ингредиенты
    ingredient = html.select(sel_ingredient)
    recipe += ingredient
    recipe.append("РЕЦЕПТ:")
    # скачиваем рецепт
    rec = html.select(sel_recipe)
    recipe += rec
    # фармируем лист с рецептами
    recipe_list.append(recipe)

# словарь 'русская буква':'латинская буква'
d_chars = {'а': 'a', 'е': 'e', 'о': 'o', 'с': 'c', 'х': 'x'}


# чистим текст строки
def clean_text(text):
    """
    Удаляем все символы в спарсенном тексте между скобками < и >.
    Заменяем русские буквы на английскик.
    :param text: вводим текст
    :return: чистый текст
    """
    global d_chars
    cl_text = str(text)
    if cl_text == '':
        return None
    while '<' in cl_text:
        cl_text = cl_text[:cl_text.find('<')] + cl_text[cl_text.find('>') + 1:]
    while '\r\n' in cl_text:
        cl_text = cl_text[:cl_text.find('\r')] + cl_text[cl_text.find('\n') + 1:]
    while '\n' in cl_text:
        cl_text = cl_text.replace('\n', ' ')
    # заменяем русские буквы на английские
    for char in d_chars:
        if char in cl_text:
            while char in cl_text:
                cl_text = cl_text.replace(char, d_chars[char])
    return cl_text


file2 = open("secondText.txt", 'w', encoding='utf-8')  # создается файл, 'w' - запись файла
try:
    # Очищенная страница записывается в список 'recipe_text' и в текстовый файл 'secondText.txt'
    recipe_text = []
    for recipe in recipe_list:
        for rcp in recipe:
            # убираем пустые строки
            if clean_text(rcp) == '':
                continue
            if clean_text(rcp) == ' ':
                continue
            recipe_text.append(clean_text(rcp))
            # пробел между строчками, кроме как между "ИНГРЕДИЕНТЫ" и "РЕЦЕПТ"
            if recipe.index('ИНГРЕДИЕНТЫ:') < recipe.index(rcp) < recipe.index('РЕЦЕПТ:') - 1:
                file2.write(clean_text(rcp) + '\n')
            else:
                    file2.write(clean_text(rcp) + '\n\n')
        file2.write('\n')
finally:  # в случае ошибок выводит то, что уже сделано
    file2.close()  # закрывает файл
    print(recipe_text)
