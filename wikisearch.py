"""1. Берем термины которых нет в мешке слов
   2. Ищем по каждому страницу в wiki
   3. Вытаскиваем категории каждой страницы, фильтруем их
   4. Ищем по каждой категории список страниц wiki
   5. Категория становится новым классом в инс,
                    а каждая статья из wiki по данной категории добавляется
                                    в обучающуу выборку для обучения нового класса
   6. Есть возможность реализации поискового паука,
                    если из каждой последующей статьи по категории доставать новые категории"""


import wikipedia as wiki
import re
import shelve
import utils
from collections import Counter

correct_dic = ["Википедия", "Умершие", "Родившиеся", "алфавиту", "имена", "века", "года", "годов", "Незавершённые",
               "Населённые пункты", "ПРО", "ВО", "Члены", "ISBN", "члены", "Статьи", "Награждённые", "Лауреаты",
               "Почётные", "Кавалеры", "Персоналии", "Иммигрировавшие", "Выпускники", "Почётные", "Люди", "Учёные",
               "интеллектуальной", "композиторы", "фильмы", "университета", "классическая"]
correct_set = set(correct_dic)

bag = shelve.open('bag')
keys = bag.keys()
t = open('texts/music.txt', 'r')
arr = t.read()
arr_music = re.split('\W+', arr)
arr_compare = utils.text_split('texts/music.txt')
arr_compare = utils.stem_arr(arr_compare)

music = []
compare = []
res = []
cat_arr = []
min_count = 2

# вывод незнакомых слов после стеммера
for i in arr_compare:
    if i not in keys:
        compare.append(i)
print(len(compare))
print(compare)

# приведение слов документа к нижнему регистру
for k in arr_music:
    music.append(k.lower())
print(len(music))
print(music)

# вывод списка восстановленных незнакомых слов
for b in compare:
    for a in music:
        if a.startswith(b):
            res.append(a)
            break
print(len(res))
print(res)

# поиск категорий
for word in res:
    try:
        wiki.set_lang("ru")
        page = wiki.page(word)
        cat = page.categories
        for item in cat:
            cat_arr.append(item)
    except:
        continue

# фильтр категорий
count_cat = Counter(cat_arr)
for c in count_cat:
    c_split = re.split('\W+', c)
    if '' in c_split:
        c_split.remove('')
    c_set = set(c_split)
    if (count_cat[c] > min_count) and not(c_set & correct_set) \
            and not (c_split[1].endswith('и') or c_split[1].endswith('ы')) \
            and (len(c_split) < 4):
        if (len(c_split) == 3) and not(c_split[2].istitle()):
            print(c, '\t\t', count_cat[c])
        elif len(c_split) < 3:
            print(c, '\t\t', count_cat[c])



