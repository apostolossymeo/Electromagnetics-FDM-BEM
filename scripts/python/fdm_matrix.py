import numpy as np
from scipy.sparse import lil_matrix, csr_matrix

def node_index(i, j, ny):
    return (i - 1) * (ny - 2) + (j - 1)

def constant_boundaries(case):
    return {
        "left": lambda y: case.left,
        "right": lambda y: case.right,
        "bottom": lambda x: case.bottom,
        "top": lambda x: case.top,
    }

def assemble(domain, case):
    nx, ny, lx, ly = domain.nx, domain.ny, domain.lx, domain.ly
    x = np.linspace(0.0, lx, nx)
    y = np.linspace(0.0, ly, ny)
    hx = x[1] - x[0]
    hy = y[1] - y[0]
    mx = nx - 2
    my = ny - 2
    n = mx * my
    A = lil_matrix((n, n), dtype=float)
    b = np.zeros(n, dtype=float)
    bx = constant_boundaries(case)
    ax = 1.0 / hx**2
    ay = 1.0 / hy**2
    ac = -2.0 * (ax + ay)
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            k = node_index(i, j, ny)
            A[k, k] = ac
            if i == 1:
                b[k] -= ax * bx["left"](y[j])
            else:
                A[k, node_index(i - 1, j, ny)] = ax
            if i == nx - 2:
                b[k] -= ax * bx["right"](y[j])
            else:
                A[k, node_index(i + 1, j, ny)] = ax
            if j == 1:
                b[k] -= ay * bx["bottom"](x[i])
            else:
                A[k, node_index(i, j - 1, ny)] = ay
            if j == ny - 2:
                b[k] -= ay * bx["top"](x[i])
            else:
                A[k, node_index(i, j + 1, ny)] = ay
    return x, y, csr_matrix(A), b

def reconstruct(v, domain, case, x, y):
    nx, ny = domain.nx, domain.ny
    V = np.zeros((nx, ny), dtype=float)
    bx = constant_boundaries(case)
    V[0, :] = [bx["left"](yy) for yy in y]
    V[-1, :] = [bx["right"](yy) for yy in y]
    V[:, 0] = [bx["bottom"](xx) for xx in x]
    V[:, -1] = [bx["top"](xx) for xx in x]
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            V[i, j] = v[node_index(i, j, ny)]
    return V
