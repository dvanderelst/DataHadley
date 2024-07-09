from Library import Process
from matplotlib import pyplot
import numpy as np
from os import path
import pickle

start_index = 45
end_index = 90

subfolder = '1pole_single_position'
plain_files = ['single-pole-no-felt-1.pck', 'single-pole-no-felt-2.pck', 'single-pole-no-felt-3.pck']
single_felt_files = ['single-pole-1x-felt-1.pck', 'single-pole-1x-felt-2.pck', 'single-pole-1x-felt-3.pck']
double_felt_files = ['single-pole-2x-felt-1.pck','single-pole-2x-felt-2.pck', 'single-pole-2x-felt-3.pck']

# subfolder = '3poles_single_position'
# plain_files = ['3-no-felt-poles.pck']
# single_felt_files = ['3-felt-poles.pck']
# double_felt_files = ['3-2x-felt-poles.pck']

all_files = [plain_files, single_felt_files, double_felt_files]
overall_max = 0
overall_min = 10000

dynamic_range = 30

pyplot.figure()
plot_index = 1
condition_means = []

for condition_index, condition in enumerate(all_files):
    current_scaled = []
    for file_index, file_name in enumerate(condition):
        full_filename = path.join('data',subfolder, file_name)
        fl = open(full_filename, 'rb')
        data = pickle.load(fl)
        fl.close()

        measurements = data['data_array']
        measurements = np.mean(measurements, axis=0)
        current_min = np.min(measurements)
        current_max = np.max(measurements)
        if current_max > overall_max: overall_max = current_max
        if current_min < overall_min: overall_min = current_min

        scaled = measurements - 1250
        scaled = scaled / (4095 - 1250)
        noise_level = Process.db2ratio(-dynamic_range)
        scaled[scaled < noise_level] = noise_level
        scaled = Process.ratio2db(scaled)
        current_scaled.append(scaled)

    current_scaled = np.array(current_scaled)
    condition_mean = np.mean(current_scaled, axis=0)
    condition_means.append(condition_mean)

    if condition_index == 0: title = 'plain'
    if condition_index == 1: title = '1x felt'
    if condition_index == 2: title = '2x felt'

    pyplot.subplot(3, 2, plot_index)
    selected = current_scaled[:, :, 0]
    selected = selected.transpose()
    pyplot.plot(selected)
    pyplot.grid()
    pyplot.title(title)

    pyplot.subplot(3, 2, plot_index + 1)
    selected = current_scaled[:, :, 1]
    selected = selected.transpose()
    pyplot.plot(selected)
    pyplot.grid()
    pyplot.title(title)

    plot_index = plot_index + 2
pyplot.show()
condition_means = np.array(condition_means)
print(overall_min, overall_max)

#%%

pyplot.figure()
pyplot.subplot(1, 2, 1)
selected0 = condition_means[:, :, 0]
selected0 = selected0.transpose()
pole_data = selected0[start_index:end_index, :].copy()
pole_data[pole_data <= (-dynamic_range+1)] = np.nan
pole_data = np.nanmean(pole_data, axis=0)
print(pole_data)
pyplot.plot(selected0)
pyplot.legend(['plain', 'single', 'double'])

pyplot.subplot(1, 2, 2)
selected1 = condition_means[:, :, 1]
selected1 = selected1.transpose()
pole_data = selected1[start_index:end_index, :].copy()
pole_data[pole_data <= (-dynamic_range+1)] = np.nan
pole_data = np.nanmean(pole_data, axis=0)
print(pole_data)
pyplot.plot(selected1)
pyplot.show()


diff1_0 = selected0[start_index:end_index, 0] - selected0[start_index:end_index, 1]
diff2_0 = selected0[start_index:end_index, 0] - selected0[start_index:end_index, 2]

diff1_1 = selected1[start_index:end_index, 0] - selected1[start_index:end_index, 1]
diff2_1 = selected1[start_index:end_index, 0] - selected1[start_index:end_index, 2]

pyplot.figure()
pyplot.plot(diff1_0, 'g-', alpha=0.5, label='1x felt, left')
pyplot.plot(diff2_0, 'g--', alpha=0.5, label='2x felt, left')
pyplot.plot(diff1_1, 'r-', alpha=0.5, label='1x felt, right')
pyplot.plot(diff2_1, 'r--', alpha=0.5, label='2x felt, right')
pyplot.title('Plain minus felted')
pyplot.legend()
pyplot.show()
