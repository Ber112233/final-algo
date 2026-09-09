"""Command-line entry point for experiments, analysis, and figures."""

import argparse
from pathlib import Path

from analysis.plots import generate_plots
from analysis.summarize_results import summarize_results
from experiments.collision_experiment import run_collision_experiment
from experiments.configurations import INITIAL_CAPACITY, INSTANCE_SIZES, REPETITIONS
from experiments.run_experiments import run_matrix
from experiments.threshold_experiment import run_threshold_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dynamic Hash Table Research")
    subparsers = parser.add_subparsers(dest="command", required=True)

    experiment = subparsers.add_parser("experiment", help="run the main matrix")
    experiment.add_argument("--repetitions", type=int, default=REPETITIONS)
    experiment.add_argument("--seed", type=int, default=42)
    experiment.add_argument("--max-n", type=int, default=max(INSTANCE_SIZES))
    experiment.add_argument("--input", choices=["random", "sequential", "clustered"], default="random")
    experiment.add_argument("--initial-capacity", type=int, default=INITIAL_CAPACITY)
    experiment.add_argument("--no-tracemalloc", action="store_true", help="disable physical peak measurement")
    experiment.add_argument("--overwrite", action="store_true")

    analyze = subparsers.add_parser("analyze", help="summarize raw results")
    analyze.add_argument("--input", type=Path, default=Path("data/raw/results.csv"))
    analyze.add_argument("--output", type=Path, default=Path("data/processed/summary.csv"))

    plot = subparsers.add_parser("plot", help="generate all figures")
    plot.add_argument("--input", type=Path, default=Path("data/raw/results.csv"))
    plot.add_argument("--figures-dir", type=Path, default=Path("figuras/final"))
    plot.add_argument("--resizes", type=Path, default=Path("data/raw/resize_events.csv"))

    threshold = subparsers.add_parser("threshold-experiment", help="observe a resize cost peak")
    threshold.add_argument("--seed", type=int, default=42)
    threshold.add_argument("--overwrite", action="store_true")

    collision = subparsers.add_parser("collision-experiment", help="measure collisions by load factor")
    collision.add_argument("--repetitions", type=int, default=REPETITIONS)
    collision.add_argument("--seed", type=int, default=42)
    collision.add_argument("--overwrite", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    print("Dynamic Hash Table Research")
    if args.command == "experiment":
        if args.repetitions <= 0:
            raise ValueError("repetitions must be positive")
        sizes = [size for size in INSTANCE_SIZES if size <= args.max_n]
        if not sizes:
            raise ValueError(f"max-n must be at least {min(INSTANCE_SIZES)}")
        run_matrix(
            sizes,
            args.repetitions,
            args.seed,
            args.input,
            overwrite=args.overwrite,
            initial_capacity=args.initial_capacity,
            trace_memory=not args.no_tracemalloc,
        )
        print("\nCompleted.\nResults saved to data/raw/results.csv")
    elif args.command == "analyze":
        summarize_results(args.input, args.output)
        print(f"Summary saved to {args.output}")
    elif args.command == "plot":
        created = generate_plots(args.input, args.figures_dir, args.resizes)
        print(f"Generated {len(created)} figures in {args.figures_dir}")
    elif args.command == "threshold-experiment":
        run_threshold_experiment(seed=args.seed, overwrite=args.overwrite)
        print("Results saved to data/raw/threshold_experiment.csv")
    elif args.command == "collision-experiment":
        if args.repetitions <= 0:
            raise ValueError("repetitions must be positive")
        run_collision_experiment(
            repetitions=args.repetitions, base_seed=args.seed, overwrite=args.overwrite
        )
        print("Results saved to data/raw/collision_experiment.csv")


if __name__ == "__main__":
    main()
