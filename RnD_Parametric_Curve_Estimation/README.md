# Parametric Curve Parameter Estimation (θ, M, X)

> Numerical parameter estimation for the provided parametric curve model.

## Problem
The assignment defines a parametric curve:

- **x(t)** = t·cos(θ) − e^(M|t|)·sin(0.3t)·sin(θ) + X
- **y(t)** = 42 + t·sin(θ) + e^(M|t|)·sin(0.3t)·cos(θ)

Unknown parameters: **θ**, **M**, **X**.

Input: **`xy_data.csv`** (columns `x`, `y`) containing sampled points that lie on the curve.

Goal: estimate **(θ, M, X)** such that the generated curve best matches the CSV points.

## Method (high level)
Because only three parameters are unknown, the solution is framed as **parameter estimation** (optimization), not ML.

1. Generate curve points for **t ∈ [6, 60]** (dense sampling).
2. Define the objective as the assignment’s **mean L1 distance** between observed points and the nearest generated curve points.
3. Use a **coarse grid search** over **θ** and **M** to obtain a strong starting guess.
4. Refine the estimate with a numerical optimizer.
5. Save plots for visual validation.

### Objective (L1 with nearest-point matching)
For each observed point, the closest generated curve point is selected, then:

- `L1 = mean( |x_pred - x_obs| + |y_pred - y_obs| )`

> Note: the CSV does not include explicit `t` values, so correspondence is done by nearest-point matching.

## Outputs
Running `solution.py` produces:

- `output_plot.png` — CSV scatter + fitted curve
- `estimated_curve.png` — quick comparison of the fitted curve components

Estimated parameters and final error are printed to the console and also documented in `RESULTS.md`.

## Repository structure

- `solution.py` — parameter estimation script
- `xy_data.csv` — input dataset
- `requirements.txt` — dependencies
- `RESULTS.md` — estimated parameters
- `output_plot.png` — visualization
- `estimated_curve.png` — visualization

## How to run
From the repository folder:

```bash
pip install -r requirements.txt
python solution.py
```

The script prints:
- θ (deg)
- M
- X
- mean L1 error

## Notes
- The optimization can take a few seconds depending on your CPU and the CSV size.
- Nearest-point matching is used because `xy_data.csv` does not provide explicit `t` values.


