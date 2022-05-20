from dataclasses import dataclass
NB_EOLIENNE = 13
CA_REDON_POPULATION = 29_521
CA_PONTCHATEAU_POPULATION = 14_399
NB_PARTICULIERS = 200
SOLAR_TOTAL_PROD = (28000+2169) # production in Redon and Pontchateau over the course of the 2020 year
PRODUCTION_SCALING_FACTOR = 1e6  / (365*24) / (CA_PONTCHATEAU_POPULATION + CA_REDON_POPULATION)
ADD_SOLAR = True
BIOENERGY_TOTAL_PROD = (18160) # production in Redon and Pontchateau over the course of the 2020 year
ADD_BIOENERGY = True

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
config = ConfigObject(
	NB_EOLIENNE               =  NB_EOLIENNE               ,
	CA_REDON_POPULATION       =  CA_REDON_POPULATION       ,
	CA_PONTCHATEAU_POPULATION =  CA_PONTCHATEAU_POPULATION ,
	NB_PARTICULIERS           =  NB_PARTICULIERS           ,
	SOLAR_TOTAL_PROD          =  SOLAR_TOTAL_PROD          ,
	PRODUCTION_SCALING_FACTOR =  PRODUCTION_SCALING_FACTOR ,
	ADD_SOLAR                 =  ADD_SOLAR                 ,
	BIOENERGY_TOTAL_PROD      =  BIOENERGY_TOTAL_PROD      ,
	ADD_BIOENERGY             =  ADD_BIOENERGY             
)