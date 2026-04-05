import pandas as pd
import math
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os

def calculate_distance(node1, node2):
    R = 6371.0 
    lat1, lon1 = math.radians(node1['x']), math.radians(node1['y'])
    lat2, lon2 = math.radians(node2['x']), math.radians(node2['y'])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2.0)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def load_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
        nodes = []
        for _, row in df.dropna().iterrows():
            nodes.append({
                'id': str(row.iloc[0]),
                'x': float(row.iloc[1]), # Latitude
                'y': float(row.iloc[2])  # Longitude
            })
        return nodes
    except Exception as e:
        print(f"Error: Could not read file '{file_path}'. {e}")
        return []

def construct_solution_nn(nodes_list):
    if len(nodes_list) < 2: return nodes_list
    unvisited = nodes_list[1:].copy()
    tour = [nodes_list[0]]
    current = nodes_list[0]
    while unvisited:
        best_dist = float('inf')
        best_idx = -1
        for i, candidate in enumerate(unvisited):
            dist = calculate_distance(current, candidate)
            if dist < best_dist:
                best_dist, best_idx = dist, i
        current = unvisited.pop(best_idx)
        tour.append(current)
    tour.append(tour[0]) 
    return tour

def construct_solution(nodes_list):
    if len(nodes_list) < 2: return nodes_list
    tour = [nodes_list[0], nodes_list[1], nodes_list[0]]
    unvisited = nodes_list[2:].copy()
    while unvisited:
        best_cost = float('inf')
        best_node_idx = -1
        best_insert_pos = -1
        for u_idx, u_node in enumerate(unvisited):
            for i in range(len(tour) - 1):
                cost = calculate_distance(tour[i], u_node) + \
                       calculate_distance(u_node, tour[i+1]) - \
                       calculate_distance(tour[i], tour[i+1])
                if cost < best_cost:
                    best_cost, best_node_idx, best_insert_pos = cost, u_idx, i + 1
        tour.insert(best_insert_pos, unvisited.pop(best_node_idx))
    return tour

def evaluate_solution(solution):
    return sum(calculate_distance(solution[i], solution[i+1]) for i in range(len(solution)-1))

def visualize_solution(solution, title):
    if not solution:
        return

    x_coords = [node['y'] for node in solution]  
    y_coords = [node['x'] for node in solution]  
    ids = [node['id'] for node in solution]

    plt.figure(figsize=(10, 6))
    plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='teal', markersize=8)
    plt.plot(x_coords[0], y_coords[0], marker='s', color='red', markersize=10, label='Start/End')

    for i, (x, y, node_id) in enumerate(zip(x_coords[:-1], y_coords[:-1], ids[:-1])):
        plt.annotate(node_id, (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

def main():
    root = tk.Tk()
    root.withdraw() 
    root.attributes("-topmost", True) 
    
    print("--- TSP HEURISTIC EVALUATOR ---")
    print("Opening file selector...")
    
    file_path = filedialog.askopenfilename(
        title="Select your TSP CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if not file_path:
        print("No file selected. Exiting.")
        return

    data = load_data(file_path)
    
    if data:
        file_name = os.path.basename(file_path)
        print(f"\nSuccessfully loaded {len(data)} nodes from: {file_name}")
        print(f"{'Size':<8} | {'Best Insertion':<15} | {'Nearest Neighbor':<18} | {'Gap (%)':<10}")
        print("-" * 65)

        limit = min(len(data), 25) 
        for i in range(5, limit + 1):
            subset = data[:i]
            val_bi = evaluate_solution(construct_solution(subset))
            val_nn = evaluate_solution(construct_solution_nn(subset))
            gap = ((val_bi - val_nn) / val_nn) * 100
            print(f"{i:<8} | {val_bi:12.2f} km | {val_nn:15.2f} km | {gap:8.2f}%")
        
        print("\nGenerating final map...")
        final_tour = construct_solution(data)
        visualize_solution(final_tour, f"Best Insertion Route: {file_name}")
    else:
        print("Could not process the data. Check the CSV format.")

if __name__ == "__main__":
    main()