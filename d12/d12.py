import math

class Ship:
    def __init__(self):
        self.pos = [0.0, 0.0]
        self.waypoint = [10.0, 1.0]
        self.dir = 90
        self.map = {
            "F": self.forward,
            "L": self.left,
            "R": self.right,
            "N": self.north,
            "S": self.south,
            "E": self.east,
            "W": self.west
        }
        self.waypmap = {
            "F": self.way_forward,
            "L": self.way_left,
            "R": self.way_right,
            "N": self.way_north,
            "S": self.way_south,
            "E": self.way_east,
            "W": self.way_west
        }

    def forward(self, steps):
        self.pos[0] += steps*math.sin(math.radians(self.dir))
        self.pos[1] += steps*math.cos(math.radians(self.dir))

    def left(self, angle):
        self.dir -= angle
    def right(self, angle):
        self.dir += angle

    def north(self, steps):
        self.pos[1] += steps
    def south(self, steps):
        self.pos[1] -= steps
    def west(self, steps):
        self.pos[0] -= steps
    def east(self, steps):
        self.pos[0] += steps

    def way_forward(self, steps):
        self.pos[0] += steps*self.waypoint[0]
        self.pos[1] += steps*self.waypoint[1]
    def way_left(self, angle):
        self.way_right(-angle)
    def way_right(self, angle):
        self.waypoint = [self.waypoint[0]*math.cos(math.radians(angle)) +
                            self.waypoint[1]*math.sin(math.radians(angle)),
                         -self.waypoint[0]*math.sin(math.radians(angle)) +
                            self.waypoint[1]*math.cos(math.radians(angle))]

    def way_north(self, steps):
        self.waypoint[1] += steps
    def way_south(self, steps):
        self.waypoint[1] -= steps
    def way_west(self, steps):
        self.waypoint[0] -= steps
    def way_east(self, steps):
        self.waypoint[0] += steps

ship = Ship()
with open("input.txt") as f:
    for line in f:
        instr, steps = line[0], int(line[1:])
        ship.map[instr](steps)
print(round(sum(abs(x) for x in ship.pos)))

ship = Ship()
with open("input.txt") as f:
    for line in f:
        instr, steps = line[0], int(line[1:])
        ship.waypmap[instr](steps)
print(round(sum(abs(x) for x in ship.pos)))