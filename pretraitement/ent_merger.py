from datetime import datetime, timedelta
FILES_TO_MERGE = ["../../../data/traite/inf36_region/bretagne/ENT.csv", "../../../data/traite/inf36_region/bretagne/ENT2.csv"]
OUT_FILE = "../../../data/traite/inf36_region/bretagne/ENT_MERGED.csv"
DATE_INDEX = 0
CONS_INDEX = 1
data_to_merge = {}
print("loading data")
for file in FILES_TO_MERGE:
	data_to_merge[file] = {}
	with open(file) as inp:
		for line in inp:
			splitted_line = line.split(";")
			date = datetime.strptime(splitted_line[DATE_INDEX][:16], "%Y-%m-%dT%H:%M")
			#date -= timedelta(hours = int(splitted_line[DATE_INDEX].split("+")[1][:2]))
			date_hour = datetime.strptime(splitted_line[DATE_INDEX][:13], "%Y-%m-%dT%H")
			#date_hour -= timedelta(hours = int(splitted_line[DATE_INDEX].split("+")[1][:2]))
			cons = float(splitted_line[CONS_INDEX])
			if date_hour not in data_to_merge[file].keys():
				data_to_merge[file][date_hour] = 0
			data_to_merge[file][date_hour] += cons

def get_merged_dates(dates1, dates2):
	dates1 = sorted(dates1)
	dates2 = sorted(dates2)
	dates_to_return = []
	i = 0
	j = 0
	while(i < len(dates1)):
		while (dates1[i] > dates2[j] and j < len(dates2)):
			j += 1
		if (dates1[i] == dates2[j]):
			dates_to_return.append(dates1[i])
		i += 1
	return dates_to_return

print("merging dates")
dates = [d for d in data_to_merge[FILES_TO_MERGE[0]].keys()]
for i in range(1, len(FILES_TO_MERGE)):
	dates = get_merged_dates(dates, [d for d in data_to_merge[FILES_TO_MERGE[i]].keys()])
print(len(dates))
print("writing out file")
with open(OUT_FILE, "w") as outp:
	for d in dates:
		conso = 0
		for file in FILES_TO_MERGE:
			conso += data_to_merge[file][d]
		print(d.strftime("%Y-%m-%dT%H:%M+00"), data_to_merge[file][d], sep = ";", file = outp)