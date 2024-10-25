import osmnx as ox
import requests
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import LineString

# Set your Google Maps API key
google_key = "Get_API_Key"

# Define location
location = (23.050563887729403, 72.51763363854504)  # Coordinates for Ahmedabad
place_name = "Ahmedabad"

# Fetch the road network for the area using OSMnx
G = ox.graph_from_point(location, dist=5000, network_type='drive')
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

# Extract the road geometries (edges)
roads = gdf_edges[['geometry']]

# Define a function to fetch traffic intensity data from Google Maps Traffic API
def get_traffic_intensity(lat, lng, google_key):
    url = f"https://maps.googleapis.com/maps/api/traffic/map/json"
    params = {
        "location": f"{lat},{lng}",
        "key": google_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Dummy traffic intensity, replace with actual logic to parse traffic data
        return np.random.choice([1, 2, 3, 4])  # Random traffic level: low (1) to high (4)
    else:
        return 1  # Default low traffic intensity

# Apply traffic intensity to each road segment
traffic_intensity = []
for idx, row in roads.iterrows():
    centroid = row['geometry'].centroid
    intensity = get_traffic_intensity(centroid.y, centroid.x, google_key)
    traffic_intensity.append(intensity)

# Add traffic intensity to GeoDataFrame
roads['traffic_intensity'] = traffic_intensity

# Plot roads with traffic intensity using a colormap
cmap = plt.cm.get_cmap('RdYlGn_r')  # Red for high traffic, Green for low
colors = [cmap(intensity / 4) for intensity in traffic_intensity]

fig, ax = plt.subplots(figsize=(10, 10))
roads.plot(ax=ax, color=colors, linewidth=1)
plt.title(f"Roads with Traffic Intensity in {place_name}")
plt.show()
