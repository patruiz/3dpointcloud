import open3d as o3d
import numpy as np

# Define the file paths for the nominal model and the scanned point cloud
nominal_ply_path = '300776400-004-001.ply'  # Update with your PLY file path
nominal_stl_path = '300776400-004-001.stl'  # Update with your STL file path
scanned_asc_path = '300776400-004-001.asc'  # Update with your scanned point cloud file path

# Load the nominal PLY model
nominal_pcd_ply = o3d.io.read_point_cloud(nominal_ply_path)
print(f"Loaded nominal PLY point cloud with {len(nominal_pcd_ply.points)} points.")

# Load the nominal STL model and convert it directly to a point cloud
nominal_mesh = o3d.io.read_triangle_mesh(nominal_stl_path)
nominal_pcd_stl = nominal_mesh.sample_points_uniformly(number_of_points=len(nominal_mesh.vertices))
print(f"Loaded nominal STL mesh to point cloud with {len(nominal_pcd_stl.points)} points.")

# Load the scanned point cloud from ASC file
# Only use the first three columns for x, y, z coordinates
scanned_points = np.loadtxt(scanned_asc_path, delimiter=',', usecols=(0, 1, 2))
scanned_pcd = o3d.geometry.PointCloud()
scanned_pcd.points = o3d.utility.Vector3dVector(scanned_points)
print(f"Loaded scanned point cloud with {len(scanned_pcd.points)} points.")

# Visualize the nominal PLY point cloud
o3d.visualization.draw_geometries([nominal_pcd_ply], window_name="Nominal PLY Point Cloud")

# Visualize the nominal STL point cloud
o3d.visualization.draw_geometries([nominal_pcd_stl], window_name="Nominal STL Point Cloud")

# Visualize the scanned point cloud
o3d.visualization.draw_geometries([scanned_pcd], window_name="Scanned Point Cloud")

# Choose which nominal point cloud to use (PLY or STL)
nominal_pcd = nominal_pcd_ply  # Use this if you prefer the PLY file
# nominal_pcd = nominal_pcd_stl  # Use this if you prefer the STL point cloud

# Preprocessing: Remove statistical outliers to reduce noise
nominal_pcd, _ = nominal_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
scanned_pcd, _ = scanned_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)

# Estimate normals for both point clouds with high resolution
nominal_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=100))
scanned_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=100))

# Registration: Align the scanned point cloud to the nominal point cloud using ICP with high precision
threshold = 0.005  # Smaller distance threshold for more accurate ICP
initial_transformation = np.identity(4)  # Initial transformation matrix

reg_p2p = o3d.pipelines.registration.registration_icp(
    scanned_pcd, nominal_pcd, threshold, initial_transformation,
    o3d.pipelines.registration.TransformationEstimationPointToPoint(),
    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=2000)  # More iterations for higher accuracy
)

# Apply the transformation to align the scanned point cloud
scanned_pcd.transform(reg_p2p.transformation)

# Color the nominal point cloud blue
nominal_pcd.paint_uniform_color([0, 0, 1])

# Color the scanned point cloud red
scanned_pcd.paint_uniform_color([1, 0, 0])

# Visualize the overlay of the nominal and scanned point clouds
o3d.visualization.draw_geometries([nominal_pcd, scanned_pcd], window_name="Overlay of Nominal and Scanned Point Clouds")
