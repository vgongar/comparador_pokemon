import numpy as np
import pandas as pd

stats = pd.read_csv("pokemon_home.csv")

escalar = np.load("escalar.npy")

vv = np.diag(escalar)

np.save("escalar_cuad_div.npy", escalar**2 / vv[:, None])