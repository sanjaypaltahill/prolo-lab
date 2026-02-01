import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy import stats

# ---- Configure matplotlib for Illustrator compatibility ----
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

# ---- Load CSV ----
df = pd.read_csv('Consent Study Clinical Project/recall-by-language-data.csv')

# ---- Filter only monolingual English (0), Spanish (1), and Bilingual English/Spanish (3) ----
df_filtered = df[df['are_you_a_fluent_speaker_o'].isin([0, 1, 3])].copy()

# ---- Map 0/1/3 to readable language names ----
df_filtered['language_category'] = df_filtered['are_you_a_fluent_speaker_o'].map({
    0: 'Monolingual English',
    1: 'Monolingual Spanish',
    3: 'Bilingual (English and Spanish)'
})

# ---- Summary statistics ----
stats_summary = df_filtered.groupby('language_category')['total_points'].agg(
    n='count',
    mean='mean',
    std='std',
    sem=lambda x: x.std() / np.sqrt(len(x))
).reset_index()

# ---- T-test ----
english_scores = df_filtered[df_filtered['language_category'] == 'Monolingual English']['total_points']
spanish_scores = df_filtered[df_filtered['language_category'] == 'Monolingual Spanish']['total_points']
bilingual_scores = df_filtered[df_filtered['language_category'] == 'Bilingual (English and Spanish)']['total_points']

t_stat_eng_spa, p_value_eng_spa = stats.ttest_ind(english_scores, spanish_scores, nan_policy='omit')
t_stat_eng_bil, p_value_eng_bil = stats.ttest_ind(english_scores, bilingual_scores, nan_policy='omit')

print("="*50)
print("STATISTICAL ANALYSIS RESULTS")
print("="*50)
print(f"T-test (English vs Spanish):")
print(f"t-statistic: {t_stat_eng_spa:.4f}")
print(f"p-value: {p_value_eng_spa:.4f}")
print(f"Statistically significant (p < 0.05): {'Yes' if p_value_eng_spa < 0.05 else 'No'}")
print()
print(f"T-test (English vs Bilingual):")
print(f"t-statistic: {t_stat_eng_bil:.4f}")
print(f"p-value: {p_value_eng_bil:.4f}")
print(f"Statistically significant (p < 0.05): {'Yes' if p_value_eng_bil < 0.05 else 'No'}")

# ---- Function to compute stacked y-positions ----
def stacked_jitter(y_base, points, spread=0.08):
    """
    y_base: the base y-position of the category (0 or 1)
    points: list/array of values at the same score
    spread: max vertical distance from the midline
    Returns: array of y-positions for plotting
    """
    n = len(points)
    if n == 1:
        return np.array([y_base])
    else:
        # Evenly space points around midline
        offsets = np.linspace(-spread, spread, n)
        return y_base + offsets

# ---- Plotting ----
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), gridspec_kw={'height_ratios': [2, 1]})

colors = {'Monolingual English': '#1f77b4', 'Monolingual Spanish': '#ff7f0e', 'Bilingual (English and Spanish)': '#2ca02c'}
# Reorder: English, Bilingual, Spanish
category_order = ['Monolingual English', 'Bilingual (English and Spanish)', 'Monolingual Spanish']
positions = [0, 1, 2]

means = [stats_summary[stats_summary['language_category'] == cat]['mean'].values[0] 
         for cat in category_order]
sems = [stats_summary[stats_summary['language_category'] == cat]['sem'].values[0] 
        for cat in category_order]

# Bar chart with error bars - narrower bars, thicker lines
ax1.barh(positions, means, color=[colors[cat] for cat in category_order], 
         height=0.25, alpha=0.8, edgecolor='black', linewidth=2)
ax1.errorbar(means, positions, xerr=sems, fmt='none', ecolor='black', capsize=6, linewidth=2, capthick=2)

