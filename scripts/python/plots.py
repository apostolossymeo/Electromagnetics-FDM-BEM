import numpy as np
import matplotlib.pyplot as plt

def style():
    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 280,
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
        "lines.linewidth": 1.7,
    })

def save(fig, path):
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
