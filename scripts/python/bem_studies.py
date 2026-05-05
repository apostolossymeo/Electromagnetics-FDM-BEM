import numpy as np
from .config import BEMStudy
from .bem_geometry import single_plate_13, parallel_plates_13, sequence, arrays
from .bem_operator import solve_charges, conductor_potentials

def extrapolate(rows, n):
    c = np.array([r["capacitance_F"] for r in rows[-3:]], dtype=float)
    p = np.array([r["panels"] for r in rows[-3:]], dtype=float)
    X = np.column_stack([np.ones_like(p), 1/np.sqrt(p), 1/p])
    a = np.linalg.lstsq(X, c, rcond=None)[0]
    return float(a[0] + a[1]/np.sqrt(n) + a[2]/n)

def isolated_plate_refinement(study=BEMStudy()):
    seq = sequence(single_plate_13(study.side), study.levels)
    rows, charges = [], {}
    for level, panels in seq:
        n = len(panels)
        if n <= study.exact_limit:
            q, P = solve_charges(panels, np.full(n, study.voltage), study.eps0)
            C = float(q.sum() / study.voltage)
            cond = float(np.linalg.cond(P))
            charges[level] = q
        else:
            C = extrapolate(rows, n)
            cond = None
        rows.append({"level": level, "panels": n, "capacitance_F": C, "condition_number": cond})
    return rows, seq, charges

def parallel_plate_refinement(study=BEMStudy()):
    seq = sequence(parallel_plates_13(study.side), study.levels)
    rows = []
    for level, panels in seq:
        n = len(panels)
        if n <= study.exact_limit:
            V = conductor_potentials(panels, {0: 0.0, 1: study.voltage})
            q, P = solve_charges(panels, V, study.eps0)
            xyz, area, cond = arrays(panels)
            Qtop = float(q[cond == 1].sum())
            C = Qtop / study.voltage
            matrix_cond = float(np.linalg.cond(P))
        else:
            C = extrapolate(rows, n)
            matrix_cond = None
        rows.append({"level": level, "panels": n, "capacitance_F": C, "condition_number": matrix_cond})
    return rows, seq

def charge_density_by_x(panels, q):
    xyz, area, cond = arrays(panels)
    sigma = q / area
    x = xyz[:, 0]
    ux = np.unique(np.round(x, 10))
    mean_sigma = np.array([np.mean(sigma[np.isclose(x, u)]) for u in ux])
    return ux, mean_sigma
