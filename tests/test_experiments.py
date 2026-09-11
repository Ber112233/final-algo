import csv
from pathlib import Path
import pytest

from analysis.plots import generate_plots
from analysis.summarize_results import summarize_results
from experiments.collision_experiment import run_collision_experiment
from experiments.run_experiments import run_experiment, run_matrix
from experiments.threshold_experiment import run_threshold_experiment


def test_run_experiment_produces_protocol_metrics() -> None:
    result, events = run_experiment(list(range(100)), 2, .75, 42, 1, "sequential", trace_memory=False)
    assert result.n == result.final_size == 100
    assert result.moved_entries > 0
    assert result.pair_collisions >= 0
    assert result.bucket_slots_peak >= result.final_capacity
    assert events


def test_small_matrix_writes_twenty_blocked_rows(tmp_path: Path) -> None:
    raw, resizes = tmp_path / "results.csv", tmp_path / "resizes.csv"
    results = run_matrix([30], 1, 7, "random", raw, resize_output_path=resizes, trace_memory=False)
    assert len(results) == 20
    assert len({(r.key_seed, r.order_seed, r.hash_seed) for r in results}) == 1
    assert raw.exists() and resizes.exists()
    with pytest.raises(FileExistsError):
        run_matrix([30], 1, 7, "random", raw, resize_output_path=resizes, trace_memory=False)


def test_specialized_experiments(tmp_path: Path) -> None:
    threshold = run_threshold_experiment(initial_capacity=20, load_threshold=.5, window=3,
                                         output_path=tmp_path / "threshold.csv")
    assert len([row for row in threshold if row["resize_occurred"]]) == 1
    collisions = run_collision_experiment(capacity=100, repetitions=2,
                                          load_factors=[.1, .5, .9], output_path=tmp_path / "collisions.csv")
    assert len(collisions) == 6
    assert all(row["pair_collisions"] >= 0 for row in collisions)


def test_summary_and_eight_protocol_plots(tmp_path: Path) -> None:
    raw, resizes = tmp_path / "results.csv", tmp_path / "resizes.csv"
    run_matrix([20, 40], 2, 11, "random", raw, resize_output_path=resizes, trace_memory=False)
    summary = summarize_results(raw, tmp_path / "summary.csv")
    assert len(summary) == 40
    assert "migrations_per_insertion_ci95_low" in summary.columns
    created = generate_plots(raw, tmp_path / "figures", resizes)
    assert len(created) == 8
    assert all(path.stat().st_size > 0 for path in created)
