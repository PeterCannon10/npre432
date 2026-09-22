import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = 'raw_data'
IMAGES_DIR = 'images'
COLORS = ["#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#7B2CBF", "#264653"]

def csv_to_array(csv_filename, skip_rows):
    return pd.read_csv(os.path.join(DATA_DIR, csv_filename), skiprows=skip_rows).to_numpy()

def find_properties(stress, strain, initial_gage_diameter, final_gage_diameter, idx):
    match idx:
        case 0:
            #304SS
            low = 0.0
            high = 0.005
        case 1:
            #1018CR
            low = 0
            high = 0.025
        case 2:
            #1045NM
            low = 0
            high = 0.085
        case 3:
            #2024
            low = 0
            high = 0.01
        case 4:
            #BR
            low = 0.0
            high = 0.005
        case 5:
            #PMMA
            low = 0
            high = 0.045
        case 6:
            #1045CR
            low = 0
            high = 0.04
    elastic_modulus_idx = np.argwhere(strain > high)[0][0]
    elastic_modulus = (stress[elastic_modulus_idx]-stress[0])/(strain[elastic_modulus_idx]-strain[0])
    yield_strength = stress[elastic_modulus_idx]
    ultimate_strength = np.max(stress)
    elongation_percent = 100 * (abs(final_gage_diameter-initial_gage_diameter)/initial_gage_diameter)
    resilience_modulus = yield_strength**2/(2*elastic_modulus)
    return np.array([elastic_modulus, yield_strength, ultimate_strength, elongation_percent, resilience_modulus], dtype=object)

def correct_hardness():
    # [304SS, 1018CR, 1045NM, 2024, BR, PMMA, 1045CR]
    initial_gage_diameters = np.array([7.14, 7.14, 7, 7.15, 7.08, 7.99, 7.26])
    rockwell_hardness = np.array([99.8, 93.8, 92.2, 73.2, 67.1, 0, 103.9])

    observed_hardness = np.array([100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0])
    low_corrections  = np.array([3.5, 3.0, 5.0, 6.0, 7.0, 8.0, 9, 10, 11, 12, 12.5])  # 6.4 mm
    high_corrections = np.array([2.5, 3.0, 3.5, 4.0, 5.0, 5.5, 6.0, 6.5, 7.5, 8.0, 8.5])  # 10.0 mm

    LOW_DIA = 6.4
    HIGH_DIA = 10.0

    # np.interp requires the x-coordinates (xp) to be increasing.
    obs_asc      = observed_hardness[::-1]
    low_asc      = low_corrections[::-1]
    high_asc     = high_corrections[::-1]

    corrected_hardness = np.zeros_like(rockwell_hardness)

    for i in range(len(rockwell_hardness)):
        if i == 5:
            continue #No PMMA

        hardness = rockwell_hardness[i]
        diameter = initial_gage_diameters[i]

        low_corr_at_hardness = np.interp(hardness, obs_asc, low_asc)

        high_corr_at_hardness = np.interp(hardness, obs_asc, high_asc)

        diameter_correction = np.interp(diameter, [LOW_DIA, HIGH_DIA], [low_corr_at_hardness, high_corr_at_hardness])

        corrected_hardness[i] = hardness + diameter_correction

    #print(corrected_hardness) #Result: [103.08855556  96.91188889  95.27333333  78.49666667  73.01222222 0. 107.16111111]
    return corrected_hardness

