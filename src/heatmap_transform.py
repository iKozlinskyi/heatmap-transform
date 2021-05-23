import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from scipy.interpolate import interp2d

NORMALIZATION = Normalize(15, 80)


def save_heatmap(data, name):
    x = np.arange(0, 8)
    y = np.arange(0, 8)
    f = interp2d(x, y, data, kind='linear')

    x_interpolated = np.linspace(0, 8, 128)
    y_interpolated = np.linspace(0, 8, 128)
    z_interpolated = f(x_interpolated, y_interpolated)
    plt.axis('off')
    fig = plt.imshow(z_interpolated,
                     interpolation='none', cmap='plasma',
                     norm=NORMALIZATION)

    plt.colorbar(ScalarMappable(norm=NORMALIZATION, cmap='plasma'))

    plt.savefig('./data/processed/%s.png' % name)
    plt.clf()
