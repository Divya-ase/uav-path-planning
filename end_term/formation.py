import numpy as np

class Formation:
    def __init__(self, offsets):
        """
        offsets: list of (x, y) tuples for each drone
        Example: [(-2,0), (-1,-1), (0,0), (1,-1), (2,0)]
        """
        self.offsets = np.array(offsets)

    def centroid_position(self, positions):
        """
        positions: current positions of drones (Nx2 array)
        returns: centroid (x, y)
        """
        return np.mean(positions, axis=0)

    def get_formation_positions(self, centroid):
        """
        centroid: (x, y)
        returns: final positions of all drones in formation
        """
        centroid = np.array(centroid)
        return self.offsets + centroid
