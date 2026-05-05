import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nem_benchmark.plot_fdm import generate as generate_fdm
from nem_benchmark.plot_bem import generate as generate_bem
from nem_benchmark.plot_benchmark import generate as generate_benchmark
from nem_benchmark.plot_research_plus import generate_extra

def main():
    project = Path(__file__).resolve().parents[3]
    figures = project / "figures"
    results = project / "results"
    for sub in ["fdm", "bem", "benchmark"]:
        (figures / sub).mkdir(parents=True, exist_ok=True)
    results.mkdir(exist_ok=True)

    fdm_result, fdm_rows, order, sensitivity_rows = generate_fdm(figures)
    iso_rows, pp_rows, iso_seq = generate_bem(figures)
    generate_benchmark(fdm_rows, iso_rows, pp_rows, figures)
    extra = generate_extra(figures, fdm_rows, {"fdm_order": order})

    summary = {
        "fdm": {
            "reference_unknowns": int(fdm_result["A"].shape[0]),
            "reference_nonzeros": int(fdm_result["A"].nnz),
            "relative_l2_error": float(fdm_result["relative_l2_error"]),
            "residual": float(fdm_result["residual"]),
            "convergence_order": float(order),
            "convergence_table": fdm_rows,
            "boundary_sensitivity": sensitivity_rows,
        },
        "bem": {
            "isolated_plate": iso_rows,
            "parallel_plates": pp_rows,
        },
        "research_plus": extra,
    }
    (results / "summary.json").write_text(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
