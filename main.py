import pandas as pd
import pyvista as pv

# Define the file path
file_path = 'A_Hedge_02SEP2022.asc'

# Read the ASC file with whitespace as the delimiter, skipping the first 6 rows
ascii_grid = pd.read_csv(file_path, skiprows=6, delimiter = ',', header=None)

# Define column names (assuming the first three columns are x, y, z coordinates)
ascii_grid.columns = ['x', 'y', 'z', 'Column4', 'Column5', 'Column6']

# Create a point cloud
point_cloud = pv.PolyData(ascii_grid[['x', 'y', 'z']].values)

# Plot the point cloud
plotter = pv.Plotter()
plotter.add_points(point_cloud, scalars=ascii_grid['z'], cmap='viridis')
plotter.show()
