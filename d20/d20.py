import math
import itertools
from collections import defaultdict
import numpy as np

class Tile:
    def __init__(self, tid, data):
        self.id = tid
        self.data = np.array(data)

        # Calculate the ids of each edge
        self.le = Tile._edge_to_id(self.data[0,:])
        self.re = Tile._edge_to_id(self.data[-1,:])
        self.te = Tile._edge_to_id(self.data[:,0])
        self.be = Tile._edge_to_id(self.data[:,-1])
        self.fle = Tile._edge_to_id(self.data[0,::-1])
        self.fre = Tile._edge_to_id(self.data[-1,::-1])
        self.fte = Tile._edge_to_id(self.data[::-1,0])
        self.fbe = Tile._edge_to_id(self.data[::-1,-1])
        self.edge_ids = {self.le: "LE",
                         self.re: "RE",
                         self.te: "TE",
                         self.be: "BE",
                         self.fle: "FLE",
                         self.fre: "FRE",
                         self.fte: "FTE",
                         self.fbe: "FBE"}
        self.joins = set()

    def rot90(self, n=1):
        return Tile(self.id, np.rot90(self.data, n))
    def flipx(self):
        return Tile(self.id, np.flipud(self.data))
    def flipy(self):
        return Tile(self.id, np.fliplr(self.data))

    @staticmethod
    def _edge_to_id(edge):
        return int("".join(str(c) for c in edge), 2)

    def __repr__(self):
        lines = [f"Tile {self.id}:"]
        for line in self.data.T:
            lines.append("".join("#" if c else "." for c in line))
        return "\n".join(lines)

# Read in inputs
tiles = {}
edge_matches = defaultdict(list)
with open("input") as f:
    lines = [l.strip() for l in f.readlines()]
    for i in range(math.ceil(len(lines)/12)):
        tid = int(lines[i*12].split()[-1][:-1])
        tdata = np.fromiter((c=="#" for c in itertools.chain(*lines[i*12+1:(i+1)*12])), dtype="uint8").reshape((10,10)).T
        tile = Tile(tid, tdata)
        tiles[tid] = tile
        for edge_id in tile.edge_ids:
            edge_matches[edge_id].append(tid)

# Find corners
for edge_match, tile_ids in edge_matches.items():
    if len(tile_ids) == 1:
        continue
    tiles[tile_ids[0]].joins.add(tile_ids[1])
    tiles[tile_ids[1]].joins.add(tile_ids[0])

corners = [x.id for x in tiles.values() if len(x.joins) == 2]
prod = 1
for tid in corners:
    prod *= tid
print(f"Part 1: {prod}")

def place_tile(grid, tile, x, y):
    grid[x*8:(x+1)*8, y*8:(y+1)*8] = tile.data[1:-1, 1:-1]

# Pick a corner and start constructing the image
im_size = int(math.sqrt(len(tiles)))
grid = np.zeros((im_size*8, im_size*8), dtype="uint8")
tile_placements = np.zeros((im_size, im_size), dtype="uint32")

for corner in corners:
    tile = tiles[corner]
    if len(edge_matches[tile.be]) == 2 and len(edge_matches[tile.re]) == 2:
        print(f"Found candidate top left tile: {tile.id}")
        tile_placements[0,0] = tile.id
        break

# Place grid
for x, y in itertools.product(range(im_size), repeat=2):
    # Corner is already filled in
    if (x, y) == (0, 0):
        continue
    if y == 0: # Top of a row
        ptile = tiles[tile_placements[x-1, y]]
        ntile = [tile for tile in tiles.values() if ptile.re in tile.edge_ids][0]
        rot = ntile.edge_ids[ptile.re]
        if rot == "LE":
            pass
        elif rot == "FLE":
            ntile = tiles[ntile.id] = ntile.flipy()
        elif rot == "TE":
            ntile = tiles[ntile.id] = ntile.rot90(-1).flipy()
        elif rot == "FTE":
            ntile = tiles[ntile.id] = ntile.rot90(-1)
        elif rot == "RE":
            ntile = tiles[ntile.id] = ntile.rot90(2).flipy()
        elif rot == "FRE":
            ntile = tiles[ntile.id] = ntile.rot90(2)
        elif rot == "BE":
            ntile = tiles[ntile.id] = ntile.rot90(1)
        elif rot == "FBE":
            ntile = tiles[ntile.id] = ntile.rot90(1).flipy()
        place_tile(grid, ntile, x, y)
        tile_placements[x, y] = ntile.id
        assert ntile.edge_ids[ptile.re] == "LE"
    else:
        ptile = tiles[tile_placements[x, y-1]]
        ntile = [tile for tile in tiles.values() if ptile.be in tile.edge_ids][0]
        rot = ntile.edge_ids[ptile.be]
        if rot == "TE":
            pass
        elif rot == "FTE":
            ntile = tiles[ntile.id] = ntile.flipx()
        elif rot == "LE":
            ntile = tiles[ntile.id] = ntile.rot90(1).flipx()
        elif rot == "FLE":
            ntile = tiles[ntile.id] = ntile.rot90(1)
        elif rot == "RE":
            ntile = tiles[ntile.id] = ntile.rot90(-1).flipx()
        elif rot == "FRE":
            ntile = tiles[ntile.id] = ntile.rot90(-1)
        elif rot == "BE":
            ntile = tiles[ntile.id] = ntile.rot90(2).flipx()
        elif rot == "FBE":
            ntile = tiles[ntile.id] = ntile.rot90(2)
        place_tile(grid, ntile, x, y)
        tile_placements[x, y] = ntile.id
        assert ntile.edge_ids[ptile.be] == "TE"
