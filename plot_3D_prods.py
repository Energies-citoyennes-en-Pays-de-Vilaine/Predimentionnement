from dataLoader import *
from datetime import *
import numpy as np
import matplotlib.pyplot as plt
import configuration as conf

dl = dataloader()
SIZE_SIM = 30
SOLAR_PROD_STEP = 0.75#power in MW
WIND_PROD_STEP  = 0.75#power in MW

print("loading user data")
user = dl.load_one_user("../data/foyer/breton/averageUser0.csv")
print("loading wind prod data")
windProd = dl.load_prod("../data/Prod Eol Elfe.csv")
print("loading solar prod data")
solarProd = dl.load_solar_panel_prod("../data/production_bretagne/Solaire.csv")
print("loading bioenergy prod data")
bioenergy_prod = dl.load_solar_panel_prod("../data/production_bretagne/Bioenergie.csv")
print("getting intersection")
intersec = user.get_intersect(windProd)
print("getting prod slice")
windProd  = windProd.get_slice(intersec)
solarProd = solarProd.get_slice(intersec)
print("getting user slice")
user = user.get_slice(intersec)
print("prod set to scale")
windProd = windProd.get_scaled([1.0, 1.0],[
	Period("01/01/2020:00", "01/01/2021:00"),
	Period("01/01/2021:00", "01/01/2022:00")
	])
print("setting solar prod to scale and adding it to prod")
solarProd = solarProd.get_scaled([1.0, 1.0], [
	Period("01/01/2020:00", "01/01/2021:00"),
	Period("01/01/2021:00", "01/01/2022:00")
	])
bioenergy_prod = bioenergy_prod.get_scaled([conf.BIOENERGY_TOTAL_PROD * conf.NB_PARTICULIERS * conf.PRODUCTION_SCALING_FACTOR]*2, [
	Period("01/01/2020:00", "01/01/2021:00"),
	Period("01/01/2021:00", "01/01/2022:00")
	])

toSimSolarProd       = []
toSimWindProd        = []
averageCoveredNeeds  = []
energyImportAverage  = []
energyExportAverage  = []
energyImportRatio    = []

for x in range(SIZE_SIM):
	solar_prod_factor = x * SOLAR_PROD_STEP * 1e6 / (conf.CA_PONTCHATEAU_POPULATION + conf.CA_REDON_POPULATION)
	print(x)
	toSimSolarProd.append([])
	toSimWindProd.append([])
	averageCoveredNeeds.append([])
	energyImportAverage.append([])
	energyExportAverage.append([])
	energyImportRatio.append([])
	for y in range(SIZE_SIM):
		wind_prod_factor = y * WIND_PROD_STEP * 1e6 / (conf.CA_PONTCHATEAU_POPULATION + conf.CA_REDON_POPULATION)
		toSimSolarProd[-1].append(x * SOLAR_PROD_STEP )
		toSimWindProd [-1].append(y * WIND_PROD_STEP)
		sim_solar_prod = solarProd * solar_prod_factor
		sim_wind_prod  = windProd  * wind_prod_factor
		sim_prod       = sim_wind_prod + sim_solar_prod
		sim_cover_need = sim_prod / user
		sim_energy_import_avg = (user - sim_prod).get_bigger_than(0.0).get_average()
		sim_energy_export_avg = (sim_prod - user).get_bigger_than(0.0).get_average()
		energyImportAverage[-1].append(sim_energy_import_avg)
		energyExportAverage[-1].append(sim_energy_export_avg)
		energyImportRatio[-1].append(sim_energy_import_avg/(user.get_average()))
		averageCoveredNeeds[-1].append(sim_cover_need.get_average()) 
plt.figure("average need cover")
ax = plt.axes(projection="3d")
ax.set_xlabel("wind prod (MW)")
ax.set_ylabel("solar prod (MW)")
ax.plot_surface(np.array(toSimWindProd), np.array(toSimSolarProd), np.array(averageCoveredNeeds), rstride=1, cstride=1, cmap='viridis', edgecolor='none')
plt.figure("average energy import")
ax = plt.axes(projection="3d")
ax.set_xlabel("wind prod (MW)")
ax.set_ylabel("solar prod (MW)")
ax.plot_surface(np.array(toSimWindProd), np.array(toSimSolarProd), np.array(energyImportAverage), rstride=1, cstride=1, cmap='viridis', edgecolor='none')
plt.figure("average energy export")
ax = plt.axes(projection="3d")
ax.set_xlabel("wind prod (MW)")
ax.set_ylabel("solar prod (MW)")
ax.plot_surface(np.array(toSimWindProd), np.array(toSimSolarProd), np.array(energyExportAverage), rstride=1, cstride=1, cmap='viridis', edgecolor='none')
plt.figure("average energy import ratio")
ax = plt.axes(projection="3d")
ax.set_xlabel("wind prod (MW)")
ax.set_ylabel("solar prod (MW)")
ax.plot_surface(np.array(toSimWindProd), np.array(toSimSolarProd), np.array(energyImportRatio), rstride=1, cstride=1, cmap='viridis', edgecolor='none')

plt.show()