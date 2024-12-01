#!pip install geopy
#!pip install datapane
import numpy as np
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import datapane as dp

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="http")

def get_latitude_longitude(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Example addresses
addresses = [
    '1600 Amphitheatre Parkway, Mountain View, CA',
    'Ault Drive, Ingleside, South Stormont, Stormont, Dundas and Glengarry Counties, Eastern Ontario, Ontario, K0C 1M0, Canada',
    '1, Potters Alley, Fredericktown Hill, East Bethlehem Township, Washington County, Pennsylvania, 15333, United States',
    'Sutton Bay, Ontario P0J 1P0, Canada'
]

lat = []
lon = []

for address in addresses:
    latitude, longitude = get_latitude_longitude(address)
    if latitude and longitude:
        lat.append(latitude)
        lon.append(longitude)

# Generate random trails for Bob and Alice around the first address location
np.random.seed(42)  # For reproducibility
num_points = 1000  # Number of points (time intervals). If 10 mins per snapshot, it will be 144 in a day

# Bob's trail
bob_trail = np.cumsum(np.random.randn(num_points, 2) * 0.01, axis=0) + np.array([lat[0], lon[0]])

# Alice's trail
alice_trail = np.cumsum(np.random.randn(num_points, 2) * 0.01, axis=0) + np.array([lat[0], lon[0]])

# Plot the trails on a Folium map
m = folium.Map(location=[lat[0], lon[0]], zoom_start=10)

# Add continuous trails to the map using PolyLine
folium.PolyLine(
    locations=bob_trail, 
    color='blue', 
    weight=3, 
    opacity=0.7, 
    popup='Bob\'s Trail'
).add_to(m)

folium.PolyLine(
    locations=alice_trail, 
    color='red', 
    weight=3, 
    opacity=0.7, 
    popup='Alice\'s Trail'
).add_to(m)

# Add initial and final points for Bob and Alice
folium.Marker(
    location=bob_trail[0], 
    popup='Bob Start', 
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=bob_trail[-1], 
    popup='Bob End', 
    icon=folium.Icon(color='darkblue')
).add_to(m)

folium.Marker(
    location=alice_trail[0], 
    popup='Alice Start', 
    icon=folium.Icon(color='red')
).add_to(m)

folium.Marker(
    location=alice_trail[-1], 
    popup='Alice End', 
    icon=folium.Icon(color='darkred')
).add_to(m)

# Display the map
m.save('contact_tracing_map.html')

# Optional: Display the distance between the first two addresses
location_1 = 0
location_2 = 1
distance = geodesic([lat[location_1], lon[location_1]], [lat[location_2], lon[location_2]]).km
print(f"The distance between {addresses[location_1]} and {addresses[location_2]} is {distance:.2f} kilometers")

# Create another map with location markers
m_locations = folium.Map(location=[lat[0], lon[0]])

for i in range(0, len(addresses)):
    folium.Marker(
        location=[lat[i], lon[i]], 
        tooltip=addresses[i]
    ).add_to(m_locations)

# Add a marker for the specific distance calculation
folium.Marker(
    location=[lat[location_1], lon[location_1]], 
    tooltip=addresses[location_1]
).add_to(m_locations)

folium.Marker(
    location=[lat[location_2], lon[location_2]], 
    tooltip=addresses[location_2],
    popup=f"Distance: {geodesic([lat[location_1], lon[location_1]], [lat[location_2], lon[location_2]]).km:.2f} km"
).add_to(m_locations)

# Save the locations map
m_locations.save('location_markers_map.html')

# Optional: If you want to use Datapane
dp.Plot(m)

"""
The distance between 1600 Amphitheatre Parkway, Mountain View, CA and Ault Drive, Ingleside, South Stormont, Stormont, Dundas and Glengarry Counties, Eastern Ontario, Ontario, K0C 1M0, Canada is 3979.50 kilometers

"""