def main():
    #[304SS, 1018CR, 1045NM, 2024, BR, PMMA, 1045CR]
    initial_gage_diameters = np.array([7.14, 7.14, 7, 7.15, 7.08, 7.99, 7.26]) #diameters in mm
    grip_diameters = np.array([12.68, 12.70, 12.58, 12.68, 12.58, 12.74, 12.78])
    rockwell_hardness = np.array([99.8, 93.8, 92.2, 73.2, 67.1, 0, 103.9]) #unconverted
    final_gage_diameters = np.array([3.57, 5.3, 5.52, 6.01, 6.03, 7.4, 5.62])
    rockwell_hardness = correct_hardness() #redefine for correction

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

    print(file_names)

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

        match i:
            case 0:
                #304SS
                low = 0.0
                high = 0.005
            case 1:
                #1018CR
                low = 0
                high = 0.025
            case 2:
                #1045NM
                low = 0
                high = 0.085
            case 3:
                #2024
                low = 0
                high = 0.01
            case 4:
                #BR
                low = 0.0
                high = 0.005
            case 5:
                #PMMA
                low = 0
                high = 0.045
            case 6:
                #1045CR
                low = 0
                high = 0.04
        
        material_label = material[4:-6]
        if material_label == "PMMA":
            continue
        if material_label == "1018": #change label to 304SS
            material_label = "304SS"

        #TEMP
        plt.axvline(low, color=COLORS[i])
        plt.axvline(high, color=COLORS[i])

        plt.plot(strain, stress, color=COLORS[i], label=material_label)
        i+=1
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.grid()
    plt.legend()
    plt.savefig(os.path.join(IMAGES_DIR, 'stress_strain_plots_final.png'))
    plt.close()

    #Plotting PMMA
    time, displacement, force, strain = dataset[-2]
    force = np.array(force)
    strain = np.array(strain)
    area = np.pi * (initial_gage_diameters[-2]/2)**2
    stress = force/area * 1000 #MPa
    plt.figure()
    plt.plot(strain, stress, color=COLORS[-2])

    #TEMP
    plt.axvline(low, color=COLORS[-2])
    plt.axvline(high, color=COLORS[-2])

    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.grid()
    plt.savefig(os.path.join(IMAGES_DIR, 'pmma_stress_strain_plot.png'))
    plt.close()

    """
    Deliverable 2
    """
    for j in range(len(file_names)):
        find_properties(stress, strain, initial_gage_diameters[j], final_gage_diameters[j], j)
    
    """
    Deliverable 3
    """
    hardnesses = []
    elastic_moduli = []
    yield_strengths = []
    elongation_percents = []
    resilience_moduli = []
    ultimate_strengths = []
    for j in range(len(file_names)):
        if j == 4 or j == 5:
            continue
        time, displacement, force, strain = dataset[j]
        force = np.array(force)
        strain = np.array(strain)
        area = np.pi * (initial_gage_diameters[j]/2)**2
        stress = force/area * 1000
        hardness = rockwell_hardness[j]
        
        elastic_modulus, yield_strength, ultimate_strength, elongation_percent, resilience_modulus = find_properties(stress, strain, initial_gage_diameters[j], final_gage_diameters[j], j)

        hardnesses.append(hardness)
        elastic_moduli.append(elastic_modulus)
        yield_strengths.append(yield_strength)
        elongation_percents.append(elongation_percent)
        resilience_moduli.append(resilience_modulus)
        ultimate_strengths.append(ultimate_strength)
        
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    ax1.scatter(hardnesses, elastic_moduli, color=COLORS[0])
    ax1.set_xlabel('Rockwell Hardness B-scale (HRB)')
    ax1.set_ylabel('Elastic Modulus (MPa)')
    ax1.grid()

    ax2.scatter(hardnesses, yield_strengths, color=COLORS[1], label="Yield Strength", marker='^')
    ax2.scatter(hardnesses, ultimate_strengths, color = COLORS[2], label="Ultimate Strength", s=5)
    ax2.set_xlabel('Rockwell Hardness B-scale (HRB)')
    ax2.set_ylabel('Strength (MPa)')
    ax2.legend(fontsize=7)
    print(hardnesses)
    print(yield_strengths)
    ax2.grid()

    ax3.scatter(hardnesses, elongation_percents, color=COLORS[3])
    ax3.set_xlabel('Rockwell Hardness B-scale (HRB)')
    ax3.set_ylabel('Elongation (%)')
    ax3.grid()

    ax4.scatter(hardnesses, resilience_moduli, color=COLORS[4])
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
        case 4:
            material_name='BR'
        case 5:
            material_name='PMMA'
        case 6:
            material_name='1045CR'

    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, f'{material_name}_dev3.png'))
    plt.close()

if __name__ == "__main__":
    main()