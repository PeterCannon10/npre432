import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = 'tension_data'
FIG_DIR = 'figures'
COLORS = ["#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#7B2CBF", "#264653", "#8377f3", "#0039f3"]

def csv_to_array(csv_filename, skip_rows, directory=DATA_DIR):
    return pd.read_csv(os.path.join(directory, csv_filename), skiprows=skip_rows).to_numpy()

def single_plot(x, y, x_label="Strain (mm/mm)", y_label="Stress (MPa)", title=None):
    plt.figure()
    plt.plot(x, y)
    plt.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if title:
        plt.title(title)
    plt.show()
    return None

def determine_skiprows(file_name):
    #order: ['N02C1045CR_1.csv', 'N02D304SS_1.csv', 'N02D1018CR_1.csv', 'N02D1045NM_1.csv', 'N02D2024_1.csv', 'N02DBR_1.csv', 'N02DPMMA_1.csv', 'N02C7075_1.csv']
    match file_name:
        case "1045CR":
            return 29
        case "304SS":
            return 29
        case "1018CR":
            return 29
        case "1045NM":
            return 29
        case "2024":
            return 29
        case "BR":
            return 31 #brass is an interesting test, come back to excel for more data
        case "PMMA":
            return 29
        case "7075":
            return 29
        case _:
            print("FILE_NAME ERROR")

def determine_elastic(file_name):
    match file_name:
            case "1045CR":
                return 0.005
            case "304SS":
                return 0.010
            case "1018CR":
                return 0.0034
            case "1045NM":
                return 0.0025
            case "2024":
                return 0.0050
            case "BR":
                return 0.003
            case "PMMA":
                return 0.022
            case "7075":
                return 0.0085
            case _:
                print("FILE_NAME ERROR")

