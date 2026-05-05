import numpy as np
import matplotlib.pyplot as plt
from .plots import style, save

def figure_storage(fdm_rows, bem_rows, out):
    style()
    fdm_u = np.array([r["unknowns"] for r in fdm_rows])
    fdm_z = np.array([r["nonzeros"] for r in fdm_rows])
    bem_n = np.array([r["panels"] for r in bem_rows])
    bem_z = bem_n**2
    fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
    ax.loglog(fdm_u, fdm_z, marker="o", label="FDM sparse nonzeros")
    ax.loglog(bem_n, bem_z, marker="s", label="BEM dense entries")
    ax.grid(True, which="both", alpha=0.3)
    ax.set_xlabel("unknowns / panels")
    ax.set_ylabel("matrix entries")
    ax.set_title("storage growth of the two formulations")
    ax.legend()
    save(fig, out / "benchmark/01_storage_comparison.png")

def figure_summary_table_image(fdm_rows, iso_rows, pp_rows, out):
    style()
    labels = ["FDM unknowns", "BEM isolated panels", "BEM parallel panels"]
    values = [fdm_rows[-1]["unknowns"], iso_rows[-1]["panels"], pp_rows[-1]["panels"]]
    fig, ax = plt.subplots(figsize=(7, 3.5), constrained_layout=True)
    ax.bar(labels, values)
    ax.set_yscale("log")
    ax.set_ylabel("count")
    ax.set_title("largest benchmark sizes in the default run")
    ax.tick_params(axis="x", rotation=12)
    save(fig, out / "benchmark/02_benchmark_sizes.png")

def generate(fdm_rows, iso_rows, pp_rows, out):
    figure_storage(fdm_rows, iso_rows, out)
    figure_summary_table_image(fdm_rows, iso_rows, pp_rows, out)
