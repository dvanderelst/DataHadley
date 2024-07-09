import pandas
import numpy
from scipy.interpolate import interp1d
from matplotlib import pyplot

call_onset = 3.1
cm_per_ms = 17.0145
emission_duration = 2.2
first_echo = 75 #???

no_felt = pandas.read_csv('midline_nofelt_auto.csv')
felt = pandas.read_csv('midline_felt_auto.csv')
#%%
no_felt['time'] = no_felt['x'] - call_onset
felt['time'] = felt['x'] - call_onset

no_felt_function = interp1d(no_felt['time'], no_felt['Curve1'])
felt_function = interp1d(felt['time'], felt['Curve1'])

time_points = numpy.linspace(0,10,1000)
distance_points = time_points * cm_per_ms
no_felt_i = no_felt_function(time_points)
felt_i = felt_function(time_points)

pyplot.figure(figsize=(10,5))
pyplot.subplot(2,2,1)
pyplot.plot(distance_points, no_felt_i)
pyplot.plot(distance_points, felt_i)
pyplot.legend(['No felt', 'Felt'])
pyplot.xlabel('Distance')
pyplot.ylabel('Volt')
pyplot.axvspan(0, emission_duration * cm_per_ms, color='y', alpha=0.25)
pyplot.text(60,-0.1, '<- Theor. first echo')
#pyplot.axvspan(emission_duration * cm_per_ms,first_echo, color='r', alpha=0.25)
pyplot.axvspan(60, 150, color='y', alpha=0.25)


pyplot.subplot(2,2,2)
decibel_felt = 20*numpy.log10(felt_i)
decibel_no_felt = 20*numpy.log10(no_felt_i)

difference = decibel_felt - decibel_no_felt

pyplot.plot(distance_points, decibel_no_felt)
pyplot.plot(distance_points, decibel_felt)
pyplot.legend(['No felt', 'Felt'])
pyplot.axvspan(0, emission_duration * cm_per_ms, color='y', alpha=0.25)
#pyplot.axvspan(emission_duration * cm_per_ms,first_echo, color='r', alpha=0.25)
pyplot.axvspan(60, 150, color='y', alpha=0.25)
pyplot.xlabel('Distance')
pyplot.ylabel('dB')
pyplot.ylim(-30,10)

pyplot.subplot(2,2,3)
pyplot.plot(distance_points, difference)

pyplot.axvspan(0, emission_duration * cm_per_ms, color='y', alpha=0.25)
#pyplot.axvspan(emission_duration * cm_per_ms,first_echo, color='r', alpha=0.25)
pyplot.axvspan(60, 150, color='y', alpha=0.25)
pyplot.ylim(-15,15)
pyplot.grid()
pyplot.xlabel('Distance')
pyplot.ylabel('dB')

pyplot.tight_layout()
pyplot.show()