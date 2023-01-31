import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import pickle

border = '#' * 60


# Функция проверки процентного соотношения совпадения векторов предсказанного и проверочного значения относительно
# предидущего значения Так как назначение программы предсказывать пробивание стоп линий на валютной бирже,
# считаю что направление графика важнее чем предсказанное число.
def vector(y_test, pred):
    vector = 0
    for i in range(1, y_test.shape[0]):
        test = y_test.iloc[i - 1] - y_test.iloc[i]
        pred_v = y_test.iloc[i - 1] - pred[i]
        if test > 0 and pred_v > 0 or test < 0 and pred_v < 0:
            vector += 1
    vector_percent = vector / (len(y_test) - 1)
    return vector_percent * 100


# Преобразуем y к булевым значениям на основе больше или меньше нуля(трактовка графика 1 вверх или равно 0 вниз)
def int_to_vec(y):
    vec = 0
    lst = []
    for i, value in enumerate(y):
        if i > 0:
            vec = y.iloc[i - 1] - value
        if vec >= 0:
            lst.append(1)
        elif vec < 0:
            lst.append(0)
    return lst


# загружаем дата сет курса валют за 13 лет
df = pd.read_csv('files/USDRUB_100101_230127.csv')
print(df)

y = df['<CLOSE>']
x = df[['<OPEN>', '<HIGH>', '<LOW>']]

# Подготавливаем данные
sc = StandardScaler()
x_sc = sc.fit_transform(x)
x_train, x_test, y_train, y_test = train_test_split(x_sc, y, test_size=0.2)

# обучаем модель
lin_r_model = LinearRegression()
lin_r_model.fit(x_train, y_train)

pred = lin_r_model.predict(x_test)

mape = metrics.mean_absolute_percentage_error(y_test, pred)
r2 = metrics.r2_score(y_test, pred)
mae = metrics.median_absolute_error(y_test, pred)
mse = metrics.mean_squared_error(y_test, pred)
print()
print(border)
print('Для линейной регресси без смещения по времени')
print('mape -', mape)
print('r2 -  ', r2)
print('mae - ', mae)
print('mse - ', mse)
print('Процент совпадение направления векторов предсказания без смещения времени', vector(y_test, pred))

# Смещаем предсказываемые данные на одну строку(данные из датафрейма представлены в интервале один день)
y5 = df['<CLOSE>']
x5 = df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>']]
y5 = y5[1:]
x5 = x5[:x5.shape[0] - 1]

# получим максимум и минимум для дальнейшей стандартизации
data_min_max = [min(x5.min()), max(x5.max())]
print()
print(border)
print('максимум из данных -', data_min_max[1])
print('минимум  из данных -', data_min_max[0])
min_max = open('files/min_max.txt', 'w+')
min_max.write(str(data_min_max[0]))
min_max.write(' ' + str(data_min_max[1]))
min_max.close()

sc5 = StandardScaler()
x5_sc = sc5.fit_transform(x5)
x5_train, x5_test, y5_train, y5_test = train_test_split(x5_sc, y5, test_size=0.2)

lin_r_model5 = LinearRegression()
lin_r_model5.fit(x5_train, y5_train)

pred5 = lin_r_model5.predict(x5_test)

mape = metrics.mean_absolute_percentage_error(y5_test, pred5)
r2 = metrics.r2_score(y5_test, pred5)
mae = metrics.median_absolute_error(y5_test, pred5)
mse = metrics.mean_squared_error(y5_test, pred5)
print()
print(border)
print('Для линейной регрессии со смещением предсказания на строку (день)')
print('mape -', mape)
print('r2 -  ', r2)
print('mae - ', mae)
print('mse - ', mse)
print('Для линейной регрессии со смещением предсказания на строку (день)', vector(y5_test, pred5))

y = df['<CLOSE>']
x = df[['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>']]

# Подготавливаем данные
sc__log = StandardScaler()
x_sc__log = sc__log.fit_transform(x)
x_train__log, x_test__log, y_train__log, y_test__log = train_test_split(x_sc__log, y, test_size=0.2)

y_train__log = int_to_vec(y_train__log)[1:]
y_test__log = int_to_vec(y_test__log)[1:]
x_train__log = x_train__log[:x_train__log.shape[0] - 1]
x_test__log = x_test__log[:x_test__log.shape[0] - 1]

clf = LogisticRegression()
clf.fit(x_train__log, y_train__log)

log__pred = clf.predict(x_test__log)

mape = metrics.mean_absolute_percentage_error(y_test__log, log__pred)
r2 = metrics.r2_score(y_test__log, log__pred)
mae = metrics.median_absolute_error(y_test__log, log__pred)
mse = metrics.mean_squared_error(y_test__log, log__pred)
print()
print(border)
print('для логистической регрессии')
print('mape -', mape)
print('r2 -  ', r2)
print('mae - ', mae)
print('mse - ', mse)

z = 0
for i in range(len(y_test__log)):
    a = y_test__log[i]
    b = log__pred[i]
    if a == b:
        z += 1
z /= len(y_test__log)
print('проверка совпаения векторов предсказания линейной и логистической регрессии', z * 100, 'процентов совпадений')

# Сохраняем модели
pkl_filename = "files/USD_RUB_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(lin_r_model5, file)
file.close()
print('модель сохранена')

figure, axis = plt.subplots(2, 2)
figure.set_size_inches(10, 6)

axis[0, 0].plot(df['<CLOSE>'])
axis[0, 0].set_title('за весь период')

axis[1, 0].plot(pred[:10])
axis[1, 0].plot(list(y_test[:10]))
axis[1, 0].set_title('линейная регрессия без смещения')

axis[1, 1].plot(pred5[:10])
axis[1, 1].plot(list(y5_test[:10]))
axis[1, 1].set_title('Предсказание следующего дня')

plt.savefig('files/predict_show.jpg')
