import matplotlib.pyplot as plt
from Library import Smoothn
from Library import DataSet
from Library import Process
import numpy as np

plot = True

Process.create_empty_directory('plots')
data_set = DataSet.DataSet('no-poles')
combos = data_set.combos
for index in range(combos):
    plt.close('all')
    data_set.plot_measurement(index=index)
    Process.save_image(index, prefix='vizualize_data')