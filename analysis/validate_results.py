"""Fail fast when the final CSV does not implement the frozen factorial."""

from pathlib import Path
import pandas as pd


def validate(path: Path = Path("data/raw/results.csv"), repetitions: int = 30) -> None:
    data = pd.read_csv(path)
    expected_rows = 5 * 4 * 3 * repetitions
    if len(data) != expected_rows:
        raise AssertionError(f"expected {expected_rows} rows, found {len(data)}")
    if data["run_id"].duplicated().any():
        raise AssertionError("duplicated run_id")
    counts = data.groupby(["n", "gamma_nominal", "tau", "key_family"]).size()
    if not (counts == repetitions).all():
        raise AssertionError("unbalanced factorial")
    for _, block in data.groupby(["n", "repetition", "key_family"]):
        if len(block) != 20:
            raise AssertionError("incomplete treatment block")
        for seed_column in ("key_seed", "order_seed", "hash_seed"):
            if block[seed_column].nunique() != 1:
                raise AssertionError(f"{seed_column} changed inside a block")
    if not (data["final_size"] == data["n"]).all():
        raise AssertionError("final size mismatch")
    if not (data["final_load_factor"] <= data["tau"] + 1e-12).all():
        raise AssertionError("load threshold violation")


if __name__ == "__main__":
    validate()
    print("Final CSV validated successfully")
