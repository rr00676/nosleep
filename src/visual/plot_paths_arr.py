# visual/plot_path_arr.py
import matplotlib.pyplot as plt
from base.pathing import PathArr # Import PathArr

def plot_paths(path_arr: PathArr) -> None:
    """Plots the source and sensor paths from a PathArr object."""
    plt.figure(figsize=(8, 6)) # Set figure size

    # Plot source paths
    for i, path in enumerate(path_arr.source_paths):
        plt.plot(*path.T, linestyle='-', marker='o', markersize=3, label=f'Source Path {i+1}')

    # Plot sensor paths
    for i, path in enumerate(path_arr.sensor_paths):
        plt.plot(*path.T, linestyle='--', marker='x', markersize=3, label=f'Sensor Path {i+1}')

    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("Field Object Paths")
    # plt.legend()
    plt.grid(True)
    plt.axis('equal') # Ensure equal aspect ratio for x and y axes
    plt.show()