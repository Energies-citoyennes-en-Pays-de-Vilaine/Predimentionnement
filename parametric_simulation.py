from sim import *
from dataLoader import *
from configuration import config
from sys import argv, getsizeof
from time import time
from multiprocessing import Process, Manager
t0 = time()
PARAMS = {
	"wind_min"               : 5, #average wind prod in MW
	"wind_max"               : 30,
	"wind_nb_points"         : 5,
	"sun_min"                : 1, #average solar prod in MW
	"sun_max"                : 40,
	"sun_nb_points"          : 3,
	"bio_min"                : 1, #average bioenergy prod in MW (Methanol)
	"bio_max"                : 20,
	"bio_nb_points"          : 4,
	"flex_min"               : 0.0, #flexibility in %
	"flex_max"               : 0.1,
	"flex_nb_points"         : 4,
	"battery_min"            : 0, #battery capacity in MWh
	"battery_max"            : 10,
	"battery_nb_points"      : 4,
	"scaling_factor_for_pop" : 1e6 / (config.CA_REDON_POPULATION + config.CA_PONTCHATEAU_POPULATION),
	"thread_count"           : 1,
}
if (len(argv) < 2):
	print("you need to specify the result file location")
	exit()
out_file_path = argv[1]
dl = dataloader()

print("loading home consumptions data")
home_consumption = dl.load_one_user("../data/foyer/breton/averageUser0.csv")
print("loading wind prod data")
windProd = dl.load_prod("../data/Prod Eol Elfe.csv")
print("loading solar prod data")
solarProd = dl.load_solar_panel_prod("../data/production_bretagne/Solaire.csv")
print("loading bioenergy prod data")
bioenergy_prod = dl.load_solar_panel_prod("../data/production_bretagne/Bioenergie.csv")
print("getting intersection")
intersec = home_consumption.get_intersect(windProd)
print("getting prod slice")
windProd  = windProd.get_slice(intersec)
solarProd = solarProd.get_slice(intersec)
print("getting hom consumption slice")
home_consumption = home_consumption.get_slice(intersec)
print("prod set to scale")
print(windProd.get_average())
windProd = windProd.get_scaled(1.0)
print("setting solar prod to scale and adding it to prod")
solarProd = solarProd.get_scaled(1.0)
bioenergyProd = bioenergy_prod.get_scaled(1.0)
t1 = time()
print(f"loading data finished, took {t1 - t0}s")
sim_params = SimParams(
	has_solar                     = True,
	has_wind                      = True,
	has_bioenergy                 = True,
	has_piloted_bioenergy         = False,
	has_battery                   = True,
	has_flexibility               = True,
	has_solar_scaling             = True,
	has_wind_scaling              = True,
	has_bioenergy_scaling         = True,
	has_piloted_bioenergy_scaling = False,
	has_consumer_scaling          = False,
	solar_power                   = 0.0,
	wind_power                    = 0.0,
	bioenergy_power               = 0.0,
	battery_capacity              = 0.0,
	piloted_bioenergy_power       = 0.0,
	flexibility_ratio             = 0.0,
	consumer_power                = 0.0,
	consumer_contrib              = None,
	solar_curve                   = solarProd,
	wind_curve                    = windProd,
	bioenergy_curve               = bioenergy_prod,
	consumer_curves               = home_consumption,
	begin                         = None,
	end                           = None
)
total_sim_count = PARAMS["wind_nb_points"] * PARAMS["sun_nb_points"] * PARAMS["bio_nb_points"] * PARAMS["battery_nb_points"] * PARAMS["flex_nb_points"] 
size = 0
def get_total_size(obj):
	size = 0
	for v in vars(obj):
		var = vars(obj)[v]
		try:
			next_vars = vars(var)
			size += get_total_size(var)
		except TypeError:
			size += getsizeof(var)
	return size

