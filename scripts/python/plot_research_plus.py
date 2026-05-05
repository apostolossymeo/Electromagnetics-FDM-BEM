import numpy as np
import matplotlib.pyplot as plt
from .config import Domain, BoundaryCase
from .fdm_performance import solver_scaling
from .fdm_masked import solve_l_shape
from .bem_studies import isolated_plate_refinement, parallel_plate_refinement
from .plots import style, save

def figure_solver_performance(rows, out):
    style()
    direct = [r for r in rows if r["method"] == "direct"]
    cg = [r for r in rows if r["method"] == "cg"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.7), constrained_layout=True)

    for data, label, marker in [(direct, "direct sparse solve", "o"), (cg, "conjugate gradient", "s")]:
        u = np.array([r["unknowns"] for r in data])
        t = np.array([r["time_s"] for r in data])
        res = np.array([r["residual"] for r in data])
        ax[0].loglog(u, t, marker=marker, label=label)
        ax[1].semilogy(u, res, marker=marker, label=label)

    ax[0].grid(True, which="both", alpha=0.3)
    ax[0].set_xlabel("interior unknowns")
    ax[0].set_ylabel("solve time (s)")
    ax[0].set_title("FDM solver cost")
    ax[0].legend()

    ax[1].grid(True, which="both", alpha=0.3)
    ax[1].set_xlabel("interior unknowns")
    ax[1].set_ylabel("relative residual")
    ax[1].set_title("linear-system residual")
    ax[1].legend()

    save(fig, out / "benchmark/03_direct_vs_cg.png")

def figure_l_shape(out):
    style()
    r = solve_l_shape(90, 90)
    x, y, V = r["x"], r["y"], r["V"]
    X, Y = np.meshgrid(x, y, indexing="ij")
    fig, ax = plt.subplots(1, 2, figsize=(12, 5.2), constrained_layout=True)

    im = ax[0].contourf(X, Y, V, levels=26, cmap="viridis")
    ax[0].set_aspect("equal")
    ax[0].set_xlabel("x")
    ax[0].set_ylabel("y")
    ax[0].set_title("L-shaped electrostatic domain")
    fig.colorbar(im, ax=ax[0], label="V")

    ax[1].spy(r["A"], markersize=0.05, color="black")
    ax[1].set_title(f"masked sparse operator ({r['A'].shape[0]} unknowns)")
    ax[1].set_xlabel("column")
    ax[1].set_ylabel("row")

    save(fig, out / "fdm/06_l_shaped_domain.png")
    return {
        "unknowns": int(r["A"].shape[0]),
        "nonzeros": int(r["A"].nnz),
        "residual": float(r["residual"]),
    }

def figure_accuracy_cost(fdm_rows, bem_rows, out):
    style()
    fig, ax = plt.subplots(figsize=(7, 5), constrained_layout=True)
    f_u = np.array([r["unknowns"] for r in fdm_rows])
    f_e = np.array([r["relative_l2_error"] for r in fdm_rows])
    b_p = np.array([r["panels"] for r in bem_rows])
    b_c = np.array([r["capacitance_F"] for r in bem_rows])
    b_ref = b_c[-1]
    b_err = np.abs((b_c - b_ref) / b_ref)

    ax.loglog(f_u, f_e, marker="o", label="FDM relative field error")
    ax.loglog(b_p, b_err, marker="s", label="BEM relative capacitance change")
    ax.grid(True, which="both", alpha=0.3)
    ax.set_xlabel("unknowns / panels")
    ax.set_ylabel("relative error proxy")
    ax.set_title("accuracy proxy under refinement")
    ax.legend()
    save(fig, out / "benchmark/04_accuracy_cost_proxy.png")

def figure_research_claims(summary, out):
    style()
    fig, ax = plt.subplots(figsize=(10, 4.8), constrained_layout=True)
    ax.axis("off")
    text = (
        "Numerical observations\\n\\n"
        "1. Sparse FDM gives a validated field solution over the full domain.\\n"
        "2. BEM uses fewer geometric unknowns but forms dense influence matrices.\\n"
        "3. Panel refinement improves capacitance estimates but increases conditioning cost.\\n"
        "4. Edge charge concentration is visible only after refinement.\\n"
        "5. Non-rectangular domains are naturally handled by masked sparse operators."
    )
    ax.text(0.02, 0.95, text, va="top", ha="left", fontsize=13)
    save(fig, out / "benchmark/05_research_observations.png")

def generate_extra(out, fdm_rows, summary):
    rows = solver_scaling(sizes=(28, 36, 48, 64, 80))
    figure_solver_performance(rows, out)
    lshape = figure_l_shape(out)
    iso_rows, _, _ = isolated_plate_refinement()
    figure_accuracy_cost(fdm_rows, iso_rows, out)
    figure_research_claims(summary, out)
    return {"solver_scaling": rows, "l_shape": lshape}
