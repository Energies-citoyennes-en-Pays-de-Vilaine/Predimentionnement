from sim import *
from dataLoader import *
from configuration import config
from sys import argv, getsizeof
PARAMS = {
	"wind_min"               : 1, #average wind prod in MW
	"wind_max"               : 10,
	"wind_nb_points"         : 10,
	"sun_min"                : 1, #average solar prod in MW
	"sun_max"                : 10,
	"sun_nb_points"          : 10,
	"bio_min"                : 1, #average bioenergy prod in MW (Methanol)
	"bio_max"                : 10,
	"bio_nb_points"          : 10,
	"flex_min"               : 0.01, #flexibility in %
	"flex_max"               : 0.1,
	"flex_nb_points"         : 10,
	"battery_min"            : 1, #battery capacity in MWh
	"battery_max"            : 10,
	"battery_nb_points"      : 10,
	"scaling_factor_for_pop" : 1e6 / (config.CA_REDON_POPULATION + config.CA_PONTCHATEAU_POPULATION)
	
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

	
print("size", get_total_size(sim_params))
current_sim_count = 0
with open(out_file_path, "w" ) as out_file:
	print("wind turbines(W/house)", "solar pannels(W/house)", "bioenergy(W/house)", "battery(Wh/house)", "flexibility (raw ratio)", sep=";", file=out_file, end="")
	print("","import_avg(W/house)", "export_avg(W/house)", "autosufficiency(%)", sep=";", file=out_file)
	for wind in range(PARAMS["wind_nb_points"]):
		for sun in range(PARAMS["sun_nb_points"]):
			for bio in range(PARAMS["bio_nb_points"]):
				for battery in range(PARAMS["battery_nb_points"]):
					for flex in range(PARAMS["flex_nb_points"]):
						print("simulation", current_sim_count, "out of", total_sim_count)
						wind_to_sim    = PARAMS["wind_min"] + (PARAMS["wind_max"] - PARAMS["wind_min"]) * wind
						bio_to_sim     = PARAMS["bio_min"] + (PARAMS["bio_max"] - PARAMS["bio_min"]) * bio
						sun_to_sim     = PARAMS["sun_min"] + (PARAMS["sun_max"] - PARAMS["sun_min"]) * sun
						battery_to_sim = PARAMS["battery_min"] + (PARAMS["battery_max"] - PARAMS["battery_min"]) * battery
						flex_to_sim    = PARAMS["flex_min"] + (PARAMS["flex_max"] - PARAMS["flex_min"]) * flex
						sim_params.wind_power        = wind_to_sim    * PARAMS["scaling_factor_for_pop"]
						sim_params.bioenergy_power   = bio_to_sim     * PARAMS["scaling_factor_for_pop"]
						sim_params.solar_power       = sun_to_sim     * PARAMS["scaling_factor_for_pop"]
						sim_params.battery_capacity  = battery_to_sim * PARAMS["scaling_factor_for_pop"]
						sim_params.flexibility_ratio = flex_to_sim    * PARAMS["scaling_factor_for_pop"]
						sim_params.check_and_convert_params()
						results = simulate_senario(sim_params)
						print(wind, sun, bio, battery, flex, sep=";", file=out_file, end="")
						print("",results.imported_power.get_average(), results.exported_power.get_average(), (results.total_production / results.total_consumption).get_average(), sep=";", file=out_file, flush=True)
						current_sim_count += 1