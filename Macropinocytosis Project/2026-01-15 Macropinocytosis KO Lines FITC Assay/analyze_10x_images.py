import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.stats import ttest_ind

## ================= CONFIGURATION ================= ##
green_threshold = 50
black_threshold = 50

# EXPERIMENT 1: KO Lines (with color scheme)
groups_exp1 = [
    ("SafeGuide", "SafeGuide 10x", "#808080"),      # Grey
    ("PELP1", "PELP1 10x", "#44b875"),                # Green
    ("AMBRA1", "AMBRA1 10x", "#c0392b"),              # Dark Red
    ("SNAP23", "SNAP23 10x", "#c0392b"),               # Dark Red
]

BASE_FOLDER_EXP1 = "Macropinocytosis Project/2026-01-15 Macropinocytosis KO Lines FITC Assay/10x"

# EXPERIMENT 2: Dose Response (add your folder configuration)
groups_exp2 = [
    ("WT/FITC only", "WT_FITC_only", "#808080"),     # Grey
    ("500 µM", "500uM", "#90ee90"),                  # Light Green
    ("2000 µM", "2000uM", "#228b22"),                # Dark Green
]

BASE_FOLDER_EXP2 = "Macropinocytosis Project/Dose_Response/10x"  # Update this path

## ================= FUNCTIONS ================= ##
def compute_green_area(img, green_threshold):
    return np.sum(img[:, :, 1] > green_threshold)

def compute_total_cell_area(img, black_threshold):
    black_pixels = np.all(img[:, :, :3] < black_threshold, axis=2)
    total_pixels = img.shape[0] * img.shape[1]
    return total_pixels - np.sum(black_pixels)

def analyze_condition(folder_path):
    ratios = []
    green_areas = []
    cell_areas = []
    
    if not os.path.exists(folder_path):
        print(f"⚠️  Missing folder: {folder_path}")
        return ratios, green_areas, cell_areas
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".tif"):
            img = mpimg.imread(os.path.join(folder_path, filename))
            green_area = compute_green_area(img, green_threshold)
            total_cell_area = compute_total_cell_area(img, black_threshold)
            ratio = green_area / total_cell_area if total_cell_area != 0 else 0
            
            ratios.append(ratio)
            green_areas.append(green_area)
            cell_areas.append(total_cell_area)
    
    return ratios, green_areas, cell_areas

