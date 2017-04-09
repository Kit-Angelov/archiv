"""Слова длиной меньше 3 не берем, слова дной меньше 2 после стеммера тоже не берем
При наличии большой обучающей выборки создаем второй мешок слов: в одном весь словарный запас, во втором
 только те слова частота которых больше 1 - его и берем для векторизации.
 Можно рассмотреть другие стеммеры"""
import re
import shelve
import math
from collections import Counter
import numpy as np


# удаление чисел и слов длиной меньше 3
def format_word(word_arr):
    alpha = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЪъЫыЬьЭэЮюЯя'
    alpha_set = set(list(alpha))
    new_arr = []
    for word in word_arr:
        word_set = set(list(word))
        compare_set = alpha_set & word_set
        if word.isalpha() and len(word) > 2 and word_set == compare_set:
            new_arr.append(word)
    return new_arr


# сплиттер текста (вход-имя документа, выход-массив слов документа)
def text_split(path_file):
    with open(path_file, 'r') as t:
        s = t.read()
        word_arr = re.split('\W+', s)
        word_arr = format_word(word_arr)
    return word_arr


# стеммер (вход-слово, выход-слово)
def stemming(word):
    afix = ["утся", "ётся", "ется", "ются", "ится", "атся", "уться", "ёться",
                    "оться", "яться", "иться", "аться", "еться", "етесь", "итесь",
                    "ась", "усь", "ись", "юсь", "есь", "ему", "ому", "ого", "его", "ать", "ять",
                    "ить", "ыть", "уть", "ете", "ёте", "ешь", "ёшь", "ишь", "ите", "сь", "ся", "ый",
                    "ий", "ая", "яя", "ое", "ее", "ой", "ей", "ом", "ую", "юю", "ым", "им", "ем", "ет",
                    "ёт", "ем", "ём" "ут", "ют", "ит", "им", "ат", "ят", "ой", "ей", "ом", "ем", "ью",
                    "а", "я", "о", "е", "ь", "ы", "и", "й", "у", "ю", "у", "ю"]

    for i in afix:
        word = word.lower()
        if word.endswith(i) and len(word) > 3:
            word = word[0:len(word) - len(i)]
            break
    return word


# стемминг массива слов (вход-массив слов, выход-массив слов)
def stem_arr(word_arr):
    stem_word_arr = []
    for word in word_arr:
        word = stemming(word)
        if len(word) > 1:
            stem_word_arr.append(word)
    return stem_word_arr


# удаление повторяющихся слов(вход-массив слов, выход-массив слов)
def del_repeate(word_arr):
    out_word_arr = []
    for word in word_arr:
        if word not in out_word_arr:
            out_word_arr.append(word)
    return out_word_arr


# массив слов в мешок слов (вход-массив слов)
def word_arr_to_bag(word_arr, path_bag):
    with shelve.open(path_bag) as bag:
        for word in word_arr:
            if word in bag.keys():
                bag[word] += 1
            else:
                bag[word] = 1


# массив слов в вектор (вход-массив слов, выход-вектор)
def word_arr_to_vec(word_arr, path_bag):
    word_count_dic = Counter(word_arr)  # словарь повторений слова в входящем массиве слов
    out_vec = []
    with shelve.open(path_bag) as bag:
        keys = bag.keys()
        for key in keys:
            if key in word_count_dic:  # and bag[key] > 1
                n = word_count_dic[key]  # число повторений слова в входящем массиве слов
                val = math.tanh(n / bag[key])  # гиперболический тангенс
                out_vec.append(val)
            else:
                out_vec.append(0)
    return out_vec


# генерация матрицы выходного словя(вход-число массивов, число классов, выход-матрица)
def gen_out_arr(num_arr, num_class):
    Y = np.zeros((num_arr, num_class))
    r = 0
    R = 0
    n = num_arr / num_class
    for c in range(num_class):
        R += n
        while r < R:
            Y[r][c] = 1
            r += 1
    return Y


# размер входного слоя (вход-путь к мешку, выход-размер входного слоя)
def count_keys(path_to_bag):
    count = []
    with shelve.open(path_to_bag) as bag:
        keys = bag.keys()
        print(keys)
        for i in keys:
            count.append(i)
    size = len(count)
    return size


# заполнение мешка слов (вход-путь до документов, путь до мешка)
def fill_bag(path_to_file, path_to_bag):
        word_arr = text_split(path_to_file)
        stem_word_arr = stem_arr(word_arr)
        unrep_word_arr = del_repeate(stem_word_arr)
        word_arr_to_bag(unrep_word_arr, path_to_bag)


# векторизация документа(вход-путь до документа, путь до мешка слов, выход-вектор документа)
def fill_vec(path_to_file, path_to_bag):
    word_arr = text_split(path_to_file)
    stem_word_arr = stem_arr(word_arr)
    vector = word_arr_to_vec(stem_word_arr, path_to_bag)
    return vector
