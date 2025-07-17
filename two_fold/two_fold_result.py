'''Prints results'''

from pickle import load
with open('datafile_2fold_2', 'rb') as datafile:
	data = load(datafile)

types = ['direct_comparison', 'two_fold_method', 'dispersion_method']
result = {types[0]: {-1: 0, 0: 0, 1: 0, 2: 0}, types[1]: {-1: 0, 0: 0, 1: 0, 2: 0}, types[2]: {-1: 0, 0: 0, 1: 0, 2: 0}}

for j in range(1000):
	for typ in types:
		result[typ][data[j]['result'][typ]] += 1

print(result)
