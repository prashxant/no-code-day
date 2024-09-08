from PIL import Image
import exifread

def extract_gps_info(image_path):
    try:
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
                print("No GPS information found.")
                return None, None
    except Exception as e:
        print(f"Error extracting GPS information: {e}")
        return None, None

def convert_to_degrees(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)

def generate_google_maps_html(latitude, longitude, api_key):
    html_code = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Display Location on Google Maps</title>
        <script src="https://maps.googleapis.com/maps/api/js?key={api_key}"></script>
        <script>
          function initMap() {{
            var location = {{ lat: {latitude}, lng: {longitude} }};
            var map = new google.maps.Map(document.getElementById("map"), {{
              zoom: 15,
              center: location,
            }});
            var marker = new google.maps.Marker({{
              position: location,
              map: map,
            }});
          }}
        </script>
      </head>
      <body onload="initMap()">
        <h1>Location from Image</h1>
        <div id="map" style="height: 500px; width: 100%;"></div>
      </body>
    </html>
    """
    try:
        with open("location_map.html", "w") as file:
            file.write(html_code)
        print("HTML file generated: location_map.html")
    except Exception as e:
        print(f"Error generating HTML file: {e}")

def main():
    # Request user input for image path
    image_path = input("Enter the path of the image file: ")

    # Your Google Maps API key
    api_key = "AIzaSyBfqcWI4g6UOSe0DhPRPvwNM5086dZHkE8"  # Replace this with your actual API key
    
    # Extract latitude and longitude from the image
    latitude, longitude = extract_gps_info(image_path)
    
    if latitude is not None and longitude is not None:
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        # Generate the HTML with the extracted coordinates
        generate_google_maps_html(latitude, longitude, api_key)
    else:
        print("Failed to generate HTML due to missing or invalid GPS data.")

# Example usage
main()
