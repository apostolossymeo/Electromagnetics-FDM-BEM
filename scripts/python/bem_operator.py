import numpy as np
from .bem_geometry import arrays

def influence_matrix(panels, eps0):
    xyz, area, cond = arrays(panels)
    diff = xyz[:, None, :] - xyz[None, :, :]
    R = np.linalg.norm(diff, axis=2)
    k = 1.0 / (4.0 * np.pi * eps0)
    P = k / np.maximum(R, 1e-30)
    radius = np.sqrt(area / np.pi)
    np.fill_diagonal(P, k * 4.0 / radius)
    return P

def solve_charges(panels, potentials, eps0):
    P = influence_matrix(panels, eps0)
    q = np.linalg.solve(P, potentials)
    return q, P

def conductor_potentials(panels, values):
    _, _, cond = arrays(panels)
    return np.array([values[int(c)] for c in cond], dtype=float)
