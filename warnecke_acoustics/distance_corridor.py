import numpy
from matplotlib import pyplot
from scipy.spatial.distance import  cdist
from scipy.interpolate import griddata

left_y = numpy.arange(0,300, 36)
left_x = numpy.ones(left_y.shape) * -60

right_y = numpy.arange(0,300, 12)
right_x = numpy.ones(right_y.shape) * 60

left = numpy.column_stack((left_x, left_y))
right = numpy.column_stack((right_x, right_y))

x_positions = numpy.linspace(-70, 70, 100)
y_positions = numpy.linspace(0,200,250)

x_positions, y_positions = numpy.meshgrid(x_positions, y_positions)

shape = x_positions.shape

x_positions = x_positions.flatten()
y_positions = y_positions.flatten()

left_distances = []
right_distances  = []

blind_zone = 1

for batx, baty in zip(x_positions, y_positions):
    selected_left = left_y > (baty + blind_zone)
    selected_right = right_y > (baty + blind_zone)
    selected_left = left[selected_left, :]
    selected_right = right[selected_right, :]

    current_position = numpy.array([[batx, baty]])

    distance_left = cdist(current_position, selected_left)
    distance_left = numpy.min(distance_left)
    distance_right = cdist(current_position, selected_right)
    distance_right = numpy.min(distance_right)

    left_distances.append(distance_left)
    right_distances.append(distance_right)

left_distances = numpy.array(left_distances)
right_distances = numpy.array(right_distances)
left_distances = numpy.reshape(left_distances, shape)
right_distances = numpy.reshape(right_distances, shape)

x_positions = numpy.reshape(x_positions, shape)
y_positions = numpy.reshape(y_positions, shape)

min_distance = numpy.minimum(left_distances , right_distances)

pyplot.contourf(x_positions,y_positions,min_distance, levels=30)
pyplot.scatter(left_x, left_y)
pyplot.scatter(right_x, right_y)
pyplot.grid()



x_positions = numpy.linspace(-70, 70, 100)
average = numpy.max(min_distance, axis=0)

pyplot.figure()
pyplot.plot(x_positions, average)
pyplot.grid()