# Scatter points using stacked jitter
for i, category in enumerate(category_order):
    data = df_filtered[df_filtered['language_category'] == category]['total_points']
    for score in sorted(data.unique()):
        indices = np.where(data == score)[0]
        y_positions = stacked_jitter(positions[i], indices, spread=0.08)
        ax1.scatter(
            [score]*len(y_positions),
            y_positions,
            alpha=0.8,
            s=80,
            color='gray',
            edgecolors='black',
            linewidth=1.2
        )

# Add significance lines
# Line 1: English (position 0) vs Bilingual (position 1) - INNER bracket
if p_value_eng_bil < 0.05:
    x_pos = 10.4  # Moved further right to avoid touching data points
    
    # Draw vertical line
    ax1.plot([x_pos, x_pos], [0, 1], 'k-', linewidth=2)
    # Draw caps
    ax1.plot([x_pos - 0.1, x_pos], [0, 0], 'k-', linewidth=2)
    ax1.plot([x_pos - 0.1, x_pos], [1, 1], 'k-', linewidth=2)
    # Add stars (** for p<0.01, * for p<0.05)
    stars = '**' if p_value_eng_bil < 0.01 else '*'
    ax1.text(x_pos + 0.25, 0.5, stars, fontsize=20, ha='center', va='center')

# Line 2: English (position 0) vs Spanish (position 2) - OUTER bracket
if p_value_eng_spa < 0.05:
    x_pos = 10.85  # Moved further right to create more space between brackets
    
    # Draw vertical line
    ax1.plot([x_pos, x_pos], [0, 2], 'k-', linewidth=2)
    # Draw caps
    ax1.plot([x_pos - 0.1, x_pos], [0, 0], 'k-', linewidth=2)
    ax1.plot([x_pos - 0.1, x_pos], [2, 2], 'k-', linewidth=2)
    # Add stars (** for p<0.01, * for p<0.05)
    stars = '**' if p_value_eng_spa < 0.01 else '*'
    ax1.text(x_pos + 0.25, 1, stars, fontsize=20, ha='center', va='center')

# Formatting
ax1.set_yticks(positions)
ax1.set_yticklabels(category_order, fontsize=11)
ax1.set_xlabel('Recall Score (0-10)', fontsize=11, fontweight='bold')
ax1.set_title('Recall Score by Language', fontsize=14, fontweight='bold', loc='center')
ax1.set_xlim(0, 12)
ax1.set_xticks([0, 5, 10])
ax1.invert_yaxis()
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_linewidth(2)
ax1.spines['bottom'].set_linewidth(2)
ax1.tick_params(width=2, length=6)

# Table with statistics
table_data = []
for category in category_order:
    row = stats_summary[stats_summary['language_category'] == category]
    # Determine p-value based on category
    if category == 'Monolingual English':
        p_val_display = "-"
    elif category == 'Bilingual (English and Spanish)':
        p_val_display = f"{p_value_eng_bil:.4f}"
    else:  # Monolingual Spanish
        p_val_display = f"{p_value_eng_spa:.4f}"
    
    table_data.append([
        category,
        int(row['n'].values[0]),
        f"{row['mean'].values[0]:.2f}",
        p_val_display
    ])

ax2.axis('tight')
ax2.axis('off')
table = ax2.table(cellText=table_data,
                  colLabels=['Language', 'n', 'Mean', 'p-value'],
                  cellLoc='center',
                  loc='center',
                  bbox=[0, 0, 1, 1])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style table
for i in range(4):
    table[(0, i)].set_facecolor('#D3D3D3')
    table[(0, i)].set_text_props(weight='bold')
for i in range(1, 4):
    color = '#F5F5F5' if i % 2 == 0 else 'white'
    for j in range(4):
        table[(i, j)].set_facecolor(color)

plt.tight_layout()

# ---- Save as PDF for Illustrator ----
plt.savefig('Consent Study Clinical Project/recall_score_by_language.pdf', format='pdf', bbox_inches='tight')
print("\nFigure saved as 'recall_score_by_language.pdf'")
print("This PDF should be fully editable in Adobe Illustrator!")

plt.show()