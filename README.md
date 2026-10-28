# Active Debris Removal: Preliminary Mission Simulation

Academic Python project exploring a **simplified active-debris-removal mission**: a service spacecraft visits a selected set of orbital debris objects, evaluates candidate rendezvous maneuvers, estimates maneuver cost and mission time, and explores the effect of visit order on total delta-v.

The project is a *preliminary/pseudo-propagation model*, not a high-fidelity orbit propagator, mission-validated optimizer or flight-dynamics tool.

## What the model contains

- A selected debris dataset in `input/Debris_excel.tsv`, prepared from orbital-object information for the original academic scenario.
- `Debris.py`, `Spacecraft.py` and `Thrusters.py` for object and propulsion models.
- `rendezvouz_manouver.py` for numerical phase/radius matching under simplifying assumptions.
- `decayment_manouvers.py` for disposal/deorbit estimates.
- `main.py` for the sequence of maneuvers and a final mission summary.
- `Iterator.py` and `Optimizer.py` for experimental random-order evaluation and minimum-delta-v selection.
- `other/` for exploratory orbit and maneuver scripts.

## Recreate the environment

Use **Python 3.10** in a clean virtual environment. In particular, the pinned `poliastro==0.17.0` supports Python 3.8–3.10 and is not compatible with Python 3.12.

```bash
python -m pip install -r requirements.txt
python main.py
```

Run these commands **from the repository root**. The project uses paths relative to the working directory. The first run also converts `input/Debris_excel.tsv` into an intermediate `input/Debris_excel.csv`; this generated file is deliberately not committed. Log files are created in `output/`, a directory kept in Git through `.gitkeep`.

On Windows, use a Python 3.10 virtual environment and invoke its `python` executable. Installation of the historical dependency pins has not been reverified on a new Windows machine.

### Experimental visit-order search

The original experimental workflow uses settings in `input/INPUTS.py`:

1. Set `ITERATIONS_PROGRAM = True` and `TOTAL_LOG = False`.
2. Choose `PROGRAM_ITERATIONS`.
3. Execute `python Iterator.py` to run randomized visits.
4. Execute `python Optimizer.py` to inspect the saved delta-v values.

The iterator/optimizer has known robustness limitations (including truncated parsing of stored numerical values). It should not be treated as a production-quality optimization algorithm.

## Data, outputs and accompanying material

- `input/Debris_excel.tsv` is the small, manually selected source dataset used by the scripts.
- `examples/` contains **historical illustrative text output**, not verified reference results.
- `docs/Spaceflight_presentation.pdf` is an accompanying academic presentation from the supplied project archive.
- Large per-object `rendezvous_*.csv` trajectory logs have been **excluded** from this public-facing source bundle. They remain in the original ZIP provided for review.

## Important modeling caveats

This is academic exploratory code. The source has not been numerically validated in this cleanup. In particular, a code inspection identified candidate issues to investigate before making quantitative performance claims:

- Some maneuver-duration calculations combine delta-v in **km/s** with acceleration in **m/s²** without a conversion factor (`Spacecraft.py`).
- Some orbital-phase update logic appears to combine **radians and degrees** (`Spacecraft.py`, `Debris.py`).
- The inclination-change expression in `Spacecraft.py` applies an extra factor of π to an angle already converted to radians.
- `Optimizer.py` reads only the first five characters of each saved delta-v value.
- Additional numerical assumptions and integration/termination behavior need independent verification.

Therefore **do not interpret the logged delta-v, propellant or mission-duration values as validated mission results** without correcting and testing the underlying physics.

## External work

The original supplied archive also contained a separate full copy of [Alfonso González's *Astrodynamics with Python* (AWP)](https://github.com/alfonsogonzalez/AWP). It is omitted from this repository because it is a distinct third-party codebase. The retained project uses packages such as `poliastro` and `astropy`, which are installed as dependencies rather than vendored in this repository.

## Historical project status

The original project code has been preserved here, with only distribution-related exclusions and documentation. There is no claim of flight suitability or numerical certification. Python files passed a syntax-compilation check, but a full end-to-end execution in the historical Python 3.10 dependency environment has **not** been performed as part of this cleanup.
