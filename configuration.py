from dataclasses import dataclass
NB_EOLIENNE = 13
PROD_PER_WINDTURBINE = 0.577 #average prod per wind turbine in MW
CA_REDON_POPULATION = 34_725
CA_REDON_RES_CONSUMPTION = 194_884 * 1e6 / (365*24)#average consumption in W
CA_PONTCHATEAU_POPULATION = 16_226
CA_PONTCHATEAU_RES_CONSUMPTION = 98_603
NB_PARTICULIERS = 200
SOLAR_TOTAL_PROD = (28000+2169) # production in Redon and Pontchateau over the course of the 2020 year
PRODUCTION_SCALING_FACTOR = 1e6  / (365*24) / (CA_PONTCHATEAU_POPULATION + CA_REDON_POPULATION)
ADD_SOLAR = True
BIOENERGY_TOTAL_PROD = (18160) # production in Redon and Pontchateau over the course of the 2020 year
ADD_BIOENERGY = True
HAS_BATTERY   = False
BATTERY_CAPACITY = 0.0

@dataclass(init=True)
class ConfigObject():
	NB_EOLIENNE               : float
	CA_REDON_POPULATION       : int
	CA_PONTCHATEAU_POPULATION : int
	NB_PARTICULIERS           : int
	SOLAR_TOTAL_PROD          : int
	PRODUCTION_SCALING_FACTOR : float
	ADD_SOLAR                 : bool
	BIOENERGY_TOTAL_PROD      : int
	ADD_BIOENERGY             : bool
	PROD_PER_WINDTURBINE      : float
	HAS_BATTERY               : bool
	BATTERY_CAPACITY          : float
config = ConfigObject(
	NB_EOLIENNE               = NB_EOLIENNE               ,
	CA_REDON_POPULATION       = CA_REDON_POPULATION       ,
	CA_PONTCHATEAU_POPULATION = CA_PONTCHATEAU_POPULATION ,
	NB_PARTICULIERS           = NB_PARTICULIERS           ,
	SOLAR_TOTAL_PROD          = SOLAR_TOTAL_PROD          ,
	PRODUCTION_SCALING_FACTOR = PRODUCTION_SCALING_FACTOR ,
	ADD_SOLAR                 = ADD_SOLAR                 ,
	BIOENERGY_TOTAL_PROD      = BIOENERGY_TOTAL_PROD      ,
	ADD_BIOENERGY             = ADD_BIOENERGY             ,
	PROD_PER_WINDTURBINE      = PROD_PER_WINDTURBINE      ,
	HAS_BATTERY               = HAS_BATTERY               ,
	BATTERY_CAPACITY          = BATTERY_CAPACITY          ,
  
)