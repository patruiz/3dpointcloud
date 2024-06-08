import pandas as pd
import open3d as o3d
from io import StringIO

# Define the file path
file_path = 'A_Hedge_02SEP2022.asc'

# Load the point cloud data from the file
ascii_grid = pd.read_csv(file_path, skiprows=6, delimiter=',', header=None)

# Assume the ASCII file has the following columns: x, y, z, nx, ny, nz
ascii_grid.columns = ['x', 'y', 'z', 'nx', 'ny', 'nz']

# Extract point coordinates and normals
points = ascii_grid[['x', 'y', 'z']].values
normals = ascii_grid[['nx', 'ny', 'nz']].values

# Create an Open3D PointCloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.normals = o3d.utility.Vector3dVector(normals)

# Perform Poisson surface reconstruction to create a volumetric mesh
poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)

# Compute vertex normals for the Poisson mesh
poisson_mesh.compute_vertex_normals()

# Assign a color to the Poisson mesh (blue)
poisson_mesh.paint_uniform_color([0, 0, 1])

# Optional: Apply minimal Laplacian smoothing to the Poisson mesh
smoothed_mesh = poisson_mesh.filter_smooth_laplacian(number_of_iterations=5)

# Compute vertex normals for the smoothed mesh
smoothed_mesh.compute_vertex_normals()

# Assign a color to the smoothed mesh (green)
smoothed_mesh.paint_uniform_color([0, 1, 0])

# Save the smoothed Poisson mesh as an STL file
stl_file_path = 'accurate_poisson_mesh.stl'
o3d.io.write_triangle_mesh(stl_file_path, smoothed_mesh)

# Visualize the original point cloud and the Poisson surface mesh
o3d.visualization.draw_geometries([pcd], window_name="Original Point Cloud")
o3d.visualization.draw_geometries([poisson_mesh], window_name="Poisson Surface Mesh (Blue)")
o3d.visualization.draw_geometries([smoothed_mesh], window_name="Smoothed Poisson Mesh (Green)")

# Visualize all together
o3d.visualization.draw_geometries([pcd, poisson_mesh, smoothed_mesh], window_name="All Meshes")
