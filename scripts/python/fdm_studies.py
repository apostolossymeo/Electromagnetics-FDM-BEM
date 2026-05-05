import numpy as np
from .config import Domain, BoundaryCase, FDMStudy
from .fdm_solver import validate_top_plate, solve, electrostatic_energy

def convergence(study=FDMStudy()):
    rows = []
    case = BoundaryCase("top_100", top=100.0)
    for n in study.sizes:
        domain = Domain(n, n)
        r = validate_top_plate(domain, case, study.series_terms)
        rows.append({
            "n": int(n),
            "h": float(domain.lx / (n - 1)),
            "unknowns": int((n - 2) * (n - 2)),
            "nonzeros": int(r["A"].nnz),
            "relative_l2_error": float(r["relative_l2_error"]),
            "linear_residual": float(r["residual"]),
            "energy_J_per_m": float(r["energy"]),
        })
    h = np.array([r["h"] for r in rows[-4:]])
    e = np.array([r["relative_l2_error"] for r in rows[-4:]])
    order = float(np.polyfit(np.log(h), np.log(e), 1)[0])
    return rows, order

def boundary_sensitivity():
    cases = [
        BoundaryCase("top_drive", top=100.0, bottom=0.0, left=0.0, right=0.0),
        BoundaryCase("opposed_plates", top=100.0, bottom=-100.0, left=0.0, right=0.0),
        BoundaryCase("side_drive", top=0.0, bottom=0.0, left=100.0, right=0.0),
        BoundaryCase("corner_bias", top=100.0, bottom=0.0, left=50.0, right=0.0),
    ]
    rows = []
    fields = {}
    for c in cases:
        d = Domain(100, 100)
        r = solve(d, c)
        rows.append({
            "case": c.name,
            "min_potential": float(r["V"].min()),
            "max_potential": float(r["V"].max()),
            "energy_J_per_m": float(electrostatic_energy(r["x"], r["y"], r["V"])),
            "residual": float(r["residual"]),
        })
        fields[c.name] = r
    return rows, fields