def create_beautiful_plot(labels, means, sems, all_scores, colors, title, control_idx=0):
    """
    Creates a beautiful bar plot with error bars, significance markers, and a data table.
    
    Parameters:
    - labels: list of group names
    - means: list of mean values
    - sems: list of SEM values
    - all_scores: list of lists containing individual measurements
    - colors: list of colors for each bar
    - title: plot title
    - control_idx: index of control group for statistical comparison
    """
    fig = plt.figure(figsize=(12, 8))
    
    # Create gridspec for plot and table
    gs = fig.add_gridspec(3, 1, height_ratios=[3, 0.1, 1], hspace=0.3)
    ax_plot = fig.add_subplot(gs[0])
    ax_table = fig.add_subplot(gs[2])
    
    # -------- BAR PLOT --------
    x_pos = np.arange(len(labels))
    bars = ax_plot.bar(x_pos, means, yerr=sems, capsize=8, 
                       color=colors, edgecolor='black', linewidth=1.5,
                       error_kw={'linewidth': 2, 'ecolor': 'black'})
    
    ax_plot.set_ylabel("Green Area / Total Cell Area", fontsize=16, weight='bold')
    ax_plot.set_title(title, fontsize=16, weight='bold', pad=20)
    ax_plot.set_xticks(x_pos)
    ax_plot.set_xticklabels(labels, fontsize=14, weight='bold')
    ax_plot.spines['top'].set_visible(False)
    ax_plot.spines['right'].set_visible(False)
    ax_plot.grid(axis='y', alpha=0.3, linestyle='--')
    
    # -------- SIGNIFICANCE TESTING --------
    control_scores = all_scores[control_idx]
    y_max = max(m + s for m, s in zip(means, sems)) * 1.15
    
    for i in range(len(labels)):
        if i == control_idx:
            continue
        if not all_scores[i] or not control_scores:
            continue
        
        _, p = ttest_ind(all_scores[i], control_scores, equal_var=False)
        
        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        else:
            sig = "ns"
        
        if sig != "ns":
            ax_plot.text(i, means[i] + sems[i] + 0.03 * y_max,
                        sig, ha="center", fontsize=16, weight='bold')
    
    # -------- DATA TABLE --------
    ax_table.axis('off')
    
    # Prepare table data
    table_data = []
    table_data.append(['Group', 'n', 'Mean ± SEM', 'p-value vs Control'])
    
    for i, label in enumerate(labels):
        n = len(all_scores[i]) if all_scores[i] else 0
        mean_sem = f"{means[i]:.4f} ± {sems[i]:.4f}" if n > 0 else "N/A"
        
        if i == control_idx:
            p_val = "—"
        elif all_scores[i] and control_scores:
            _, p = ttest_ind(all_scores[i], control_scores, equal_var=False)
            if p < 0.001:
                p_val = "< 0.001"
            else:
                p_val = f"{p:.3f}"
        else:
            p_val = "N/A"
        
        table_data.append([label, str(n), mean_sem, p_val])
    
    # Create table
    table = ax_table.table(cellText=table_data, cellLoc='center', loc='center',
                          colWidths=[0.25, 0.15, 0.35, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header row
    for i in range(4):
        cell = table[(0, i)]
        cell.set_facecolor('#34495e')
        cell.set_text_props(weight='bold', color='white')
    
    # Alternate row colors and bold group names
    for i in range(1, len(table_data)):
        for j in range(4):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#ecf0f1')
            else:
                cell.set_facecolor('white')
            # Bold the group names (first column)
            if j == 0:
                cell.set_text_props(weight='bold')
    
    plt.tight_layout()
    return fig

def print_summary_table(labels, avg_green, avg_cell_area, all_scores):
    """Print a detailed summary table to console"""
    print("\n" + "="*70)
    print("DETAILED SUMMARY TABLE")
    print("="*70)
    print(f"{'Group':<15}{'n':>5}{'Avg Green Area':>18}{'Avg Cell Area':>18}{'Ratio':>12}")
    print("-" * 70)
    
    for i, label in enumerate(labels):
        n = len(all_scores[i]) if all_scores[i] else 0
        ratio = avg_green[i] / avg_cell_area[i] if avg_cell_area[i] != 0 else 0
        print(f"{label:<15}{n:>5}{avg_green[i]:>18.1f}{avg_cell_area[i]:>18.1f}{ratio:>12.4f}")
    print("="*70 + "\n")

## ================= EXPERIMENT ANALYSIS ================= ##
def analyze_experiment(groups, base_folder, experiment_name, control_idx=0):
    """
    Analyze a single experiment and create visualizations.
    
    Parameters:
    - groups: list of tuples (label, folder_name, color)
    - base_folder: base directory path
    - experiment_name: name for the plot title
    - control_idx: index of control group
    """
    print(f"\n{'='*70}")
    print(f"ANALYZING: {experiment_name}")
    print(f"{'='*70}")
    
    means, sems, all_scores = [], [], []
    avg_green, avg_cell_area = [], []
    labels, colors = [], []
    
    for label, folder, color in groups:
        labels.append(label)
        colors.append(color)
        folder_path = os.path.join(base_folder, folder)
        
        ratios, green_areas, cell_areas = analyze_condition(folder_path)
        all_scores.append(ratios)
        
        if ratios:
            means.append(np.mean(ratios))
            sems.append(np.std(ratios, ddof=1) / np.sqrt(len(ratios)))
            avg_green.append(np.mean(green_areas))
            avg_cell_area.append(np.mean(cell_areas))
            print(f"✓ {label}: {len(ratios)} images analyzed")
        else:
            means.append(0)
            sems.append(0)
            avg_green.append(0)
            avg_cell_area.append(0)
            print(f"✗ {label}: No data found")
    
    # Print summary table
    print_summary_table(labels, avg_green, avg_cell_area, all_scores)
    
    # Create beautiful plot
    fig = create_beautiful_plot(labels, means, sems, all_scores, colors, 
                                experiment_name, control_idx)
    
    return fig

## ================= MAIN ================= ##
if __name__ == "__main__":
    # Experiment 1: KO Lines
    fig1 = analyze_experiment(
        groups_exp1, 
        BASE_FOLDER_EXP1,
        "Macropinocytosis FITC Uptake - KO Lines (10x)",
        control_idx=0  # SafeGuide is control
    )
    
    # Experiment 2: Dose Response
    # Uncomment when you have the correct folder path
    # fig2 = analyze_experiment(
    #     groups_exp2, 
    #     BASE_FOLDER_EXP2,
    #     "Macropinocytosis FITC Uptake - Dose Response (10x)",
    #     control_idx=0  # WT/FITC only is control
    # )
    
    plt.show()
    
    print("\n✅ Analysis complete! Graphs displayed.")
    print("💡 Tip: Use plt.savefig() to save figures as high-res images for your presentation.")