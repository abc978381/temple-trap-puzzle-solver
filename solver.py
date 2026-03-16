# Defining the rotate sides function for a tile (clockwise)
ROTATE = {'I': 'II', 'II': 'III', 'III': 'IV', 'IV': 'I'}

def rotate_sides(sides, rotations):
    new_sides = set(sides)
    for _ in range(rotations%4):
        new_sides = {ROTATE[s] for s in new_sides}
    return new_sides

# Defining the tile class
class Tile:
    def __init__(self, name, symbol, top_open, ground_open, hole, stairs, stair_side=None, orientation=0):
        self.name = name
        self.symbol = symbol
        self.orientation = orientation
        self.top_open = rotate_sides(top_open,orientation)
        self.ground_open = rotate_sides(ground_open, orientation)
        self.hole = hole
        self.stairs = stairs
        self.stair_side = stair_side

# Defining the dictionary for the basic tiles on the board
TILES = {
    'A': Tile('A','=',top_open={'I','II'},ground_open=set(),hole=False,stairs=False),
    'B': Tile('B','▢',top_open = {'I','II'},ground_open=set(),hole=False, stairs=False),
    'C': Tile('C','+',top_open={'II','IV'},ground_open=set(),hole=False,stairs=False),
    'D': Tile('D','◇',top_open={'IV'},ground_open={'II'},hole=True,stairs=True,stair_side='IV'),
    'E': Tile('E','*',top_open={'IV'},ground_open={'II'},hole=True,stairs=True,stair_side='IV'),
    'F': Tile('F','▷',top_open=set(),ground_open={'I','II'},hole=True,stairs=False),
    'G': Tile('G','x',top_open=set(),ground_open={'I','II'},hole=True,stairs=False),
    'H': Tile('H','○',top_open=set(),ground_open={'I','II'},hole=True,stairs=False)
}

# Function to get the adjacent cells of a given index on a 3x3 board
def get_neighbours(index):
    neighbours = []
    if (index % 3 != 2):
        neighbours.append(index + 1)
    if (index % 3 != 0):
        neighbours.append(index - 1)
    if (index >= 3):
        neighbours.append(index - 3)
    if (index < 6):
        neighbours.append(index + 3)
    return neighbours

def get_direction(from_idx, to_idx): # to clearly get the direction of movement
    diff = to_idx - from_idx
    if diff==-3: return "up"
    if diff==3: return "down"
    if diff==1: return "right"
    if diff==-1: return "left"
    return None

# function to get all the cells reachable by the pawn initially at index pawn_posn, given layer on the board
def pawn_reachable_cells(pawn_posn, layer, board):
    reachable = {} # set of (cell, layer) reachable
    visited = set()
    queue = [(pawn_posn, layer, 0)] # (cell, layer, cost)
    
    # BFS to traverse reachable cells
    while queue:
        curr, curr_layer, cost = queue.pop(0)
        if (curr, curr_layer) in visited:
            continue
        visited.add((curr, curr_layer))
        reachable[(curr, curr_layer)] = cost
        
        curr_tile_name, curr_orient = board[curr]
        if curr_tile_name not in TILES:
            continue
        
        curr_tile = Tile(curr_tile_name, TILES[curr_tile_name].symbol,TILES[curr_tile_name].top_open, TILES[curr_tile_name].ground_open, TILES[curr_tile_name].hole, TILES[curr_tile_name].stairs, TILES[curr_tile_name].stair_side, curr_orient)
        curr_open = curr_tile.top_open if curr_layer== "Top" else curr_tile.ground_open
        
        if curr_tile.stairs:
            stair_cost = 0
            stair_layer = "Top" if curr_layer == "Ground" else "Ground"
            if (curr, stair_layer) not in visited:
                queue.append((curr, stair_layer, cost+stair_cost))
                
        neighbours = get_neighbours(curr)
        for n in neighbours:
            neighbour_tile_name, neighbour_orient = board[n]
            if ((neighbour_tile_name == '_') or neighbour_tile_name not in TILES):
                continue
            neighbour_tile = Tile(neighbour_tile_name, TILES[neighbour_tile_name].symbol, TILES[neighbour_tile_name].top_open, TILES[neighbour_tile_name].ground_open, TILES[neighbour_tile_name].hole, TILES[neighbour_tile_name].stairs, TILES[neighbour_tile_name].stair_side, neighbour_orient)
            neighbour_open = neighbour_tile.top_open if curr_layer=="Top" else neighbour_tile.ground_open
            
            # check connectivity of cells
            if n==curr-1: # left
                if 'IV' not in curr_open or 'II' not in neighbour_open:
                    continue
            elif n==curr+1: #right
                if 'II' not in curr_open or 'IV' not in neighbour_open:
                    continue
            elif n==curr-3: #top
                if 'I' not in curr_open or 'III' not in neighbour_open:
                    continue
            elif n==curr+3: #bottom
                if 'III' not in curr_open or 'I' not in neighbour_open:
                    continue
            
            if (n, curr_layer) not in visited:
                queue.append((n,curr_layer,cost+1))
                
    return reachable 

# function to return the board after sliding a tile
def slide_tile(board, tile_index, blank_index):
    new_board = board.copy()
    new_board[blank_index], new_board[tile_index] = new_board[tile_index], new_board[blank_index]
    return new_board

