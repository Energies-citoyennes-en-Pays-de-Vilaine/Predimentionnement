from __future__ import annotations
from typing import *
from datetime import datetime, timedelta
from math import floor
import numpy as np
import matplotlib.pyplot as plt
class Period:
	beginning : datetime
	end : datetime
	def __init__(self, beginning : Union[datetime, str], end : Union[datetime, str]):
		if (isinstance(beginning, str)):
			beginning = datetime.strptime(beginning, "%d/%m/%Y:%H")
		if (isinstance(end, str)):
			end = datetime.strptime(end, "%d/%m/%Y:%H")
		self.beginning = beginning
		self.end = end

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

	def __add__(self, p2 : Union[PowerData, float, int]) -> PowerData:
		if (isinstance(p2, float)):
			return PowerData(self.dates[:], p2 + self.power)
		if (isinstance(p2, int)):
			return PowerData(self.dates[:], p2 + self.power)
		if not self.check_simalarity(p2):
			raise("data should be similar to be added")#expect data to have the same dateTime
		return PowerData(self.dates[:], p2.power + self.power)
	
	def __sub__(self, p2 : PowerData) -> PowerData:
		if not self.check_simalarity(p2):
			raise("data should be similar to be added")#expect data to have the same dateTime
		return PowerData(self.dates[:], self.power - p2.power)

	def __mul__(self, toMul : Union[np.array, List[float], float, PowerData, int]) -> PowerData:
		if (isinstance(toMul, float)):
			return PowerData(self.dates, self.power * toMul)
		if (isinstance(toMul, int)):
			return PowerData(self.dates, self.power * toMul)
		if (isinstance(toMul, PowerData)):
			return PowerData(self.dates, self.power * toMul.power)
		if len(self.power) == len(toMul):
			return PowerData(self.dates, self.power * np.array(toMul))

	def __truediv__(self, toDivBy : Union[np.array, List[float], float, PowerData]) -> PowerData:
		if (isinstance(toDivBy, float)):
			return PowerData(self.dates, self.power / toDivBy)
		if (isinstance(toDivBy, PowerData)):
			power = []
			for i in range(len(self.power)):
				if toDivBy.power[i] == 0:
					power.append(0)
				else:
					power.append(self.power[i]/toDivBy.power[i])
			return PowerData(self.dates, np.array(power))
		if len(self.power) == len(toDivBy):
			return PowerData(self.dates, self.power / np.array(toDivBy))

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
	
	def get_slice_over_period(self, beginning: datetime = None, end : datetime = None) -> PowerData:
		if (beginning == None):
			beginning = self.dates[0]
		if (end == None):
			end = self.dates[-1]
		i = 0
		while(i < len(self.dates) and self.dates[i] < beginning):
			i += 1
		j = i
		powerToReturn : List[float] = []
		dateToReturn : List[datetime] = []
		while(j < len(self.dates) and self.dates[j] < end):
			powerToReturn.append(self.power[j])
			dateToReturn.append(self.dates[j])
			j += 1
		return PowerData(dateToReturn, np.array(powerToReturn))

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
	def get_rolling_average(self, count) -> PowerData:
		current_sum = 0
		powerToReturn = []
		for i in range(floor(count/2)):
			current_sum += self.power[i]
		for i in range(len(self.power)):
			powerToReturn.append(current_sum / count)
			if (i + floor(count/2) < len(self.power)):
				current_sum += self.power[i + floor(count/2)]
			if (i - floor(count/2) > 0):
				current_sum -= self.power[i - floor(count/2)]
		return PowerData(self.dates, np.array(powerToReturn))
	def get_cumulated_average(self) -> PowerData:
		data = 0
		power = []
		for i in range(len(self.power)):
			data += self.power[i]
			power.append(data/(i+1))
		return PowerData(self.dates, np.array(power))
	def get_bigger_than(self, power : Union[int,float]) -> PowerData:
		toReturn = []
		for i in range(len(self.power)):
			if (self.power[i] <= power):
				toReturn.append(power)
			else:
				toReturn.append(self.power[i])
		return PowerData(self.dates, np.array(toReturn))
	def get_copy(self) -> PowerData:
		return PowerData(self.dates, np.copy(self.power))
	def get_average(self, beginning : datetime = None, end : datetime = None) -> float:
		if (beginning == None):
			beginning = self.dates[0]
		if (end == None):
			end = self.dates[-1]
		i = 0
		while(i < len(self.dates) and self.dates[i] < beginning):
			i += 1
		j = i
		summ = 0.0
		while(j < len(self.dates) and self.dates[j] < end):
			summ += self.power[j]
			j += 1
		return summ / (j - i)
	def get_merged_to(self, p2 : PowerData) -> PowerData:
		if (len(self.dates) == 0):
			return p2.get_copy()
		if (self.dates[0] < p2.dates[0]):
			return PowerData(self.dates + p2.dates,np.concatenate((self.power, p2.power)))
		else:
			return PowerData(p2.dates + self.dates, np.concatenate(p2.power, self.power))
	def get_scaled(self, power : Union[List[float], float], periods : List[Period] = None) -> PowerData:
		if (isinstance(power, float) or isinstance(power, int)):
			return self/self.get_average() * power

		toReturn = PowerData([], np.array([]))
		for i in range(len(power)):
			newPowerData = self.get_slice_over_period(periods[i].beginning, periods[i].end)
			newPowerData = newPowerData / newPowerData.get_average()
			newPowerData = newPowerData * power[i]
			toReturn = toReturn.get_merged_to(newPowerData)
		return toReturn

class Battery(PowerData):
	capacity : float
	def __init__(self, capacity : float, dates: List[datetime] = None, power: np.array = None):
		if dates is None or power is None:
			dates = []
			power = np.array([])
		super().__init__(dates, power)
		self.capacity = capacity #capacity is in wh
		#convention is here power is positive to charge the battery
		self.dated_energy = []
	def from_power_data(self, data : PowerData):
		self.power = np.copy(data.power)
		self.dates = data.dates[:]
		energy = 0.0
		self.power[0] = 0.0
		self.dated_energy = [0]
		for i in range(len(self.dates) - 1):
			time_delta = ((self.dates[i + 1] - self.dates[i]).seconds / 3600)
			nextEnergy = energy + self.power[i + 1] * time_delta
			nextEnergy = min(max(nextEnergy, 0), self.capacity)
			self.power[i + 1] = (nextEnergy - energy) / time_delta
			energy = nextEnergy
			self.dated_energy.append(nextEnergy)
			
			