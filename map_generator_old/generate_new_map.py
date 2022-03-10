from terrain import MapGrid
import os

options = ['shore', 'island', 'mountain', 'desert']
path = os.path.dirname(__file__)

def new_map():
    for op in options:
        print(f'~~~~~ Beginning to generate a/an {op}. ~~~~~')
        m = MapGrid(op)
        m.print_self()
        filename = f"{path}/{op}.png"
        print('.PNG stored at', filename)
        m.plot(filename)
    return filename 


if __name__ == '__main__':
    new_map()