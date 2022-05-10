from calc import *
from datetime import *
def prod_bretagne(inpath, outpath):
	DATE_POS = 0
	TYPE_PROD_POS = 4
	ENERGY_POS = 6
	toTreat = {"F5" : "Solaire"}
	dates = {}
	prods = {}
	for key in toTreat.keys():
		dates[key] = []
		prods[key] = []
	with open(inpath, 'r') as inp:
		first_line = None
		for line in inp:
			if (first_line == None):
				first_line = line
				continue
			splittedLine = line.split(";")
			date = splittedLine[DATE_POS]
			type_prod = splittedLine[TYPE_PROD_POS]
			if(splittedLine[ENERGY_POS].strip() == ''):
				splittedLine[ENERGY_POS] = "0.0"
			energy_prod = float(splittedLine[ENERGY_POS].strip())
			parsedDate = datetime.strptime(date[:16], "%Y-%m-%dT%H:%M")
			dateUTC = parsedDate - timedelta(hours = int(date.split("+")[1][:2]))
			key = type_prod[:2]
			if (key in toTreat.keys()):
				dates[key].append(parsedDate)
				prods[key].append(energy_prod)
	for key in toTreat.keys():
		#assumes the data is just in decreasing date order, reverses the data
		dates[key] = [d for d in reversed(dates[key])]
		prods[key] = [p for p in reversed(prods[key])]
		hourlyDates : List[datetime] = []
		hourlyProds : List[float] = []
		for i in range(len(dates[key])):
			date = dates[key][i]
			if len(hourlyDates) != 0 and hourlyDates[-1].hour == date.hour:
				hourlyProds[-1] += prods[key][i]
			else:
				hourlyDates.append(date)
				hourlyProds.append(prods[key][i])
		with open(outpath + f"{toTreat[key]}.csv", "w") as outp:
			for i in range(len(hourlyDates)):
				print(hourlyDates[i].strftime("%Y-%m-%dT%H"), hourlyProds[i], sep=";", file=outp)