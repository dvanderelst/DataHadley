import matplotlib.pyplot as plt
from Library import Smoothn
from Library import DataSet
from Library import Process
import numpy as np

plot = True

Process.create_empty_directory('plots')
reference_set = DataSet.DataSet('no-poles')
compare_set = DataSet.DataSet('far-no-felt-poles')
felt_set = DataSet.DataSet('far-2x-felt-poles')

result0 = np.zeros(reference_set.combo_shape)
result1 = np.zeros(reference_set.combo_shape)
combos = reference_set.combos
plt.close('all')

for index in range(combos):
    # Get extent of pole echoes
    result = Process.compare_sets(reference_set, compare_set, index=index, plot=plot)
    start = result['start']
    end = result['end']
    if plot:
        Process.save_image(index, prefix='find_poles')
        plt.close('all')

    # Compare felt and no felt
    result = Process.compare_sets(compare_set, felt_set, index=index, plot=plot, extent=(start, end))
    if plot:
        Process.save_image(index, prefix='felt_result')
        plt.close('all')

    delta0 = result['delta0']
    delta1 = result['delta1']
    i, j, k = result['indices']
    result0[i, j, k] = delta0
    result1[i, j, k] = delta1

#%%
# selected0 = result0[:, :, 0]
# selected0 = np.nanmean(selected0, axis=0)
# selected1 = result1[:, :, 0]
# selected1 = np.nanmean(selected1, axis=0)
#
# plt.figure()
# plt.plot(selected0)
# plt.plot(selected1)
# plt.show()

selected0 = np.nanmean(result0, axis=0)
selected1 = np.nanmean(result1, axis=0)

minn = np.min(np.minimum(selected0, selected1))
maxx = np.max(np.maximum(selected0, selected1))
minn = -5
maxx = 1


plt.figure()
plt.subplot(1,2,1)
plt.imshow(selected0, vmin=minn, vmax=maxx, cmap='jet')
plt.colorbar()
plt.subplot(1,2,2)
plt.imshow(selected1, vmin=minn, vmax=maxx, cmap='jet')
plt.colorbar()
plt.show()

