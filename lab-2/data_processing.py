import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = 'raw_data'
DATA_DIR_LAB1 = 'raw_data_lab1'
IMAGES_DIR = 'images'
COLORS = ["#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#7B2CBF", "#264653"]

def csv_to_array(csv_filename, skip_rows, directory=DATA_DIR):
    return pd.read_csv(os.path.join(directory, csv_filename), skiprows=skip_rows).to_numpy()

def find_properties(stress, strain, initial_gage_diameter, final_gage_diameter, idx, is_lab1 = False):
    if is_lab1 == False:
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
    else:
        match idx:
            case 0:
                #1018CR
                low = 0.0
                high = 0.0025
            case 1:
                #1045NM
                low = 0
                high = 0.0015
            case 2:
                #7075
                low = 0
                high = 0.0075
    print(high)
    print(np.argwhere(strain > high))
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

def integrate_discrete(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculates the definite integral (area under the curve) for discrete 
    (x, y) data points using the Trapezoidal Rule.
    
    Parameters:
        x (np.ndarray): 1D array of x-coordinates.
        y (np.ndarray): 1D array of y-coordinates matching x.
        
    Returns:
        float: The total area under the curve.
    """
    x = np.asarray(x)
    y = np.asarray(y)
    
    if x.shape != y.shape:
        raise ValueError("x and y arrays must have the same shape.")
    if len(x) < 2:
        raise ValueError("At least 2 points are required to calculate an integral.")
        
    # Sort x and y by x-values if x is not strictly increasing
    if not np.all(np.diff(x) >= 0):
        sort_indices = np.argsort(x)
        x = x[sort_indices]
        y = y[sort_indices]

    # Calculate integral using standard numerical integration
    # Note: Use np.trapz(y, x=x) if running NumPy version < 2.0
    return float(np.trapezoid(y, x=x))


# --- Example Usage ---
if __name__ == "__main__":
    # Example: Integrate y = x^2 from x = 0 to 4
    x_data = np.linspace(0, 4, 100)
    y_data = x_data ** 2
    
    area = integrate_discrete(x_data, y_data)
    print(f"Calculated Area: {area:.4f}")  # Analytical answer is (4^3)/3 = 21.3333

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

    dataset_lab1 = []
    file_names_lab1 = []
    for csv in os.listdir(DATA_DIR_LAB1):
        if csv.endswith('csv'):
            file_names_lab1.append(csv)
            match csv:
                case "N02C7075_1.csv":
                    skip_rows = 29
                case "N02D1045NM_1.csv":
                    skip_rows = 30
                case "N02D1018CR_1.csv":
                    skip_rows = 30
        data_array_lab1 = csv_to_array(csv, skip_rows, DATA_DIR_LAB1).T
        dataset_lab1.append(data_array_lab1)

    """
    Deliverable 1
    """
    i = 0
    plt.figure()
    for material in file_names:
        if material == "N02DBR_1.csv":
            continue #comment out if you want brass in main graph
        time, displacement, force, strain = dataset[i]
        force = np.array(force)
        strain = np.array(strain)
        area = np.pi * (initial_gage_diameters[i]/2)**2
        stress = force/area * 1000 #MPa

        match i:
            case 0:
                #304SS
                low = 0.0
                high = 0.0075
            case 1:
                #1018CR
                low = 0
                high = 0.021
            case 2:
                #1045NM
                low = 0
                high = 0.0425
            case 3:
                #2024
                low = 0
                high = 0.01
            case 4:
                #BR
                low = 0.0
                high = 0.01
            case 5:
                #PMMA
                low = 0
                high = 0.045
            case 6:
                #1045CR
                low = 0
                high = 0.035
        
        material_label = material[4:-6]
        if material_label == "PMMA":
            continue
        if material_label == "1018": #change label to 304SS
            material_label = "304SS"

        #TEMP
        #plt.axvline(low, color=COLORS[i], ls="--")
        #plt.axvline(high, color=COLORS[i], ls="--")

        plt.plot(strain, stress, color=COLORS[i], label=material_label)
        i+=1
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.grid()
    '''uncomment for aluminum 7075 in main figure
    initial_gage_diameters_lab1 = [12.68, 12.54, 7.23]
    aluminum7075_data = dataset_lab1[-1]
    time, displacement, force, strain = aluminum7075_data
    stress = force / initial_gage_diameters_lab1[-1] * 1000
    plt.plot(strain, stress, color='#ad9c6c', label="7075")
    '''
    plt.legend()
    plt.plot()
    plt.savefig(os.path.join(IMAGES_DIR, 'stress_strain_plots_final.png'))
    plt.close()

    """
    Deliverable 1 for lab 1
    """
    hardnesses_lab1 = [97.5, 88.5, 87.3]
    initial_gage_diameters_lab1 = [12.68, 12.54, 7.23]
    final_gage_diameters_lab1 = [12.67, 12.98, 5.94]

    i = 0
    plt.figure()
    for material in file_names_lab1:
        if material == 'N02C7075_1.csv':
            continue
        time, displacement, force, strain = dataset_lab1[i]
        force = np.array(force)
        strain = np.array(strain)
        area = np.pi * (initial_gage_diameters_lab1[i]/2)**2
        stress = force/area * 1000 #MPa

        #['N02D1018CR_1.csv', 'N02D1045NM_1.csv', 'N02C7075_1.csv']
        match i:
            case 0:
                #1018CR
                low = 0.0
                high = 0.01
            case 1:
                #1045NM
                low = 0
                high = 0.0125
            case 2:
                #7075
                low = 0
                high = 0.025
        
        material_label = material[4:-6]

        #TEMP
        #plt.axvline(low, color=COLORS[i])
        #plt.axvline(high, color=COLORS[i])

        plt.plot(strain, stress, color=COLORS[i], label=material_label)
        i+=1
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.grid()
    plt.legend()
    plt.savefig(os.path.join(IMAGES_DIR, 'stress_strain_plots_lab1.png'))
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
    #plt.axvline(low, color=COLORS[-2])
    #plt.axvline(high, color=COLORS[-2])

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

    #['N02D1018CR_1.csv', 'N02D1045NM_1.csv', 'N02C7075_1.csv']
    hardnesses_lab1 = [97.5, 88.5, 87.3]
    initial_gage_diameters_lab1 = [12.68, 12.54, 7.23]
    final_gage_diameters_lab1 = [12.67, 12.98, 5.94]
    for k in range(len(file_names_lab1)):
        time, displacement, force, strain = dataset_lab1[k]
        force = np.array(force)
        strain = np.array(strain)
        area = np.pi * (initial_gage_diameters[k]/2)**2
        stress = force/area * 1000
        hardness = hardnesses_lab1[k]

        print(strain)
        
        elastic_modulus, yield_strength, ultimate_strength, elongation_percent, resilience_modulus = find_properties(stress, strain, initial_gage_diameters_lab1[k], final_gage_diameters_lab1[k], k, True)

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

    """
    Calculating Area for Mason
    """
    i = 0
    for material in file_names:
        time, displacement, force, strain = dataset[i]
        force = np.array(force)
        strain = np.array(strain)
        area = np.pi * (initial_gage_diameters[i]/2)**2
        stress = force/area * 1000 #MPa
        '''
        print(material + " integral:")
        print(integrate_discrete(strain, stress))
        print()
        '''
        i+=1

    i=0
    for material in file_names_lab1:
        time, displacement, force, strain = dataset_lab1[i]
        force = np.array(force)
        strain = np.array(strain)
        area = np.pi * (initial_gage_diameters_lab1[i]/2)**2
        stress = force/area * 1000 #MPa
        '''
        print(material + " integral:")
        print(integrate_discrete(strain, stress))
        print()
        '''
        i+=1


if __name__ == "__main__":
    main()