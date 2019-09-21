#!/usr/bin/env python3

import copy
from sys import argv, stderr
import json as js
import time

#Construct a Tree
class Tree:
    def __init__(self, board, up=None, left=None, down=None, right=None, parent=None):
        self.board = board
        self.up = up
        self.left = left
        self.down = down
        self.right = right

        def __str__(self):
            return str(self.board)


#Define a solution search that receives the tree
def solsearch(depth, maximum, treestate, goalstate):
    global iterations
    global seenboards
    global deperations
    up = False
    down = False
    left = False
    right = False

    iterations += 1
    deperations += 1
    #First check: Are we at the goal state?
    #if TERM(DATA), return NIL;
    if treestate.board == goalstate:
        return 1
    
    #Next check: Are we at max depth?
    #if 
    if depth > maximum:
        return 0

    #Third check: Have we seen this state before?
    #if MEMBER(DATA, TAIL(DATALIST)), return FAIL;
    if treestate.board in seenboards:
        #Return a unique FAIL so we know to remove the node from the tree
        return 2

    #Add the board to the "seen" list
    seenboards.append(treestate.board)
    
    #Find the zero!
    try:
        x = [x for x in treestate.board if 0 in x][0]
        #Don't really need to append where the 0 "row" is since all "possible" states are built out at once.
    except Exception as error:
        print("Error:",error)
        exit(1)
    new_node = Tree(treestate.board, None, None, None, None, None)
    #row is treestate.board.index(x), column is x.index(0)
    #Determine which new states need to be visited.
    #RULES <- APPRULES(DATA)
    #Start with up
    if treestate.board.index(x) > 0:
        new_up = copy.deepcopy(new_node)
        new_up.board[treestate.board.index(x)][x.index(0)] = new_up.board[treestate.board.index(x) - 1][x.index(0)]
        new_up.board[treestate.board.index(x)-1][x.index(0)] = 0
        treestate.up = new_up
        up = True
    #Left
    if x.index(0) > 0:
        new_left = copy.deepcopy(new_node)
        new_left.board[treestate.board.index(x)][x.index(0)] = new_left.board[treestate.board.index(x)][x.index(0)-1]
        new_left.board[treestate.board.index(x)][x.index(0)-1] = 0
        treestate.left = new_left
        left = True
    #Down
    if treestate.board.index(x) < gridsize_x - 1:
        new_down = copy.deepcopy(new_node)
        new_down.board[treestate.board.index(x)][x.index(0)] = new_down.board[treestate.board.index(x) + 1][x.index(0)]
        new_down.board[treestate.board.index(x)+1][x.index(0)] = 0
        treestate.down = new_down
        down = True
    #Right
    if x.index(0) < gridsize_y - 1:
        new_right = copy.deepcopy(new_node) 
        new_right.board[treestate.board.index(x)][x.index(0)] = new_right.board[treestate.board.index(x)][x.index(0)+1]
        new_right.board[treestate.board.index(x)][x.index(0)+1] = 0
        treestate.right = new_right
        right = True
    
    #We have our rules in place, so now run them
    if up:
        #Recursively call the function
        #PATH <- BACKTRACK(RDATA)
        res = solsearch(depth+1, maximum, treestate.up, goalstate)
        #return CONS(R,PATH);
        if res == 1:
            #Add "up" to the solution
            solboard.insert(0,treestate.up.board)
            solpath.insert(0,"up")
            return 1
        elif res == 2:
            #State was already examined, remove it.
            treestate.up = None
    #if PATH=FAIL, go LOOP;
    if right:
        res = solsearch(depth+1, maximum, treestate.right, goalstate)
        if res == 1:
            solboard.insert(0,treestate.right.board)
            solpath.insert(0,"right")
            return 1
        elif res == 2:
            treestate.right = None
    if down:
        res = solsearch(depth+1, maximum, treestate.down, goalstate)
        if res == 1:
            solboard.insert(0,treestate.down.board)
            solpath.insert(0,"down")
            return 1
        elif res == 2:
            treestate.down = None
    if left:
        res = solsearch(depth+1, maximum, treestate.left, goalstate)
        if res == 1:
            solboard.insert(0,treestate.left.board)
            solpath.insert(0,"left")
            return 1
        elif res == 2:
            treestate.left = None
    #LOOP: if NULL(RULES), return FAIL
    seenboards.pop(-1)
    return 0

#Start: open file and extract json
try:
    with open(argv[1]) as jsonfile:
        data = js.load(jsonfile)
except Exception as error:
    print("Could not open file.")
    print("Message:",error)
    exit(1)

   
#Assign json to values
for x in data:
    print(x,data[x])
#Separate out x and y dimensions, for future-proofing
gridsize_x = data['n']
gridsize_y = data['n']
grid_start = data['start']
grid_goal = data['goal']

#Define max depth, if known
#Max depth is the most moves an optimal solution can take
if gridsize_x == 2 and gridsize_y == 2:
    #minmax for a 2x2 should be 2. 3 could be solved as 1 in the opposite direction
    maxdepth = 2
elif gridsize_x == 3 and gridsize_y == 3:
    #minmax for a 3x3 is 31 moves
    maxdepth = 31
elif gridsize_x == 4 and gridsize_y == 4:
    #minmax for a 4x4 is 80 moves
    maxdepth = 80
elif gridsize_x == 5 and gridsize_y == 5:
    #minmax for a 5x5 is ~205 moves. This is a stupid idea and should not be done
    maxdepth = 205
else:
    #Set maxdepth to an arbitrarily large number. Also a stupid idea.
    maxdepth = 206

iterations = 0
deperations = 0
depth = 0
res = 0

beftime = time.time()
#Iterate from 1 to maxdepth, attempting to find a solution.
for x in range(0,maxdepth+1):
    deperations = 0
    seenboards = []
    solpath = []
    solboard = []
    #print("Starting depth",x)
    #Build the initial node of the tree
    tree = Tree(grid_start)
    res = solsearch(depth,x,tree,grid_goal)
    print("Starting depth",x,file=stderr)
    if res == 1:
        break
aftime = time.time()
restime = aftime - beftime
if res == 1:
    solboard.insert(0,tree.board)
    print("Solution found")
    print("moves:",len(solpath))
    for x in solpath:
        print(x," ", end='')
    print()
    print("Total time:",restime)
    print("Total states generated:",iterations)
    print("States visited at last depth:",deperations)
    for v in solboard:
        for x in v:
            print(x)
        print("-------")
else:
    print("No solution found")