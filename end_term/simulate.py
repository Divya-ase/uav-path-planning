import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

from formation import Formation
from trajectory import generate_trajectory
from path import PathPlanner
from map import GridMap

os.makedirs("results", exist_ok=True)

grid_map = GridMap()
planner = PathPlanner(grid_map)

start = (0, 0)
goal = (10, 10)

waypoints = planner.plan(start, goal)

plt.figure()
grid_map.draw()
wx, wy = zip(*waypoints)
plt.plot(wx, wy, marker="o", label="Planned Path")
plt.scatter(start[0], start[1], c="green", label="Start")
plt.scatter(goal[0], goal[1], c="red", label="Goal")
plt.title("Path Planning")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid()
plt.savefig("results/path_plot.png")
plt.close()

offsets = [
    (-2, 0),
    (-1, -1),
    (0, 0),
    (1, -1),
    (2, 0)
]

formation = Formation(offsets)

traj_fast = generate_trajectory(waypoints, mode="fast")
traj_smooth = generate_trajectory(waypoints, mode="smooth")

traj_fast = np.array(traj_fast)
traj_smooth = np.array(traj_smooth)

def compute_speed(path):
    return np.linalg.norm(np.diff(path, axis=0), axis=1)

def compute_acc(speed):
    return np.diff(speed)

speed_fast = compute_speed(traj_fast)
speed_smooth = compute_speed(traj_smooth)

acc_fast = compute_acc(speed_fast)
acc_smooth = compute_acc(speed_smooth)

t_speed = np.arange(len(speed_fast))
t_acc = np.arange(len(acc_fast))

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(t_speed, speed_fast, label="Min-Time")
plt.plot(t_speed, speed_smooth, label="Min-Energy")
plt.title("Speed vs Time")
plt.xlabel("Time Step")
plt.ylabel("Speed")
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(t_acc, acc_fast, label="Min-Time")
plt.plot(t_acc, acc_smooth, label="Min-Energy")
plt.title("Acceleration vs Time")
plt.xlabel("Time Step")
plt.ylabel("Acceleration")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("results/trajectory_comparison.png")
plt.close()

def formation_positions(traj):
    return np.array([formation.get_formation_positions(p) for p in traj])

fast_pos = formation_positions(traj_fast)
smooth_pos = formation_positions(traj_smooth)

fig, ax = plt.subplots()

ax.set_xlim(-5, 15)
ax.set_ylim(-5, 15)
ax.set_title("Formation Flight (Min-Time vs Min-Energy)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid()

scatter = ax.scatter([], [])

text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

mode_flag = {"mode": "fast"}

def update(frame):
    if frame < len(fast_pos):
        pts = fast_pos[frame]
        mode_flag["mode"] = "Min-Time"
    else:
        pts = smooth_pos[frame - len(fast_pos)]
        mode_flag["mode"] = "Min-Energy"

    scatter.set_offsets(pts)
    text.set_text(f"Mode: {mode_flag['mode']}")
    return scatter, text

total_frames = len(fast_pos) + len(smooth_pos)

anim = FuncAnimation(fig, update, frames=total_frames, interval=80)

anim.save("results/formation_animation.gif", writer=PillowWriter(fps=10))

plt.close()

print("\n===== OUTPUT GENERATED =====")
print("results/path_plot.png")
print("results/trajectory_comparison.png")
print("results/formation_animation.gif")


