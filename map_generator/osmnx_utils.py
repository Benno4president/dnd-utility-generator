from math import radians, sin, cos, asin
import numpy as np

def weird_format_to_dict(weird):
    out_ldict = []
    for i, road in enumerate(weird):
        #print(road.keys())
        if not 'geometry' in road:
            continue    
            
        coordinates_str = str(road['geometry']).split('(')[1].split(')')[0].split(',')
        coordinates = []
        for cor in coordinates_str:
            cor = cor.strip().split(' ')
            coordinates.append((float(cor[0]), float(cor[1])))
        
        out_ldict.append({
            'geometry': coordinates,
            'length': float(road['length']),
            'name': road['name'] if 'name' in road else '' 
        })
            
    #print(out_dict, len(out_dict))
    #pprint(out_dict)
    return out_ldict

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