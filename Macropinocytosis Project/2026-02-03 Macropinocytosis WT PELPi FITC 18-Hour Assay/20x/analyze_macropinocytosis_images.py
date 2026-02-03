import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.stats import ttest_ind

## CONFIGURATION ##
green_threshold = 0
red_threshold = 0

# Doses (folders)
conditions = ["0 nM PELPi", "500 nM PELPi", "2000 nM PELPi"]

BASE_FOLDER = "Macropinocytosis Project/2026-02-03 Macropinocytosis WT PELPi FITC 18-Hour Assay/20x"

def compute_green_area(img, green_threshold):
    return np.sum(img[:, :, 1] > green_threshold)

def compute_red_area(img, red_threshold):
    return np.sum(img[:, :, 0] > red_threshold)

def analyze_condition(folder_path):
    scores = []

    if not os.path.exists(folder_path):
        print("Missing folder:", folder_path)
        return scores

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".tif"):
            img = mpimg.imread(os.path.join(folder_path, filename))

            green_area = compute_green_area(img, green_threshold)
            red_area = compute_red_area(img, red_threshold)

            ratio = green_area / red_area if red_area != 0 else 0
            scores.append(ratio)

    return scores

def perform_macropinocytosis_analysis():
    means, sems, all_scores = [], [], []

    for condition in conditions:
        folder_path = os.path.join(BASE_FOLDER, condition)
        scores = analyze_condition(folder_path)
        all_scores.append(scores)

        if scores:
            mean = np.mean(scores)
            sem = np.std(scores) / np.sqrt(len(scores))
        else:
            mean, sem = 0, 0

        means.append(mean)
        sems.append(sem)

    # Plot
    plt.figure(figsize=(7, 5))
    plt.bar(conditions, means, yerr=sems, capsize=5)
    plt.ylabel("Green / Red Ratio")
    plt.title("Macropinocytosis vs PELPi Dose", fontsize=14, weight="bold")

    # Stats vs 0 nM
    control_scores = all_scores[0]
    y_max = max(m + s for m, s in zip(means, sems)) * 1.1

    for i in range(1, len(conditions)):
        if not all_scores[i] or not control_scores:
            continue

        _, p = ttest_ind(all_scores[i], control_scores)
        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        else:
            sig = ""

        if sig:
            plt.text(i, means[i] + sems[i] + 0.02 * y_max, sig,
                     ha="center", fontsize=14)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    perform_macropinocytosis_analysis()
