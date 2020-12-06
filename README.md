# Graf-za-praktikum
Za ponavljajoče risanje grafov in fitanje.

## Kako uporabljati?
Dodaj `mygraphlib.py` v isto mapo kot `.py` file. Ali pa dodaj v Python path. Lahko v novo mapo s praznim `__init__.py` file-om.

## Primer uporabe
Za uporabo primera je treba dodati v isto mapo `SDS00003.txt`.
```Python
import math as m
import os

import matplotlib.pyplot as plt
import numpy as np
import uncertainties as u
from scipy.odr import ODR, Data, Model, RealData

from mygraphlib import MyGraph as mgp


# Fit
def func(beta, x):
    Ub, U0, tau, t0 = beta[0], beta[1], beta[2], beta[3]
    return Ub + U0 * np.exp( (t0 - x) / tau ) * np.where(x < t0, 0, 1)

def narisi_layout():
    # Figure
    #mgp.use_fancy_latex()  # porabi več časa
    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize = (6, 4))
    
    # Podatki
    relative_path = "SDS00003.txt"
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, relative_path)
    t, U = np.loadtxt(abs_file_path, skiprows=0, unpack=True)

    # Graf
    a = mgp(ax1, t, U, xlabel='$t \, \mathrm{[s]}$', ylabel='$U \, \mathrm{[V]}$', title='Obremenitev 502 g')
    a.graph_data()

    # Fit
    output1 = a.graph_fit(func, [-0.01, 0.6, 8, -0.001])

    # Model
    a.graph_model(func, [0, 0.655, 7.77, 0])

    # Dodaj text box box na graf
    output1.beta = np.round(output1.beta, 3)
    output1.sd_beta = np.round(output1.sd_beta, 3)

    a.add_text_box([
        ('$U_b = ({} \pm {}) \, V$'.format(output1.beta[0], output1.sd_beta[0])),
        ('$U_0 = ({} \pm {}) \, V$'.format(output1.beta[1], output1.sd_beta[1])),
        (r'$\tau = ({} \pm {}) \, s^{{-1}}$'.format(output1.beta[2], output1.sd_beta[2])),
        ('$t_0 = ({} \pm {}) \, s$'.format(output1.beta[3], output1.sd_beta[3]))
    ])

    plt.tight_layout()
    #mgp.save_figure('obr_502g')
    plt.show()

    tau = u.ufloat(output1.beta[2], output1.sd_beta[2])
    R = u.ufloat(5e9, 0.1e9)
    C = tau / R
    print(C)

narisi_layout()
```
