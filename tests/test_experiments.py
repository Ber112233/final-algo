import csv
from pathlib import Path

import pytest

from experiments.run_experiments import run_experiment, run_matrix
from experiments.collision_experiment import run_collision_experiment
from experiments.threshold_experiment import run_threshold_experiment
from analysis.plots import generate_plots
from analysis.summarize_results import summarize_results


def test_run_experiment_produces_coherent_result() -> None:
    result = run_experiment(list(range(100)), 2.0, 0.75, 42, 1, "sequential")
    assert result.n == result.final_size == 100
    assert result.final_load_factor == pytest.approx(result.final_size / result.final_capacity)
    assert result.total_operation_cost == result.insert_cost + result.rehash_cost
    assert result.amortized_cost == pytest.approx(result.total_operation_cost / result.n)


def test_small_matrix_writes_nine_comparable_rows(tmp_path: Path) -> None:
    output = tmp_path / "results.csv"
    results = run_matrix([30], 1, 7, "random", output, overwrite=False)
    assert len(results) == 9
    assert len({(result.seed, result.n, result.input_type) for result in results}) == 1
    with output.open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))
    assert len(rows) == 9
    with pytest.raises(FileExistsError):
        run_matrix([10], 1, 7, "random", output, overwrite=False)


def test_threshold_experiment_exposes_one_resize_peak(tmp_path: Path) -> None:
    rows = run_threshold_experiment(
        initial_capacity=20,
        load_threshold=0.5,
        window=3,
        output_path=tmp_path / "threshold.csv",
    )
    resize_rows = [row for row in rows if row["resize_occurred"]]
    assert len(resize_rows) == 1
    assert resize_rows[0]["individual_operation_cost"] > 3


def test_collision_experiment_keeps_capacity_fixed(tmp_path: Path) -> None:
    rows = run_collision_experiment(
        capacity=100,
        repetitions=2,
        load_factors=[0.1, 0.5, 0.9],
        output_path=tmp_path / "collisions.csv",
    )
    assert len(rows) == 6
    assert all(0 <= row["collisions_per_operation"] <= 1 for row in rows)


def test_summary_and_ten_main_plots(tmp_path: Path) -> None:
    raw = tmp_path / "results.csv"
    run_matrix([20, 40], 2, 11, "random", raw)
    summary = summarize_results(raw, tmp_path / "summary.csv")
    assert len(summary) == 18
    assert "amortized_cost_mean" in summary.columns
    created = generate_plots(raw, tmp_path / "figures")
    assert len(created) == 10
    assert all(path.stat().st_size > 0 for path in created)
