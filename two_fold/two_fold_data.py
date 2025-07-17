'''This script generates data and performs direct comparision of mean and variance
followed by Goodness-of-Fit test for Poisson distribution on the generated data.'''

def get_result(data, eps, tol = 1e-4):
	'''Performs direct comparision of mean and variance
	followed by Goodness-of-Fit test for Poisson distribution
	Arguments:
		data [list]: A sample dataset generated from some distribution
		eps [float]: significant level for the GoF test
		[optional] tol [float]: error tolerence for direct comparison
	returns:
		[int] 0/1/2 for sub-/Poissonian/super-Poissonian distribution
		-1 in case of Poissonain but not Poisson
	'''
	
	# Direct Comparison
	from statistics import mean, variance
	diff = mean(data) - variance(data)
	if diff > tol:
		return 0	# sub-Poissonian
	if diff < -tol:
		return 2	# super-Poissonian
		
	
	
	# Apply chi-square test for GoF
	from scipy.stats import poisson, chisquare
	from collections import Counter
	
	binned_data = [int(x) for x in data if x >= 0]
	count_data = Counter(binned_data)
	max_observed = int(max(count_data.keys()))

	# Build observed and expected frequencies
	obs_freq = []
	exp_freq = []
	total_count = len(binned_data)

	for k in range(0, max_observed + 1):
		obs = count_data.get(k, 0)
		exp = poisson.pmf(k, mean(data)) * total_count
		obs_freq.append(obs)
		exp_freq.append(exp)
	
	if sum(obs_freq) != sum(exp_freq):
		exp_freq[-1] += sum(obs_freq) - sum(exp_freq)

	# Combine low-frequency tail if necessary (to meet chi-square assumptions)
	# Combine bins where exp < 5
	def combine_tail(obs, exp):
		new_obs, new_exp = [], []
		temp_obs, temp_exp = 0, 0
		for o, e in zip(obs, exp):
		    if e < 5:
		        temp_obs += o
		        temp_exp += e
		    else:
		        if temp_exp > 0:
		            new_obs.append(temp_obs)
		            new_exp.append(temp_exp)
		            temp_obs, temp_exp = 0, 0
		        new_obs.append(o)
		        new_exp.append(e)
		if temp_exp > 0:
		    new_obs.append(temp_obs)
		    new_exp.append(temp_exp)
		return new_obs, new_exp

	obs_freq, exp_freq = combine_tail(obs_freq, exp_freq)

	# Chi-Square Test
	chi2_stat, p_value = chisquare(f_obs = obs_freq, f_exp = exp_freq)
	
	if p_value < eps:
		return -1
	return 1
	

from math import sqrt
from numpy.random import poisson, geometric, normal
from pickle import load, dump
N = 1000
filename = 'datafile_2fold_3'
while N:
	print(f'\n***Running {1000-N+1} out of 1000...\n')
	# dataset = geometric(p = 0.5, size = 100000)
	# dataset = poisson(lam = 0.5, size = 100000)
	dataset = normal(loc = 0.5, scale = sqrt(0.5), size = 100000)
	result = {}
	result = {'direct_comparison': get_result(list(map(float, dataset)), eps = 0.01)}
	N -= 1

	try:
		with open(filename, 'rb') as datafile:
			data = load(datafile)
	except:
		data = []
	data.append({'data': dataset, 'result': result})
	with open(filename, 'wb') as datafile:
		dump(data, datafile)
