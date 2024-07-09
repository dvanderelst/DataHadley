import pandas as pd
from matplotlib import pyplot as plt
set1 = pd.read_csv('warnecke_acoustics/warnecke1.csv')
set1 = set1.query('x < 15')
call_onset = 3
call_offset = 3 + 1.5
first_possible_echo = (15 / 17) + call_onset

plt.figure()
plt.plot(set1['x'], set1['NoFelt'], label='NoFelt')
plt.plot(set1['x'], set1['1Felt'], label='1Felt')
plt.plot(set1['x'], set1['2Felt'], label='2Felt')
plt.vlines(call_onset, 20, 80, linestyles='--', colors='g', label=str('call_onset'))
plt.vlines(call_offset, 20, 80, linestyles='--', colors='k', label=str('call_offset'))
plt.vlines(first_possible_echo, 20, 80, linestyles='--', colors='r',label=str('first_possible_echo'))
plt.title('Data were recorded 45 cm from the dense corridor side')
plt.legend()
plt.grid()
plt.show()
