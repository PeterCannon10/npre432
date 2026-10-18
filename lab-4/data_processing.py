import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

DATA_DIR = "raw_data"
FIG_DIR = "figures"
COLORS = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#56B4E9', '#D55E00']

def plot_cooling_curves():
    for file in os.listdir(DATA_DIR):
        if file[-11:] == "Summ_d.xlsx":
            continue #"N01-Summ_d.xlsx" corresponds to transition points, not cooling curves
        else:
            name = file.replace("_d.xlsx", "")
            label = name

        file_path = os.path.join(DATA_DIR, file)
        df = pd.read_excel(file_path)
        temp0, temp1, time = df.to_numpy().T

        if label[-5] == "1":
            label = label[-5:]
        else:
            label = label[-4:]

        plt.figure()
        plt.plot(time, temp0, label=f"{label[:-2]}% Bi", color=COLORS[0])
        plt.xlabel("Time (s)")
        plt.ylabel("Temperature (°C)")
        plt.grid()
        plt.legend()
        plt.savefig(os.path.join(FIG_DIR, f"{label}.png"))
        plt.close()

def plot_single_cooling_curve():
    plt.figure()
    for file in os.listdir(DATA_DIR):
        if file[-11:] == "Summ_d.xlsx":
            continue #Summ_d.xlsx" corresponds to transition points, not cooling curves
        else:
            name = file.replace("_d.xlsx", "")
            label = name

        file_path = os.path.join(DATA_DIR, file)
        df = pd.read_excel(file_path)
        temp0, temp1, time = df.to_numpy().T

        if label[-5] == "1":
            label = label[-5:]
        else:
            label = label[-4:]

        plt.plot(time, temp0, label=f"{label[:-2]}% Bi")

    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.grid()
    plt.legend()
    plt.savefig(os.path.join(FIG_DIR, "all_cooling_curves.png"))
    plt.close()

#plot_cooling_curves()
#plot_single_cooling_curve()
