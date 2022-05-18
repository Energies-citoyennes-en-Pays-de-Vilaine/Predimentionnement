from calc import *


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
	has_battery_scaling           : bool
	has_flexibility_scaling       : bool
	has_piloted_bioenergy_scaling : bool

	#defaults to 0
	solar_power             : float
	wind_power              : float
	bioenergy_power         : float
	battery_capacity        : float
	piloted_bioenergy_power : float
	flexibility_ratio       : float	

	#defaults to None
	solar_curve             : PowerData
	wind_curve              : PowerData
	bioenergy_curve         : PowerData

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
		has_battery_scaling           : bool = True,\
		has_flexibility_scaling       : bool = True,\
		has_piloted_bioenergy_scaling : bool = True,\
		solar_power                   : float = 0.0,\
		wind_power                    : float = 0.0,\
		bioenergy_power               : float = 0.0,\
		battery_capacity              : float = 0.0,\
		piloted_bioenergy_power       : float = 0.0,\
		flexibility_ratio             : float = 0.0,\
		solar_curve                   : PowerData = None,\
		wind_curve                    : PowerData = None,\
		bioenergy_curve               : PowerData = None,\
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
		self.has_battery_scaling           : bool = has_battery_scaling
		self.has_flexibility_scaling       : bool = has_flexibility_scaling
		self.has_piloted_bioenergy_scaling : bool = has_piloted_bioenergy_scaling

		self.solar_power             : float = solar_power
		self.wind_power              : float = wind_power
		self.bioenergy_power         : float = bioenergy_power
		self.battery_capacity        : float = battery_capacity
		self.piloted_bioenergy_power : float = piloted_bioenergy_power
		self.flexibility_ratio       : float = flexibility_ratio	

		self.solar_curve             : PowerData = solar_curve 
		self.wind_curve              : PowerData = wind_curve 
		self.bioenergy_curve         : PowerData = bioenergy_curve
		#adds checks as an insurance
		if has_solar and solar_curve == None:
			raise Exception("solar production curve needed but not initialized")
		if has_wind and wind_curve == None:
			raise Exception("wind turbine production curve needed but not initialized")
		if has_bioenergy and bioenergy_curve == None:
			raise Exception("non pilotable bioenergy curve needed but not initialized")

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
		if (self.has_battery_scaling):
			return self.bioenergy_curve.get_scaled(self.bioenergy_power)
		return self.bioenergy_curve.get_copy()

def simulate_senario():
	pass