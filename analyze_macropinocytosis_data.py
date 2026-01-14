import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
    stds = []

    # Define the colors for each condition
    color_map = {
        "PELP1": "#8D9C86",
        "SafeGuide": "#B8B2B2",
        "AMBRA1": "#D4A498",
        "SNAP23": "#D4A498"
    }

    for condition in conditions:
        folder_path = os.path.join(base_folder, f"{condition} {choice}")
        scores = analyze_condition(folder_path)

        if scores:  # only compute if there are images
            mean_ratio = np.mean(scores)
            std_ratio = np.std(scores)
        else:
            mean_ratio = 0
            std_ratio = 0

        means.append(mean_ratio)
        stds.append(std_ratio)

    # Assign colors in the order of conditions
    bar_colors = [color_map.get(cond, "#AAAAAA") for cond in conditions]  # default grey if missing

    # Plotting
    plt.figure(figsize=(8,5))
    bars = plt.bar(conditions, means, yerr=stds, capsize=5, color=bar_colors)
    plt.ylabel("Green/Red Ratio")
    plt.title(f"Macropinocytosis in KO Lines: {choice}", fontsize=16, weight='bold')
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