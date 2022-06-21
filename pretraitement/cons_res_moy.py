IN_FILE = "../../../data/traite/inf36_region/bretagne/RES_Bretagne2.csv"
OUT_FILE = "../../data/foyer/breton/averageUser.csv"

DATE_INDEX      = 0
CONSO_INDEX     = 1
SOUTIRAGE_INDEX = 2
from datetime import *


fulldata = {}
with open(IN_FILE, "r") as inp:

	for line in inp:
		splitted_line = line.split(";")
		date = datetime.strptime(splitted_line[DATE_INDEX][:16], "%Y-%m-%dT%H:%M")
		date -= timedelta(hours = int(splitted_line[DATE_INDEX].split("+")[1][:2]))
		date_hour = datetime.strptime(splitted_line[DATE_INDEX][:13], "%Y-%m-%dT%H")
		date_hour -= timedelta(hours = int(splitted_line[DATE_INDEX].split("+")[1][:2]))
		if (date_hour not in fulldata.keys()):
			fulldata[date_hour] = {}
			fulldata[date_hour]["date"] = date_hour.strftime("%Y-%m-%dT%H:%M+00")
			fulldata[date_hour]["conso"] = 0.0
			fulldata[date_hour]["soutirage"] = int(splitted_line[SOUTIRAGE_INDEX])
		fulldata[date_hour]["conso"] += float(splitted_line[CONSO_INDEX])
with open(OUT_FILE, "w") as outp:
	for key in fulldata.keys():
		print( fulldata[key]["date"], fulldata[key]["conso"] / fulldata[date_hour]["soutirage"], sep=";", file=outp)