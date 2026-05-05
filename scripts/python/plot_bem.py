import numpy as np
import matplotlib.pyplot as plt
from .bem_studies import isolated_plate_refinement, parallel_plate_refinement, charge_density_by_x
from .plots import style, save

def figure_panel_refinement(sequence, out):
    style()
    fig, ax = plt.subplots(2, 2, figsize=(9.5, 8), constrained_layout=True)
    for a, (level, panels) in zip(ax.flat, sequence[:4]):
        for p in panels:
            a.add_patch(plt.Rectangle((p.x-p.sx/2, p.y-p.sy/2), p.sx, p.sy, fill=False, lw=0.45, color="black"))
        a.set_title(f"iteration {level}: {len(panels)} panels")
        a.set_xlim(-0.53, 0.53)
        a.set_ylim(-0.53, 0.53)
        a.set_aspect("equal")
        a.set_xticks([])
        a.set_yticks([])
    fig.suptitle("recursive panel refinement", fontsize=15)
    save(fig, out / "bem/01_panel_refinement.png")

def figure_capacitance(iso_rows, pp_rows, out):
    style()
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.7), constrained_layout=True)
    for rows, label in [(iso_rows, "isolated plate"), (pp_rows, "parallel plates")]:
        n = np.array([r["panels"] for r in rows])
        c = np.array([r["capacitance_F"] for r in rows]) * 1e12
        ax[0].plot(n, c, marker="o", label=label)
    ax[0].set_xscale("log", base=4)
    ax[0].grid(True, which="both", alpha=0.3)
    ax[0].set_xlabel("number of panels")
    ax[0].set_ylabel("capacitance estimate (pF)")
    ax[0].set_title("capacitance under refinement")
    ax[0].legend()
    for rows, label in [(iso_rows, "isolated plate"), (pp_rows, "parallel plates")]:
        n = np.array([r["panels"] for r in rows if r["condition_number"] is not None])
        k = np.array([r["condition_number"] for r in rows if r["condition_number"] is not None])
        ax[1].semilogy(n, k, marker="o", label=label)
    ax[1].grid(True, which="both", alpha=0.3)
    ax[1].set_xlabel("number of panels")
    ax[1].set_ylabel("condition number")
    ax[1].set_title("influence matrix conditioning")
    ax[1].legend()
    save(fig, out / "bem/02_capacitance_conditioning.png")

def figure_charge(sequence, charges, out):
    style()
    fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
    lookup = dict(sequence)
    for level in sorted(charges.keys()):
        x, sigma = charge_density_by_x(lookup[level], charges[level])
        ax.plot(x, sigma, marker=".", lw=1.3, label=f"{len(lookup[level])} panels")
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("panel center x")
    ax.set_ylabel("surface charge density estimate")
    ax.set_title("edge charge concentration")
    ax.legend()
    save(fig, out / "bem/03_charge_density.png")

def generate(out):
    iso_rows, iso_seq, charges = isolated_plate_refinement()
    pp_rows, pp_seq = parallel_plate_refinement()
    figure_panel_refinement(iso_seq, out)
    figure_capacitance(iso_rows, pp_rows, out)
    figure_charge(iso_seq, charges, out)
    return iso_rows, pp_rows, iso_seq
