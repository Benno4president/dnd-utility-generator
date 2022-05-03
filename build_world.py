import os
from world_generation.world import World

ROOT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

def new_world():

    config = {
        'root_dir': ROOT_FOLDER_PATH,
        'save_file_dir': ROOT_FOLDER_PATH + '/static/world_folder',
        'root_point': (56.56902182914228, 14.132388581706845), 
        'dist': 600
    }

    world = World(config)

if __name__ == '__main__':
    new_world()
    