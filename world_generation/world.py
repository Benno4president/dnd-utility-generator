from world_generation.map_generator.generate_map import generate_map_and_cities
from world_generation.event import Event
import utm
from math import radians, sin, cos, asin, tan
import numpy as np

class World:
    def __init__(self, Config):
        self.config = Config
        
        self.coordinates_of_interest = None
        self.event_list = []

        self.generate_world()
        
    
    def generate_world(self):
        self.coordinates_of_interest = generate_map_and_cities(self.config)
        
        for i in self.coordinates_of_interest['houses']:
            p = next(iter(i))
            xy = calc_placement((p[1],p[0]), self.config['root_point'], self.config['dist'])
            print('NEW:\n', xy, p[1], p[0])


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
    
    
    