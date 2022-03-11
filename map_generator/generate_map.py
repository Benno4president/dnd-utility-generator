
import osmnx as ox
from pprint import pprint
import osmnx_utils

def new_map(Filename=None):
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

def new_map_type_2(map_settings):
    bgcolor = '#343434'
    edge_color = '#FFB0E2'
    bldg_color = '#F4FF6E'
    dist = 3000

    bbox = ox.utils_geo.bbox_from_point(map_settings['point'], dist=map_settings['dist'])
    fp = ox.geometries_from_point(map_settings['point'], tags=map_settings['tags'], dist=map_settings['dist'])
    G = ox.graph_from_point(map_settings['point'], network_type='all', dist=map_settings['dist'], truncate_by_edge=True, retain_all=True)

    fig, ax = ox.plot_graph(G, bgcolor=map_settings['bgcolor'], node_size=0, edge_color=map_settings['edge_color'], show=False)
    fig, ax = ox.plot_footprints(fp, ax=ax, bbox=bbox, color=bldg_color, save=True)

def discover_event_spots(roads):
    """'geometry'
        'length:'
        'name'
    """
    inner_city = []
    
    for dt in roads:
        l = dt['length']
        if l < 30:
            inner_city.append(dt)
        elif 60 < l:
           #pprint(dt)
           pass 


def generate_map_and_cities():
    map_settings = dict(
    dist=2200,
    edge_color='k',
    bgcolor='w',
    dpi = 300,
    point = (53.800545818126146, 10.76708534735293),#(57.0567, 10.1770),
    default_width=2,
    tags = {
        'building':True,
        'amenity':True, 
        'landuse': ['retail','commercial', 'forest'], 
        'highway':'bus_stop',
        'natural':['water', 'sand'],
        'water': 'river',
        'waterway': ['river', 'stream']
        },
    )
    
    name, data = new_map_type_2(map_settings) #new_map()
    #data = discover_event_spots(data)
"""    lat1 = 57.056754784538676
    lon1 = 10.177020976637465
    lat2 = 57.066523794635664
    lon2 = 10.12668123924413
    print(f"{osmnx_utils.calculate_spherical_distance(lat1, lon1, lat2, lon2):.4f} km")
"""

if __name__ == '__main__':
    generate_map_and_cities()