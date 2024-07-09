import pandas
from matplotlib import pyplot

call_onset = 3.4
cm_per_ms = 17.0145


def plot_events(x='time'):
    scale = 1
    call_duration = 2
    distance_near_side = 15
    label_near_side = 'dense (with felt)'
    distance_far_side = 105
    label_far_side = 'sparse'

    if x == 'distance': scale = cm_per_ms
    start_of_emission = 0
    end_of_emission = start_of_emission + call_duration
    first_possible_from_near = distance_near_side / cm_per_ms
    first_possible_from_far = distance_far_side / cm_per_ms

    axis = pyplot.gca()
    lims = axis.get_ylim()
    min_y = lims[0]
    max_y = lims[1]

    pyplot.axvspan(start_of_emission * scale, end_of_emission * scale, color='y', alpha=0.25)
    pyplot.text(start_of_emission, (min_y + max_y) / 2, 'Emission')
    pyplot.vlines(first_possible_from_near * scale, min_y, max_y, 'g', label=label_near_side)


    pyplot.vlines(first_possible_from_far * scale, min_y, max_y, 'r', label=label_far_side)
    pyplot.text(first_possible_from_near * scale, min_y, label_near_side)
    pyplot.text(first_possible_from_far * scale, min_y, label_far_side)


title = '45 cm off midline towards dense side'

data = pandas.read_csv('warnecke1.csv')
data['time'] = data['x'] - call_onset

data = data.query('time > 0')
data = data.query('time < 10')

data['dist'] = data['time'] * cm_per_ms

data['Diff1'] = data['1Felt'] - data['NoFelt']
data['Diff2'] = data['2Felt'] - data['NoFelt']

pyplot.figure(figsize=(7, 7))

pyplot.subplot(3, 1, 1)

pyplot.plot(data['time'], data['NoFelt'])
pyplot.plot(data['time'], data['1Felt'])
pyplot.plot(data['time'], data['2Felt'])
plot_events(x='time')
pyplot.grid()
pyplot.legend(['NoFelt', '1Felt', '2Felt'], loc=4)
pyplot.title(title)
pyplot.ylabel('dB')
pyplot.xlabel('Original time = t +' + str(call_onset))
pyplot.subplot(3, 1, 2)

pyplot.plot(data['time'], data['Diff1'])
pyplot.plot(data['time'], data['Diff2'])
plot_events(x='time')
pyplot.grid()

pyplot.subplot(3, 1, 3)

pyplot.plot(data['dist'], data['Diff1'])
pyplot.plot(data['dist'], data['Diff2'])
plot_events(x='distance')
pyplot.legend(['1Felt', '2Felt'])

pyplot.xlabel('Distance/time since onset of emission')
pyplot.grid()

pyplot.tight_layout()
pyplot.show()
