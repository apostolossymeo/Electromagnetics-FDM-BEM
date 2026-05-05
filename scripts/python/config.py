from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Domain:
    nx: int
    ny: int
    lx: float = 4.0
    ly: float = 4.0

@dataclass(frozen=True)
class BoundaryCase:
    name: str
    top: float = 100.0
    bottom: float = 0.0
    left: float = 0.0
    right: float = 0.0

@dataclass(frozen=True)
class FDMStudy:
    sizes: tuple = (24, 32, 48, 64, 88, 112)
    reference_n: int = 100
    series_terms: int = 401

@dataclass(frozen=True)
class BEMStudy:
    side: float = 1.0
    initial_panels: int = 13
    levels: int = 5
    exact_limit: int = 208
    voltage: float = 1.0
    eps0: float = 8.8541878128e-12

@dataclass(frozen=True)
class Paths:
    figures: Path = Path("figures")
    results: Path = Path("results")
