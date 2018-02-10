import xlrd

def getData(filename, index_sheet):
	data = xlrd.open_workbook(filename)
	sheet = data.sheet_by_index(index_sheet)
	return sheet

data = getData("dummy.xls",0)

def laplace(data, value, x):
	vy = 1.0
	vn = 1.0
	for row in range(data.nrows):
		if data.cell_value(row, x)==value and data.cell_value(row, 4)=='Yes':
			vy += 1.0
		elif data.cell_value(row, x)==value and data.cell_value(row, 4)=='No':
			vn += 1.0
	return [vy, vn]

def yes_no(data, value1, value2, value3, value4, x):
	d = laplace(data, value1, x)
	e = laplace(data, value2, x)
	if (value3 == 0) and (value4 == 0):	f = [0,0]; g = [0,0]
	elif (value4 == 0): f = laplace(data, value3, x); g = [0,0]
	else: f = laplace(data, value3, x); g = laplace(data, value4, x)
	yes = [d[0],e[0],f[0],g[0]]
	no = [d[1],e[1],f[1],g[1]]
	return [yes, no]

def likelihood(data, value1, value2, value3, value4, x, test, delay):
	d = yes_no(data, value1, value2, value3, value4, x)
	yes = 0; no = 0; j = 0
	for i in d[0]: 
		yes+= d[0][j]; no+= d[1][j]; j+=1
	
	if (test==value1) and delay=='Yes': likeli = d[0][0]/yes; return likeli
	elif (test==value2) and delay=='Yes': likeli = d[0][1]/yes; return likeli
	elif (test==value3) and delay=='Yes': likeli = d[0][2]/yes; return likeli
	elif (test==value4) and delay=='Yes': likeli = d[0][3]/yes; return likeli
	elif (test==value1) and delay=='No': likeli = d[1][0]/no; return likeli
	elif (test==value2) and delay=='No': likeli = d[1][1]/no; return likeli
	elif (test==value3) and delay=='No': likeli = d[1][2]/no; return likeli
	elif (test==value4) and delay=='No': likeli = d[1][3]/no; return likeli

def probability(test1, test2, test3, test4, delay):
	international = likelihood(data, 'Yes', 'No', 0, 0, 0, test1, delay)
	time = likelihood(data, 'Morning', 'Evening', 'Afternoon', 'Dawn', 1, test2, delay)
	weather = likelihood(data, 'Clear', 'Rainy', 'Cloudy', 0, 2, test3, delay)
	wind = likelihood(data, 'Weak', 'Strong', 'Moderate', 0, 3, test4, delay)
	
	d = laplace(data, 'Yes', 4); e = laplace(data, 'No', 4)
	delay = [d[0],e[1]]; total = d[0]+e[1]
	likeli_yes = delay[0]/total
	likeli_no = delay[1]/total
	
	if delay=='Yes': probability = international * time * weather * wind * likeli_yes; return probability
	else: probability = international * time * weather * wind * likeli_no; return probability

def delay(x,y):
	if x>y: print ("Delay : Yes")
	else: print ("Delay : No")

d1=probability('Yes', 'Dawn', 'Cloudy', 'Strong', 'Yes')
d2=probability('Yes', 'Dawn', 'Cloudy', 'Strong', 'No')
e1=probability('No', 'Evening', 'Clear', 'Weak', 'Yes')
e2=probability('No', 'Evening', 'Clear', 'Weak', 'No')

print ("TESTING DATA-1")
print ("Value Yes : %.4f " % (d1), "Value No : %.4f " % (d2))
delay(d1,d2)
print (" ")
print ("TESTING DATA-2")
print ("Value Yes : %.4f " % (e1), "Value No : %.4f " % (e2))
delay(e1,e2)