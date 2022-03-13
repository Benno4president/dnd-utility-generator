
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


def extract_coords_from_shape(shapely_shape):
    if str(shapely_shape).startswith('POLYGON'):
        return list(shapely_shape.exterior.coords)
    else:
        return list(shapely_shape.coords)
        

