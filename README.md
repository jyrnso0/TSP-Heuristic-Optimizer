# TSP-Heuristic-Optimizer
This project solves the **Traveling Salesman Problem (TSP)** applied to real-world geographical data from various retail stores across Mexico. The goal is to develop a robust system that transitions from geometric approximations to real-world logistics.

## Project Structure
The code is organized moduly to separate data management from the optimization logic:

* **/src**
    * `matriz_distancias.py`: Script responsible for processing nodes and generating the cost matrix.
    * `main.py`: Core engine that currently implements the constructive optimization phase.
* **/instances**: Contains the retail store datasets.
* **/docs**: Technical documentation and formal academic reports.
* **/notebook**: Includes the `.ipynb` interactive notebook for initial testing and visualization.

## Optimization Methodology
The project is designed to be implemented in two major stages:

1.  **Phase 1: Constructive Heuristic (Current)**
    * Uses **Best Insertion** to build an initial feasible solution.
    * Focuses on finding a valid route that visits all nodes efficiently from scratch.
2.  **Phase 2: Improvement Heuristic (Coming Soon )**
    * Planned implementation of local search algorithms (such as **2-opt**) to refine the initial route.
    * Aim: Eliminate edge crossings and further reduce the total **Objective Value**.

## Distance Calculation & Future Work
* **Current**: Uses the **Haversine Formula** for geodesic distance (great-circle distance).
* **Planned Update**: Migration to **Road Network Distance**. This will allow the solver to consider actual street layouts, directions, and real-world turn restrictions in Mexico.

## How to Run
1. Install dependencies:
   ```bash
   pip install pandas matplotlib
