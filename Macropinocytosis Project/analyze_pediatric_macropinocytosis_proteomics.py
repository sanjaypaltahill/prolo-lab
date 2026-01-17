import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# ---- Load txt files (tab-delimited) ----
pelp1 = pd.read_csv("PELP1_expression_enrichment.txt", sep="\t")
snap23 = pd.read_csv("SNAP23_expression_enrichment.txt", sep="\t")

# ---- Standardize group names ----
def clean_groups(df):
    df["Group"] = (
        df["Group"]
        .str.replace("(A) Pediatric High Grade Gliomas", "High-grade", regex=False)
        .str.replace("(B) Pediatric Low Grade Gliomas", "Low-grade", regex=False)
    )
    return df

pelp1 = clean_groups(pelp1)
snap23 = clean_groups(snap23)

# ---- Generic plotting function ----
def plot_gene(df, value_col, title):
    # define order and colors
    order = ["Low-grade", "High-grade"]
    palette = {"Low-grade": "#ADA5A5", "High-grade": "#D96F6F"}  # your original colors

    high = df[df.Group == "High-grade"][value_col]
    low = df[df.Group == "Low-grade"][value_col]

    # t-test
    t, p = ttest_ind(high, low, equal_var=False)

    # Plot
    plt.figure(figsize=(4,6))
    ax = sns.boxplot(
        data=df, x="Group", y=value_col,
        order=order, palette=palette,
        width=0.5, showfliers=False
    )
    sns.stripplot(
        data=df, x="Group", y=value_col,
        order=order, color="black", size=3, jitter=0.15
    )

    ax.set_title(f"{title} (p={p:.3e})")
    ax.set_ylabel("Protein level")

    # ---- Significance bar ----
    y_max = max(high.max(), low.max())
    y_range = df[value_col].max() - df[value_col].min()
    pad = y_range * 0.1 if y_range > 0 else 0.1

    y = y_max + pad
    ax.plot([0, 0, 1, 1], [y, y + pad, y + pad, y], lw=1.3, c='black')

    # stars
    if p < 0.001:
        stars = "***"
    elif p < 0.01:
        stars = "**"
    elif p < 0.05:
        stars = "*"
    else:
        stars = "ns"

    ax.text(0.5, y + pad*1.2, stars, ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# ---- Run for PELP1 + SNAP23 ----
plot_gene(pelp1, "PELP1, Protein levels", "PELP1 Expression in Pediatric Glioma")
plot_gene(snap23, "SNAP23, Protein levels", "SNAP23 Expression in Pediatric Glioma")
