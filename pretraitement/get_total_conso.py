import sys
CATEGORY_ID = 8
if (len(sys.argv) != 3):
	print("error, usage" , sys.argv[0], "inpath", "position")
	exit(-1)
toskip = True
summ = {}
position = int(sys.argv[2])
with open(sys.argv[1]) as inp:
	for line in inp:
		split = line.split(";")
		if (toskip == True):
			print(split[position])
			toskip = False
			continue
		if (split[CATEGORY_ID] not in summ.keys()):
			summ[split[CATEGORY_ID]] = 0
		summ[split[CATEGORY_ID]] += float(split[position])
print(summ)