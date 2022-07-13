from datetime import datetime
import matplotlib.pyplot as plt
IN_FILE = "../../data/conso_sup36_bretagne.csv"
OUT_FILE = "../../../data/traite/inf36_region/bretagne/ENT2.csv"
CONSO_INDEX = 7
HORRAIRE_INDEX = 0
PLAGE_INDEX  = 4
DATE_INDEX = 0
usefull_plages = ["P3", "P7"]#totals
toskip = True
data = {}
with open(IN_FILE) as inp:
	for line in inp:
		if (toskip == True):
			toskip = False
			continue
		splittedLine = line.split(";")
		if (splittedLine[CONSO_INDEX] == ''):
			splittedLine[CONSO_INDEX] = "0"
		conso = float(splittedLine[CONSO_INDEX])
		plage = splittedLine[PLAGE_INDEX]
		date = splittedLine[DATE_INDEX]
		if plage[:2] in usefull_plages:
			if date not in data.keys():
				data[date] = 0
			data[date] += conso
dates = []
consos = []
with open(OUT_FILE, "w") as outp:
	for date in reversed([key for key in data.keys()]):
		print(date, data[date], sep=";", file=outp)