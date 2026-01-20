import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import numpy as np


# ---- Load txt files ----
pelp1 = pd.read_csv("Macropinocytosis Project/PELP1_expression_enrichment.txt", sep="\t")
snap23 = pd.read_csv("Macropinocytosis Project/SNAP23_expression_enrichment.txt", sep="\t")


# ---- Clean group names ----
def clean_groups(df):
    df["Group"] = (
        df["Group"]
        .str.replace("(A) Pediatric High Grade Gliomas", "High-grade", regex=False)
        .str.replace("(B) Pediatric Low Grade Gliomas", "Low-grade", regex=False)
    )
    return df

pelp1 = clean_groups(pelp1)
snap23 = clean_groups(snap23)


# ---- Normalization (shift-only for visualization) ----
def normalize_shift(df, value_col):
    offset = abs(df[value_col].min())
    df[value_col + "_norm"] = df[value_col] + offset
    return df

pelp1 = normalize_shift(pelp1, "PELP1, Protein levels")
snap23 = normalize_shift(snap23, "SNAP23, Protein levels")


# ---- Boxplot (raw data) ----
def plot_gene_box(df, value_col, title):
    order = ["Low-grade", "High-grade"]
    palette = {"Low-grade": "#ADA5A5", "High-grade": "#D96F6F"}

    high = df[df.Group == "High-grade"][value_col]
    low = df[df.Group == "Low-grade"][value_col]
    t, p = ttest_ind(high, low, equal_var=False)

    plt.figure(figsize=(4,6))
    ax = sns.boxplot(data=df, x="Group", y=value_col,
                     order=order, palette=palette,
                     width=0.5, showfliers=False)
    sns.stripplot(data=df, x="Group", y=value_col,
                  order=order, color="black", size=3, jitter=0.15)

    ax.set_title(f"{title} (p={p:.3e})")
    ax.set_ylabel("Protein level")

    y_max = max(high.max(), low.max())
    y_range = df[value_col].max() - df[value_col].min()
    pad = y_range * 0.1 if y_range > 0 else 0.1
    y = y_max + pad

    ax.plot([0, 0, 1, 1], [y, y+pad, y+pad, y], lw=1.3, c='black')
    stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    ax.text(0.5, y + pad*1.2, stars, ha='center')

    plt.tight_layout()
    plt.show()


# ---- Mean ± SEM barplot (normalized for visualization) ----
def plot_gene_sem(df, raw_col, title):
    norm_col = raw_col + "_norm"       # for visuals
    order = ["Low-grade", "High-grade"]
    palette = {"Low-grade": "#ADA5A5", "High-grade": "#D96F6F"}

    raw_groups = [df[df.Group == g][raw_col] for g in order]
    norm_groups = [df[df.Group == g][norm_col] for g in order]

    # stats from raw values (correct)
    t, p = ttest_ind(raw_groups[0], raw_groups[1], equal_var=False)

    # means/sem for normalized dislay
    means = [g.mean() for g in norm_groups]
    sems = [g.sem() for g in norm_groups]

    plt.figure(figsize=(4,6))
    ax = plt.gca()
    x = np.arange(len(order))

    ax.bar(x, means, color=[palette[g] for g in order],
           width=0.6, edgecolor='black', linewidth=1.3)

    ax.errorbar(x, means, yerr=sems, fmt='none',
                capsize=6, ecolor='black', elinewidth=1.4)

    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_ylabel("Normalized protein level")
    ax.set_title(f"{title} (p={p:.3e})")

    y_max = max([m + s for m, s in zip(means, sems)])
    pad = (max(means) - min(means))*0.25 if max(means)!=min(means) else 0.1
    y = y_max + pad

    ax.plot([0, 0, 1, 1], [y, y+pad, y+pad, y], lw=1.3, c='black')
    stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    ax.text(0.5, y + pad*0.9, stars, ha='center')

    plt.tight_layout()
    plt.show()


# ---- Run all four ----
plot_gene_box(pelp1, "PELP1, Protein levels", "PELP1 Expression in Pediatric Glioma")
plot_gene_box(snap23, "SNAP23, Protein levels", "SNAP23 Expression in Pediatric Glioma")

plot_gene_sem(pelp1, "PELP1, Protein levels", "PELP1 Expression (Mean ± SEM)")
plot_gene_sem(snap23, "SNAP23, Protein levels", "SNAP23 Expression (Mean ± SEM)")
