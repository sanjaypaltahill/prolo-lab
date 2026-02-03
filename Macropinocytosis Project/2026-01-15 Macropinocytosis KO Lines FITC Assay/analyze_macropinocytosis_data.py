import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.stats import ttest_ind

## CONFIGURATION ##
# Choose thresholds to avoid counting background noise
green_threshold = 0
red_threshold = 0

# Define conditions
conditions = ["SafeGuide", "PELP1", "AMBRA1", "SNAP23"]

# Given an image, return the number of pixels whose greenxa
# value exceeds the threshold
def compute_green_area(img, green_threshold):
    green_img = img[:,:,1]
    return np.sum(green_img > green_threshold)

# Given an image, return the number of pixels whose red
# value exceeds the threshold
def compute_red_area(img, red_threshold):
    red_img = img[:,:,0]
    return np.sum(red_img > red_threshold)

# Given a condition, analyze the images for that condition
# and return a vector of the resulting metrics. 
def analyze_condition(folder_path):
    scores = []
    if not os.path.exists(folder_path):
        print("Folder does not exist:", folder_path)
        return scores

    # Loop through tif files
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".tif"):
            img_path = os.path.join(folder_path, filename)

            # Load the tif as a numpy array (replace with your actual loading method)
            img = mpimg.imread(img_path)

            green_area = compute_green_area(img, green_threshold)
            red_area = compute_red_area(img, red_threshold)

            # Avoid division by zero
            ratio = green_area / red_area if red_area != 0 else 0
            scores.append(ratio)

    return scores

# Given the user's choice, analyze all conditions.
def perform_macropinocytosis_analysis(choice):
    base_folder = f"Macropinocytosis {choice} Images"
    
    means = []
    sems = []  # Changed from stds to sems
    all_scores = []

    # Define the colors for each condition
    color_map = {
        "PELP1": "#8D9C86",   # greenish for increase
        "SafeGuide": "#B8B2B2", # neutral
        "AMBRA1": "#D46C6C",  # reddish for decrease
        "SNAP23": "#D46C6C"
    }

    for condition in conditions:
        folder_path = os.path.join(base_folder, f"{condition} {choice}")
        scores = analyze_condition(folder_path)
        all_scores.append(scores)

        if scores:  # only compute if there are images
            mean_ratio = np.mean(scores)
            std_ratio = np.std(scores)
            n = len(scores)
            sem = std_ratio / np.sqrt(n)  # Calculate SEM instead of SD
        else:
            mean_ratio = 0
            sem = 0

        means.append(mean_ratio)
        sems.append(sem)  # Store SEM instead of SD

    # Plotting
    plt.figure(figsize=(8,5))
    bars = plt.bar(conditions, means, yerr=sems, capsize=5, color=[color_map.get(c, "#AAAAAA") for c in conditions])
    plt.ylabel("Green/Red Ratio")
    plt.title(f"Macropinocytosis in KO Lines: {choice}", fontsize=16, weight='bold')

    # Add significance vs SafeGuide
    control_scores = all_scores[conditions.index("SafeGuide")]
    y_max = max([m + s for m, s in zip(means, sems)]) * 1.1  # space above tallest bar

    for i, scores in enumerate(all_scores):
        if conditions[i] == "SafeGuide":
            continue  # skip control itself
        if not scores or not control_scores:
            continue
        stat, p = ttest_ind(scores, control_scores)
        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        else:
            sig = ""
        if sig:
            plt.text(i, means[i] + sems[i] + 0.02 * y_max, sig, ha='center', fontsize=14, color='black')

    plt.tight_layout()
    plt.show()


# Call function
def main():
    # User chooses to analyze 10x, 20x, or 63x images
    choice = input("Which images would you like to analyze? 10x, 20x, or 63x?")

    # Perform analysis
    perform_macropinocytosis_analysis(choice)

if __name__ == "__main__":
    main()