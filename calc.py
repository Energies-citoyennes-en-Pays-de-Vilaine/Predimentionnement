from __future__ import annotations
from typing import *
from datetime import datetime
import numpy as np

class PowerData():
	power : np.array
	dates : List[datetime]
	def check_simalarity(self, p2:PowerData) -> bool:	
		if (len(self.dates) != len(p2.dates) or len(self.power) != len(p2.power)):
			return False
		for i in range(len(self.dates)):
			if self.dates[i] != p2.dates[i]:
				return False
		return True

	def __add__(self, p2 : PowerData) -> PowerData:
		if not self.check_simalarity(p2):
			raise("data should be similar to be added")#expect data to have the same dateTime
		return PowerData(self.dates[:], p2.power + self.power)
	
	def __sub__(self, p2 : PowerData) -> PowerData:
		if not self.check_simalarity(p2):
			raise("data should be similar to be added")#expect data to have the same dateTime
		return PowerData(self.dates[:], p2.power - self.power)

	def __mul__(self, toMul : Union[np.array, List[float], float, PowerData]) -> PowerData:
		if (isinstance(toMul, float)):
			return PowerData(self.dates, self.power * toMul)
		if (isinstance(toMul, PowerData)):
			return PowerData(self.dates, self.power * toMul.power)
		if len(self.power) == len(toMul):
			return PowerData(self.dates, self.power * np.array(toMul))
	
	def __init__(self, dates: List[datetime], power : np.array):
		if (len(power) != len(dates)):
			raise("power and dates should have the same length")
		self.power = power
		self.dates = dates[:]

	def get_slice(self, dates: List[datetime]) -> PowerData:
		power = []
		i = 0
		#this function assumes the array is sorted to drop the complexity by one magnitude
		for d in dates:
			while(self.dates[i] < d):
				i += 1
			power.append(self.power[i])
		return PowerData(dates, np.array(power))

	def get_intersect(self, p2 : PowerData) -> List[datetime]:
		#this function assumes the date arrays are sorted to speed up the process
		toReturn:List[datetime] = []
		i = 0
		j = 0
		while (i < len(self.dates) and j < len(p2.dates)):
			if (self.dates[i] == p2.dates[j]):
				toReturn.append(self.dates[i])
				i += 1
				j += 1
			elif (self.dates[i] < p2.dates[j]):
				i += 1
			else:
				j += 1
		return toReturn
