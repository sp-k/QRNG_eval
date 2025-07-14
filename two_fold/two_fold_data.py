def get_result(data, tol = 1e-4):
	from statistics import mean, variance
	diff = mean(data) - variance(data)
	if diff > tol:
		return 0
	if diff < -tol:
		return 2
	return 1
	

from math import sqrt
from numpy.random import poisson
from pickle import load, dump
N = 1000
filename = 'datafile_2fold_2'
while N:
	print(f'\n***Running {1000-N+1} out of 1000...\n')
	dataset = poisson(lam = 10, size = 100000)
	result = {}
	result = {'direct_comparison': get_result(list(map(float, dataset)))}
	N -= 1

	try:
		with open(filename, 'rb') as datafile:
			data = load(datafile)
	except:
		data = []
	data.append({'data': dataset, 'result': result})
	with open(filename, 'wb') as datafile:
		dump(data, datafile)
