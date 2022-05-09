from dataLoader import *
from datetime import *
import numpy as np
import matplotlib.pyplot as plt

dl = dataloader()
print("loading user data")
user = dl.load_one_user("../data/foyer/breton/averageUser0.csv")
print("loading prod data")
prod = dl.load_prod("../data/Prod Eol Elfe.csv")
prod *= 1000.0
print("getting intersection")
intersec = user.get_intersect(prod)
print("getting prod slice")
prod = prod.get_slice(intersec)
print("getting user slice")
user = user.get_slice(intersec)
print("plotting")
plt.plot(prod.dates, prod.power)

plt.plot(user.dates, (user.power * 200))
plt.show()
