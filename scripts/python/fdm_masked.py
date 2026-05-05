import numpy as np
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve

def l_shape_mask(nx, ny):
    mask = np.ones((nx, ny), dtype=bool)
    mask[nx//2:, ny//2:] = False
    return mask

def solve_l_shape(nx=120, ny=120, lx=4.0, ly=4.0, v_top=100.0):
    x = np.linspace(0.0, lx, nx)
    y = np.linspace(0.0, ly, ny)
    hx = x[1] - x[0]
    hy = y[1] - y[0]
    mask = l_shape_mask(nx, ny)

    unknown = np.zeros((nx, ny), dtype=bool)
    unknown[1:-1, 1:-1] = mask[1:-1, 1:-1]

    index = -np.ones((nx, ny), dtype=int)
    pts = np.argwhere(unknown)
    for k, (i, j) in enumerate(pts):
        index[i, j] = k

    A = lil_matrix((len(pts), len(pts)), dtype=float)
    b = np.zeros(len(pts), dtype=float)
    V = np.full((nx, ny), np.nan)
    V[mask] = 0.0

    def boundary_value(i, j):
        if not mask[i, j]:
            return 0.0
        if j == ny - 1:
            return v_top
        return 0.0

    cx = 1.0 / hx**2
    cy = 1.0 / hy**2
    cc = -2.0 * (cx + cy)

    for row, (i, j) in enumerate(pts):
        A[row, row] = cc
        for di, dj, coeff in [(-1,0,cx), (1,0,cx), (0,-1,cy), (0,1,cy)]:
            ii, jj = i + di, j + dj
            if 0 <= ii < nx and 0 <= jj < ny and unknown[ii, jj]:
                A[row, index[ii, jj]] = coeff
            else:
                b[row] -= coeff * boundary_value(ii, jj)

    A = csr_matrix(A)
    v = spsolve(A, b)
    for val, (i, j) in zip(v, pts):
        V[i, j] = val

    for i in range(nx):
        for j in range(ny):
            if mask[i, j] and not unknown[i, j]:
                V[i, j] = boundary_value(i, j)

    residual = float(np.linalg.norm(A @ v - b) / np.linalg.norm(b))
    return {"x": x, "y": y, "V": V, "mask": mask, "A": A, "b": b, "v": v, "residual": residual}
