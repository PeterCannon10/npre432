import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = 'raw_data'
IMAGES_DIR = 'images'
COLORS = ["#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#7B2CBF", "#264653"]

def csv_to_array(csv_filename, skip_rows):
    return pd.read_csv(os.path.join(DATA_DIR, csv_filename), skiprows=skip_rows).to_numpy()

def main():
    dataset = []
    file_names = []
    for csv in os.listdir(DATA_DIR):
        if csv.endswith('.csv'):
            file_names.append(csv)
            # Determine the number of rows to skip based on the file name
            if csv == 'N02DBR_1.csv':
                skip_rows = 31
            else:
                skip_rows = 29
        data_array = csv_to_array(csv, skip_rows).T
        dataset.append(data_array)

    """
    Deliverable 1
    """
    i = 0
    plt.figure()
    for material in file_names:
        time, displacement, force, strain = dataset[i]
        area = 1 #TEMP FIX THIS
        
        material_label = material[4:-6]
        print(material_label)
        if material_label == "PMMA":
            plt.savefig(os.path.join(IMAGES_DIR, 'stress_strain_curves.png'))
            plt.close()

            plt.figure()
            plt.plot(strain, force/area, color=COLORS[-1])
            plt.xlabel("Strain")
            plt.ylabel("Stress (N) currently -- SHOULD BE STRESS (MPa)")
            plt.grid()
            plt.savefig(os.path.join(IMAGES_DIR, 'pmma_stress_strain_plot.png'))
            plt.close()
        if material_label == "1018": #change label to 304SS
            material_label = "304SS"
            
        plt.plot(strain, force/area, color=COLORS[i], label=material_label)
        plt.xlabel("Strain")
        plt.ylabel("Stress (N) currently -- SHOULD BE STRESS (MPa)")
        plt.grid()
        plt.legend()
        i+=1

    
    



    

if __name__ == "__main__":
    main()