# Parametric Curve Parameter Estimation

## Overview

This project estimates the unknown parameters **θ (Theta)**, **M**, and **X** of a given parametric curve using numerical optimization techniques. The objective is to determine the parameter values that best fit the provided dataset (`xy_data.csv`) while minimizing the L1 distance between the observed data points and the generated curve.

---

# Problem Statement

The given parametric curve is defined as

\[
x(t)=t\cos(\theta)-e^{M|t|}\sin(0.3t)\sin(\theta)+X
\]

\[
y(t)=42+t\sin(\theta)+e^{M|t|}\sin(0.3t)\cos(\theta)
\]

where

- **θ** = Rotation angle
- **M** = Exponential scaling parameter
- **X** = Horizontal translation

The parameter constraints are

| Parameter | Range |
|-----------|----------------|
| θ | 0° < θ < 50° |
| M | -0.05 < M < 0.05 |
| X | 0 < X < 100 |
| t | 6 ≤ t ≤ 60 |

The objective is to estimate the values of **θ**, **M**, and **X** using the provided dataset.

---

# Methodology

Since only three unknown parameters need to be estimated, this problem is formulated as a **numerical parameter estimation** problem rather than a machine learning problem.

The following steps are performed:

1. Load the dataset (`xy_data.csv`).
2. Generate a dense parametric curve over the interval **6 ≤ t ≤ 60**.
3. Compute the Mean L1 distance between the observed points and the nearest generated curve points.
4. Perform a coarse Grid Search to obtain a suitable initial estimate.
5. Refine the parameters using numerical optimization.
6. Generate plots for visual verification.

---

# Objective Function

The optimization minimizes the Mean L1 Distance

\[
L_1=\frac{1}{N}\sum_{i=1}^{N}\left(|x_i-\hat{x}_i|+|y_i-\hat{y}_i|\right)
\]

where each observed point is matched to its nearest generated curve point.

Since the dataset does not contain explicit values of **t**, nearest-point matching is used throughout the optimization process.

---

# Estimated Parameters

| Parameter | Estimated Value |
|-----------|-----------------:|
| **θ** | **29.999535°** |
| **M** | **0.030001** |
| **X** | **54.998681** |

---

# Final Parametric Equation

### x(t)

```text
x(t)=t*cos(29.999535°)-exp(0.030001|t|)*sin(0.3t)*sin(29.999535°)+54.998681
```

### y(t)

```text
y(t)=42+t*sin(29.999535°)+exp(0.030001|t|)*sin(0.3t)*cos(29.999535°)
```

---

# Repository Structure

```
RnD_Parametric_Curve_Estimation/
│
├── solution.py
├── xy_data.csv
├── requirements.txt
├── README.md
├── RESULTS.md
├── output_plot.png
├── estimated_curve.png
└── .gitignore
```

---

# Output Files

Running the project generates

- **output_plot.png** — Original dataset with fitted parametric curve
- **estimated_curve.png** — Generated curve visualization

The estimated parameters and optimization statistics are also written to **RESULTS.md**.

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/RnD_Parametric_Curve_Estimation.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the project

```bash
python solution.py
```

---

# Results

Estimated Parameters

```
Theta (deg) : 29.999535
M           : 0.030001
X           : 54.998681
```

The optimization successfully estimates the unknown parameters and generates a parametric curve that closely follows the provided dataset.

---

# Technologies Used

- Python
- NumPy
- Pandas
- SciPy
- Matplotlib

---

# Conclusion

This project demonstrates a numerical optimization approach for estimating unknown parameters of a parametric curve. By combining coarse parameter search with optimization and nearest-point matching, the generated curve closely approximates the observed data while satisfying the given parameter constraints.
