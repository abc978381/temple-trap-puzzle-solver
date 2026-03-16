# Temple Trap Puzzle Solver

A Python implementation of a **Temple Trap puzzle solver** using the **A\* search algorithm**.  
The solver finds an optimal sequence of pawn movements and tile slides to guide the pawn to the exit on a 3×3 puzzle board.

---

## Puzzle Overview

Temple Trap is a tile-sliding puzzle consisting of:

- **8 tiles (A–H)** with different path configurations  
- **1 blank cell** used for sliding tiles  
- **A pawn** that moves through connected paths  
- **Two layers**: Ground and Top

The objective is to move the pawn to **cell 0 and exit through its left boundary**.

Board indexing:
0 1 2
3 4 5
6 7 8

---

## Search Formulation

**State Representation**
(board configuration, pawn position, layer)

**Actions**

1. **Pawn Movement**
   - Move through connected open sides of tiles
   - Pawn can only rest on tiles with holes
   - Stairs allow switching between Ground and Top layers

2. **Tile Sliding**
   - A tile adjacent to the blank cell can slide into the blank
   - A tile cannot slide if the pawn is standing on it

**Costs**

- Pawn movement: proportional to path distance  
- Tile slide: cost = 1

---

## Heuristic Function

The A\* heuristic combines:

- **Manhattan distance** from pawn to exit `(0,0)`
- Penalty if exit tile is **blank**
- Penalty if exit tile **does not open to the left**

---

## Project Structure
Temple-Trap-Solver
│
├── solver.py # A* search solver
├── levels.py # predefined and custom levels
└── README.md

---

## Available Levels

| Difficulty | Levels |
|---|---|
| Starter | 1 – 4 |
| Junior | 17 – 20 |
| Expert | 25 – 28 |

Custom levels can also be created by choosing **level 0**.

---

## Running the Solver

```bash
python solver.py

Example output:
Goal reached!

Move pawn from 8 (Ground) to 5 (Ground)
Slide tile D left
Move pawn from 5 (Ground) to 1 (Ground)

Goal reached in total cost: 5