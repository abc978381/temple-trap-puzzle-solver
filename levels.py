LEVELS = {
    1: {
        "board": [
            ('C',0), ('D',0), ('G',2),
            ('B',1), ('_',0), ('H',3),
            ('A',0), ('E',0), ('F',2)
        ],
        "pawn_posn": 8,
        "layer": "Ground"
    },
    
    2: {
        "board": [
            ('A',2), ('E',3), ('G',0),
            ('B',0), ('_',0), ('D',0),
            ('H',0), ('C',2), ('F',2)
        ],
        "pawn_posn": 1,
        "layer": "Ground"
    },
    
    3: {
        "board": [
            ('G',2), ('E',1), ('B',3),
            ('D',0), ('H',3), ('F',0),
            ('A',0), ('_',2), ('C',1)
        ],
        "pawn_posn": 1,
        "layer": "Ground"
    },
    
    4: {
        "board": [
            ('B',1), ('D',0), ('H',2),
            ('E',1), ('G',0), ('F',3),
            ('_',0), ('A',0), ('C',0)
        ],
        "pawn_posn": 3,
        "layer": "Ground"
    },
    
    17: {
        "board": [
            ('G',2), ('F',1), ('E',3),
            ('A',2), ('B',1), ('C',1),
            ('H',0), ('_',2), ('D',1)
        ],
        "pawn_posn": 6,
        "layer": "Ground"
    },
    
    18: {
        "board": [
            ('C',0), ('E',0), ('G',1),
            ('F',0), ('_',0), ('D',2),
            ('H',0), ('B',3), ('A',1)
        ],
        "pawn_posn": 5,
        "layer": "Ground"
    },
    
    19: {
        "board": [
            ('C',1), ('A',0), ('B',2),
            ('D',2), ('E',0), ('G',2),
            ('_',0), ('F',2), ('H',1)
        ],
        "pawn_posn": 3,
        "layer": "Ground"
    },
    
    20: {
        "board": [
            ('G',2), ('H',0), ('C',1),
            ('B',1), ('_',0), ('D',0),
            ('A',0), ('E',0), ('F',2)
        ],
        "pawn_posn": 7,
        "layer": "Ground"
    },
    
    25: {
        "board": [
            ('D',1), ('B',2), ('C',1),
            ('G',0), ('F',2), ('A',3),
            ('H',3), ('E',3), ('_',2)
        ],
        "pawn_posn": 0,
        "layer": "Ground"
    },
    
    26: {
        "board": [
            ('B',2), ('A',0), ('D',1),
            ('C',0), ('F',2), ('G',1),
            ('_',0), ('H',3), ('E',3)
        ],
        "pawn_posn": 4,
        "layer": "Ground"
    },
    
    27: {
        "board": [
            ('C',1), ('A',2), ('_',0),
            ('B',0), ('H',1), ('D',2),
            ('E',0), ('G',0), ('F',2)
        ],
        "pawn_posn": 5,
        "layer": "Ground"
    },
    
    28: {
        "board": [
            ('B',1), ('D',0), ('F',2),
            ('A',0), ('E',0), ('G',2),
            ('H',0), ('C',1), ('_',0)
        ],
        "pawn_posn": 5,
        "layer": "Ground"
    }
    
}

def load_level(level_num):
    if level_num==0:
        return create_custom_level()
    if level_num not in LEVELS:
        return None
    data = LEVELS[level_num]
    return data["board"], data["pawn_posn"], data["layer"]

def create_custom_level():
    print("Create your own level!")
    print("Enter tile name (A-H) and respective orientation (0-3) for each index of 3x3 board (0-8).")
    print("Use '_ 0' for blank cell")
    print("Example input: A 2 -> tile A rotated twice clockwise.")
    
    board = []
    for i in range(9):
        tile, orient = input(f"Cell {i}: ").strip().upper().split()
        if tile == '_':
            board.append(('_', 0))
        else:
            board.append((tile, int(orient)))
    
    pawn_posn = int(input("Enter pawn starting position (0-8): "))
    layer = input("Enter starting layer (Ground/Top): ").capitalize()
    print("Custom level created successfully!")
    return board, pawn_posn, layer