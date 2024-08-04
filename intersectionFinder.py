import arcpy
import csv

# Set up the workspace
workspace = r"C:\Users\Oscar\Desktop\Austin\MyProject24\MyProject24.gdb"
arcpy.env.workspace = workspace

# Feature class names
points_fc = "fishnet_points"
buffer3d_fc = "single_Buffer3D"

# Output CSV file path
output_csv_path = r"C:\Users\Oscar\Desktop\fishnet_points_with_altitude.csv"

# Check if buffer3d dataset exists
if not arcpy.Exists(buffer3d_fc):
    raise ValueError(f"The dataset {buffer3d_fc} does not exist. Please check the path and try again.")

# Open CSV file for writing
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["X", "Y", "Altitude"])

    # Iterate through each point in the fishnet
    with arcpy.da.SearchCursor(points_fc, ["SHAPE@XY"]) as cursor:
        for row in cursor:
            x, y = row[0]

            # Create a point geometry
            point = arcpy.Point(x, y)
            point_geometry = arcpy.PointGeometry(point)

            # Intersect the point with the buffer3d to get the altitude
            try:
                arcpy.MakeFeatureLayer_management(buffer3d_fc, "buffer_layer")
                arcpy.SelectLayerByLocation_management("buffer_layer", "INTERSECT", point_geometry)

                altitude = None
                with arcpy.da.SearchCursor("buffer_layer", ["SHAPE@"]) as buffer_cursor:
                    for buffer_row in buffer_cursor:
                        multipatch = buffer_row[0]
                        if multipatch:
                            z = multipatch.centroid.Z
                            altitude = z
                            break

                writer.writerow([x, y, altitude])
            except Exception as e:
                print(f"Error processing point ({x}, {y}): {e}")
                writer.writerow([x, y, None])

print(f"CSV file with X, Y, and altitude has been created at {output_csv_path}.")
