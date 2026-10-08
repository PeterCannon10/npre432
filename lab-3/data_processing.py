import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FIG_DIR = 'figures'
COLORS = ["#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#7B2CBF", "#264653", "#8377f3"]
LAB2_DATA_DIR = 'lab_2_data'

def csv_to_array(csv_filename, skip_rows, directory=LAB2_DATA_DIR):
    return pd.read_csv(os.path.join(directory, csv_filename), skiprows=skip_rows).to_numpy()

def percent_cold_work(t_o, t_f):
    """
    calculates cold work
    t_o: original thickness
    t_f: final thickness
    """
    return 100*((t_o-t_f)/t_o)

def linear_fit(x,y):
    """
    makes a linear fit and returns m, b, and R^2
    """
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

def plot_hardness_vs_cold_work(thickness_an1, thickness_an2, original_hardness_an, avg_rolled_hardness_an, thickness_cr1, thickness_cr2, original_hardness_cr, avg_rolled_hardness_cr):
    # (label, marker, color, regions, thickness_1, thickness_2, original_hardness, avg_rolled_hardness)
    series = [
        ("5.0 mm, Annealed",  "^", "#1f4e79", slice(0, 4), thickness_an1, thickness_an2, original_hardness_an, avg_rolled_hardness_an),
        ("2.5 mm, Annealed",  "D", "#ed7d31", slice(4, 8), thickness_an1, thickness_an2, original_hardness_an, avg_rolled_hardness_an),
        ("5.0 mm, As Rolled", "o", "#2e7d32", slice(0, 4), thickness_cr1, thickness_cr2, original_hardness_cr, avg_rolled_hardness_cr),
        ("2.5 mm, As Rolled", "s", "#00a2e0", slice(4, 8), thickness_cr1, thickness_cr2, original_hardness_cr, avg_rolled_hardness_cr),
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    for label, marker, color, r, t1, t2, h0, h in series:
        cw = np.concatenate([[0], percent_cold_work(t1[r], t2[r])])
        hardness = np.concatenate([[h0[r].mean()], h[r]])
        ax.scatter(cw, hardness, marker=marker, color=color, linestyle="-", label=label)

    ax.set_xlabel("Cold Work (%)")
    ax.set_ylabel("Hardness")
    ax.set_xlim(-0.5, 80)
    ax.set_ylim(0, 100)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
    fig.tight_layout()
    plt.grid()
    plt.savefig(os.path.join(FIG_DIR, 'cold_work_vs_hardness.png'))
    plt.close()

def main():
    """
    Annealing variable definitions
    Annealed at 350C
    """
    #Regions: [I, II, III, IV, V, VI, VII, VIII]
    original_hardness_an = np.array([36.7, 36.1, 35.3, 34.4, 34.1, 35.2, 33.9, 34.6]) #original hardness on edge
    rolled_hardness_an1 = np.array([64.3, 67.3, 69.4, 64.2, 69.3, 69.8, 70.7, 74.3]) #rolled hardness on mark for I-VIII
    rolled_hardness_an2 = np.array([64.4, 68.3, 71.2, 63.2, 67.2, 68.9, 70.7, 71.8]) 
    rolled_hardness_an3 = np.array([65.5, 68, 75, 63, 61.1, 67.8, 70.6, 72.5])
    avg_rolled_hardness_an = (rolled_hardness_an1+rolled_hardness_an2+rolled_hardness_an3)/3

    thickness_an1 = np.array([5.8, 6.53, 7.41, 8.45, 5.79, 6.43, 7.46, 8.46]) #initial thicknesses
    thickness_an2 = np.array([4.72, 4.75, 4.85, 4.91, 2.34, 2.55, 2.5, 2.69]) #final thicknesses

    mk3_width_an = np.array([18.98, 19.46]) #initial, final -- 5mm thickness
    mk7_width_an = np.array([18.99, 20.25]) #initial, final -- 2.5mm thickness

    """
    Cold Roll variable definitions
    as rolled
    """
    #Regions: [I, II, III, IV, V, VI, VII, VIII]
    original_hardness_cr = np.array([41.7, 42.9, 42.8, 42.5, 41.9, 43.1, 42.4, 41.7]) #original hardness on edge
    rolled_hardness_cr1 = np.array([71.2, 76.8, 82.7, 82.8, 88.2, 90, 90.9, 91]) #rolled hardness on mark I-VIII
    rolled_hardness_cr2 = np.array([71.5, 76.6, 83.4, 84.6, 88.5, 86.5, 90.6, 90.8])
    rolled_hardness_cr3 = np.array([71.3, 76.9, 83.6, 84.8, 88.1, 90.7, 91.2, 90])
    avg_rolled_hardness_cr = (rolled_hardness_cr1+rolled_hardness_cr2+rolled_hardness_cr3)/3

    thickness_cr1 = np.array([5.63, 6.25, 7.09, 8.32, 5.69, 6.52, 7.4, 8.47]) #initial thickness per mark
    thickness_cr2 = np.array([5.02, 5.03, 5.09, 5.11, 1.54, 2.66, 2.45, 3.23]) #final thickness per mark

    mk3_width_cr = np.array([18.95, 19.63]) #initial, final -- 5mm thickness
    mk7_width_cr = np.array([19.08, 20.81]) #initial, final -- 2.5mm thickness

    """
    Deliverable 1
    """
    plot_hardness_vs_cold_work(thickness_an1, thickness_an2, original_hardness_an, avg_rolled_hardness_an, thickness_cr1, thickness_cr2, original_hardness_cr, avg_rolled_hardness_cr)

    """
    Deliverable 2
    """
    initial_gage_diamater_br = 7.08 #mm
    grip_diameter_br = 12.58 #mm
    converted_hardness_br = 54.7085 #HRB
    final_gage_diameter_br = 4.88 #mm
    uniform_gage_diameter_br = 6.03 #mm
    area_gage_br = np.pi * (initial_gage_diamater_br/2)**2
    original_yield_strengths_br = np.array([131, 162, 236]) #MPa
    cold_works_br = np.array([0, 27.54, 58.408])

    plt.figure()
    plt.scatter(cold_works_br, original_yield_strengths_br, color=COLORS[0], label="Yield Strength at %CW data")
    m_br, b_br, r_squared_br = linear_fit(cold_works_br, original_yield_strengths_br)
    cold_work_space_br = np.linspace(cold_works_br[0], cold_works_br[-1], 100)
    plt.plot(cold_work_space_br, m_br*cold_work_space_br+b_br, color=COLORS[0], ls="--", label=f"Linear fit $\sigma_y$ = {m_br:.3f}$CW$ + {b_br:.3f}, $R^2$={r_squared_br:.4f}")
    plt.grid()
    plt.legend()
    plt.ylabel("Yield Strength (MPa)")
    plt.xlabel("Cold Work (%)")
    plt.savefig(os.path.join(FIG_DIR, 'cold_work_vs_yield_strength.png'))
    plt.close()

    #predict increase in yield strength
    yield_strength_mk4 = m_br * cold_works_br[-1] + 124.486
    percent_increase_ys = (yield_strength_mk4-original_yield_strengths_br[0])/original_yield_strengths_br[0] * 100
    print(yield_strength_mk4, original_yield_strengths_br[0])
    print(f"Deliverable 2: yield strength increased by {percent_increase_ys:.3f}%")

    """
    Deliverable 3
    """
    annealing_temp_350_lab = np.array([350, 350, 350, 350])
    annealing_temp_350 = np.array([350, 350, 350, 350])
    annealing_temp_400 = np.array([400, 400, 400, 400])
    annealing_temp_450 = np.array([450, 450, 450, 450])
    annealing_temp_500 = np.array([500, 500, 500, 500])

    #5.0-II, 5.0-IV, 2.5-II, and 2.5-IV
    hardnesses_350_lab = np.array([avg_rolled_hardness_an[1], avg_rolled_hardness_an[3], avg_rolled_hardness_an[5], avg_rolled_hardness_an[7]])
    hardnesses_350_past = np.array([66, 65, 65, 67])
    hardnesses_400_past = np.array([64, 62, 64, 67])
    hardnesses_450_past = np.array([44, 53, 58, 60])
    hardnesses_500_past = np.array([36, 45, 50, 52])

    def plot_hardness_vs_anneal_temp():
        labels  = ["5.0-II", "5.0-IV", "2.5-II", "2.5-IV"]
        markers = ["^", "o", "D", "s"]

        x_blocks = [annealing_temp_350, annealing_temp_400,
                    annealing_temp_450, annealing_temp_500]
        y_blocks = [hardnesses_350_past, hardnesses_400_past,
                    hardnesses_450_past, hardnesses_500_past]

        fig, ax = plt.subplots(figsize=(8, 5))

        for i, (label, marker) in enumerate(zip(labels, markers)):
            x = [xb[i] for xb in x_blocks]
            y = [yb[i] for yb in y_blocks]
            line, = ax.plot(x, y, marker=marker, label=label)

            # This lab's 350 C point, same color, no connecting line
            ax.plot(annealing_temp_350_lab[i], hardnesses_350_lab[i],
                    marker=marker, linestyle="none", color=line.get_color(),
                    markerfacecolor="none", markersize=9)

        ax.set_xlabel("Annealing Temperature (°C)")
        ax.set_ylabel("Hardness (HRB)")
        ax.set_xticks([350, 400, 450, 500])
        ax.grid(alpha=0.3)
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
        fig.tight_layout()
        return fig, ax

    plot_hardness_vs_anneal_temp()
    plt.savefig(os.path.join(FIG_DIR, 'anneal_temp_vs_hardness.png'))
    plt.close()

    '''
    Is there a crticial temperature for annealing to have a substantial effect on hardness?
    Yes, there is a significant drop between 400 and 450 C, so it is reasonable to assume that the critical temperature is between 400 and 450 C where recrystallization may occur.

    Compute critical homogenous temperature (ratio between this temperature and the melting temperature of the brass)
    Source: melting temp of brass = ~935 C https://www.enzemfg.com/melting-point-of-brass/

    ratio = 450/935
    '''

    #Testing
    print(percent_cold_work(thickness_an1, thickness_an2))
    print(avg_rolled_hardness_an)




    return None

if __name__ == "__main__":
    main()