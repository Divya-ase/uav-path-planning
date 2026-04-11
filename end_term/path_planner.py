import heapq
import numpy as np
import matplotlib.pyplot as plt
from map_setup import grid, start, goal

# Heuristic (Euclidean distance)
def heuristic(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Get 8-direction neighbors
def get_neighbors(node):
    directions = [(-1,0),(1,0),(0,-1),(0,1),
                  (-1,-1),(-1,1),(1,-1),(1,1)]
    
    neighbors = []
    for dx, dy in directions:
        x = node[0] + dx
        y = node[1] + dy
        
        if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
            if grid[x][y] == 0:  # free space
                neighbors.append((x, y))
    
    return neighbors

# A* Algorithm
def astar(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from = {}
    g_cost = {start: 0}
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        for neighbor in get_neighbors(current):
            new_cost = g_cost[current] + heuristic(current, neighbor)
            
            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                f_cost = new_cost + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_cost, neighbor))
                came_from[neighbor] = current
    
    return None

# Plot path (IMPORTANT for marks)
def plot_path(path):
    plt.imshow(grid.T, origin='lower', cmap='gray')
    
    if path:
        x, y = zip(*path)
        plt.plot(x, y, color='blue', label='Path')
    
    plt.scatter(start[0], start[1], color='green', label='Start')
    plt.scatter(goal[0], goal[1], color='red', label='Goal')
    
    plt.title("Path Planning using A*")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()

# Run test
if __name__ == "__main__":
    path = astar(start, goal)
    print("Path length:", len(path))
    plot_path(path)