# defining the state class 
class State:
    def __init__(self, board, pawn_posn, layer, g=0, parent=None, action=None):
        self.board = board
        self.pawn_posn = pawn_posn
        self.g = g
        self.layer = layer
        self.action = action
        self.parent = parent
        self.blank_posn = self.find_blank()
        
    def __lt__(self, other):
        return self.g < other.g
    
    def find_blank(self): # function to find the index of blank tile in given board
        for i in range(9):
            if (self.board[i][0] == "_"):
                self.blank_posn = i
                return i
        return None
    
    def is_valid(self): # function to check validity of state
        if self.blank_posn is None:
            self.find_blank()
        
        if (self.pawn_posn == self.blank_posn): # pawn can not stand on blank index
            return False
        
        pawn_tile_name, pawn_tile_orient = self.board[self.pawn_posn]
        if pawn_tile_name not in TILES:
            return False
        
        tile = TILES[pawn_tile_name]
        if self.layer=="Ground" and tile.hole:
            return True
        else:
            return False
            
    def is_goal(self): # function to check if given state is goal state
        reachable = pawn_reachable_cells(self.pawn_posn, self.layer, self.board)
        
        for (cell, layer) in reachable.keys():
            if cell==0:
                first_tile_name, first_tile_orient = self.board[0]
                first_tile = Tile(first_tile_name, TILES[first_tile_name].symbol, TILES[first_tile_name].top_open, TILES[first_tile_name].ground_open, TILES[first_tile_name].hole, TILES[first_tile_name].stairs, TILES[first_tile_name].stair_side, first_tile_orient)
                first_tile_open = first_tile.top_open if layer=="Top" else first_tile.ground_open
                if 'IV' in first_tile_open: # checking if exit from board is open from first tile
                    return True
        return False
    
def get_successors(state): # function to define successors of a give state
    successors = []
    reachable = pawn_reachable_cells(state.pawn_posn, state.layer, state.board)
    
    for (cell, layer), walk_cost in reachable.items():
        if (cell, layer) == (state.pawn_posn, state.layer):
            continue
        
        tile_name, _ = state.board[cell]
        if not TILES[tile_name].hole:
            continue # can only rest on tiles with hole
        
        action = f"Move pawn from {state.pawn_posn} ({state.layer}) to {cell}({layer})"

        new_state = State(state.board.copy(), cell, layer, state.g+walk_cost, state, action=action)
        if new_state.is_valid():
            successors.append(new_state)
    
    for n in get_neighbours(state.blank_posn):
        tile_name, _ = state.board[n]
        if tile_name not in TILES:
            continue
        if n==state.pawn_posn:
            continue # lock rule
        
        new_board = slide_tile(state.board, n, state.blank_posn)
        new_blank_posn = n
        new_g = state.g + 1 # slide cost
        slide_direction = get_direction(n, state.blank_posn)
        slide_action = f"Slide tile {tile_name}({TILES[tile_name].symbol}) {slide_direction}"
        new_state = State(new_board, state.pawn_posn, state.layer, new_g, state, slide_action)
        if new_state.is_valid():
            successors.append(new_state)
    
    return successors

# defining heuristic function
def heuristic(state):
    pawn_row = state.pawn_posn//3
    pawn_col = state.pawn_posn%3
    exit_row, exit_col = 0,0
    h = abs(pawn_row - exit_row) + abs(pawn_col - exit_col) # Manhattan distance as base heuristic
    
    first_tile_name, first_tile_orient = state.board[0]
    if first_tile_name == '_':
        h += 1 # penalty for first tile being blank
        
    if first_tile_name in TILES:
        first_tile = Tile(first_tile_name,TILES[first_tile_name].symbol, TILES[first_tile_name].top_open, TILES[first_tile_name].ground_open, TILES[first_tile_name].hole, TILES[first_tile_name].stairs, TILES[first_tile_name].stair_side, first_tile_orient)
        if 'IV' not in first_tile.top_open and 'IV' not in first_tile.ground_open:
            h += 1 # penalty for closed exit
    
    return h

# Astar search for solving 
import heapq

def astar_search(start_state):
    frontier = []
    heapq.heappush(frontier, (start_state.g + heuristic(start_state), start_state))
    explored = set()
    
    while frontier:
        f,curr = heapq.heappop(frontier)
        state_key = (tuple(curr.board), curr.pawn_posn, curr.layer)
        
        if state_key in explored:
            continue
        explored.add(state_key)
        
        # check for goal state
        if curr.is_goal():
            print("Goal reached!")
            return curr
        
        for succ in get_successors(curr):
            succ_key = (tuple(succ.board), succ.pawn_posn, succ.layer)
            if succ_key not in explored:
                f_succ = succ.g + heuristic(succ)
                heapq.heappush(frontier, (f_succ, succ))
    
    print("No solution")
    return None

# reconstructing path
def reconstruct_path(state):
    path = []
    while state:
        path.append(state)
        state = state.parent
    path.reverse()
    return path

# Choose level and implement solver
from levels import load_level
print("Temple Trap Puzzle Solver")
print('''Available levels:
      Starter: 1-4
      Junior: 17-20
      Expert: 25-28
      Create custom level: 0''')
level_num = int(input("Choose level number: "))
level_data = load_level(level_num)
if level_data is None:
    print("Invalid level number.")
    exit()
board, pawn_posn, layer = level_data

state = State(board, pawn_posn, layer)
goal_state = astar_search(state)

if goal_state:
    path = reconstruct_path(goal_state)
    print("Solution Path:")
    for step in path:
        if step.action:
            print(step.action, "| Total Cost", step.g)
    print("Walk to exit")
    print(f"Goal reached in total cost: {goal_state.g}")
else:
    print("No solution found.")
    