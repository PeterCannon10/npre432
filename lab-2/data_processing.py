import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = 'raw_data'
IMAGES_DIR = 'images'
COLORS = ["#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#7B2CBF", "#264653"]

def csv_to_array(csv_filename, skip_rows):
    return pd.read_csv(os.path.join(DATA_DIR, csv_filename), skiprows=skip_rows).to_numpy()

def find_properties(stress, strain, initial_gage_diameter, final_gage_diameter):
    print(stress.shape, strain.shape, initial_gage_diameter.shape, final_gage_diameter.shape)
    elastic_modulus = stress/strain
    yield_strength = stress[np.where(strain >= 0.002)[0][0]]
    ultimate_strength = np.max(stress)
    elongation_percent = 100 * ((final_gage_diameter-initial_gage_diameter)/initial_gage_diameter)
    resilience_modulus = yield_strength**2/(2*elastic_modulus)
    return np.array([elastic_modulus, yield_strength, ultimate_strength, elongation_percent, resilience_modulus], dtype=object)

def main():
    #[304SS, 1018CR, 1045NM, 2024, BR, PMMA]
    initial_gage_diameters = np.array([7.14, 7.14, 7, 7.15, 7.08, 7.99]) #diameters in mm
    grip_diameters = np.array([12.68, 12.70, 12.58, 12.68, 12.58, 12.74])
    rockwell_hardness = np.array([99.8, 93.8, 92.2, 73.2, 67.1, 0]) #unconverted
    final_gage_diameters = np.array([3.57, 5.3, 5.52, 6.01, 6.03, 7.4])

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
        force = np.array(force)
        strain = np.array(strain)
        area = np.pi * (initial_gage_diameters[i]/2)**2
        stress = force/area
        
        material_label = material[4:-6]
        print(material_label)
        if material_label == "PMMA":
            plt.savefig(os.path.join(IMAGES_DIR, 'stress_strain_curves.png'))
            plt.close()

            plt.figure()
            plt.plot(strain, stress, color=COLORS[-1])
            plt.xlabel("Strain")
            plt.ylabel("Stress (N) currently -- SHOULD BE STRESS (MPa)")
            plt.grid()
            plt.savefig(os.path.join(IMAGES_DIR, 'pmma_stress_strain_plot.png'))
            plt.close()
            break
        if material_label == "1018": #change label to 304SS
            material_label = "304SS"

        plt.plot(strain, stress, color=COLORS[i], label=material_label)
        plt.xlabel("Strain")
        plt.ylabel("Stress (N) currently -- SHOULD BE STRESS (MPa)")
        plt.grid()
        plt.legend()
        i+=1

    """
    Deliverable 2
    """
    for j in range(len(file_names)):
        print(find_properties(stress, strain, initial_gage_diameters[j], final_gage_diameters[j]))
    
    



    

if __name__ == "__main__":
    main()