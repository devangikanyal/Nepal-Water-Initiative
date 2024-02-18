import os
import exifread
import pandas as pd

def get_decimal_coordinates(tags, ref_type, coordinate_type):
    if ref_type in tags and coordinate_type in tags:
        ref = tags[ref_type].printable
        coords = tags[coordinate_type].values
        degrees = coords[0].num / coords[0].den
        minutes = coords[1].num / coords[1].den
        seconds = coords[2].num / coords[2].den
        decimal_coords = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            decimal_coords *= -1
        return decimal_coords
    return None

def process_images(directory_path):
    data = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'rb') as f:
                tags = exifread.process_file(f)
                latitude = get_decimal_coordinates(tags, 'GPS GPSLatitudeRef', 'GPS GPSLatitude')
                longitude = get_decimal_coordinates(tags, 'GPS GPSLongitudeRef', 'GPS GPSLongitude')
                if latitude and longitude:
                    data.append({"Image": filename, "Latitude": latitude, "Longitude": longitude})
    
    return pd.DataFrame(data)

# Example usage
directory_path = '/Users/devangikanyal/Desktop/GPS_Photos1'
df = process_images(directory_path)

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv('/Users/devangikanyal/Desktop/GPS_Photos1/coordinates.csv', index=False)

# Or save to an Excel file if preferred
# df.to_excel('/Users/devangikanyal/Desktop/GPS_Photos1/coordinates.xlsx', index=False)
