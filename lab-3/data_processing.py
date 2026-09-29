import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FIG_DIR = 'figures'
COLORS = ["#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#7B2CBF", "#264653", "#8377f3"]

def percent_cold_reduction(t_o, t_f):
    """
    t_o: original thickness
    t_f: final thickness
    """
    return 100*((t_o-t_f)/t_o)

'''
def dev1(cold_work, hardness):

'''

def main():
    """
    Annealing variable definitions
    """
    #Regions: [I, II, III, IV, V, VI, VII, VIII]
    original_hardness_an = np.array([36.7, 36.1, 35.3, 34.4, 34.1, 35.2, 33.9, 34.6])
    rolled_hardness_an1 = np.array([64.3, 67.3, 69.4, 64.2, 69.3, 69.8, 70.7, 74.3])
    rolled_hardness_an2 = np.array([64.4, 68.3, 71.2, 63.2, 67.2, 68.9, 70.7, 71.8])
    rolled_hardness_an3 = np.array([65.5, 68, 75, 63, 61.1, 67.8, 70.6, 72.5])

    thickness_an1 = np.array([5.8, 6.53, 7.41, 8.45, 5.79, 6.43, 7.46, 8.46])
    thickness_an2 = np.array([4.72, 4.75, 4.85, 4.91, 2.34, 2.55, 2.5, 2.69])

    mk3_width_an = np.array([18.98, 19.46]) #initial, final -- 5mm thickness
    mk7_width_an = np.array([18.99, 20.25]) #initial, final -- 2.5mm thickness

    """
    Cold Roll variable definitions
    """
    #Regions: [I, II, III, IV, V, VI, VII, VIII]
    original_hardness_cr = np.array([41.7, 42.9, 42.8, 42.5, 41.9, 43.1, 42.4, 41.7])
    rolled_hardness_cr1 = np.array([71.2, 76.8, 82.7, 82.8, 88.2, 90, 90.9, 91])
    rolled_hardness_cr2 = np.array([71.5, 76.6, 83.4, 84.6, 88.5, 86.5, 90.6, 90.8])
    rolled_hardness_cr3 = np.array([71.3, 76.9, 83.6, 84.8, 88.1, 90.7, 91.2, 90])

    thickness_cr1 = np.array([5.63, 6.25, 7.09, 8.32, 5.69, 6.52, 7.4, 8.47])
    thickness_cr2 = np.array([5.02, 5.03, 5.09, 5.11, 1.54, 2.66, 2.45, 3.23])

    mk3_width_cr1 = np.array([18.95, 19.63]) #initial, final -- 5mm thickness
    mk7_width_cr2 = np.array([19.08, 20.81]) #initial, final -- 2.5mm thickness

    """
    Deliverable 1
    """
    cold_work_an = percent_cold_reduction(thickness_an2, thickness_an1)


    return None

if __name__ == "__main__":
    main()