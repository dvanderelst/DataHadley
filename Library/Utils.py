import os
import glob
import numpy as np
from natsort import natsorted


def time_axis(offset=0):
    samples = 200
    sample_rate = 10000
    max_time_ms = (samples / sample_rate) * 1000
    time_axis = np.linspace(0, max_time_ms, samples)
    time_axis = time_axis + offset
    return time_axis


def distance_axis(offset=0):
    samples = 200
    sample_rate = 10000
    max_time_ms = (samples / sample_rate) * 1000
    max_distance = max_time_ms * 17.15
    distance = np.linspace(0, max_distance, samples)
    distance = distance + offset
    return distance


def get_files(folder_path, pattern, full_path=False):
    search_pattern = os.path.join(folder_path, pattern)
    matching_files = glob.glob(search_pattern)
    sorted_files = natsorted(matching_files)
    if not full_path: sorted_files = [os.path.basename(f) for f in sorted_files]
    return sorted_files
