IN_FILE = "../../data/conso_bretagne_i36.csv"
OUT_FILE = "../../../data/traite/inf36_region/bretagne/RES_Bretagne2.csv"
SOUTIRAGE_INDEX = 5
CONSO_INDEX = 6
REGION_INDEX = 1
HORRAIRE_INDEX = 0
PROFIL_INDEX = 3
PLAGE_INDEX  = 4
region_list = {}
first_line = None
with open(IN_FILE, "r") as inp:
	for line in inp:
		line = line.strip()
		line = ";".join(line.split(";")[:-2])
		if first_line == None:
			first_line = line
			continue
		splittedLine = line.split(";")
		region = splittedLine[REGION_INDEX]
		horraire = splittedLine[HORRAIRE_INDEX]
		if splittedLine[CONSO_INDEX] == '':
			splittedLine[CONSO_INDEX] = 0
		conso = float(splittedLine[CONSO_INDEX])
		soutirage = int(splittedLine[SOUTIRAGE_INDEX])
		profil = splittedLine[PROFIL_INDEX]
		plage = splittedLine[PLAGE_INDEX]
		region = region.replace("/", " et ")
		if (profil[:3] == "RES" and plage[:2] == "P0"):
			if region not in region_list.keys():
				region_list[region] = {}
			if (horraire not in region_list[region].keys()):
				region_list[region][horraire] = {}
			if (profil not in region_list[region][horraire].keys()):
				region_list[region][horraire][profil] = {}
				region_list[region][horraire][profil]["conso"] = 0
				region_list[region][horraire][profil]["soutirage"] = 0
				region_list[region][horraire][profil]["has_p0"] = False
			if (plage[:2] == "P0"):
				region_list[region][horraire][profil]["conso"] = conso
				region_list[region][horraire][profil]["soutirage"] = soutirage
				region_list[region][horraire][profil]["has_p0"] = True
			if region_list[region][horraire][profil]["has_p0"] != True:
				region_list[region][horraire][profil]["conso"] += conso
				region_list[region][horraire][profil]["soutirage"] += soutirage


for region in region_list.keys():
	for horraire in region_list[region].keys():
		conso = 0
		soutirage = 0
		for profil in region_list[region][horraire].keys():
			conso += region_list[region][horraire][profil]["conso"]
			soutirage += region_list[region][horraire][profil]["soutirage"] 
		region_list[region][horraire]["conso"] = conso
		region_list[region][horraire]["soutirage"] = soutirage
	with open(OUT_FILE, "w") as outp:
		horraire_list = []
		for horraire in region_list[region].keys():
			horraire_list.append(horraire)
		for horraire in reversed(horraire_list):
			print(horraire, region_list[region][horraire]["conso"],region_list[region][horraire]["soutirage"] , sep=";", file=outp)