"""
Author: Sofiane Abbar - sofiane.abbar@gmail.com
Date: 2020-09-21

Make sure your file is in geojson and projection in: EPSG:4326 - WGS 84
This code will parse each street and create points along it every DIST meters.
(e.g., 50 meters).

The output is a file names: points_DIST.csv

Dependencies:
    - geopy.distance

"""

import geopy.distance
import json

def densify(e, densification_rate=1):
    s,d = e
    dist = geopy.distance.distance(e[0], e[1]).meters
    if dist < densification_rate:
        return [e] 
    nb_points_frac = float(dist / densification_rate)

    nb_points = 0 
    if (int(nb_points_frac) == nb_points_frac):
        # for 200/50 = 4.0 we need to generate 3 points
        nb_points = int(nb_points_frac) - 1 
    elif (int(nb_points_frac) < nb_points_frac):
        # for 170/50 = ~3.4 we need to generate 3 points
        nb_points = int(nb_points_frac)
    else:
        # for 220/50 = ~4.4 we need 4 points
        nb_points = int(nb_points_frac) + 1 

    x_delta = float(s[0] - d[0]) / (nb_points + 1)
    y_delta = float(s[1] - d[1]) / (nb_points + 1)
    dense_points = [s]
    pv_pt = s
    for i in range(1, nb_points + 1): 
        cur_pt = (s[0] - x_delta * i, s[1] - y_delta * i)
        dense_points.append(cur_pt)
        pv_pt = cur_pt
    return dense_points + [d]


DIST = 50
o = json.load(open('Sydney_ST.geojson'))
print("There are: %s streets." % len(o['features']))

points = set([])
for i, street in enumerate(o['features']):
    print("Processing street: %s" % i)
    # stetch segments of the same street.
    segs = []
    dps = []
    for segment in street['geometry']['coordinates']:
        segs += [(_[1], _[0]) for _ in segment]
    for e in zip(segs, segs[1:]):
        x = densify(e, densification_rate=1)
        dps += x
    idx = 0
    while idx < len(dps):
        points.add(dps[idx])
        idx = idx + DIST
    # Add the last point in the street
    if idx != len(dps) - 1:
        points.add(dps[-1])

with open('points_%s.csv' % DIST, 'w') as g:
    g.write('latitude,longitude\n')
    for pt in points:
        g.write('%s,%s\n' % (pt[0], pt[1]))
print("Generated %s points." % len(points))

