def two_fold_test(data, eps):
	n = len(data)
	
	# Apply step I: Interval estimation
	from math import sqrt
	from scipy.stats import chi2
	from statistics import mean, variance
	
	est_var = variance(data)
	est_mean = mean(data)
	
	print(f'Sample mean: {est_mean}')
	print(f'Sample variance: {est_var}')
	
	conf_interval = [(n-1)*est_var / chi2.ppf(1 - eps/2, df=n-1), (n-1)*est_var / chi2.ppf(eps/2, df=n-1)]
	
	if est_mean >= conf_interval[1]:
		# Variance is less than mean => sub_Poissonian
		return 0
	if est_mean <= conf_interval[0]:
		# Variance is greater than mean => super_Poissonian
		return 2
	
	# Apply step II: chi-square test
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
		exp = poisson.pmf(k, est_mean) * total_count
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
	else:
		return 1


from pickle import load, dump
filename = 'datafile_2fold_2'
with open(filename, 'rb') as datafile:
	dataset = load(datafile)

for j in range(1000):
	data = dataset[j]['data']
	dataset[j]['result']['two_fold_method'] = two_fold_test(list(map(float, data)), eps = 0.01)

with open(filename, 'wb') as datafile:
	dump(dataset, datafile)
