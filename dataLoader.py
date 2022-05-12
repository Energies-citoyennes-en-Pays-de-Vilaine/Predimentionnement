from __future__ import annotations
from typing import *
from datetime import datetime, timedelta
import numpy as np

if len(__name__.split("."))==1:
	from calc import PowerData, Period
else:
	from .calc import PowerData, Period

class dataloader():
	def load_prod(self, path : str, startDate : Optional[datetime] = None) -> PowerData:
		#expecting a csv mm/dd/yyyy hh:mm:ss,"12,34"
		with open(path) as inp:
			first_line = True
			dates = []
			power = []
			for line in inp:
				if first_line or line.strip() == '':
					first_line = False
					continue
				splittedLine = line.split('"')
				if (len(splittedLine) == 1):
					splittedLine = line.split(",")
				date = datetime.strptime(splittedLine[0].strip(","), "%m/%d/%Y %H:%M:%S")
				if (startDate != None and date < startDate):
					continue
				dates.append(date)
				power.append(float(splittedLine[1].replace(",", ".")))
		return PowerData(dates, np.array(power))
	def load_one_user(self, path : str, startDate : Optional[datetime] = None) -> PowerData:
		#expecting a csv mm/dd/yyyy hh:mm:ss,"12,34"
		with open(path) as inp:
			first_line = True
			dates = []
			power = []
			for line in inp:
				if first_line or line.strip() == '':
					first_line = False
					continue
				splittedLine = line.split(';')
				
				date = datetime.strptime(splittedLine[0][:16], "%Y-%m-%dT%H:%M")
				date -= timedelta(hours = int(splittedLine[0].split("+")[1][:2]))
				if (startDate != None and date < startDate):
					continue
				dates.append(date)
				power.append(float(splittedLine[1]))
		return PowerData(dates, np.array(power))
	def load_solar_panel_prod(self, path : str, startDate : Optional[datetime] = None) -> PowerData:
		#expecting a csv mm/dd/yyyy hh:mm:ss,"12,34"
		with open(path) as inp:
			dates = []
			power = []
			for line in inp:
				splittedLine = line.split(';')
				date = datetime.strptime(splittedLine[0], "%Y-%m-%d:%H")
				if (startDate != None and date < startDate):
					continue
				dates.append(date)
				power.append(float(splittedLine[1]))
		return PowerData(dates, np.array(power))
				
