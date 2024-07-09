from Library import Process
import numpy as np
from os import path
import pickle
from matplotlib import pyplot as plt

class DataSet:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.samples = 200
        self.sample_rate = 10000
        self.dynamic_range = 40
        self.min_value = 45
        self.max_value = 2900
        self.read_file(filename)
        self.subtraction_set = False

    def read_file(self, filename):
        full_name = path.join('data', filename)
        fl = open(full_name, 'rb')
        data = pickle.load(fl)
        fl.close()
        self.data = data

    def plot_measurement(self, index, type='decibel'):
        data0, _, _ = self.get_measurement(index, 0, type)
        data1, indices, position = self.get_measurement(index, 1, type)
        distance = self.distance_axis
        title = str(indices) + str(position)
        plt.plot(distance, data0, label='ear 0')
        plt.plot(distance, data1, label='ear 1')
        plt.legend(loc='upper right')
        plt.title(title)
        plt.xlabel('Distance, cm')
        plt.ylabel('Amplitude, dB')
        plt.grid()

    def get_measurement(self, index, ear=0, type='raw'):
        if type.startswith('r'): selected_data = self.raw_data
        if type.startswith('s'): selected_data = self.scaled_data
        if type.startswith('d'): selected_data = self.decibel_data
        shape = self.combo_shape
        i, j, k = np.unravel_index(index, shape=shape)
        x = self.x_positions[i]
        y = self.y_positions[j]
        yaw = self.yaw_positions[k]
        selected = selected_data[i, j, k, :, ear]
        indices = (i, j, k)
        position = (x, y, yaw)
        return selected, indices, position

    @property
    def description(self):
        return self.data['description']

    @property
    def combos(self):
        n = self.combo_shape[0] * self.combo_shape[1] * self.combo_shape[2]
        return n

    @property
    def combo_shape(self):
        shape = self.data_shape[0:3]
        return shape

    @property
    def x_positions(self):
        return self.data['x_positions']

    @property
    def y_positions(self):
        return self.data['y_positions']

    @property
    def yaw_positions(self):
        return self.data['yaw_positions']


    @property
    def keys(self):
        return self.data.keys()

    @property
    def raw_data(self):
        data = self.data['data_array']
        data = np.mean(data, axis=3)
        if self.subtraction_set:
            subtraction_data = self.subtraction_set.raw_data
            data = data - subtraction_data
            data[data <0] = 0
        return data

    @property
    def data_shape(self):
        return self.raw_data.shape

    @property
    def distance_axis(self, offset=0):
        samples = self.samples
        sample_rate = self.sample_rate
        max_time_ms = (samples / sample_rate) * 1000
        max_distance = max_time_ms * 17.15
        distance = np.linspace(0, max_distance, samples)
        distance = distance + offset
        return distance

    @property
    def scaled_data(self):
        data = self.raw_data - self.min_value
        data = data / (self.max_value - self.min_value)
        data[data < 0] = 0
        data[data > 1] = 1
        lower_value = Process.db2ratio(-self.dynamic_range)
        data[data < lower_value] = lower_value
        return data

    @property
    def decibel_data(self):
        data = self.scaled_data
        data = Process.ratio2db(data)
        return data