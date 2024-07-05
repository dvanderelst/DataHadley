import numpy as np
from os import path
import os
import shutil
from matplotlib import pyplot as plt


def find_threshold_crossings(arr, threshold1, threshold2):
    start_index = None
    end_index = None
    exceeding = False
    for i in range(len(arr)):
        if not exceeding and arr[i] > threshold1:
            start_index = i
            exceeding = True
        elif exceeding and arr[i] < threshold2:
            end_index = i
            break
    return start_index, end_index


def find_difference(ref, comp, index, ear):
    threshold = 6
    reference, _, _ = ref.get_measurement(index, type='d', ear=ear)
    signal, _, _ = comp.get_measurement(index, type='d', ear=ear)
    difference = signal - reference

    start_index, end_index = find_threshold_crossings(difference, 6, -1)
    if start_index is not None:
        end_index = start_index + 50
        if end_index > len(difference)-1: end_index = len(difference)-1
    return start_index, end_index


def compare_sets(ref, comp, index, plot=False, extent=False):
    if not extent:
        start_index0, end_index0 = find_difference(ref, comp, index, 0)
        start_index1, end_index1 = find_difference(ref, comp, index, 1)
        start = min_none((start_index0, start_index1))
        end = max_none((end_index0, end_index1))
    if extent:
        start = extent[0]
        end = extent[1]

    distance_axis = ref.distance_axis
    reference_label = ref.description
    comp_label = comp.description

    start_distance = distance_axis[start]
    end_distance = distance_axis[end]

    _, indices, position = ref.get_measurement(index, type='d', ear=0)

    # Get data ear 0
    reference0, _, _ = ref.get_measurement(index, type='d', ear=0)
    comp0, _, _ = comp.get_measurement(index, type='d', ear=0)
    difference0 = comp0 - reference0
    delta0 = np.mean(difference0[start:end])
    # Get data ear 1
    reference1, _, _ = ref.get_measurement(index, type='d', ear=1)
    comp1, _, _ = comp.get_measurement(index, type='d', ear=1)
    difference1 = comp1 - reference1
    delta1 = np.mean(difference1[start:end])

    if plot:
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(distance_axis, reference0, label=reference_label)
        plt.plot(distance_axis, comp0, label=comp_label)
        plt.axvspan(start_distance, end_distance, color='red', alpha=0.25)
        plt.title('ear 0 ' + str(indices) + str(position))
        plt.legend(loc='upper right')

        plt.subplot(2, 1, 2)
        plt.plot(distance_axis, reference1, label=reference_label)
        plt.plot(distance_axis, comp1, label=comp_label)
        plt.axvspan(start_distance, end_distance, color='red', alpha=0.25)
        plt.title('ear 1 ' + str(indices) + str(position))
        plt.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    result = {}
    result['reference0'] = reference0
    result['reference1'] = reference1
    result['comp0'] = comp0
    result['comp1'] = comp1
    #
    result['start_distance'] = start_distance
    result['end_distance'] = end_distance
    result['start'] = start
    result['end'] = end
    #
    result['difference0'] = delta0
    result['difference1'] = delta1
    result['delta0'] = delta0
    result['delta1'] = delta1
    #
    result['indices'] = indices
    result['position'] = position
    return result


def max_none(values, none_value=0):
    filtered_values = [v for v in values if v is not None]
    if not filtered_values: return none_value
    return max(filtered_values)


def min_none(values, none_value=0):
    filtered_values = [v for v in values if v is not None]
    if not filtered_values: return none_value
    return min(filtered_values)

def ratio2db(ratio):
    db = 20 * np.log10(ratio)
    return db


def db2ratio(db):
    db = np.array(db, dtype='f')
    db = db.astype(float)
    ratio = 10 ** (db / 20.0)
    return ratio


def create_empty_directory(directory_path):
    if os.path.exists(directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        os.makedirs(directory_path)


def save_image(index, prefix=''):
    fig = plt.gcf()
    name = image_filename(index, prefix=prefix)
    fig.savefig(name)


def image_filename(number, prefix):
    name = prefix + '_image' + f"{number:0{5}d}" + '.png'
    name = path.join('plots', name)
    return name


