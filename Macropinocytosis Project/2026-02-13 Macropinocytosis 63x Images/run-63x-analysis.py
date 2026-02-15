import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.stats import ttest_ind

## ================= CONFIGURATION ================= ##
yellow_threshold = 50  # Threshold for TMR dye detection
black_threshold = 50   # Threshold for background detection

# EXPERIMENT: 63x Images (2026-02-13)
# Updated for the three cell lines in your project
# Order: SF188 WT (control), Pancreatic 8988T, Lung H1299
groups_63x = [
    ("SF188 WT", "SF188 WT", "#808080"),              # Grey (Control)
    ("Pancreatic 8988T", "Pancreatic 8988T", "#e67e22"),  # Orange
    ("Lung H1299", "Lung H1299", "#e67e22"),          # Dark Orange
]

BASE_FOLDER_63X = "Macropinocytosis Project/2026-02-13 Macropinocytosis 63x Images"

## ================= FUNCTIONS ================= ##
def compute_yellow_area(img, yellow_threshold):
    """Calculate the total area of yellow pixels above threshold (TMR dye)"""
    # Yellow is combination of Red + Green channels
    # We'll sum both R and G channels and check if above threshold
    yellow_intensity = (img[:, :, 0].astype(float) + img[:, :, 1].astype(float)) / 2
    return np.sum(yellow_intensity > yellow_threshold)

def compute_total_cell_area(img, black_threshold):
    """Calculate total cell area by excluding black background pixels"""
    black_pixels = np.all(img[:, :, :3] < black_threshold, axis=2)
    total_pixels = img.shape[0] * img.shape[1]
    return total_pixels - np.sum(black_pixels)

def analyze_condition(folder_path):
    """
    Analyze all TIFF images in a folder and compute yellow/cell area ratios.
    
    Returns:
        ratios: list of yellow_area/total_cell_area for each image
        yellow_areas: list of yellow pixel counts
        cell_areas: list of total cell pixel counts
    """
    ratios = []
    yellow_areas = []
    cell_areas = []
    
    if not os.path.exists(folder_path):
        print(f"⚠️  Missing folder: {folder_path}")
        return ratios, yellow_areas, cell_areas
    
    # Look for both .tif and .tiff extensions
    image_files = [f for f in os.listdir(folder_path) 
                   if f.lower().endswith(('.tif', '.tiff'))]
    
    if not image_files:
        print(f"⚠️  No TIFF images found in: {folder_path}")
        return ratios, yellow_areas, cell_areas
    
    for filename in image_files:
        img = mpimg.imread(os.path.join(folder_path, filename))
        yellow_area = compute_yellow_area(img, yellow_threshold)
        total_cell_area = compute_total_cell_area(img, black_threshold)
        ratio = yellow_area / total_cell_area if total_cell_area != 0 else 0
        
        ratios.append(ratio)
        yellow_areas.append(yellow_area)
        cell_areas.append(total_cell_area)
    
    return ratios, yellow_areas, cell_areas

