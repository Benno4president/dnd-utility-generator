
class Event:
    def __init__(self, name=None, point=None, sumbol=None):
        self.name = name or 'Test Event'
        self.x, self.y = point or (0,0)
        self.symbol = symbol or 'Event'