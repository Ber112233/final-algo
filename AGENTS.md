# Repository Guidelines

## Project Structure & Module Organization

Core Python code lives in `src/`: the dynamic hash table, universal hashing, generators, metrics, and the linear-probing comparison. Experimental orchestration belongs in `experiments/`, while summaries, validation, LaTeX exports, and plots belong in `analysis/`. Add tests under `tests/` using the same module boundaries.

Treat `data/raw/` as reproducible observations and `data/processed/` as derived output. Final charts are in `figuras/final/`; pilot and legacy results remain separate for traceability. The article source is `main.tex`; bibliography, appendices, and individual journals are in `referencias.bib`, `anexos/`, and `bitacoras/`. Compiled submission PDFs are copied to `output/pdf/`.

## Build, Test, and Development Commands

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python analysis/validate_results.py
powershell -File scripts/reproduce.ps1
powershell -File scripts/compile_documents.ps1
```

The first command installs `pandas`, `matplotlib`, and `pytest`. Run tests before experiments. The validator checks the final CSV schema and factorial coverage. `reproduce.ps1` regenerates tests, data, summaries, and figures; it can be expensive. `compile_documents.ps1` builds the article and all four journals. For a quick run, use `python main.py experiment --repetitions 5 --max-n 10000 --overwrite`.

## Coding Style & Naming Conventions

Use four-space indentation and standard Python conventions: `snake_case` for functions, variables, and modules; `PascalCase` for classes; uppercase names for constants. Keep experiment configuration explicit and preserve separate key, order, and hash seeds. Do not merge distinct metrics such as `insert_collision_events`, `pair_collisions`, and probing counts. No formatter is enforced, so keep imports organized and changes PEP 8-compatible.

## Testing Guidelines

Pytest is the test framework. Name files `test_<module>.py` and tests `test_<behavior>`. Cover invariants, boundary loads, duplicate keys, rehash conservation, seeded reproducibility, and output schemas. Avoid replacing the checked-in final dataset during ordinary unit tests.

## Commit & Pull Request Guidelines

History favors short, descriptive commit subjects, for example `Align article and journals with official templates`. Use an imperative summary and keep one logical change per commit. Pull requests should explain the algorithmic or experimental effect, list commands executed, identify regenerated CSV/PDF/figures, and include screenshots for visible LaTeX or chart changes. Never present planned contributions or unverified AI-generated references as completed work.
