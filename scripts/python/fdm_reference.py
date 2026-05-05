import numpy as np

def top_plate_series(x, y, lx, ly, v_top, terms):
    X, Y = np.meshgrid(x, y, indexing="ij")
    V = np.zeros_like(X, dtype=float)
    for n in range(1, terms + 1, 2):
        a = n * np.pi / lx
        ratio = np.exp(a * (Y - ly)) * (1.0 - np.exp(-2.0 * a * Y)) / (1.0 - np.exp(-2.0 * a * ly))
        V += (4.0 * v_top / (n * np.pi)) * np.sin(n * np.pi * X / lx) * ratio
    return V

def bilinear_case(x, y, lx, ly, left, right, bottom, top):
    X, Y = np.meshgrid(x, y, indexing="ij")
    sx = X / lx
    sy = Y / ly
    return (1 - sx) * (1 - sy) * bottom + sx * (1 - sy) * bottom + (1 - sx) * sy * top + sx * sy * top
