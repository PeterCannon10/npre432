import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FIG_DIR = 'figures'
COLORS = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#56B4E9', '#D55E00', "#7B2CBF"]
DATA_DIR = 'raw_mtil_data'

def csv_to_array(csv_filename, skip_rows=29, directory=DATA_DIR):
    return pd.read_csv(os.path.join(directory, csv_filename), skiprows=skip_rows).to_numpy().T

def obtain_extra_data(csv_filename, directory=DATA_DIR):
    df = pd.read_csv(os.path.join(directory, csv_filename), header=None, names=range(4))
    
    gage_diameter_initial, grip_diameter, rockwell_hardness, rockwell_scale, gage_diameter_final = df.iloc[[14, 15, 16, 17, 19], 2]
    return float(gage_diameter_initial), float(grip_diameter), float(rockwell_hardness), str(rockwell_scale), float(gage_diameter_final)

def fix_strain(strain, csv_filename):
    """
    Fixes strain for select files where errors were made
    STILL NEEDS A LOT OF WORK!!!
    """
    strain = np.array(strain)
    if csv_filename == "N01C4340Temper550C_1.csv":
        shift_idx = np.argwhere(strain < 0)[0][0]
        shift_value = strain[shift_idx] - strain[shift_idx-1]
        adjusted_strain = np.zeros_like(strain)
        for i in range(len(strain)):
            if i < shift_idx:
                adjusted_strain[i] = strain[i]
            else:
                adjusted_strain[i] = strain[i] - shift_value
        return adjusted_strain
    elif csv_filename == "N01D4340Anneal_1.csv":
        return strain
    elif csv_filename == "N2B4340Normal_1.csv":
        return strain
    return strain

def plot_stress_strain(data_dir=DATA_DIR):
    """
    Deliverable 1
    """
    i=0
    plt.figure()
    for file in os.listdir(DATA_DIR):
        time, displacement, force, strain = csv_to_array(file)
        strain = fix_strain(strain, file)
        gage_diameter_initial, grip_diameter, rockwell_hardness, rockwell_scale, gage_diameter_final = obtain_extra_data(file)
        gage_area = np.pi * (gage_diameter_initial / 2) ** 2
        stress = force/gage_area * 1000

        #annealed, normalized, water quenched, oil quenched, two quenched-and-tempered specimens
        match file:
            case "M01A4340Anneal_1.csv":
                label="Annealed"
                continue
            case "M01A4340OilQ_1.csv":
                label="Oil-Quenched"
                continue
            case "M01B4340Temper550C_1.csv":
                label="Tempered 550C"
                continue
            case "N01A4340Temper400C_1.csv":
                label="Tempered 400C"
                continue
            case "N01C4340Normal_1.csv":
                label="Normalized"
                continue
            case "N01C4340Temper550C_1.csv":
                label="Tempered 550C"
            case "N01C4340WaterQ_1.csv":
                label="Water-Quenched"
                continue
            case "N01D4340Anneal_1.csv":
                label="Annealed"
            case "N01D4340OilQ_1.csv":
                label="Oil-Quenched"
            case "N01D4340Temper400C_1.csv":
                label="Tempered 400C"
            case "N02B4340WaterQ_1.csv":
                label="Water-Quenched"
            case "N2B4340Normal_1.csv":
                label="Normalized"

        plt.plot(strain, stress, label=label, color=COLORS[i])
        i+=1
    plt.grid()
    plt.legend()
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.savefig(os.path.join(FIG_DIR, 'dev1.png'))
    plt.close()

def plot_indp_stress_strain(data_dir=DATA_DIR):
    """
    Plot independent stress strains
    """
    i=0
    for file in os.listdir(DATA_DIR):
        plt.figure()
        time, displacement, force, strain = csv_to_array(file)
        strain = fix_strain(strain, file)
        gage_diameter_initial, grip_diameter, rockwell_hardness, rockwell_scale, gage_diameter_final = obtain_extra_data(file)
        gage_area = np.pi * (gage_diameter_initial / 2) ** 2
        stress = force/gage_area * 1000

        #annealed, normalized, water quenched, oil quenched, two quenched-and-tempered specimens
        match file:
            case "M01A4340Anneal_1.csv":
                label="Annealed"
                continue
            case "M01A4340OilQ_1.csv":
                label="Oil-Quenched"
                continue
            case "M01B4340Temper550C_1.csv":
                label="Tempered 550C"
                continue
            case "N01A4340Temper400C_1.csv":
                label="Tempered 400C"
                continue
            case "N01C4340Normal_1.csv":
                label="Normalized"
                continue
            case "N01C4340Temper550C_1.csv":
                label="Tempered 550C"
            case "N01C4340WaterQ_1.csv":
                label="Water-Quenched"
                continue
            case "N01D4340Anneal_1.csv":
                label="Annealed"
            case "N01D4340OilQ_1.csv":
                label="Oil-Quenched"
            case "N01D4340Temper400C_1.csv":
                label="Tempered 400C"
            case "N02B4340WaterQ_1.csv":
                label="Water-Quenched"
            case "N2B4340Normal_1.csv":
                label="Normalized"

        print(file)
        print("Strain:")
        print(strain)
        print()
        print()
        print(strain, stress)
        plt.plot(strain, stress, label=label, color=COLORS[i])
        plt.grid()
        plt.legend()
        plt.xlabel("Strain (mm/mm)")
        plt.ylabel("Stress (MPa)")
        plt.savefig(os.path.join(FIG_DIR, f"indp_{file[:-4]}"))
        plt.close()
        i+=1












def main():
    plot_stress_strain()
    plot_indp_stress_strain()

main()