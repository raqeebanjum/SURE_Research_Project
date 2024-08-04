import csv
import math
from pyproj import Proj, transform

# Input CSV file path with X, Y, and Altitude
input_csv_path = r"C:\Users\Oscar\Desktop\fishnet_points_with_altitude.csv"

# Output file path for the converted data
output_file_path = r"C:\Users\Oscar\Desktop\converted_fishnet_points.xml"

# Original coordinate system (assuming it is a projected coordinate system, for example, UTM Zone 15N)
# Replace this with the appropriate EPSG code for your coordinate system
original_proj = Proj('EPSG:32615')

# WGS 1984 geographic coordinate system
wgs84_proj = Proj('EPSG:4326')

# Conversion factor from feet to meters
feet_to_meters = 0.3048

# Open input CSV file for reading
with open(input_csv_path, mode='r') as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip the header row

    # Prepare output file
    with open(output_file_path, mode='w') as outfile:
        outfile.write('<array>\n')

        # Process each row
        for row in reader:
            x, y, altitude_feet = map(float, row)
            longitude, latitude = transform(original_proj, wgs84_proj, x, y)
            altitude_meters = math.ceil(altitude_feet * feet_to_meters)

            outfile.write('\t<array>\n')
            outfile.write(f'\t\t<real>{latitude}</real>\n')
            outfile.write(f'\t\t<real>{longitude}</real>\n')
            outfile.write(f'\t\t<real>{altitude_meters}</real>\n')
            outfile.write('\t</array>\n')

        outfile.write('</array>\n')

print(f"Converted data has been written to {output_file_path}.")
