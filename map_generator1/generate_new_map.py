from terrain import MapGrid


options = ['shore', 'island', 'mountain', 'desert']

def new_map():
    for op in options:
        print(f'~~~~~ Beginning to generate a/an{op}. ~~~~~')
        m = MapGrid(op)
        filename = f"./{op}.png"
        m.plot(filename)
    return filename 


if __name__ == '__main__':
    new_map()