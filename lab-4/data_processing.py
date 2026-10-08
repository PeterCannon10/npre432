import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

DATA_DIR = "raw_data"
FIG_DIR = "figures"
COLORS = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#56B4E9', '#D55E00']

def plot_cooling_curves():
    for file in os.listdir(DATA_DIR):
        if file == "N01-Summ_d.xlsx":
            continue #"N01-Summ_d.xlsx" corresponds to transition points, not cooling curves
        elif file == "N01D05Bi_d.xlsx":
            name = "5Bi"
            label = "5% Bismuth"
        elif file == "N01D100Bi_d.xlsx":
            name = "100Bi"
            label = "100% Bismuth"

        file_path = os.path.join(DATA_DIR, file)
        df = pd.read_excel(file_path)
        temp0, temp1, time = df.to_numpy().T

        plt.figure()
        plt.title(label)
        plt.plot(time, temp0, label="Initial Temperature", color=COLORS[0])
        plt.plot(time, temp1, label="Final Temperature", color=COLORS[1])
        plt.xlabel("Time (s)")
        plt.ylabel("Temperature (°C)")
        plt.grid()
        plt.legend()
        plt.savefig(os.path.join(FIG_DIR, f"{name}.png"))
        plt.close()

plot_cooling_curves()
