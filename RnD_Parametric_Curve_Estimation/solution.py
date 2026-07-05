import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize


def model(theta_deg: float, M: float, X: float, t: np.ndarray):
    theta = np.deg2rad(theta_deg)
    abs_t = np.abs(t)
    exp_term = np.exp(M * abs_t)
    x = t * np.cos(theta) - exp_term * np.sin(0.3 * t) * np.sin(theta) + X
    y = 42 + t * np.sin(theta) + exp_term * np.sin(0.3 * t) * np.cos(theta)
    return x, y


def mean_l1_nearest(theta_deg: float, M: float, X: float, x_obs: np.ndarray, y_obs: np.ndarray, t_samples: np.ndarray):
    x_curve, y_curve = model(theta_deg, M, X, t_samples)

    curve = np.column_stack([x_curve, y_curve])
    obs = np.column_stack([x_obs, y_obs])

    # For each observed point, match to the closest curve point by Euclidean distance.
    # Then compute L1 distance in coordinates to that matched point.
    d2 = (
        (obs[:, 0][:, None] - curve[:, 0][None, :]) ** 2
        + (obs[:, 1][:, None] - curve[:, 1][None, :]) ** 2
    )
    idx = np.argmin(d2, axis=1)

    x_m = curve[idx, 0]
    y_m = curve[idx, 1]

    l1 = np.abs(x_m - x_obs) + np.abs(y_m - y_obs)
    return float(np.mean(l1))


def main():
    # Use paths relative to this script so execution works from any working directory.
    import os

    project_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(project_dir, "xy_data.csv")
    df = pd.read_csv(csv_path)


    if not {"x", "y"}.issubset(df.columns):
        raise ValueError("CSV must contain columns named 'x' and 'y'.")

    x_obs = df["x"].to_numpy(dtype=float)
    y_obs = df["y"].to_numpy(dtype=float)

    theta_bounds = (0.0, 50.0)
    M_bounds = (-0.05, 0.05)
    X_bounds = (0.0, 100.0)

    t_samples = np.linspace(6.0, 60.0, 1500, dtype=float)

    theta_grid = np.linspace(theta_bounds[0], theta_bounds[1], 25)
    M_grid = np.linspace(M_bounds[0], M_bounds[1], 17)


    def score_for_params(theta_deg: float, M: float, X: float) -> float:
        return mean_l1_nearest(theta_deg, M, X, x_obs, y_obs, t_samples)

    best_params = None
    best_score = np.inf

    def best_X_l1_nearest(theta_deg: float, M: float):
        # x(t) shifts by +X, so for any fixed (theta,M), matching is still nearest-point based.
        # We approximate X by searching a small set of candidate values.
        candidates = np.linspace(X_bounds[0], X_bounds[1], 61)
        best_x = None
        best_s = np.inf
        for Xc in candidates:
            s = score_for_params(theta_deg, M, float(Xc))
            if s < best_s:
                best_s = s
                best_x = float(Xc)
        return best_x

    for theta_deg in theta_grid:
        for M in M_grid:
            X0 = best_X_l1_nearest(theta_deg, M)
            s = score_for_params(theta_deg, M, X0)
            if s < best_score:
                best_score = s
                best_params = np.array([theta_deg, M, X0], dtype=float)

    def objective(params):
        theta_deg, M, X = params
        if not (theta_bounds[0] <= theta_deg <= theta_bounds[1]):
            return 1e6
        if not (M_bounds[0] <= M <= M_bounds[1]):
            return 1e6
        if not (X_bounds[0] <= X <= X_bounds[1]):
            return 1e6
        return score_for_params(theta_deg, M, X)

    theta0, M0, X0 = best_params
    x_opt = minimize(
        objective,
        x0=np.array([theta0, M0, X0], dtype=float),
        method="Powell",
        options={"maxiter": 3000, "disp": False},
    )

    theta_opt, M_opt, X_opt = x_opt.x

    final_mean_l1 = score_for_params(theta_opt, M_opt, X_opt)

    print("Estimated parameters")
    print(f"theta (deg): {theta_opt:.6f}")
    print(f"M        : {M_opt:.6f}")
    print(f"X        : {X_opt:.6f}")
    print(f"mean L1  : {final_mean_l1:.6f}")

    x_curve, y_curve = model(theta_opt, M_opt, X_opt, t_samples)

    plt.figure(figsize=(7, 6))
    plt.scatter(x_obs, y_obs, s=18, label="CSV points")
    plt.plot(x_curve, y_curve, linewidth=2.0, label="Fitted curve")
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("output_plot.png", dpi=200)

    plt.figure(figsize=(7, 6))
    plt.plot(t_samples, x_curve, "-", linewidth=2, label="x fitted")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("estimated_curve.png", dpi=200)

    theta_str = f"{theta_opt:.6f}°"
    M_str = f"{M_opt:.6f}"
    X_str = f"{X_opt:.6f}"

    print("\nEquation (copy-friendly):")
    print(
        "x(t) = t*cos(" + theta_str + ") - exp(" + M_str + "*|t|)*sin(0.3*t)*sin(" + theta_str + ") + " + X_str
        )

    print(
        "y(t) = 42 + t*sin(" + theta_str + ") + exp(" + M_str + "*|t|)*sin(0.3*t)*cos(" + theta_str + ")"
    )



if __name__ == "__main__":
    main()

