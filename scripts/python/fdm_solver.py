import numpy as np
from scipy.sparse.linalg import spsolve
from .fdm_matrix import assemble, reconstruct
from .fdm_reference import top_plate_series

def solve(domain, case):
    x, y, A, b = assemble(domain, case)
    v = spsolve(A, b)
    V = reconstruct(v, domain, case, x, y)
    residual = float(np.linalg.norm(A @ v - b) / np.linalg.norm(b))
    return {"x": x, "y": y, "A": A, "b": b, "v": v, "V": V, "residual": residual}

def electric_field(x, y, V):
    dVdx, dVdy = np.gradient(V, x, y, edge_order=2)
    return -dVdx, -dVdy

def electrostatic_energy(x, y, V, eps0=8.8541878128e-12):
    Ex, Ey = electric_field(x, y, V)
    density = 0.5 * eps0 * (Ex**2 + Ey**2)
    return float(np.trapz(np.trapz(density, y, axis=1), x, axis=0))

def validate_top_plate(domain, case, terms):
    r = solve(domain, case)
    ref = top_plate_series(r["x"], r["y"], domain.lx, domain.ly, case.top, terms)
    err = r["V"] - ref
    r["reference"] = ref
    r["error"] = err
    r["relative_l2_error"] = float(np.linalg.norm(err) / np.linalg.norm(ref))
    r["energy"] = electrostatic_energy(r["x"], r["y"], r["V"])
    return r
