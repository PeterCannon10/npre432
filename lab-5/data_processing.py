import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FIG_DIR = 'figures'
COLORS = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#56B4E9', '#D55E00', "#7B2CBF"]
DATA_DIR = 'raw_mtil_data'

def csv_to_array(csv_filename, skip_rows=29, directory=DATA_DIR):
    return pd.read_csv(os.path.join(directory, csv_filename), skiprows=skip_rows).to_numpy().T

def alternative_csv_to_array(csv_filename, skip_rows, directory=DATA_DIR):
    return pd.read_csv(os.path.join(directory, csv_filename), skiprows=skip_rows)














def main():
    for file in os.listdir(DATA_DIR):
        if file == 'M01A4340Anneal_1.csv':
            #print(csv_to_array(file))
            print(alternative_csv_to_array(file, 25))

main()