# UAV path planning project
**what did you build ?**
* This project is about UAV path planning.
* I used a V-shape formation for the UAVs.
* There are a total of 5 UAVs in the system.
* I used the A* algorithm for path planning.

**SETUP :**
* First, clone the repository using `git clone https://github.com/Divya-ase/uav-path-planning.git`
* Then go to the project folder using `cd uav-path-planning/end_term`
* Finally, install the required libraries using `pip install -r requirements.txt`

**How to run ?**

* Run the program using `python simulate.py`
* When it runs, it opens a window showing the UAVs moving in formation along the planned path.
* It also saves the output as a GIF file in the `results` folder.
* Some basic information or metrics may also be printed in the terminal.

**What each script does ?**

* map_setup.py — defines the grid, obstacles, and start/goal positions.
* path_planner.py — uses A* algorithm to find a path from start to goal.
* trajectory.py — converts the path into smooth trajectories for UAVs.
* formation.py — manages the V-shape formation and UAV positions.
* simulate.py — runs the full simulation and shows animation and results.

**Results**
Path Plot
![Path Plot](results/path_plot.png)

Trajectory Comparison
![Trajectory Comparison](results/trajectory_comparison (1).png)

**Observation:**
- Min-time trajectory completes in **20.2 seconds** at speed 5 units/s.
- Min-energy trajectory completes in **67.2 seconds** at speed 1.5 units/s.
- Min-time is **69.9% faster** than min-energy.
- Min-energy uses **69.9% less energy** than min-time.



**Formation Details**
- Formation shape: **V-shape**
- Number of UAVs: **N = 5**
- Drone assignment: Each drone is offset from the centroid in local frame.
  - Drone 1: far left back
  - Drone 2: left back
  - Drone 3: centre (lead)
  - Drone 4: right back
  - Drone 5: far right back
- The centroid follows the A* path and all drones maintain V-shape formation throughout the flight.


