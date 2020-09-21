# streetpoints

This code sampling points from a given street maps based on a preferred distance.
Let's say you have the street map of Sydney (extracted from openstreetmap) and you'd like to sample points on the streets every 50 meters.

# How to run
1. Make sure you convert your osm map into geojson (using QGIS or any other tool.)
2. Specify the desired distance in meters
3. run the code: `python sample_street_points.py` 

# Example

![50 meters sampling](/figs/sampling.png)
