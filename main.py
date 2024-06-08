import time 
import pandas as pd
import pyvista as pv

file_path = 'A_Hedge_02SEP2022.asc'
print("Loading data...")

ascii_grid = pd.read_csv(file_path, skiprows=6, delimiter = ',', header=None)

ascii_grid.columns = ['x', 'y', 'z', 'Column4', 'Column5', 'Column6']
print("Creating point cloud...")

point_cloud = pv.PolyData(ascii_grid[['x', 'y', 'z']].values)
print("Generating mesh...")

start_time = time.time()
mesh = point_cloud.delaunay_3d()
end_time = time.time()
print("Preparing plot...")

mesh.save('test.vtk')
print("Saving mesh...")

plotter = pv.Plotter()
# plotter.add_points(point_cloud, scalars=ascii_grid['z'], cmap='viridis')
plotter.add_mesh(mesh, scalars=ascii_grid['z'], cmap='viridis', show_edges=True)
plotter.add_axes(line_width=5, labels_off=True)
print("Displaying plot...")

plotter.show()


print(f"Mesh generation time: {end_time - start_time}")