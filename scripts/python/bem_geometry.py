from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Panel:
    x: float
    y: float
    z: float
    sx: float
    sy: float
    conductor: int = 0

    @property
    def area(self):
        return self.sx * self.sy

def single_plate_13(side=1.0):
    n = 13
    dx = side / n
    return [Panel(-side/2 + (i + 0.5) * dx, 0.0, 0.0, dx, side, 0) for i in range(n)]

def parallel_plates_13(side=1.0, separation=0.20):
    top = [Panel(p.x, p.y, separation/2, p.sx, p.sy, 1) for p in single_plate_13(side)]
    bottom = [Panel(p.x, p.y, -separation/2, p.sx, p.sy, 0) for p in single_plate_13(side)]
    return top + bottom

def refine_panel(p):
    out = []
    for ax in (-0.25, 0.25):
        for ay in (-0.25, 0.25):
            out.append(Panel(p.x + ax*p.sx, p.y + ay*p.sy, p.z, p.sx/2, p.sy/2, p.conductor))
    return out

def refine_all(panels):
    out = []
    for p in panels:
        out.extend(refine_panel(p))
    return out

def sequence(panels, levels):
    current = list(panels)
    out = []
    for level in range(levels):
        out.append((level, current))
        current = refine_all(current)
    return out

def arrays(panels):
    xyz = np.array([[p.x, p.y, p.z] for p in panels], dtype=float)
    area = np.array([p.area for p in panels], dtype=float)
    cond = np.array([p.conductor for p in panels], dtype=int)
    return xyz, area, cond
