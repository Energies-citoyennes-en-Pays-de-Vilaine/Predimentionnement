import sys

if (len(sys.argv) != 3):
	print("error, usage :", sys.argv[0],"inpath", "outpath")
	exit()
summ = 0
dic = {}
count_dup = 0
with open(sys.argv[1]) as inp:
	for data in inp:
		split = data.split(";")
		if split[12] in dic.keys():
			#print(split[5])
			if (split[5][:3] == "Ill"):
				dic[split[12]] = data
			count_dup += 1
			#print(data, dic[split[12]])
		dic[split[12]] = data
print(count_dup)
with open(sys.argv[2], 'w') as outp:
	for key in dic.keys():
		print(dic[key], file=outp, end="")
