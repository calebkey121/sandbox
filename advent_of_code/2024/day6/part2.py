import os
from enum import Enum, auto

class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

def delta(dir: Direction) -> tuple:
    dx = -1 if dir == Direction.WEST else 1 if dir == Direction.EAST else 0
    dy = -1 if dir == Direction.SOUTH else 1 if dir == Direction.NORTH else 0
    return dx, dy

def turn(dir: Direction) -> Direction:
    match dir: # 90 Degree turn to the right
        case Direction.NORTH:
            return Direction.EAST
        case Direction.EAST:
            return Direction.SOUTH
        case Direction.SOUTH:
            return Direction.WEST
        case Direction.WEST:
            return Direction.NORTH


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Coord(x={self.x}, y={self.y})"
    
    def __eq__(self, value):
        return isinstance(value, Coord) and self.x == value.x and self.y == value.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    @staticmethod
    def distance(a, b):
        if isinstance(a, Coord) and isinstance(b, Coord):
            if a.x == b.x:
                return abs(a.y - b.y)
            elif a.y == b.y:
                return abs(a.x - b.x)
            # we can compute the distance if theyre not equal, but this problem doesn't ask us to
        return NotImplemented

class PuzzleMap:
    def __init__(self, obstacles: list[Coord], map_size):
        self.rows = {}
        self.cols = {}
        self.visited_tiles = set()
        self.loop_objs = set()
        self.map_width, self.map_height = map_size
        for obstacle in obstacles:
            # Add if it doesn't exist
            if obstacle.y not in self.rows:
                self.rows[obstacle.y] = []
            if obstacle.x not in self.cols:
                self.cols[obstacle.x] = []
            
            # Lets do a sorted insert, because we want to sort by x for rows and vis versa
            inserted = False
            for i, check in enumerate(self.rows[obstacle.y]):
                # if we find an x that is lower than ours we would add it
                if obstacle.x < check.x:
                    self.rows[obstacle.y].insert(i, obstacle)
                    inserted = True
            # If we find none then we add it to the end
            if not inserted:
                self.rows[obstacle.y].append(obstacle)
            
            # Same for cols
            inserted = False
            for j, check in enumerate(self.cols[obstacle.x]):
                if obstacle.y < check.y:
                    self.cols[obstacle.x].insert(j, obstacle)
                    inserted = True
            if not inserted:
                self.cols[obstacle.x].append(obstacle)
    
    def find_next_point(self, starting_point: Coord, dir: Direction, hypothetical_object: Coord = None) -> Coord:
        x = starting_point.x
        y = starting_point.y

        # We'll explicitly go one by one, i can think of ways to combine these, but might just be best to do it this way
        next_point = None
        col = self.cols.get(x, [])
        row = self.rows.get(y, [])
        if dir == Direction.NORTH:
            # Since we're going north, we'll find the first obstacle north of our starting point
            for obstacle in col: # sorted low to high y
                if obstacle.y > y:
                    next_point = Coord(x, obstacle.y - 1) # because we don't stop ontop of obstacle, we stop before
                    break
            if not next_point:
                next_point = Coord(x, self.map_height - 1) # because we stop on the edge
            # for part 2 we want to allow hypothetical objects
            if hypothetical_object and hypothetical_object.x == x and hypothetical_object.y > y and next_point.y >= hypothetical_object.y:
                next_point = Coord(x, hypothetical_object.y - 1)
        elif dir == Direction.SOUTH:
            for obstacle in col[::-1]: # reversed because its sorted from low to high
                if obstacle.y < y:
                    next_point = Coord(x, obstacle.y + 1)
                    # for part 2 we want to allow hypothetical objects
                    break
            if not next_point:
                next_point = Coord(x, 0)
            if hypothetical_object and hypothetical_object.x == x and hypothetical_object.y < y and next_point.y <= hypothetical_object.y:
                next_point = Coord(x, hypothetical_object.y + 1)
        elif dir == Direction.EAST:
            for obstacle in row:
                if obstacle.x > x:
                    next_point = Coord(obstacle.x - 1, y)
                    break
            if not next_point:
                next_point = Coord(self.map_width - 1, y)
            # for part 2 we want to allow hypothetical objects
            if hypothetical_object and hypothetical_object.y == y and hypothetical_object.x > x and next_point.x >= hypothetical_object.x:
                next_point = Coord(hypothetical_object.x - 1, y)
        elif dir == Direction.WEST:
            for obstacle in row[::-1]: # reversed to have it sorted from high to low
                if obstacle.x < x:
                    next_point = Coord(obstacle.x + 1, y)
                    break
            if not next_point:
                next_point = Coord(0, y)
            # for part 2 we want to allow hypothetical objects
            if hypothetical_object and hypothetical_object.y == y and hypothetical_object.x < x and next_point.x <= hypothetical_object.x:
                next_point = Coord(hypothetical_object.x + 1, y)
        return next_point

    def visit(self, point_a: Coord, point_b: Coord, curr_direction: Direction) -> None:
        # This function tracks the tiles we've visited and checks for loops
        dx, dy = delta(curr_direction)
        curr_tile = point_a

        # Do (while)
        self.visited_tiles.add(Coord(curr_tile.x, curr_tile.y))
        self.check_for_loops(curr_tile, curr_direction)
        while curr_tile != point_b:
            # Advance
            curr_tile.x += dx
            curr_tile.y += dy

            # Track visited tiles
            self.visited_tiles.add(Coord(curr_tile.x, curr_tile.y))

            # Check for loops
            self.check_for_loops(curr_tile, curr_direction)
    
    def check_for_loops(self, curr_tile: Coord, curr_direction: Direction) -> None: # keep track in self.loops
        if curr_tile == Coord(6, 2) and curr_direction == Direction.EAST:
            pass # check for specific coord debugging
        
        # First - hypothetical object! 
        x, y = curr_tile.x, curr_tile.y
        dx, dy = delta(curr_direction)
        hypothetical_object = Coord(x + dx, y + dy)

        # Second - we will do tortise and hare, if they ever meet up that makes a loop!
        tortoise = hare = curr_tile
        # Once for tortise...
        tortoise_dir = turn(curr_direction)
        tortoise = self.find_next_point(tortoise, tortoise_dir, hypothetical_object)
        # Twice for hare!
        hare_dir = turn(curr_direction)
        hare = self.find_next_point(hare, hare_dir, hypothetical_object)
        if self.on_edge(hare):
            return
        hare_dir = turn(hare_dir)
        hare = self.find_next_point(hare, hare_dir, hypothetical_object)
        
        counter = 0
        maxCounter = 100000
        while ( tortoise != hare ) or counter >= maxCounter:
            if self.on_edge(tortoise) or self.on_edge(hare):
                return # no way theres a loop
            
            # Once for tortise...
            tortoise_dir = turn(tortoise_dir)
            tortoise = self.find_next_point(tortoise, tortoise_dir, hypothetical_object)
            # Twice for hare!
            hare_dir = turn(hare_dir)
            hare = self.find_next_point(hare, hare_dir, hypothetical_object)
            hare_dir = turn(hare_dir)
            hare = self.find_next_point(hare, hare_dir, hypothetical_object)

            counter += 1

        if tortoise == hare and tortoise_dir == hare_dir:
            self.loop_objs.add(hypothetical_object)

    def on_edge(self, point) -> bool:
        if point.x == 0 or point.y == 0 or point.x == self.map_width - 1 or point.y == self.map_height - 1:
            return True
        return False

    def print_map(self):
        my_map = [ ['.'] * self.map_width for _ in range(self.map_height) ]
        for col in self.cols.values():
            for o in col:
                i = self.map_height - 1 - o.y
                j = o.x
                my_map[i][j] = '#'
        for visit in self.visited_tiles:
            i = self.map_height - 1 - visit.y
            j = visit.x
            my_map[i][j] = 'X'
        for _, line in enumerate(my_map):
            print("".join(line))

