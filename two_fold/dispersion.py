def dispersion_test(data, eps):
	n = len(data)
	
	# Apply step I: Interval estimation
	from math import sqrt
	from scipy.stats import chi2
	from statistics import mean, variance
	
	est_var = variance(data)
	est_mean = mean(data)
	
	print(f'Sample mean: {est_mean}')
	print(f'Sample variance: {est_var}')
	
	upper = chi2.ppf(1-eps, df=n-1)
	lower = chi2.ppf(eps, df=n-1)
	
	if est_var*(n-1)/est_mean >= upper:
		# Variance is less than mean => sub_Poissonian
		return 0
	if est_var*(n-1)/est_mean <= lower:
		# Variance is greater than mean => super_Poissonian
		return 2
	else:
		return 1


from pickle import load, dump
filename = 'datafile_2fold_1'
with open(filename, 'rb') as datafile:
	dataset = load(datafile)

for j in range(1000):
	data = dataset[j]['data']
	dataset[j]['result']['dispersion_method'] = dispersion_test(list(map(float, data)), eps = 0.01)

with open(filename, 'wb') as datafile:
	dump(dataset, datafile)
