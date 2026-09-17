import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = './raw_data'
IMAGES_DIR = './images'
COLORS = ["#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#7B2CBF", "#264653"]

def csv_to_array(csv_filename, skip_rows):
    return pd.read_csv(os.path.join(DATA_DIR, csv_filename), skiprows=skip_rows).to_numpy()

def plot_stress_strain_curve(time, displacement, force, composite_strain, material_name):
    plt.figure(figsize=(10, 6))
    plt.plot(composite_strain, force, color=COLORS[0], label='Stress-Strain Curve')
    plt.title(f'Stress-Strain Curve for {material_name}')
    plt.xlabel('Composite Strain')
    plt.ylabel('Force (N) currently -- SHOULD BE STRESS (MPa)')
    plt.grid()
    plt.legend()
    plt.savefig(os.path.join(IMAGES_DIR, f'{material_name}_stress_strain_curve.png'))
    plt.close()


def main():
    file_names = []
    dataset = []
    for csv in os.listdir(DATA_DIR):
        if csv.endswith('.csv'):
            file_names.append(csv)
            # Determine the number of rows to skip based on the file name
            if csv == 'N02DBR_1.csv':
                skip_rows = 31
            else:
                skip_rows = 29
            data_array = csv_to_array(csv, skip_rows)


    

if __name__ == "__main__":
    main()