manager = Manager()
thread_sims_to_do    = [[] for i in range(PARAMS["thread_count"])]
thread_sim_params    = [sim_params.get_clone() for i in range(PARAMS["thread_count"])]
thread_results       = manager.list()
running_thread_count = 0
print("size", get_total_size(sim_params))
current_sim_count = 0
print("generating data")
t1 = time()
for wind in range(PARAMS["wind_nb_points"]):
		for sun in range(PARAMS["sun_nb_points"]):
			for bio in range(PARAMS["bio_nb_points"]):
				for battery in range(PARAMS["battery_nb_points"]):
					for flex in range(PARAMS["flex_nb_points"]):
						#print("simulation", current_sim_count, "out of", total_sim_count)
						wind_to_sim    = (PARAMS["wind_min"]    + (PARAMS["wind_max"]    - PARAMS["wind_min"])    * wind    / PARAMS["wind_nb_points"])    * PARAMS["scaling_factor_for_pop"]
						bio_to_sim     = (PARAMS["bio_min"]     + (PARAMS["bio_max"]     - PARAMS["bio_min"])     * bio     / PARAMS["bio_nb_points"])     * PARAMS["scaling_factor_for_pop"]
						sun_to_sim     = (PARAMS["sun_min"]     + (PARAMS["sun_max"]     - PARAMS["sun_min"])     * sun     / PARAMS["sun_nb_points"])     * PARAMS["scaling_factor_for_pop"]
						battery_to_sim = (PARAMS["battery_min"] + (PARAMS["battery_max"] - PARAMS["battery_min"]) * battery / PARAMS["battery_nb_points"]) * PARAMS["scaling_factor_for_pop"]
						flex_to_sim    = (PARAMS["flex_min"]    + (PARAMS["flex_max"]    - PARAMS["flex_min"])    * flex    / PARAMS["flex_nb_points"]) 
						thread_sims_to_do[current_sim_count%PARAMS["thread_count"]].append({
							"wind_to_sim"    : wind_to_sim,
							"bio_to_sim"     : bio_to_sim, 
							"sun_to_sim"     : sun_to_sim,
							"battery_to_sim" : battery_to_sim,
							"flex_to_sim"    : flex_to_sim,
						})
						current_sim_count += 1
t2 = time()
print(f"finished, took {t2 - t1}s (elapsed {t2 - t0}s)")
def sim_process_function(i, params_to_sim, sim_param, sim_results):
	print("process", i, "has started")
	results = []
	sim_param : SimParams = thread_sim_params[i]
	for j in range(len(params_to_sim)):
		if (i == 0):
			print("thread 0 is simming", j+1, "out of", len(params_to_sim))
		param = params_to_sim[j]
		sim_param.solar_power = param["sun_to_sim"]
		sim_param.wind_power = param["wind_to_sim"]
		sim_param.bioenergy_power = param["bio_to_sim"]
		sim_param.battery_capacity = param["battery_to_sim"]
		sim_param.flexibility_ratio = param["flex_to_sim"]
		sim_param.check_and_convert_params()
		result = simulate_senario(sim_param)
		result = {**param,
			"storage_use"    : (result.battery.get_average() / result.battery.capacity if result.battery.capacity != 0 else 1),
			"imported_power" : result.imported_power.get_average(),
			"exported_power" : result.exported_power.get_average(),
			"autoconso"      : (result.total_production / result.total_consumption).get_average(),
			"imported_time"  : (result.imported_power.count_greater_than(0.0) / len(result.imported_power.power)),
			"exported_time"  : (result.exported_power.count_greater_than(0.0) / len(result.exported_power.power)),
			"low_conso_peak" : (result.total_consumption.get_percentile(5)),
			"high_conso_peak": (result.total_consumption.get_percentile(95)),
			"low_import_peak" : (result.imported_power.get_percentile(5)),
			"high_import_peak": (result.imported_power.get_percentile(95)),
		}
		results.append(result)
	if (i == 0):
			print("thread 0 has finished", j+1, "out of", len(params_to_sim))
	sim_results.append(results)

processes = []
print("starting all simulations")
t1 = time()
for i in range(PARAMS["thread_count"]):
	print("trying to start thread ", i)
	process = Process(target=sim_process_function, args=(i, thread_sims_to_do[i], thread_sim_params[i], thread_results))
	process.start()
	processes.append(process)

for i in range(len(processes)):
	processes[i].join()
	t2 = time()
	print("process", i, "finished, took",t2 - t1,"s")
print(f"all threads have finished, total time : {t2-t0} ({t2-t1}s in simulation)")
print(thread_results[0][0])
print(thread_results[0][1])
with open(out_file_path, "w" ) as out_file:
	print("wind turbines(W/house)", "solar pannels(W/house)", "bioenergy(W/house)", "battery(Wh/house)", "flexibility (raw ratio)", sep=";", file=out_file, end="")
	print("",
	"storage_use (ratio)",
	"imported_power (W/house)",#scaling will be done after the results, only for display
	"exported_power (W/house)",
	"autoconso (ratio)",
	"imported_time (ratio)",
	"exported_time (ratio)",
	"low_conso_peak (W/house)",
	"high_conso_peak (W/house)",
	"low_import_peak (W/house)",
	"high_import_peak (W/house)",
	sep=";",
	file=out_file)
	for results in thread_results:
		for result in results:
			print(result["wind_to_sim"],
			    result["sun_to_sim"],
				result["bio_to_sim"],
				result["battery_to_sim"],
				result["flex_to_sim"],
				result["storage_use"     ],
				result["imported_power"  ],
				result["exported_power"  ],
				result["autoconso"       ],
				result["imported_time"   ],
				result["exported_time"   ],
				result["low_conso_peak"  ],
				result["high_conso_peak" ],
				result["low_import_peak" ],
				result["high_import_peak"],
				sep=";",
				file=out_file)


