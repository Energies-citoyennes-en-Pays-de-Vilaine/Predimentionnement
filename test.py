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
print("getting intersection")
intersec = user.get_intersect(prod)
print("getting prod slice")
prod = prod.get_slice(intersec)
print("getting user slice")
user = user.get_slice(intersec) * float(200.0)
print("prod set to scale")
for nb_eol_add in range(30):
	prod_scaled = prod * 1000.0  * float(200.0 * (conf.NB_EOLIENNE + nb_eol_add)/ (conf.CA_REDON_POPULATION + conf.CA_PONTCHATEAU_POPULATION))
	print("calculating rolling average")
	prod_avg = prod_scaled.get_rolling_average(24)
	user_avg = user.get_rolling_average(24)
	energy_import = (user - prod_scaled).get_bigger_than(0).get_rolling_average(24)
	energy_export = (prod_scaled - user).get_bigger_than(0).get_rolling_average(24)
	print("plotting")
	fig1 = plt.figure(f"pourcentage de besoin couverts {nb_eol_add}")
	plt.plot(user.dates, (prod_scaled/user * 100.0).get_rolling_average(24).power)
	plt.plot(user.dates, (prod_scaled/user * 100.0).get_cumulated_average().power)
	plt.savefig(f"../results/pourcentage/{nb_eol_add}.png")
	fig2 = plt.figure(f"import and export {nb_eol_add}")
	plt.plot(energy_import.dates, energy_import.power)
	plt.plot(energy_export.dates, energy_export.power)
	plt.savefig(f"../results/importexport/{nb_eol_add}.png")

