
import osmnx as ox
from pprint import pprint
import osmnx_utils
import matplotlib.pyplot as plt

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
    filename = './out/type2test2.png'
    bgcolor = '#343434'
    edge_color = '#FFB0E2'
    bldg_color = '#F4FF6E'
    dist = 3000
    land_color = '#aaaaaa'

    bbox = ox.utils_geo.bbox_from_point(map_settings['point'], dist=map_settings['dist'])
    fp = ox.geometries_from_point(map_settings['point'], tags=map_settings['tags'], dist=map_settings['dist'])    
    G = ox.graph_from_point(map_settings['point'], network_type='all', dist=map_settings['dist'], truncate_by_edge=True, retain_all=True)
    # get n evenly-spaced colors from some matplotlib colormap
    ox.plot.get_colors(n=5, cmap="plasma", return_hex=True)
    
    for i in fp:
        a = fp[i]
        print(a.axes)
    
    fig, ax = ox.plot_graph(G, bgcolor=map_settings['bgcolor'], node_size=0, edge_color=map_settings['edge_color'], show=False)
    fig, ax = ox.plot_footprints(fp, ax=ax, bbox=bbox, color=bldg_color, save=False)

    fig.savefig(filename, dpi=300, bbox_inches='tight', format="png", 
                facecolor=fig.get_facecolor(), transparent=False,
                ax=ax)

# helper funcion to get one-square-mile street networks, building footprints, and plot them
def map_helper(
    point,
    tags,
    network_type="drive",
    dpi=76,
    dist=1805,
    default_width=4,
    street_widths=None,
    ):
    fp = './out/type3test1.png'
    gdf = ox.geometries_from_point(point, tags, dist=dist)
    
    colors = colour_factory(gdf)
    
    fig, ax = ox.plot_figure_ground(
        point=point,
        dist=dist,
        network_type=network_type,
        default_width=default_width,
        street_widths=street_widths,
        edge_color="brown", # color of the roads
        save=False,
        show=False,
        close=True,
    )
    fig, ax = ox.plot_footprints(
        gdf, ax=ax, filepath=fp, dpi=dpi, save=False, 
        show=False, close=True, color=colors
    )
    fig.savefig(fp, dpi=300, bbox_inches='tight', format="png", 
                facecolor=fig.get_facecolor(), transparent=False,
                ax=ax)

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

def new_map_4():
    bbox = [38.7969489, 38.6919296, -9.088, -9.2296891]

    G = ox.graph_from_bbox(
        *bbox,
        simplify=True,
        retain_all=True,
        clean_periphery=True,
        truncate_by_edge=True,
        network_type="drive_service",
        )

    # Find additional geometries
    water_1 = ox.geometries_from_bbox(*bbox, tags={"natural": ["water"]})
    water_2 = ox.geometries_from_bbox(
        *bbox,
        tags={
            "waterway": ["riverbank", "canal", "dock"],
            "water": ["river", "canal", "reservoir"],
            "natural": ["bay"],
        },
    )
    water_3 = ox.geometries_from_bbox(*bbox, tags={"place": ["sea", "ocean"]})
    motoway = ox.geometries_from_bbox(
        *bbox,
        tags={
            "highway": [
                "motorway",
                "motorway_link",
                "trunk",
                "trunk_link",
            ]
        },
    )
    filepath="./out/type4test2.png"
    # PLOT
    fig, ax = ox.plot_graph(
        G,
        bgcolor="white",
        node_size=0,
        edge_linewidth=1,
        show=False,
        close=False,
        figsize=(60, 80),
        dpi=100,
        save=False,
        filepath=filepath,
    )

    water_1.plot(color="#466A8C", linewidth=1, ax=ax)
    water_2.plot(color="#466A8C", linewidth=1, ax=ax)
    water_3.plot(color="#466A8C", linewidth=1, ax=ax)
    motoway.plot(color="#000000", linewidth=2, ax=ax)
    
    fig.savefig(filepath, dpi=300, bbox_inches='tight', format="png", 
                facecolor=fig.get_facecolor(), transparent=False,
                ax=ax)


def new_map_5():
    # Specify the name that is used to seach for the data
    point = (57.05652920976395, 10.177341401778113)
    dist = 1200
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
    tags = {'building': True}
    buildings = ox.geometries_from_point(point, tags, dist=dist)
    
    # List key-value pairs for tags
    tags = {'leisure': 'park', 'landuse': ['grass', 'forest']}
    parks = ox.geometries_from_point(point, tags, dist=dist)
    # parks.plot(color="green");
    tags = {'water':True,'waterways':True}
    water = ox.geometries_from_point(point, tags, dist=dist)

    
    #fig, ax = plt.subplots(figsize=(12,8))
    # Plot the footprint
        #area.plot(ax=ax, facecolor='black', zorder=0)
    # Plot street edges
    edges.plot(ax=ax, linewidth=0.5, edgecolor='silver', zorder=1)
    # Plot buildings
    buildings.plot(ax=ax, facecolor='brown', alpha=0.7, zorder=2)
    # Plot parks
    parks.plot(ax=ax, color='green', alpha=0.7, markersize=10, zorder=3)
    
    water.plot(ax=ax, color='blue')

    
    plt.tight_layout(pad=0)
    plt.axis('off')
    
    #plt.xlim((-4.05, -4.01))
    #plt.ylim((39.89, 39.85))
    fig.savefig('./out/new5_1.png', dpi=600, bbox_inches='tight', format="png", 
                facecolor=fig.get_facecolor(), transparent=False,
                ax=ax)

def generate_map_and_cities():
    map_settings = dict(
    dist=2200,
    edge_color='k',
    bgcolor='w',
    dpi = 300,
    point = (57.05652152746672, 10.177531538966981),#(57.0567, 10.1770),
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
    new_map_5()
    # map_helper(map_settings['point'], map_settings['tags'], network_type="all", 
              # default_width=1, street_widths={"secondary": 3, "primary": 6})
    #name, data = new_map_type_2(map_settings) #new_map()
    #data = discover_event_spots(data)
"""    lat1 = 57.056754784538676
    lon1 = 10.177020976637465
    lat2 = 57.066523794635664
    lon2 = 10.12668123924413
    print(f"{osmnx_utils.calculate_spherical_distance(lat1, lon1, lat2, lon2):.4f} km")
"""

if __name__ == '__main__':
    generate_map_and_cities()