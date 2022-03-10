
import osmnx as ox
from pprint import pprint


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

def new_map(Filename=None):
    filename = './out/' + (Filename or 'generated_map.png')
    #Center of the map
    latitude = 57.056754784538676#57.0563 #40.4168 57.05630316106769, 10.230879697040052
    longitude = 10.177020976637465#10.2308 #-3.7038    
    center_point = (latitude, longitude)

    G = ox.graph_from_point(center_point, dist=1200, retain_all=True, simplify = True, network_type='all')

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
            """
            if item["length"] <= 100:
                linewidth = 0.10
                color = "#a6a6a6"     
                         
            elif item["length"] > 100:# and item["length"] <= 200:
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
            """
            
        if "primary" in item["highway"]:
            linewidth = 0.5
            color = "#ffff"
        else:
            color = '#ffff' #"#a6a6a6"
            linewidth = 0.25#0.10
        
        roadColors.append(color)
        roadWidths.append(linewidth)

    
    size = 0.10
    #Limit borders 
    north = latitude + size 
    south = latitude - size 
    east = longitude + size 
    west = longitude - size 

    bgcolor = "#061529"
    #bbox = (north, south, east, west)
    fig, ax = ox.plot_graph(G, node_size=0,
                            dpi = 300,bgcolor = bgcolor,
                            save = False, edge_color=roadColors,
                            edge_linewidth=roadWidths, edge_alpha=1)

    fig.tight_layout(pad=0)
    fig.savefig(filename, dpi=300, bbox_inches='tight', format="png", 
                facecolor=fig.get_facecolor(), transparent=False)
    
    data_dict = weird_format_to_dict(data)
    
    return filename, data_dict


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
            pprint(dt) 


def generate_map_and_cities():
    name, data = new_map()
    data = discover_event_spots(data)


if __name__ == '__main__':
    generate_map_and_cities()