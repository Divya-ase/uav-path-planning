import numpy as np
import matplotlib.pyplot as plt

# Grid size
GRID_SIZE = 100

# Start and Goal
start = (5, 50)
goal = (95, 50)

# Obstacle (circle)
obstacle_center = (50, 50)
obstacle_radius = 10

# Create grid (0 = free, 1 = obstacle)
grid = np.zeros((GRID_SIZE, GRID_SIZE))

# Mark obstacle
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        if (x - obstacle_center[0])**2 + (y - obstacle_center[1])**2 <= obstacle_radius**2:
            grid[x][y] = 1

# Visualization function
def plot_map():
    plt.imshow(grid.T, origin='lower', cmap='gray')
    plt.scatter(start[0], start[1], color='green', label='Start')
    plt.scatter(goal[0], goal[1], color='red', label='Goal')
    
    # Draw obstacle boundary (optional but looks good)
    circle = plt.Circle(obstacle_center, obstacle_radius, color='blue', fill=False)
    plt.gca().add_patch(circle)

    plt.title("2D Map with Obstacle")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()

# Run to check
if __name__ == "__main__":
    plot_map()
