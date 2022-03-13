import os
from world_generation.world import World

ROOT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

def new_world():

    config = {
        'root_dir': ROOT_FOLDER_PATH,
        'save_file_dir': ROOT_FOLDER_PATH + '/static/world_folder',
        'root_point': (57.142050216802865, 10.225257399553259), 
        'dist': 300
    }

    world = World(config)

if __name__ == '__main__':
    new_world()
    