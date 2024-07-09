from Library import Process
from Library import Utils
from matplotlib import pyplot
import numpy as np
from os import path
import pickle

start_index = 45
end_index = 90

plain_color = 'red'
felt_color = 'blue'
double_felt_color = 'green'

# subfolder = '1pole_single_position'
# plain_files = ['single-pole-no-felt-1.pck', 'single-pole-no-felt-2.pck', 'single-pole-no-felt-3.pck']
# single_felt_files = ['single-pole-1x-felt-1.pck', 'single-pole-1x-felt-2.pck', 'single-pole-1x-felt-3.pck']
# double_felt_files = ['single-pole-2x-felt-1.pck','single-pole-2x-felt-2.pck', 'single-pole-2x-felt-3.pck']

subfolder = '3poles_single_position'
full_folder = path.join('data', subfolder)
plain_files = Utils.get_files(full_folder, 'combination-no-felt*')
single_felt_files = Utils.get_files(full_folder, 'combination-1x-felt*')
double_felt_files = Utils.get_files(full_folder, 'combination-2x-felt*')

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
        full_filename = path.join('data', subfolder, file_name)
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

# %%
colors = [plain_color, felt_color, double_felt_color]
time_axis = Utils.time_axis()
selected_time_axis = time_axis[start_index:end_index]

pyplot.figure(figsize=(8, 3))
pyplot.subplot(1, 2, 1)
selected0 = condition_means[:, :, 0]
pyplot.plot(time_axis, selected0[0, :], color=colors[0])
pyplot.plot(time_axis, selected0[1, :], color=colors[1])
pyplot.plot(time_axis, selected0[2, :], color=colors[2])
pyplot.grid()
pyplot.xlabel('Time [ms]')
pyplot.ylabel('Amplitude [dB]')
pyplot.legend(['Plain', 'Single Felt', 'Double Felt'], loc='lower right')

pyplot.subplot(1, 2, 2)
selected1 = condition_means[:, :, 1]
pyplot.plot(time_axis, selected1[0, :], color=colors[0])
pyplot.plot(time_axis, selected1[1, :], color=colors[1])
pyplot.plot(time_axis, selected1[2, :], color=colors[2])
pyplot.grid()
pyplot.xlabel('Time [ms]')
pyplot.ylabel('Amplitude [dB]')
pyplot.legend(['Plain', 'Single Felt', 'Double Felt'], loc='lower right')

pyplot.tight_layout()
pyplot.show()

diff1_0 = selected0[0, start_index:end_index] - selected0[1, start_index:end_index]
diff2_0 = selected0[0, start_index:end_index] - selected0[2, start_index:end_index]

diff1_1 = selected1[0, start_index:end_index] - selected1[1, start_index:end_index]
diff2_1 = selected1[0, start_index:end_index] - selected1[2, start_index:end_index]

pyplot.figure()
pyplot.plot(selected_time_axis, diff1_0, '-', color=colors[1], alpha=0.5, label='1x felt, left')
pyplot.plot(selected_time_axis, diff2_0, '--', color=colors[1], alpha=0.5, label='2x felt, left')
pyplot.plot(selected_time_axis, diff1_1, '-', color=colors[2], alpha=0.5, label='1x felt, right')
pyplot.plot(selected_time_axis, diff2_1, '--', color=colors[2], alpha=0.5, label='2x felt, right')
pyplot.title('Plain minus felted')
pyplot.grid()
pyplot.xlabel('Time [ms]')
pyplot.ylabel('Amplitude [dB]')
pyplot.legend()
pyplot.show()
