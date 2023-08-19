import numpy as np

# Создаем массив с координатами
coordinates = np.array(np.meshgrid(np.arange(3), np.arange(3))).T.reshape(-1, 2)

# Добавляем столбцы с нулями
coordinates_with_zeros = np.hstack((coordinates, np.zeros((coordinates.shape[0], 3), dtype=int)))

print(coordinates_with_zeros.reshape(3, 3, 5))