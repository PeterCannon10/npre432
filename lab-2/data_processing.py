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
    elastic_modulus = stress/strain
    yield_strength = stress[np.where(strain >= 0.002)[0][0]]
    ultimate_strength = np.max(stress)
    elongation_percent = 100 * (abs(final_gage_diameter-initial_gage_diameter)/initial_gage_diameter)
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
        stress = force/area * 1000 #MPa
        
        material_label = material[4:-6]
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
        find_properties(stress, strain, initial_gage_diameters[j], final_gage_diameters[j])
    
    """
    Deliverable 3
    """
    for j in range(len(file_names)-2):
        time, displacement, force, strain = dataset[j]
        force = np.array(force)
        strain = np.array(strain)
        area = np.pi * (initial_gage_diameters[j]/2)**2
        stress = force/area * 1000
        hardness = rockwell_hardness[j]
        
        elastic_modulus, yield_strength, ultimate_strength, elongation_percent, resilience_modulus = find_properties(stress, strain, initial_gage_diameters[j], final_gage_diameters[j])

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        ax1.plot(hardness, elastic_modulus, color=COLORS[0])
        ax1.set_xlabel('Rockwell Hardness B-scale (HRB)')
        ax1.set_ylabel('Elastic Modulus (MPa)')
        ax1.grid()

        ax2.plot(hardness, yield_strength, color=COLORS[1], label="Yield Strength")
        ultimate_strengths = np.full(len(rockwell_hardness), ultimate_strength)
        ax2.plot(hardness, ultimate_strengths, color = COLORS[2], label="Ultimate Strength")
        ax2.set_xlabel('Rockwell Hardness B-scale (HRB)')
        ax2.set_ylabel('Strength (MPa)')
        ax2.legend()
        ax2.grid()

        ax3.plot(hardness, elongation_percent, color=COLORS[3])
        ax3.set_xlabel('Rockwell Hardness B-scale (HRB)')
        ax3.set_ylabel('Elongation (%)')
        ax3.grid()

        ax4.plot(hardness, resilience_modulus, color=COLORS[4])
        ax4.set_xlabel('Rockwell Hardness B-scale (HRB)')
        ax4.set_ylabel('Modulus of Resilience (MPa)')
        ax4.grid()

        match j:
            case 0:
                material_name='304SS'
            case 1:
                material_name='1018CR'
            case 2:
                material_name='1045NM'
            case 3:
                material_name='2024'

        plt.tight_layout()
        plt.savefig(os.path.join(IMAGES_DIR, f'{material_name}_dev3.png'))
        plt.close()



            



    

if __name__ == "__main__":
    main()