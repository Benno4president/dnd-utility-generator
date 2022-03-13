
import osmnx as ox
from pprint import pprint
import world_generation.map_generator.osmnx_utils as oxutil
import matplotlib.pyplot as plt
import random

def OLD_new_map(Filename=None):
    filename = './out/' + (Filename or 'generated_map.png')
    #Center of the map
    latitude = 57.056754784538676#57.0563 #40.4168 57.05630316106769, 10.230879697040052
    longitude = 10.177020976637465#10.2308 #-3.7038    
    tags = {"building": True}
    
    center_point = (latitude, longitude)
    G = ox.graph_from_point(center_point, dist=11200, retain_all=True, simplify=True, network_type='all')
    # Unpack Data
    u = []
    v = []
    key = []
    data = []
    for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
        u.append(uu)
        v.append(vv)
        key.append(kkey)
        data.append(ddata)
    
    # Lists to store colors and widths 
    roadColors = []
    roadWidths = []

    for item in data:
        ### Roads
        if "length" in item.keys():
            
            if item["length"] <= 100:
                linewidth = 0.10
                color = "#a6a6a6"     
                         
            elif item["length"] > 100 and item["length"] <= 200:
                linewidth = 0.15
                color = "#676767"
            
            elif item["length"] > 200 and item["length"] <= 400:
                linewidth = 0.25
                color = "#454545"
            
            elif item["length"] > 400 and item["length"] <= 800:
                color = "#bdbdbd"
                linewidth = 0.35
            else:
                color = "#d5d5d5"
                linewidth = 0.45
            
            
        if "primary" in item["highway"]:
            linewidth = 0.5
            color = "#ffff"
        else:
            color = "#ffff" #"#a6a6a6"
            linewidth = 0.10
        
        roadColors.append(color)
        roadWidths.append(linewidth)



    bgcolor = "#061529"
    fig, ax = ox.plot_graph(G, node_size=0,
                            dpi = 300,bgcolor = bgcolor,
                            save = False, edge_color=roadColors,
                            edge_linewidth=roadWidths, edge_alpha=1)

    fig.tight_layout(pad=0)
    fig.savefig(filename, dpi=300, bbox_inches='tight', format="png", 
                facecolor=fig.get_facecolor(), transparent=False,
                ax=ax)
    
    data_dict = osmnx_utils.weird_format_to_dict(data)
    
    return filename, data_dict


def generate_new_map(filename, coordinates=None, distance=1200):
    # Specify the name that is used to seach for the data
    point = coordinates or (56.69142216428653, 14.605520381219193)#(57.05652920976395, 10.177341401778113)
    dist = distance
    # Fetch OSM street network from the location
    graph = ox.graph_from_point(point, dist=dist, network_type='all')
    # Plot the streets
    fig, ax = ox.plot_graph(graph, node_size=0, bgcolor='#e6d9ae')
    # Retrieve nodes and edges
    nodes, edges = ox.graph_to_gdfs(graph)
    
    # Get place boundary related to the place name as a geodataframe
        #area = ox.geocode_to_gdf(point)
        #area.plot();
    # List key-value pairs for tags
    # List key-value pairs for tags
    tags = {'leisure': 'park', 'landuse': ['grass', 'forest'], 
            'natural': ['wood', 'tree', 'tree_row']  
        }
    parks = ox.geometries_from_point(point, tags, dist=dist)
    
    tags = {'boundary': True}
    large_forests = ox.geometries_from_point(point, tags, dist=dist)

    tags = {'building': True, 'amenity':True}
    buildings = ox.geometries_from_point(point, tags, dist=dist)
    
    # parks.plot(color="green");
    tags = {'water':True,'waterways':True, 'natural': 'water'}
    water = ox.geometries_from_point(point, tags, dist=dist)

    
    #fig, ax = plt.subplots(figsize=(12,8))
    # Plot the footprint
        #area.plot(ax=ax, facecolor='black', zorder=0)
        
    # Plot street edges
    print('plotting edges')
    edges.plot(ax=ax, linewidth=0.5, edgecolor='silver', zorder=1)
    
    print('plotting parks')
    parks.plot(ax=ax, color='green', alpha=0.7, markersize=10, zorder=3)
    
    print('plotting large forest/reserve')
    large_forests.plot(ax=ax, color='#257a23', alpha=0.7, markersize=10, zorder=3)
    
    print('plotting buildings')
    buildings.plot(ax=ax, facecolor='brown', alpha=0.7, zorder=2)
    
    print('plotting water')
    water.plot(ax=ax, color='#03cafc')

    
    plt.tight_layout(pad=0)
    plt.axis('off')
    
    #plt.xlim((-4.05, -4.01))
    #plt.ylim((39.89, 39.85))
    fig.savefig(filename, dpi=600, bbox_inches='tight', format="png", 
                facecolor=fig.get_facecolor(), transparent=False)
    
    geometry_collection = {
        'nodes': nodes,
        'edges': edges,
        'graph': graph,
        'buildings': buildings,
        'parks': parks,
        'large_forest': large_forests,
        'water': water
    }
    return geometry_collection


def discover_event_spots(geod):
    """
    city? dist over ~4000
    in city if below ~1200
    in forest
    by water
    on road
    
    """
    #view all
    for g in geod:
        print('!!###',g, type(g))
        for b in geod[g]:
            print(b)
    
    houses = []
    
    for build in geod['buildings']['geometry']:
        houses.append(oxutil.extract_coords_from_shape(build))
    
    out_dict = {
        'houses':houses
    }
    
    return out_dict

    for dt in roads:
        l = dt['length']
        if l < 30:
            inner_city.append(dt)
        elif 60 < l:
           #pprint(dt)
           pass 


def generate_map_and_cities(config):
    
    geo_items = generate_new_map(
        filename=config['save_file_dir']+'/world1/world1_map.png',
        coordinates=config['root_point'],
        distance=config['dist']
        )
    event_spots = discover_event_spots(geo_items)
    
    return event_spots
    
    # map_helper(map_settings['point'], map_settings['tags'], network_type="all", 
              # default_width=1, street_widths={"secondary": 3, "primary": 6})
    #name, data = new_map_type_2(map_settings) #new_map()
"""    lat1 = 57.056754784538676
    lon1 = 10.177020976637465
    lat2 = 57.066523794635664
    lon2 = 10.12668123924413
    print(f"{osmnx_utils.calculate_spherical_distance(lat1, lon1, lat2, lon2):.4f} km")
"""

if __name__ == '__main__':
    generate_map_and_cities()