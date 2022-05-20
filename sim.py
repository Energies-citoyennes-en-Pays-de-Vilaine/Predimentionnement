from __future__ import annotations
from calc import *
from typing import *
from dataclasses import dataclass

class SimParams():
	#when implemented, the batteries will come after the flexibility, or both will be used by python's optimize
	#defaults to false
	has_solar             : bool
	has_wind              : bool
	has_bioenergy         : bool
	has_piloted_bioenergy : bool
	has_battery           : bool
	has_flexibility       : bool

	#defaults to true
	has_solar_scaling             : bool
	has_wind_scaling              : bool
	has_bioenergy_scaling         : bool
	has_piloted_bioenergy_scaling : bool
	has_consumer_scaling          : Union[bool, List[bool]]

	#defaults to 0.0
	solar_power             : float
	wind_power              : float
	bioenergy_power         : float
	battery_capacity        : float
	piloted_bioenergy_power : float
	flexibility_ratio       : Union[float, List[float]]
	consumer_power          : Union[float, List[float]]
	consumer_contrib        : List[float]
	#defaults to None
	solar_curve             : PowerData
	wind_curve              : PowerData
	bioenergy_curve         : PowerData
	consumer_curves         : Union[List[PowerData], PowerData]

	def __init__(self, \
		has_solar                     : bool = False,\
		has_wind                      : bool = False,\
		has_bioenergy                 : bool = False,\
		has_piloted_bioenergy         : bool = False,\
		has_battery                   : bool = False,\
		has_flexibility               : bool = False,\
		has_solar_scaling             : bool = True,\
		has_wind_scaling              : bool = True,\
		has_bioenergy_scaling         : bool = True,\
		has_piloted_bioenergy_scaling : bool = True,\
		has_consumer_scaling          : Union[bool, List[bool]] = False,\
		solar_power                   : float = 0.0,\
		wind_power                    : float = 0.0,\
		bioenergy_power               : float = 0.0,\
		battery_capacity              : float = 0.0,\
		piloted_bioenergy_power       : float = 0.0,\
		flexibility_ratio             : Union[float, List[float]] = 0.0,\
		consumer_power                : Union[float, List[float]] = 0.0,\
		consumer_contrib              : List[float] = None,\
		solar_curve                   : PowerData = None,\
		wind_curve                    : PowerData = None,\
		bioenergy_curve               : PowerData = None,\
		consumer_curves               : Union[List[PowerData], PowerData] = None\
	) -> None:
		self.has_solar             : bool = has_solar
		self.has_wind              : bool = has_wind
		self.has_bioenergy         : bool = has_bioenergy
		self.has_piloted_bioenergy : bool = has_piloted_bioenergy
		self.has_battery           : bool = has_battery
		self.has_flexibility       : bool = has_flexibility
		
		self.has_solar_scaling             : bool = has_solar_scaling
		self.has_wind_scaling              : bool = has_wind_scaling
		self.has_bioenergy_scaling         : bool = has_bioenergy_scaling
		self.has_piloted_bioenergy_scaling : bool = has_piloted_bioenergy_scaling
		self.has_consumer_scaling          : Union[bool, List[bool]] = has_consumer_scaling

		self.solar_power             : float = solar_power
		self.wind_power              : float = wind_power
		self.bioenergy_power         : float = bioenergy_power
		self.battery_capacity        : float = battery_capacity
		self.piloted_bioenergy_power : float = piloted_bioenergy_power
		self.flexibility_ratio       : Union[float, List[float]] = flexibility_ratio
		self.consumer_power          : Union[float, List[float]] = consumer_power
		self.consumer_contrib        : Union[float, List[float]] = consumer_contrib

		self.solar_curve             : PowerData = solar_curve.get_copy() 
		self.wind_curve              : PowerData = wind_curve.get_copy()
		self.bioenergy_curve         : PowerData = bioenergy_curve.get_copy()
		self.consumer_curves         : Union[PowerData, List[PowerData]] = consumer_curves
		
		self.check_and_convert_params()

	def get_clone(self) -> SimParams:
		return SimParams(
			has_solar                     = self.has_solar                    ,
			has_wind                      = self.has_wind                     ,
			has_bioenergy                 = self.has_bioenergy                ,
			has_piloted_bioenergy         = self.has_piloted_bioenergy        ,
			has_battery                   = self.has_battery                  ,
			has_flexibility               = self.has_flexibility              ,
			has_solar_scaling             = self.has_piloted_bioenergy_scaling, 
			has_wind_scaling              = self.has_bioenergy_scaling        , 
			has_bioenergy_scaling         = self.has_wind_scaling             , 
			has_piloted_bioenergy_scaling = self.has_solar_scaling            , 
			has_consumer_scaling          = self.has_consumer_scaling if isinstance(self.has_consumer_scaling, bool) else self.has_consumer_scaling[:],
			solar_power                   = self.solar_power                  ,
			wind_power                    = self.wind_power                   ,
			bioenergy_power               = self.bioenergy_power              ,
			battery_capacity              = self.battery_capacity             ,
			piloted_bioenergy_power       = self.piloted_bioenergy_power      ,
			flexibility_ratio             = self.flexibility_ratio if isinstance(self.flexibility_ratio, float) else self.flexibility_ratio[:],
			consumer_power                = self.consumer_power    if isinstance(self.consumer_power   , float) else self.consumer_power   [:],
			consumer_contrib              = self.consumer_contrib[:]          ,
			solar_curve                   = self.solar_curve    .get_clone()  ,
			wind_curve                    = self.wind_curve     .get_clone()  ,
			bioenergy_curve               = self.bioenergy_curve.get_clone()  ,
			consumer_curves               = self.consumer_curves if isinstance(self.consumer_curves, PowerData) else self.consumer_curves[:]
		)

	def get_wind_curve(self) -> PowerData:
		if (not self.has_wind):
			raise Exception("no wind curve in this config")
		if (self.has_wind_scaling):
			return self.wind_curve.get_scaled(self.wind_power)
		return self.wind_curve.get_copy()

	def get_solar_curve(self) -> PowerData:
		if (not self.has_solar):
			raise Exception("no solar curve in this config")
		if (self.has_solar_scaling):
			return self.solar_curve.get_scaled(self.solar_power)
		return self.solar_curve.get_copy()

	def get_constant_bioenergy_curve(self) -> PowerData:
		if (not self.has_bioenergy):
			raise Exception("no non-piloted bioenergy curve in this config")
		if (self.has_bioenergy_scaling):
			return self.bioenergy_curve.get_scaled(self.bioenergy_power)
		return self.bioenergy_curve.get_copy()
	
	def get_consumers_agglomerated_curves(self) -> PowerData:
		#usefull when there is no flexibility
		toReturn : PowerData = None
		for i in range(len(self.consumer_curves)):
			curve = self.consumer_curves[i].get_copy()
			if toReturn is not None:
				#this may be slow, a has_same_dates will later be added to powerdata
				intersec = curve.get_intersect(toReturn)
				curve = curve.get_slice(intersec)
				toReturn = toReturn.get_slice(toReturn)
			if (self.has_consumer_scaling[i]):
				curve = curve.get_scaled(self.consumer_power[i])
			curve *= self.consumer_contrib[i]
			if toReturn is None:
				toReturn = curve
			else:
				toReturn += curve
		return toReturn
	def get_consumers_curve_index(self, index : int = 0) -> PowerData:
		if index >= len(self.consumer_curves) or index < 0:
			raise Exception("index out of range")
		curve = self.consumer_curves[index].get_copy()
		if self.has_consumer_scaling[index] is True:
			curve = curve.get_scaled(self.consumer_power[index])
		curve *= self.consumer_contrib[index]
	def check_and_convert_params(self):
		if self.has_solar and self.solar_curve == None:
			raise Exception("solar production curve needed but not initialized")
		if self.has_wind and self.wind_curve == None:
			raise Exception("wind turbine production curve needed but not initialized")
		if self.has_bioenergy and self.bioenergy_curve == None:
			raise Exception("non pilotable bioenergy curve needed but not initialized")
		if self.consumer_curves is None:
			raise Exception("consumer curves are mandatory")

		if isinstance(self.consumer_curves, PowerData):
			self.consumer_curves = [self.consumer_curves]
		if isinstance(self.has_consumer_scaling, bool):
			self.has_consumer_scaling = [self.has_consumer_scaling] * len(self.consumer_curves)
		if isinstance(self.consumer_power, float):
			self.consumer_power = [self.consumer_power] * len(self.consumer_curves)
		if self.has_flexibility is True and isinstance(self.flexibility_ratio, float):
			self.flexibility_ratio = [self.flexibility_ratio] * len(self.consumer_curves)
		if self.consumer_contrib is None:
			self.consumer_contrib = [1.0/len(self.consumer_curves)] * len(self.consumer_curves)
		
		if len(self.consumer_curves) != len(self.has_consumer_scaling):
			raise Exception("consumer curves and their scaling MUST be the same length")
		if len(self.consumer_curves) != len(self.consumer_power):
			raise Exception("consumer curves and their power MUST be the same length")
		if len(self.consumer_curves) != len(self.consumer_contrib):
			raise Exception("consumer curves and their contributions MUST be the same length")
		if self.has_flexibility is True and len(self.consumer_curves) != len(self.flexibility_ratio):
			raise Exception("consumer curves and their flexibility ratio MUST be the same length")
		#gets all the curves to the sames date places
		curves_to_intersect = self.consumer_curves[:]
		if (self.has_solar):
			curves_to_intersect.append(self.solar_curve)
		if (self.has_bioenergy):
			curves_to_intersect.append(self.bioenergy_curve)
		if (self.has_wind):
			curves_to_intersect.append(self.wind_curve)
		intersect = curves_to_intersect[0].get_multiple_intersect(curves_to_intersect)
		for i in range(len(self.consumer_curves)):
			self.consumer_curves[i] = self.consumer_curves[i].get_slice(intersect)
		if (self.has_solar):
			self.solar_curve = self.solar_curve.get_slice(intersect)
		if (self.has_bioenergy):
			self.bioenergy_curve = self.bioenergy_curve.get_slice(intersect)
		if (self.has_wind):
			self.wind_curve = self.wind_curve.get_slice(intersect)