def create_beautiful_plot(labels, means, sems, all_scores, colors, title, control_idx=None):
    """
    Creates a beautiful bar plot with error bars, significance markers, and a data table.
    
    Parameters:
    - labels: list of group names
    - means: list of mean values
    - sems: list of SEM values
    - all_scores: list of lists containing individual measurements
    - colors: list of colors for each bar
    - title: plot title
    - control_idx: index of control group for statistical comparison (None = compare all pairs)
    """
    fig = plt.figure(figsize=(14, 10))
    
    # Create gridspec for plot and table
    gs = fig.add_gridspec(3, 1, height_ratios=[3, 0.1, 1], hspace=0.3)
    ax_plot = fig.add_subplot(gs[0])
    ax_table = fig.add_subplot(gs[2])
    
    # -------- BAR PLOT --------
    x_pos = np.arange(len(labels))
    bars = ax_plot.bar(x_pos, means, yerr=sems, capsize=8, 
                       color=colors, edgecolor='black', linewidth=1.5,
                       error_kw={'linewidth': 2, 'ecolor': 'black'})
    
    ax_plot.set_ylabel("Yellow Area / Total Cell Area (TMR)", fontsize=16, weight='bold')
    ax_plot.set_title(title, fontsize=18, weight='bold', pad=20)
    ax_plot.set_xticks(x_pos)
    ax_plot.set_xticklabels(labels, fontsize=14, weight='bold')
    ax_plot.spines['top'].set_visible(False)
    ax_plot.spines['right'].set_visible(False)
    ax_plot.grid(axis='y', alpha=0.3, linestyle='--')
    ax_plot.tick_params(axis='both', labelsize=12)
    
    # -------- SIGNIFICANCE TESTING --------
    y_max = max(m + s for m, s in zip(means, sems)) * 1.2
    
    # Determine comparison group
    if control_idx is not None:
        comparison_idx = control_idx
    else:
        comparison_idx = 0  # Default to first group (SF188 WT)
    
    comparison_scores = all_scores[comparison_idx]
    
    for i in range(len(labels)):
        if i == comparison_idx:
            continue
        if not all_scores[i] or not comparison_scores:
            continue
        
        _, p = ttest_ind(all_scores[i], comparison_scores, equal_var=False)
        
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
                        sig, ha="center", fontsize=18, weight='bold')
    
    # -------- DATA TABLE --------
    ax_table.axis('off')
    
    # Prepare table data
    table_data = []
    if control_idx is not None:
        table_data.append(['Group', 'n', 'Mean ± SEM', f'p-value vs {labels[control_idx]}'])
    else:
        table_data.append(['Group', 'n', 'Mean ± SEM', f'p-value vs {labels[0]}'])  # Default to first group
    
    for i, label in enumerate(labels):
        n = len(all_scores[i]) if all_scores[i] else 0
        mean_sem = f"{means[i]:.4f} ± {sems[i]:.4f}" if n > 0 else "N/A"
        
        # Determine which group to compare against
        if control_idx is not None:
            comparison_idx = control_idx
        else:
            comparison_idx = 0  # Default to first group (SF188 WT)
        
        if i == comparison_idx:
            p_val = "Control"
        elif all_scores[i] and all_scores[comparison_idx]:
            _, p = ttest_ind(all_scores[i], all_scores[comparison_idx], equal_var=False)
            if p < 0.001:
                p_val = "< 0.001 ***"
            elif p < 0.01:
                p_val = f"{p:.3f} **"
            elif p < 0.05:
                p_val = f"{p:.3f} *"
            else:
                p_val = f"{p:.3f} ns"
        else:
            p_val = "N/A"
        
        table_data.append([label, str(n), mean_sem, p_val])
    
    # Create table
    table = ax_table.table(cellText=table_data, cellLoc='center', loc='center',
                          colWidths=[0.25, 0.15, 0.35, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.2)
    
    # Style header row
    for i in range(4):
        cell = table[(0, i)]
        cell.set_facecolor('#34495e')
        cell.set_text_props(weight='bold', color='white', fontsize=12)
    
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
                cell.set_text_props(weight='bold', fontsize=11)
    
    plt.tight_layout()
    return fig

def print_summary_table(labels, avg_yellow, avg_cell_area, all_scores):
    """Print a detailed summary table to console"""
    print("\n" + "="*80)
    print("DETAILED SUMMARY TABLE")
    print("="*80)
    print(f"{'Group':<20}{'n':>5}{'Avg Yellow Area':>18}{'Avg Cell Area':>18}{'Ratio':>12}")
    print("-" * 80)
    
    for i, label in enumerate(labels):
        n = len(all_scores[i]) if all_scores[i] else 0
        ratio = avg_yellow[i] / avg_cell_area[i] if avg_cell_area[i] != 0 else 0
        print(f"{label:<20}{n:>5}{avg_yellow[i]:>18.1f}{avg_cell_area[i]:>18.1f}{ratio:>12.4f}")
    print("="*80 + "\n")

def print_pairwise_comparisons(labels, all_scores):
    """Print all pairwise statistical comparisons"""
    print("\n" + "="*80)
    print("PAIRWISE STATISTICAL COMPARISONS")
    print("="*80)
    
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            if all_scores[i] and all_scores[j]:
                _, p = ttest_ind(all_scores[i], all_scores[j], equal_var=False)
                
                if p < 0.001:
                    sig = "***"
                elif p < 0.01:
                    sig = "**"
                elif p < 0.05:
                    sig = "*"
                else:
                    sig = "ns"
                
                print(f"{labels[i]} vs {labels[j]}: p = {p:.4f} {sig}")
    print("="*80 + "\n")

## ================= EXPERIMENT ANALYSIS ================= ##
def analyze_experiment(groups, base_folder, experiment_name, control_idx=None):
    """
    Analyze a single experiment and create visualizations.
    
    Parameters:
    - groups: list of tuples (label, folder_name, color)
    - base_folder: base directory path
    - experiment_name: name for the plot title
    - control_idx: index of control group (None = no control, show all comparisons)
    """
    print(f"\n{'='*80}")
    print(f"ANALYZING: {experiment_name}")
    print(f"{'='*80}")
    
    means, sems, all_scores = [], [], []
    avg_yellow, avg_cell_area = [], []
    labels, colors = [], []
    
    for label, folder, color in groups:
        labels.append(label)
        colors.append(color)
        folder_path = os.path.join(base_folder, folder)
        
        ratios, yellow_areas, cell_areas = analyze_condition(folder_path)
        all_scores.append(ratios)
        
        if ratios:
            means.append(np.mean(ratios))
            sems.append(np.std(ratios, ddof=1) / np.sqrt(len(ratios)))
            avg_yellow.append(np.mean(yellow_areas))
            avg_cell_area.append(np.mean(cell_areas))
            print(f"✓ {label}: {len(ratios)} images analyzed")
        else:
            means.append(0)
            sems.append(0)
            avg_yellow.append(0)
            avg_cell_area.append(0)
            print(f"✗ {label}: No data found")
    
    # Print summary table
    print_summary_table(labels, avg_yellow, avg_cell_area, all_scores)
    
    # Print pairwise comparisons
    print_pairwise_comparisons(labels, all_scores)
    
    # Create beautiful plot
    fig = create_beautiful_plot(labels, means, sems, all_scores, colors, 
                                experiment_name, control_idx)
    
    return fig

## ================= MAIN ================= ##
if __name__ == "__main__":
    print("\n" + "="*80)
    print("MACROPINOCYTOSIS 63x IMAGE ANALYSIS")
    print("2026-02-13 Dataset")
    print("="*80)
    
    # Analyze 63x Images comparing three cell lines
    # SF188 WT is the control (index 0)
    fig_63x = analyze_experiment(
        groups_63x, 
        BASE_FOLDER_63X,
        "Macropinocytosis TMR Uptake - 63x Imaging (Cell Line Comparison)",
        control_idx=0  # SF188 WT is the control
    )
    
    # Save the figure
    output_filename = "macropinocytosis_63x_analysis_2026-02-13.png"
    fig_63x.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"\n💾 Figure saved as: {output_filename}")
    
    plt.show()
    
    print("\n✅ Analysis complete! Graph displayed and saved.")
    print("\n📊 INTERPRETATION GUIDE:")
    print("  * p < 0.05  = statistically significant")
    print("  ** p < 0.01  = highly significant")
    print("  *** p < 0.001 = very highly significant")
    print("  ns = not significant")
    print("\n💡 TIPS:")
    print("  - Higher ratio = more macropinocytosis (more TMR uptake)")
    print("  - The script compares all cell lines to SF188 WT (control)")
    print("  - Check the console output for detailed statistics")
    print("  - Modify 'control_idx' if you want to designate a different cell line as control")