import numpy as np
import matplotlib.pyplot as plt
from .config import Domain, BoundaryCase, FDMStudy
from .fdm_solver import validate_top_plate, electric_field
from .fdm_studies import convergence, boundary_sensitivity
from .plots import style, save

def figure_operator(result, out):
    style()
    A = result["A"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.7), constrained_layout=True)
    ax[0].spy(A, markersize=0.06, color="black")
    ax[0].set_title(f"sparse operator ({A.shape[0]} unknowns)")
    ax[0].set_xlabel("column")
    ax[0].set_ylabel("row")
    ax[1].spy(A[:500, :500], markersize=0.55, color="black")
    ax[1].set_title("stencil connectivity zoom")
    ax[1].set_xlabel("column")
    ax[1].set_ylabel("row")
    save(fig, out / "fdm/01_sparse_operator.png")

def figure_potential_field(result, out):
    style()
    x, y, V = result["x"], result["y"], result["V"]
    X, Y = np.meshgrid(x, y, indexing="ij")
    Ex, Ey = electric_field(x, y, V)
    fig, ax = plt.subplots(figsize=(7, 6), constrained_layout=True)
    im = ax.contourf(X, Y, V, levels=np.linspace(0, 100, 26), cmap="viridis")
    cs = ax.contour(X, Y, V, levels=np.arange(10, 100, 10), colors="white", linewidths=0.65, alpha=0.8)
    ax.clabel(cs, fmt="%d V", fontsize=7)
    ax.streamplot(x, y, Ex.T, Ey.T, color="black", density=0.85, linewidth=0.55, arrowsize=0.75)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("potential contours and electric field lines")
    fig.colorbar(im, ax=ax, label="V")
    save(fig, out / "fdm/02_potential_field.png")

def figure_validation(result, out):
    style()
    x, y, V, R = result["x"], result["y"], result["V"], result["reference"]
    E = np.abs(result["error"])
    X, Y = np.meshgrid(x, y, indexing="ij")
    M = E.copy()
    M[:3, :] = np.nan; M[-3:, :] = np.nan; M[:, :3] = np.nan; M[:, -3:] = np.nan
    vmax = np.nanpercentile(M, 99)
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.8), constrained_layout=True)
    for a, Z, title in zip(ax[:2], [V, R], ["sparse FDM", "analytical series"]):
        im = a.contourf(X, Y, Z, levels=np.linspace(0, 100, 24), cmap="viridis")
        a.set_aspect("equal")
        a.set_title(title)
        a.set_xlabel("x")
        a.set_ylabel("y")
    im2 = ax[2].imshow(M.T, origin="lower", extent=[0,4,0,4], aspect="equal", cmap="magma", vmin=0, vmax=vmax)
    ax[2].set_title("interior absolute error")
    ax[2].set_xlabel("x")
    ax[2].set_ylabel("y")
    fig.colorbar(im, ax=ax[:2], label="V", shrink=0.85)
    fig.colorbar(im2, ax=ax[2], label="|error|", shrink=0.85)
    save(fig, out / "fdm/03_validation_error.png")

def figure_convergence(rows, order, out):
    style()
    h = np.array([r["h"] for r in rows])
    e = np.array([r["relative_l2_error"] for r in rows])
    u = np.array([r["unknowns"] for r in rows])
    z = np.array([r["nonzeros"] for r in rows])
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.7), constrained_layout=True)
    ax[0].loglog(h, e, marker="o")
    ax[0].invert_xaxis()
    ax[0].grid(True, which="both", alpha=0.3)
    ax[0].set_title(f"grid convergence, slope ≈ {order:.2f}")
    ax[0].set_xlabel("grid spacing h")
    ax[0].set_ylabel("relative L2 error")
    ax[1].loglog(u, z, marker="o")
    ax[1].grid(True, which="both", alpha=0.3)
    ax[1].set_title("sparse matrix growth")
    ax[1].set_xlabel("interior unknowns")
    ax[1].set_ylabel("nonzero entries")
    save(fig, out / "fdm/04_convergence_scaling.png")

def figure_boundary_sensitivity(fields, out):
    style()
    fig, ax = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
    for a, (name, r) in zip(ax.flat, fields.items()):
        x, y, V = r["x"], r["y"], r["V"]
        X, Y = np.meshgrid(x, y, indexing="ij")
        im = a.contourf(X, Y, V, levels=24, cmap="viridis")
        a.set_aspect("equal")
        a.set_title(name.replace("_", " "))
        a.set_xlabel("x")
        a.set_ylabel("y")
    fig.colorbar(im, ax=ax, shrink=0.85, label="V")
    save(fig, out / "fdm/05_boundary_sensitivity.png")

def generate(out):
    study = FDMStudy()
    result = validate_top_plate(Domain(study.reference_n, study.reference_n), BoundaryCase("top_100", top=100.0), study.series_terms)
    rows, order = convergence()
    sensitivity_rows, fields = boundary_sensitivity()
    figure_operator(result, out)
    figure_potential_field(result, out)
    figure_validation(result, out)
    figure_convergence(rows, order, out)
    figure_boundary_sensitivity(fields, out)
    return result, rows, order, sensitivity_rows