@dataclass(init=True)
class SimResults():
	total_consumption           : PowerData
	production_before_batteries : PowerData
	total_production            : PowerData
	imported_power              : PowerData
	exported_power              : PowerData
	battery                     : Battery
def simulate_senario(params: SimParams) -> SimResults:
	total_consumption : PowerData = None #batteries are in reciever convention but are considered a "producer"
	if not params.has_flexibility:
		battery : Battery = None
		total_consumption = params.get_consumers_agglomerated_curves()
		production : PowerData = None
		if params.has_wind:
			production = params.get_wind_curve() + production
		if params.has_solar:
			production = params.get_solar_curve() + production
		if params.has_bioenergy:
			production = params.get_constant_bioenergy_curve() + production
		production_before_batteries = production
		diff_before_batteries = (production - total_consumption)
		if params.has_battery:
			battery = Battery(params.battery_capacity)
			battery.from_power_data(diff_before_batteries)
			production = production - battery
		exported_power = (production - total_consumption).get_bigger_than(0.0)
		imported_power = (total_consumption - production).get_bigger_than(0.0)
		return SimResults(\
				total_consumption = total_consumption,\
				production_before_batteries = production_before_batteries,\
				total_production=production,\
				exported_power=exported_power,\
				imported_power=imported_power,\
				battery=battery
			)