import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from scipy.interpolate import interp2d
import re

NORMALIZATION = Normalize(15, 80)

data = np.array([
    [27.00, 28.25, 29.25, 28.75, 27.75, 26.50, 25.25, 24.00],
    [27.25, 28.00, 29.75, 30.25, 28.00, 26.00, 24.50, 22.75],
    [26.00, 27.25, 28.50, 29.50, 28.75, 27.00, 24.00, 24.00],
    [25.50, 27.00, 28.00, 29.00, 29.25, 29.25, 25.75, 23.75],
    [25.50, 26.25, 27.00, 28.75, 28.75, 28.75, 29.00, 25.00],
    [25.25, 25.25, 26.50, 27.75, 28.75, 29.00, 29.00, 27.25],
    [25.00, 25.25, 26.25, 27.00, 28.25, 29.00, 29.50, 29.50],
    [24.25, 24.75, 25.75, 26.50, 28.00, 28.00, 29.25, 28.25]
])

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

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
    
    valid_name = get_valid_filename(name)
    plt.savefig('data/processed/%s.png' % valid_name)
    plt.clf()
