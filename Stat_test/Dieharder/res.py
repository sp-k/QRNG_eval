from os import listdir

dic = {}
dMaxP = {}
dMinP = {}
dMaxW = {}
dMinW = {}
for file in listdir('.'):
	if file == 'res.py':
		continue
	if file[7:] not in list(dic.keys()):
		dic[file[7:]] = {}
	with open(file, 'r') as f:
		lines = f.readlines()
		data = lines[8:117]+lines[118:120]+lines[121:123]+lines[124:]
	for line in data:
		d = line.split()
		if d[0][:-1] not in list(dic[file[7:]].keys()):
			dic[file[7:]][d[0][:-1]] = {'PASSED': 0, 'WEAK': 0, 'FAILED': 0}
		dic[file[7:]][d[0][:-1]][d[-1]] += 1
		
	dic[file[7:]]['PASSED'] = -1
	dic[file[7:]]['WEAK'] = -1
	dic[file[7:]]['FAILED'] = 0
	for item in dic[file[7:]].items():
		if item[0] in ['PASSED', 'WEAK', 'FAILED']:
			continue
		Max = max(item[1], key = lambda x: item[1][x])
		dic[file[7:]][Max] += 1
		if Max == 'PASSED':
			dic[file[7:]]['WEAK'] += 1
	if file[7:12] == '0.002':
		print(f'file: {file}')
		print('------------------------------------------------------------')
		for item in dic[file[7:]].items():
			print(f'{item[1]}\t{item[0]}')
		print(dic[file[7:]]['PASSED'], dic[file[7:]]['WEAK'],dic[file[7:]]['FAILED'])
		print('------------------------------------------------------------')
	key = float(file[7:11])
	if not key:
		key = float(file[7:12])
	if key not in list(dMaxP.keys()):
		dMaxP[key] = 0
	if key not in list(dMinP.keys()):
		dMinP[key] = 30
	if key not in list(dMaxW.keys()):
		dMaxW[key] = 0
	if key not in list(dMinW.keys()):
		dMinW[key] = 30
	dMaxP[key] = max(dMaxP[key], dic[file[7:]]['PASSED'])
	dMaxW[key] = max(dMaxW[key], dic[file[7:]]['WEAK'])
	dMinP[key] = min(dMinP[key], dic[file[7:]]['PASSED'])
	dMinW[key] = min(dMinW[key], dic[file[7:]]['WEAK'])
print(list(dMaxP.keys()))
print(list(dMaxP.values()))
print(list(dMinP.values()))
print(list(dMaxW.values()))
print(list(dMinW.values()))
