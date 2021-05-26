import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from scipy.interpolate import interp2d

NORMALIZATION = Normalize(15, 80)


def save_heatmap(data, name):
    """
    получаем матрицу данных и имя для файла
    """
    # Создаем массив 0, 1... 8
    # для x и y
    x = np.arange(0, 8)
    y = np.arange(0, 8)
    # Библиотченая функция interp2d - возвращает интерполированную функцию
    # Можно поиграться с типами интерполяции
    f = interp2d(x, y, data, kind='linear')

    # Задаем координаты лдя интерполяции по x и y
    x_interpolated = np.linspace(0, 8, 128)
    y_interpolated = np.linspace(0, 8, 128)
    # Получаем интерполированные значения массива данных
    z_interpolated = f(x_interpolated, y_interpolated)

    # Выключаем показ осей на графике
    plt.axis('off')
    # Создаем картинку. Пробрасываем нормализацию - можешь менять ее
    # И цвет - 'plasma'
    fig = plt.imshow(z_interpolated,
                     interpolation='none', cmap='plasma',
                     norm=NORMALIZATION)

    # добавляем шкалу справа с тем же цветом и нормализацией
    plt.colorbar(ScalarMappable(norm=NORMALIZATION, cmap='plasma'))

    # Сохраняем картинку
    plt.savefig('./data/processed/%s.png' % name)
    # Чистим буфер (иначе картинки будут в памяти накладываться)
    plt.clf()
