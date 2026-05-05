import time
import numpy as np
from scipy.sparse.linalg import spsolve, cg
from .config import Domain, BoundaryCase
from .fdm_matrix import assemble, reconstruct
from .fdm_solver import electrostatic_energy

def direct_solve(domain, case):
    x, y, A, b = assemble(domain, case)
    t0 = time.perf_counter()
    v = spsolve(A, b)
    elapsed = time.perf_counter() - t0
    V = reconstruct(v, domain, case, x, y)
    residual = float(np.linalg.norm(A @ v - b) / np.linalg.norm(b))
    return {
        "method": "direct",
        "n": int(domain.nx),
        "unknowns": int(A.shape[0]),
        "nonzeros": int(A.nnz),
        "time_s": float(elapsed),
        "residual": residual,
        "energy_J_per_m": float(electrostatic_energy(x, y, V)),
    }

def cg_solve(domain, case, rtol=1e-8, maxiter=3000):
    x, y, A, b = assemble(domain, case)
    Ap = -A
    bp = -b
    t0 = time.perf_counter()
    v, info = cg(Ap, bp, rtol=rtol, maxiter=maxiter)
    elapsed = time.perf_counter() - t0
    V = reconstruct(v, domain, case, x, y)
    residual = float(np.linalg.norm(A @ v - b) / np.linalg.norm(b))
    return {
        "method": "cg",
        "n": int(domain.nx),
        "unknowns": int(A.shape[0]),
        "nonzeros": int(A.nnz),
        "time_s": float(elapsed),
        "residual": residual,
        "info": int(info),
        "energy_J_per_m": float(electrostatic_energy(x, y, V)),
    }

def solver_scaling(sizes=(28, 36, 48, 64, 80)):
    case = BoundaryCase("top_drive", top=100.0)
    rows = []
    for n in sizes:
        domain = Domain(int(n), int(n))
        rows.append(direct_solve(domain, case))
        rows.append(cg_solve(domain, case))
    return rows
