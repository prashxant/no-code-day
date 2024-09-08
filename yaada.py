from PIL import Image
import exifread

def extract_gps_info(image_path):

    with open(image_path, 'rb') as img_file:

        tags = exifread.process_file(img_file)
        
    
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
        gps_longitude = tags.get('GPS GPSLongitude')
        gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

        if gps_latitude and gps_longitude:

            lat = convert_to_degrees(gps_latitude)
            lon = convert_to_degrees(gps_longitude)

      
            if gps_latitude_ref.values != 'N':
                lat = -lat
            if gps_longitude_ref.values != 'E':
                lon = -lon
            
            return lat, lon
        else:
            return None, None

def convert_to_degrees(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


image_path = 'IMG_20210217_144216.jpg'
latitude, longitude = extract_gps_info(image_path)

if latitude and longitude:
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("No GPS information found in the image.")
