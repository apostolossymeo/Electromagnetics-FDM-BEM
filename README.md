# Sparse FDM–BEM/MoM Formulations in Numerical Electromagnetics

## Overview

This repository implements a numerical electromagnetics benchmark for electrostatic field and capacitance modeling. It compares a sparse finite-difference discretization of Laplace’s equation with a boundary-element (Method of Moments) formulation defined on conductor surfaces.

The objective is to examine how domain-based and boundary-based approaches behave under refinement. The finite-difference model is assembled as a global sparse system and validated against an analytical reference, while the boundary-element model resolves conductor charge through recursive panel refinement.

The comparison is carried out in terms of accuracy, conditioning, and computational structure. In particular, the contrast between sparse domain operators and dense boundary operators is treated as a central aspect of the analysis.

## Scope
The benchmark includes:

- sparse finite-difference matrix assembly for Laplace boundary-value problems;
- analytical validation for a canonical rectangular electrostatic problem;
- grid-convergence analysis;
- boundary-condition sensitivity;
- direct sparse solve versus conjugate-gradient solve comparison;
- masked-domain FDM for a non-rectangular L-shaped geometry;
- panel-based MoM/BEM capacitance extraction;
- isolated-plate and parallel-plate capacitance studies;
- recursive panel refinement from \(13\) to \(3328\) panels;
- edge charge-density concentration under refinement;
- influence-matrix conditioning;
- sparse FDM versus dense BEM storage growth.

The benchmark remains electrostatic. It does not attempt full-wave electromagnetics.

## Results

| Figure | Interpretation |
|--------|----------------|
| Fig. 1 | Sparse finite-difference operator and local stencil connectivity. |
| Fig. 2 | Potential contours and electric field lines from the FDM solution. |
| Fig. 3 | FDM validation against the analytical series solution and interior error distribution. |
| Fig. 4 | FDM grid convergence and sparse matrix growth. |
| Fig. 5 | Boundary-condition sensitivity across four electrostatic cases. |
| Fig. 6 | L-shaped masked-domain FDM problem and corresponding sparse operator. |
| Fig. 7 | Recursive BEM/MoM panel refinement. |
| Fig. 8 | Capacitance convergence and influence-matrix conditioning. |
| Fig. 9 | Charge-density concentration near conductor edges. |
| Fig. 10 | Sparse FDM versus dense BEM storage growth. |
| Fig. 11 | Direct sparse solve versus conjugate-gradient solve cost and residual. |
| Fig. 12 | Accuracy proxy under FDM grid refinement and BEM panel refinement. |
| Fig. 13 | Summary of benchmark observations. |


## Conclusion
The benchmark shows the expected tradeoff: sparse FDM is natural for full-field solutions and scales through sparse operators, while BEM/MoM focuses computation on conductor boundaries but produces dense systems whose conditioning and storage cost grow rapidly under refinement. The strongest use of the two methods depends on whether the target quantity is the field in a region or the conductor response itself.
