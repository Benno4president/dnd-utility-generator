


import utm
import numpy as np
from math import radians, sin, asin, cos ,tan

def calc_placement(point, mid_point, dist):
    map_dist = dist + 2 * (dist * tan(16)) # what the fuck
    
    u = utm.from_latlon(*mid_point)
    u = (u[0]-map_dist/2,u[1]+map_dist/2,u[2],u[3])
    tl_coor =  utm.to_latlon(*u)
    print('top left:', tl_coor, '\nu:', u)
    meters_from_top = calculate_spherical_distance(point[0], tl_coor[1], tl_coor[0],  tl_coor[1])
    meters_from_top = meters_from_top*1000
    print('meters from top:', meters_from_top)
    meters_from_left = calculate_spherical_distance(point[0], point[1], point[0],  tl_coor[1])
    meters_from_left = meters_from_left*1000
    print('meters from left:', meters_from_left)
    percent_from_top = round((meters_from_top / map_dist ) * 100, 2)
    percent_from_left = round((meters_from_left / map_dist) * 100, 2)
    
    return percent_from_top, percent_from_left
    
    
def calculate_spherical_distance(lat1, lon1, lat2, lon2, r=6371):
    # Convert degrees to radians
    coordinates = lat1, lon1, lat2, lon2
    # radians(c) is same as c*pi/180
    phi1, lambda1, phi2, lambda2 = [
        radians(c) for c in coordinates
    ]  
    # Apply the haversine formula
    a = (np.square(sin((phi2-phi1)/2)) + cos(phi1) * cos(phi2) * 
         np.square(sin((lambda2-lambda1)/2)))
    d = 2*r*asin(np.sqrt(a))
    return d

# vectorized haversine function
def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))


point = (56.69169629841078, 14.606472183594853)#(57.05652920976395, 10.177341401778113)
distance = 3000
dist = distance #* 100 *1.775 # magic number i guess.

u = utm.from_latlon(*point)
print('Root:')
print(u)
print(utm.to_latlon(*u))
north = (u[0]+dist/2,u[1],u[2],u[3])
south = (u[0]-dist/2,u[1],u[2],u[3])
east = (u[0],u[1]+dist/2,u[2],u[3])
west = (u[0],u[1]-dist/2,u[2],u[3])
lln = utm.to_latlon(*north)
lls = utm.to_latlon(*south)
lle = utm.to_latlon(*east)
llw = utm.to_latlon(*west)
print('North:', lln)
print('South:', lls)
print('East:', lle)
print('West:', llw)

"""  THIS IS TRUE BUT THE VALS ARE FUCKED """
print('SE corner', llw[0], lln[1])
print('NW corner', lle[0], lls[1])
# NSEW
bbox = (lle[0], llw[0], lln[1], lls[1])

def get_bbox_custom(point, xy_dist=400)
    u = utm.from_latlon(*point)
    nw = (u[0]-dist/2,u[1]+dist/2,u[2],u[3])
    se = (u[0]+dist/2,u[1]-dist/2,u[2],u[3])
    llnw = utm.to_latlon(*nw)
    llse = utm.to_latlon(*se)
    cbbox = (llnw[0], llse[0], llnw[1], llse[1])
    return cbbox

print(bbox)
# both function work
print('Distance between N S:', haversine(*lln, *lls), 'km')
print('Distance between E W:', haversine(*lle, *llw), 'km')
print('Distance between E W:', calculate_spherical_distance(*lle, *llw), 'km')
# print('Testing', utm.to_latlon(u[0]+dist,u[1],u[2],u[3]))



