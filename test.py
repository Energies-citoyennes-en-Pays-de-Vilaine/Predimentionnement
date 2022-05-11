from dataLoader import *
from datetime import *
import numpy as np
import matplotlib.pyplot as plt
import configuration as conf

dl = dataloader()
print("loading user data")
user = dl.load_one_user("../data/foyer/breton/averageUser0.csv")
print("loading prod data")
prod = dl.load_prod("../data/Prod Eol Elfe.csv")
print("loading solar prod data")
solarProd = dl.load_solar_panel_prod("../data/production_bretagne/Solaire.csv")
print("loading bioenergy prod data")
bioenergy_prod = dl.load_solar_panel_prod("../data/production_bretagne/Bioenergie.csv")
print("getting intersection")
intersec = user.get_intersect(prod)
print("getting prod slice")
prod = prod.get_slice(intersec)
print("getting user slice")
user = user.get_slice(intersec) * float(conf.NB_PARTICULIERS)
print("prod set to scale")
prod_scaled = prod * 1000.0  * float(conf.NB_PARTICULIERS * (conf.NB_EOLIENNE)/ (conf.CA_REDON_POPULATION + conf.CA_PONTCHATEAU_POPULATION))
print("setting solar prod to scale and adding it to prod")
solarProd = solarProd.get_scaled([conf.SOLAR_SCALING_FACTOR]*2, [
	Period("01/01/2020:00", "01/01/2021:00"),
	Period("01/01/2021:00", "01/01/2022:00")
	])
if (conf.ADD_SOLAR):
	prod_scaled += solarProd.get_slice(intersec)
bioenergy_prod = bioenergy_prod.get_scaled([conf.BIOENERGY_SCALING_FACTOR]*2, [
	Period("01/01/2020:00", "01/01/2021:00"),
	Period("01/01/2021:00", "01/01/2022:00")
	])
if (conf.ADD_BIOENERGY):
	prod_scaled += bioenergy_prod.get_slice(intersec)

print("calculating rolling average")
prod_avg = prod_scaled.get_rolling_average(24)
user_avg = user.get_rolling_average(24)
energy_import = (user - prod_scaled).get_bigger_than(0).get_rolling_average(24)
energy_export = (prod_scaled - user).get_bigger_than(0).get_rolling_average(24)
print(user.get_average(datetime.strptime("01/01/2020", "%d/%m/%Y"), datetime.strptime("01/01/2021", "%d/%m/%Y")), "Watts/200homes over the course of year 2020")
print(user.get_average(datetime.strptime("01/01/2021", "%d/%m/%Y"), datetime.strptime("01/01/2022", "%d/%m/%Y")), "Watts/200homes over the course of year 2021")
print("plotting")
fig1 = plt.figure("pourcentage de besoin couverts")
coverage_cumulated_average = (prod_scaled/user * 100.0).get_cumulated_average()
plt.plot(user.dates, (prod_scaled/user * 100.0).get_rolling_average(24).power)
plt.plot(user.dates, coverage_cumulated_average.power)
print(f"cumulated average production, {coverage_cumulated_average.power[-1]}")
fig2 = plt.figure("import and export, over a year")
subplot = plt.subplot(2, 1, 1)
e_i = energy_import.get_slice_over_period(end=datetime.strptime("01/01/2021", "%d/%m/%Y"))
e_e = energy_export.get_slice_over_period(end=datetime.strptime("01/01/2021", "%d/%m/%Y")) 
subplot.plot(e_i.dates, e_i.power)
subplot.plot(e_e.dates, e_e.power)
subplot = plt.subplot(2, 1, 2)
e_i = energy_import.get_slice_over_period(beginning=datetime.strptime("01/01/2021", "%d/%m/%Y"))
e_e = energy_export.get_slice_over_period(beginning=datetime.strptime("01/01/2021", "%d/%m/%Y")) 
subplot.plot(e_i.dates, e_i.power)
subplot.plot(e_e.dates, e_e.power)
plt.show()

