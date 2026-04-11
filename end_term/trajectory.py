import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from path_planner import astar
from map_setup import start, goal

# Generate smooth trajectory
def generate_trajectory(path, speed_factor=1.0):
    path = np.array(path)
    
    # parameter (t)
    t = np.linspace(0, 1, len(path))
    
    # spline for x and y
    cs_x = CubicSpline(t, path[:, 0])
    cs_y = CubicSpline(t, path[:, 1])
    
    # finer time steps
    t_fine = np.linspace(0, 1, int(200 * speed_factor))
    
    x_smooth = cs_x(t_fine)
    y_smooth = cs_y(t_fine)
    
    return x_smooth, y_smooth, t_fine

# Compare trajectories
def plot_trajectories(path):
    # minimum-time (faster → more aggressive)
    x_fast, y_fast, t_fast = generate_trajectory(path, speed_factor=1.0)
    
    # minimum-energy (slower → smoother)
    x_slow, y_slow, t_slow = generate_trajectory(path, speed_factor=0.5)
    
    plt.plot(x_fast, y_fast, label="Min-Time", color='red')
    plt.plot(x_slow, y_slow, label="Min-Energy", color='blue')
    
    plt.title("Trajectory Comparison")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()

# Run test
if __name__ == "__main__":
    path = astar(start, goal)
    plot_trajectories(path)
