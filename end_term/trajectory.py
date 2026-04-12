import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import os

from path_planner import plan_path

MIN_TIME_SPEED = 5.0
MIN_ENERGY_SPEED = 1.5
DT = 0.1


def smooth_trajectory(waypoints, speed):
    waypoints = np.array(waypoints, dtype=float)
    diffs = np.diff(waypoints, axis=0)
    chord = np.sqrt((diffs ** 2).sum(axis=1))
    s = np.concatenate([[0], np.cumsum(chord)])

    cs_x = CubicSpline(s, waypoints[:, 0])
    cs_y = CubicSpline(s, waypoints[:, 1])

    total_length = s[-1]
    total_time = total_length / speed
    t_samples = np.arange(0, total_time + DT, DT)
    s_samples = (t_samples / total_time) * total_length

    xs = cs_x(s_samples)
    ys = cs_y(s_samples)
    return list(zip(xs.tolist(), ys.tolist(), t_samples.tolist()))


def generate_trajectories(waypoints=None):
    if waypoints is None:
        waypoints = plan_path()
    traj_fast = smooth_trajectory(waypoints, speed=MIN_TIME_SPEED)
    traj_energy = smooth_trajectory(waypoints, speed=MIN_ENERGY_SPEED)
    print(f"Min-time   trajectory: {len(traj_fast)} points, total time ~ {traj_fast[-1][2]:.1f} s")
    print(f"Min-energy trajectory: {len(traj_energy)} points, total time ~ {traj_energy[-1][2]:.1f} s")
    return traj_fast, traj_energy


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    waypoints = plan_path()
    traj_fast, traj_energy = generate_trajectories(waypoints)

    xf, yf, tf = zip(*traj_fast)
    xe, ye, te = zip(*traj_energy)
    wx, wy = zip(*waypoints)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for ax, xs, ys, ts, label, color in [
        (axes[0], xf, yf, tf, "Min-Time", "steelblue"),
        (axes[1], xe, ye, te, "Min-Energy", "darkorange"),
    ]:
        ax.plot(wx, wy, "k--", linewidth=0.8, alpha=0.5, label="Raw waypoints")
        sc = ax.scatter(xs, ys, c=ts, cmap="plasma", s=4, label=label)
        plt.colorbar(sc, ax=ax, label="Time (s)")
        ax.set_title(f"{label} Trajectory")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend(fontsize=8)
        ax.set_aspect("equal")

    plt.tight_layout()
    plt.savefig("results/trajectory_comparison.png", dpi=150)
    plt.show()
    print("Saved -> results/trajectory_comparison.png")
   
    
    