# Readlines from given file
def get_file_data(filename: str, input_directory: str) -> list:
    path = os.path.join(input_directory, filename)
    with open(path) as file:
        lines = file.readlines()
        puzzle_input = [ line.strip() for line in lines ]      
    return puzzle_input

# Put the puzzle input into the form you want
def parse_input(puzzle_input: list):
    obstacles = []
    starting_point = None
    map_width = len(puzzle_input[0]) # assuming we have a puzzle input, otherwise this will error
    map_height = len(puzzle_input)
    for i, line in enumerate(puzzle_input[::-1]): # reverse to make it simple to make the x/y conversion
        # have to be carefule with how we treat i/j and Coords x/y
        # to make the logic simpler and more obvious to a cartesian layout, i will convert
        # puzzle_input[i=0][j=0] is Coord(x=0, y=height-1)
        # puzzle_input[i=5][j=5] is Coord(x=5, y=height-1-5)
        # this is why we reversed above, and did Coord(j, i) because i grows from top to bottom, y grows bottom to top
        obstacles.extend([ Coord(j, i) for j, char in enumerate(line) if char == "#" ])
        if not starting_point and '^' in line:
            starting_point = Coord(line.index('^'), i)


    map_size = (map_width, map_height)
    return starting_point, obstacles, map_size    

# Figure out the guard path from the map
def map_path(puzzle_input: list):
    starting_point, obstacles, map_size = parse_input(puzzle_input)
    dir = Direction.NORTH
    point = starting_point

    # Lets make a hash table of cols and rows, for quick lookup if someone is in our col / row
    puzzle_map = PuzzleMap(obstacles, map_size)

    # now we can easily check if an obstacle is in our way
    reached_edge = False
    while not reached_edge:
        # Loop through finding the next point, map will do this based on the obstacles we gave it earlier
        next_point = puzzle_map.find_next_point(point, dir)
        
        # Tracks visited tiles and checks for loops
        puzzle_map.visit(point, next_point, dir)

        # Find if we're on the edge of the map
        reached_edge = puzzle_map.on_edge(next_point)

        # continue to next point and turn
        point = next_point
        if not reached_edge: # not necessary but might be helpful in debugging
            dir = turn(dir)
    # puzzle_map.print_map()
    return len(puzzle_map.visited_tiles), len(puzzle_map.loop_objs)

def main():
    input_directory = "input"
    input_filenames = [
        "test_input.txt",
        "puzzle_input.txt",
        # "my_input.txt",
    ]
    for file in input_filenames:
        puzzle_input = get_file_data(file, input_directory)
        distinct_tiles, loops = map_path(puzzle_input)

        print(f"For input '{file}': distinct_tiles = {distinct_tiles}, loops = {loops}")

if __name__ == "__main__":
    main()

# Part 1
# 743 too low!
# 750 too low!
# 5145!!!

# Part 2
# 1587 too high!
# 1569 too high!
# (1523 from help.py)