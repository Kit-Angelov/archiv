from keras.layers.core import Dense
from keras.optimizers import SGD
import numpy as np
from keras.models import Sequential
import utils
import time

# подготовка данных
path_to_bag = 'bag'
input_learn_arr = []
input_test_arr = []

file_fit = ['kino1.txt', 'kino2.txt', 'kino3.txt', 'kino4.txt',
        'kino5.txt', 'philo1.txt', 'philo2.txt', 'philo3.txt',
        'philo4.txt', 'philo5.txt', 'politic1.txt', 'politic2.txt',
        'politic3.txt', 'politic4.txt', 'politic5.txt', 'sport1.txt',
        'sport2.txt', 'sport3.txt', 'sport4.txt', 'sport5.txt']
file_test = ['kino_test.txt', 'philo_test.txt',
             'politic_test.txt', 'sport_test.txt']

# заполняем мешок слов
for file in file_fit:
    path_to_file = 'texts/' + file
    utils.fill_bag(path_to_file, path_to_bag)

# заполняем входящий вектор обучающей выборки
for file in file_fit:
    path = 'texts/' + file
    vector = utils.fill_vec(path, path_to_bag)
    input_learn_arr.append(vector)
X = np.asarray(input_learn_arr)

# генерируем массив выходных векторов обучающей выборки
Y = utils.gen_out_arr(20, 4)

# заполняем входящей вектор тестовой выборки
for file in file_test:
    path = 'texts/' + file
    word_arr = utils.text_split(path)
    stem_word_arr = utils.stem_arr(word_arr)
    vector = utils.word_arr_to_vec(stem_word_arr, path_to_bag)
    input_test_arr.append(vector)
Z = np.asarray(input_test_arr)

# генерируем массив выодных векторов тестовой выборки
L = np.eye(4)

# сама сеть
input_size = utils.count_keys(path_to_bag)
print(input_size)
model = Sequential()
model.add(Dense(7000, input_dim=input_size, activation='relu'))
#model.add(Dense(800, activation='sigmoid'))
model.add(Dense(4, activation='softmax'))

sgd = SGD(lr=0.1)
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='rmsprop')
start = time.time()
model.fit(X, Y, batch_size=2, nb_epoch=6, verbose=1, validation_data=(Z, L))
end = time.time()
delta = end - start
print(model.predict_proba(X))

score = model.evaluate(X, Y, verbose=0)
print('accuracy:', score[1])
print('score:', score[0])
predict = model.predict(Z)
print('time = ', delta)
print(predict)