def linear_fit(x,y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    x_mean, y_mean = x.mean(), y.mean()
    ss_xx = np.sum((x-x_mean)**2)

    slope = np.sum((x-x_mean)*(y-y_mean)) / ss_xx
    intercept = y_mean - slope * x_mean

    y_pred = slope * x + intercept
    ss_res = np.sum((y-y_pred)**2)
    ss_tot = np.sum((y-y_mean)**2)
    r_squared = 1.0 if ss_tot == 0 else 1.0 - ss_res/ss_tot

    return slope, intercept, r_squared

def fit_power_law(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.shape != y.shape:
        raise ValueError("x and y must have the same shape.")

    mask = (x > 0) & (y > 0)
    if mask.sum() < 2:
        raise ValueError("Need at least two points with x > 0 and y > 0.")
    x, y = x[mask], y[mask]

    ln_x = np.log(x)
    ln_y = np.log(y)

    n, ln_K = np.polyfit(ln_x, ln_y, 1)
    K = np.exp(ln_K)

    ln_y_pred = n * ln_x + ln_K
    ss_res = np.sum((ln_y - ln_y_pred) ** 2)
    ss_tot = np.sum((ln_y - np.mean(ln_y)) ** 2)
    r_squared = 1 - ss_res / ss_tot

    return K, n, r_squared

def find_properties(stress, strain, gage_diameter_i, gage_diameter_f, file_name):
    yield_strain = determine_elastic(file_name)
    yield_strain_idx = np.argwhere(strain > yield_strain)[0][0]
    elastic_stress = stress[:yield_strain_idx]
    elastic_strain = strain[:yield_strain_idx]
    elastic_modulus, b, r_squared = linear_fit(elastic_strain, elastic_stress)
    yield_strength = stress[yield_strain_idx]
    ultimate_strength = np.max(stress)
    elongation_percent = 100 * (abs(gage_diameter_f-gage_diameter_i)/gage_diameter_i)
    resilience_modulus = yield_strength**2/(2*elastic_modulus)
    return np.array([elastic_modulus, yield_strength, ultimate_strength, elongation_percent, resilience_modulus])

def correct_hardness():
    gage_diameters_i = np.array([7.26, 7.14, 7.14, 7, 7.15, 7.08, 7.99, 7.23]) #mm
    rockwell_hardness = np.array([103.9, 99.8, 93.8, 92.2, 73.2, 46.9, 0, 87.3]) #HRB

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
        if i == 6:
            corrected_hardness[i] = 0
            continue #No PMMA

        hardness = rockwell_hardness[i]
        diameter = gage_diameters_i[i]

        low_corr_at_hardness = np.interp(hardness, obs_asc, low_asc)

        high_corr_at_hardness = np.interp(hardness, obs_asc, high_asc)

        diameter_correction = np.interp(diameter, [LOW_DIA, HIGH_DIA], [low_corr_at_hardness, high_corr_at_hardness])

        corrected_hardness[i] = hardness + diameter_correction

    print(corrected_hardness) #Result: [103.08855556  96.91188889  95.27333333  78.49666667  73.01222222 0. 107.16111111]
    return corrected_hardness

def main():
    #unit_test()
    gage_diameters_i = np.array([7.26, 7.14, 7.14, 7, 7.15, 7.08, 7.99, 7.23]) #mm
    grip_diameters = np.array([12.78, 12.68, 12.7, 12.58, 12.68, 12.58, 12.74, 12.82]) #mm
    rockwell_hardness = np.array([103.9, 99.8, 93.8, 92.2, 73.2, 46.9, 0, 87.3]) #HRB
    gage_diameters_f = np.array([5.62, 3.57, 5.3, 5.52, 6.01, 4.88, 7.4, 5.94]) #mm
    corrected_hardness = correct_hardness()
    """
    Structuring Data
    """
    i=0
    file_names = []
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        file_names.append(file_name)

        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000
        #single_plot(strain, stress, file_name)
        #print(find_properties(stress, strain, gage_diameters_i[i], gage_diameters_f[i], file_name))

        i+=1

    print(file_names)
    """
    Deliverable 1
    """
    i=0
    plt.figure()
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        if file_name == "BR" or file_name == "PMMA":
            continue
        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000 #MPa
        plt.plot(strain, stress, color=COLORS[i], label=file_name)
        i+=1
    plt.grid()
    plt.legend()
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.savefig(os.path.join(FIG_DIR, 'stress_strain_plots.png'))
    plt.close()

    #PMMA
    i=0
    plt.figure()
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        if file_name != "PMMA":
            continue
        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000 #MPa
        plt.plot(strain, stress, color=COLORS[i], label=file_name)
        i+=1
    plt.grid()
    plt.legend()
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.savefig(os.path.join(FIG_DIR, 'pmma_plot.png'))
    plt.close()

    #BR - technically dev 6
    i=0
    plt.figure()
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        if file_name != "BR":
            continue
        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000 #MPa
        plt.plot(strain, stress, color=COLORS[i], label=file_name)
        print(strain, stress)
        i+=1
    plt.grid()
    plt.legend()
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.show()
    plt.savefig(os.path.join(FIG_DIR, 'br_plot.png'))
    plt.close()


    """
    Deliverable 2
    """
    i=0
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        if file_name == "BR" or file_name == "PMMA":
            continue
        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000 #MPa

        elastic_modulus, yield_strength, ultimate_strength, elongation_percent, resilience_modulus = find_properties(stress, strain, gage_diameters_i[i], gage_diameters_f[i], file_name)
        #uncomment for deliverable:
        #print(f"{file_name}\n-------------\nElastic Modulus: {elastic_modulus:.3f}\nYield strength: {yield_strength:.3f}\nUltimate strength: {ultimate_strength:.3f}\nElongation Percent: {elongation_percent:.3f}\nResilience Modulus: {resilience_modulus:.3f}\n")
        i+=1

    """
    Deliverable 3
    """
    hardnesses = []
    elastic_moduli = []
    yield_strengths = []
    elongation_percents = []
    resilience_moduli = []
    ultimate_strengths = []
    i=0
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        if file_name == "BR" or file_name == "PMMA":
            continue
        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000 #MPa

        elastic_modulus, yield_strength, ultimate_strength, elongation_percent, resilience_modulus = find_properties(stress, strain, gage_diameters_i[i], gage_diameters_f[i], file_name)
        hardness = corrected_hardness[i]

        hardnesses.append(hardness)
        elastic_moduli.append(elastic_modulus)
        yield_strengths.append(yield_strength)
        ultimate_strengths.append(ultimate_strength)
        elongation_percents.append(elongation_percent)
        resilience_moduli.append(resilience_modulus)

        i+=1

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

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'property_plots.png'))
    plt.close()

    """
    Deliverable 4
    """
    i=0
    plt.figure()
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        if file_name != "304SS":
            continue
        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000 #MPa
        plt.plot(strain, stress, color=COLORS[i], label="Engineering stress-strain")
        true_strain = np.log(1+strain)
        true_stress = stress * (1+strain)
        plt.plot(true_strain, true_stress, color=COLORS[-1], label="True stress-strain")
        i+=1
    plt.grid()
    plt.legend()
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.savefig(os.path.join(FIG_DIR, '304SS_plot.png'))
    plt.close()

    """
    Deliverable 5
    """
    i=0
    plt.figure()
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        if file_name != "304SS":
            continue
        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000 #MPa
        true_strain = np.log(1+strain)
        true_stress = stress * (1+strain)
        plt.plot(true_strain, true_stress, color=COLORS[-1], label="True stress-strain")
        K, n, r_squared = fit_power_law(true_strain, true_stress)
        true_strain_fit = K * (true_strain)**n
        fit_label = f"Power-law fit: K={K:.2f}, n={n:.2f}, $R^2$={r_squared:.4f}"
        plt.plot(true_strain, true_strain_fit, color=COLORS[1], label=fit_label)
        i+=1
    plt.grid()
    plt.legend()
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.savefig(os.path.join(FIG_DIR, '304SS_power_law_plot.png'))
    plt.close()


    """
    All combined
    """
    i=0
    plt.figure()
    for file in os.listdir(DATA_DIR):
        file_name = file[4:-6]
        skip_rows = determine_skiprows(file_name)
        property_data = csv_to_array(file, skip_rows).T
        time, displacement, force, strain = property_data
        area_gage = np.pi * (gage_diameters_i[i]/2)**2
        stress = force / area_gage * 1000 #MPa
        plt.plot(strain, stress, color=COLORS[i], label=file_name)
        i+=1
    plt.xlim(0, 0.7)
    plt.ylim(0, 1000)
    plt.grid()
    plt.legend(fontsize=10, loc="upper right")
    plt.xlabel("Strain (mm/mm)")
    plt.ylabel("Stress (MPa)")
    plt.savefig(os.path.join(FIG_DIR, 'combined_stress_strain_plots.png'))
    plt.close()

    print(file_names, correct_hardness())

    return None


if __name__ == "__main__":
    main()