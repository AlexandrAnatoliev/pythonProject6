# pythonProject6

[Ru] Парсер рецептов с сайта

## Описание:

Парсит рецепты со страницы и выводит в виде списка строк. Видео в You Tube от Хауди-Хо "Парсинг в Python за 10 минут!"

## Требования

* Установить внешние зависимости
* $ pip install -r requirements.txt
* создать файл config.py в котором разместить адрес сайта и селектор в виде:

```python
# Сайт Анекдоты.ру: адрес и селектор
site_adress = "https://anekdoty.ru/samye-smeshnye/page/"
sel = " div > div.holder-body > p"
```

## Подключаем модули

```python
import requests
from bs4 import BeautifulSoup as BS
from config import site_adress, sel_title, sel_ingredient, sel_recipe
```

## Примеры использования

#### Указываем нужные нам страницы, диапазон (певая, последняя) ВАЖНО! Python не обрабатывает тектовые файлы весом более 2.56мб!

```python
# парсим нужные страницы. 
page_list = range(10000, 10100)
recipe_list = []
```

#### Пишем адрес сайта

```python
r = requests.get("https://anekdoty.ru/samye-smeshnye/")
```

#### Ищем на странице нужный селектор и вписываем

```python
fun = html.select(" div > div.holder-body > p")
```

#### Скачиваем нужный текст со страницы (с мусором)

```python
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
```

#### # словарь 'русская буква':'латинская буква'

```python
d_chars = {'А': 'A', 'а': 'a', 'В': 'B', 'е': 'e', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'о': 'o', 'О': 'O', 'Р': 'P',
           'с': 'c', 'С': 'C', 'Т': 'T', 'х': 'x', 'Х': 'X'}
```

#### Чистим содержимое от лишнего

```python
def clean_text(text):
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
```

#### Записываем спарсенные рецепты в тестовый файл. Каждая между рецептами - два пробела (\n\n\n)

"Название текста", w - запись текста, 'кодировка текста'

```python
file2 = open("secondText.txt", 'w', encoding='utf-8')  # создается файл, 'w' - запись файла
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
file2.close()  # закрывает файл
```