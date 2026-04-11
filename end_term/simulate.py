import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from formation import Formation
from trajectory import generate_trajectory
from path import PathPlanner
from map import GridMap

import os

os.makedirs("results", exist_ok=True)

grid_map = GridMap()
planner = PathPlanner(grid_map)

start = (0, 0)
goal = (10, 10)

waypoints = planner.plan(start, goal)

offsets = [
    (-2, 0),
    (-1, -1),
    (0, 0),
    (1, -1),
    (2, 0)
]

formation = Formation(offsets)

traj_min_time = generate_trajectory(waypoints, mode="fast")
traj_min_energy = generate_trajectory(waypoints, mode="smooth")

centroid_fast = np.array(traj_min_time)
centroid_smooth = np.array(traj_min_energy)

def get_all_drone_positions(centroid, formation):
    return np.array([formation.get_formation_positions(c) for c in centroid])

fast_positions = get_all_drone_positions(centroid_fast, formation)
smooth_positions = get_all_drone_positions(centroid_smooth, formation)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

ax1, ax2 = axes

ax1.set_title("Min-Time Trajectory")
ax2.set_title("Min-Energy Trajectory")

for ax in axes:
    ax.set_xlim(-5, 15)
    ax.set_ylim(-5, 15)
    ax.grid(True)

scatter1 = ax1.scatter([], [])
scatter2 = ax2.scatter([], [])

def update(frame):
    pts1 = fast_positions[frame]
    scatter1.set_offsets(pts1)

    pts2 = smooth_positions[frame]
    scatter2.set_offsets(pts2)

    return scatter1, scatter2

anim = FuncAnimation(fig, update, frames=len(centroid_fast), interval=100)

gif_path = "results/simulation.gif"
anim.save(gif_path, writer=PillowWriter(fps=10))

plt.figure()

plt.plot(centroid_fast[:, 0], centroid_fast[:, 1], label="Min-Time Path")
plt.plot(centroid_smooth[:, 0], centroid_smooth[:, 1], label="Min-Energy Path")

plt.scatter(start[0], start[1], c="green", label="Start")
plt.scatter(goal[0], goal[1], c="red", label="Goal")

plt.legend()
plt.title("Planned Paths")
plt.grid()

plt.savefig("results/path_comparison.png")

def compute_stats(path):
    dist = np.sum(np.linalg.norm(np.diff(path, axis=0), axis=1))
    time = len(path)
    energy = np.sum(np.linalg.norm(np.diff(path, axis=0), axis=1) ** 2)
    return dist, time, energy

d1, t1, e1 = compute_stats(centroid_fast)
d2, t2, e2 = compute_stats(centroid_smooth)

print("\n===== TRAJECTORY SUMMARY =====")
print("Min-Time:")
print(f"  Distance: {d1:.2f}")
print(f"  Time steps: {t1}")
print(f"  Energy: {e1:.2f}")

print("\nMin-Energy:")
print(f"  Distance: {d2:.2f}")
print(f"  Time steps: {t2}")
print(f"  Energy: {e2:.2f}")

print("\nSaved files:")
print(" - results/simulation.gif")
print(" - results/path_comparison.png")
