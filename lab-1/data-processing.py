import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = 'raw_data'
IMAGES_DIR = 'images'
DATA_FILENAMES = ['N02D1018CR_1.csv', 'N02D1045NM_1.csv', 'N02D7075_1.csv', 'N02DPMMA_1.csv']
HARDNESS_DATA = 'N-02-hard_d.txt'
SKIP_ROWS = 30 #changes on a per-file basis, this is the rows to skip for stress testing. Look at raw data to inform skiprows.

def csv_to_array(csv_filename):
    return pd.read_csv(os.path.join(DATA_DIR, csv_filename), skiprows=SKIP_ROWS).to_numpy()

def create_material_dataset():
    arrays = np.array([csv_to_array(file) for file in DATA_FILENAMES], dtype=object)
    return arrays

def create_hardness_dataset():
    df = pd.read_csv(os.path.join(DATA_DIR, HARDNESS_DATA), skiprows=1, delimiter='\t')
    return df.to_numpy()

def separate_material_columns(arrays):
    time, displacement, force, composite_strain = arrays.T
    return time, displacement, force, composite_strain

def separate_hardness_columns(df):
    al_bhn, stl_bhn, al_hrb, stl_hrb, al_hrc, stl_hrc = df.T
    return al_bhn, stl_bhn, al_hrb, stl_hrb, al_hrc, stl_hrc

def calculate_hardness_statistics():
    """
    Deliverable 1: Calculate the mean, median, and standard deviation for each hardness measurement (BHN, HRB, HRC) for both Aluminum 7075 and Steel 1018. Return a dictionary containing these statistics.

    0s were removed from the data because they indicated that students did not take a measurement.
    """
    hardness_data = create_hardness_dataset()
    al_bhn, stl_bhn, al_hrb, stl_hrb, al_hrc, stl_hrc = separate_hardness_columns(hardness_data)
    
    hardness_stats = {
        'Aluminum 7075': {
            'BHN': {'mean': np.mean(al_bhn[al_bhn != 0]), 'median': np.median(al_bhn[al_bhn != 0]), 'std': np.std(al_bhn[al_bhn != 0])},
            'HRB': {'mean': np.mean(al_hrb[al_hrb != 0]), 'median': np.median(al_hrb[al_hrb != 0]), 'std': np.std(al_hrb[al_hrb != 0])},
            'HRC': {'mean': np.mean(al_hrc[al_hrc != 0]), 'median': np.median(al_hrc[al_hrc != 0]), 'std': np.std(al_hrc[al_hrc != 0])}
        },
        'Steel 1018': {
            'BHN': {'mean': np.mean(stl_bhn[stl_bhn != 0]), 'median': np.median(stl_bhn[stl_bhn != 0]), 'std': np.std(stl_bhn[stl_bhn != 0])},
            'HRB': {'mean': np.mean(stl_hrb[stl_hrb != 0]), 'median': np.median(stl_hrb[stl_hrb != 0]), 'std': np.std(stl_hrb[stl_hrb != 0])},
            'HRC': {'mean': np.mean(stl_hrc[stl_hrc != 0]), 'median': np.median(stl_hrc[stl_hrc != 0]), 'std': np.std(stl_hrc[stl_hrc != 0])}
        }
    }
    
    return hardness_stats

def print_hardness_statistics(hardness_stats):
    print("=" * 50)
    print("HARDNESS STATISTICS")
    print("=" * 50)
    
    for material, measurements in hardness_stats.items():
        print(f"\n{material}")
        print("-" * len(material))
        for scale, stats in measurements.items():
            print(f"  {scale:<5} | Mean: {stats['mean']:>7.2f}  "
                  f"Median: {stats['median']:>7.2f}  "
                  f"Std: {stats['std']:>7.2f}")
    print("\n" + "=" * 50)

def deliverable_2():
    """
    Deliverable 2: using conversion charts
    cant really code this in but I wanted to put dev 2 in the codebase
    too lazy to convert now, here is the data to be compared with:

    Aluminum 7075
    -------------
    BHN   | Mean:  150.14  Median:  150.00  Std:    2.95
    HRB   | Mean:   82.79  Median:   82.70  Std:    0.58
    HRC   | Mean:   -0.01  Median:    0.40  Std:    0.85

    Steel 1018
    ----------
    BHN   | Mean:  729.10  Median:  718.00  Std:   28.15
    HRB   | Mean:  121.44  Median:  121.40  Std:    0.82
    HRC   | Mean:   61.27  Median:   61.00  Std:    1.39


    """


    return None

def plot_stress_strain_curves():
    """
    Deliverable 3: Generate stress-strain curves for each material (Steel 1018, Steel 1045, Aluminum 7075, PMMA)
    """
    arrays = create_material_dataset()
    material_names = ['Steel 1018', 'Steel 1045', 'Aluminum 7075', 'PMMA']
    diameters = [12.675, 12.76, 12.72, 19.03] #fetched from raw data by hand, averaged before and after for metals in mm
    colors = ['#CC321B', '#135925', '#2935CF', '#E028D7']
    cross_sectional_areas = [np.pi * (d/2)**2 for d in diameters] #in mm^2

    plt.figure()
    plt.xlabel("Composite strain")
    plt.ylabel("Stress (MPa)")
    for i in range(len(material_names)):
        time, displacement, force, composite_strain = separate_material_columns(arrays[i])
        stress = force / cross_sectional_areas[i] * 1000 #in MPa
        plt.plot(composite_strain, stress, label=material_names[i], color=colors[i])
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(IMAGES_DIR, 'stress_strain_curves.png'))
    plt.xlim(0, 0.06)
    plt.legend(loc='right')
    plt.savefig(os.path.join(IMAGES_DIR, 'stress_strain_curves_zoomed.png'))
    plt.close()

def calculate_material_properties():
    """
    Deliverable 4: Compute & tabulate elastic modulus, engineering 0.2% offset yield strength, and ultimate strength.
    """
    arrays = create_material_dataset()
    material_names = ['Steel 1018', 'Steel 1045', 'Aluminum 7075', 'PMMA']
    diameters = [12.675, 12.76, 12.72, 19.03]
    cross_sectional_areas = [np.pi * (d/2)**2 for d in diameters] #in mm^2
    for i in range(len(material_names)):
        time, displacement, force, composite_strain = separate_material_columns(arrays[i])
        stress = force / cross_sectional_areas[i] * 1000#in MPa
        elastic_modulus = stress/composite_strain
        yield_strength = stress[np.where(composite_strain >= 0.002)[0][0]] #engineering 0.2% offset yield strength
        ultimate_strength = np.max(stress)
        print(f"{material_names[i]}: Elastic Modulus = {np.mean(elastic_modulus):.2f} MPa, Yield Strength = {yield_strength:.2f} MPa, Ultimate Strength = {ultimate_strength:.2f} MPa")

    return None


def main():
    print_hardness_statistics(calculate_hardness_statistics())
    plot_stress_strain_curves()
    calculate_material_properties()

if __name__ == "__main__":
    main()