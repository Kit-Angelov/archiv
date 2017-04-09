# считываем ключи шелва мешка слов,
# каждое слово из мешка сверяем на наличие в входящем доке
# если слово есть то берем значение ключа, если нет то 0
# далее создаем массив для обучения сети
# и заполняем его векторами разных текстов
import shelve
import re
import numpy as np

arr = []

with shelve.open("bag") as bag:
    k = bag.keys()
    for z in file:
        z = "texts/"+z
        with open(z, "r") as t:
            arr_inp = []
            s = t.read()
            arr_txt = re.split('\W+', s)
            # print(arr_txt)
            for i in k:
                if i in arr_txt:
                    arr_inp.append(bag[i])
                else:
                    arr_inp.append(0)
        arr.append(arr_inp)

X = np.asarray(arr)
# print(X)

# генерируем матрицу выходного слоя для обучения

Y = np.zeros((20, 4))
r = 0
R = 0
for c in range(4):
    R += 5
    while r < R:
        Y[r][c] = 1
        r += 1
# print(Y)


