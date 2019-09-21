#!/usr/bin/env python3

import copy
from sys import argv, stderr
import json as js
import time
import heapq

#Construct a Tree
class Tree:
    def __init__(self, board, up=None, left=None, down=None, right=None, parent=None, depth=0, manh=0):
        self.board = board
        self.up = up
        self.left = left
        self.down = down
        self.right = right
        self.parent = parent
        self.depth = depth
        self.manh = manh

        def __str__(self):
            return str(self.board)
    
    def __lt__(self, other):
        return self.manh < other.manh

#Algorithm A:
#Pop off the first element, compute its successors and their Manhattan distance.
#If a successor is new, add it to the priority queue.
#If a successor has been visited, determine if its Manhattan distance is shorter or not.
def calcmanh(board,goal):
    manhdist = 0
    #For each non-zero square:
    #Determine x and y position of the square.
    for x in board:
        for y in x:
            #Except for the space...
            if y != 0:
                posx = board.index(x)
                posy = x.index(y)
                #Determine where y is in the goal state
                goalxrow = [goalxrow for goalxrow in goal if y in goalxrow][0]
                goalx = goal.index(goalxrow)
                goaly = goalxrow.index(y)
                manhdist += abs(posx - goalx) + abs(posy - goaly)
    
    return manhdist


#Receives: the current depth, maximum depth, list of tree nodes to search, goal board state
def solsearch(depth, maximum, openlist, closelist, goalstate):
    #print("Solsearching...")
    global stategen
    global statevisit
    #Iterate while there are items in openlist
    while openlist:
        #Pop from OPEN
        x = heapq.heappop(openlist)
        statevisit += 1
        #Add to CLOSED
        closelist.append(x)
        #Check if the board is at the goal state
        if x.board == goalstate:
            #If so, build the solution
            trueboard = x
            while trueboard.parent is not None:
                solboard.insert(0,x.board)
                if trueboard.parent.up is trueboard:
                    solpath.insert(0,"up")
                elif trueboard.parent.right is trueboard:
                    solpath.insert(0,"right")
                elif trueboard.parent.down is trueboard:
                    solpath.insert(0,"down")
                elif trueboard.parent.left is trueboard:
                    solpath.insert(0,"left")
                else:
                    solpath.insert(0,"wtf")
                trueboard = trueboard.parent
            return 1
        
        #Find the zero!
        try:
            z = [z for z in x.board if 0 in z][0]
        except Exception as error:
            print("Error:",error)
            exit(1)
        new_board = x.board        
        up_node = copy.deepcopy(new_board)
        new_up = Tree(up_node,None, None, None, None, x, x.depth+1)
        left_node = copy.deepcopy(new_board)
        new_left = Tree(left_node,None,None,None,None,x,x.depth+1)
        down_node = copy.deepcopy(new_board)
        new_down = Tree(down_node,None, None, None, None, x, x.depth+1)
        right_node = copy.deepcopy(new_board)
        new_right = Tree(right_node,None,None,None,None,x,x.depth+1)
                
        #Start up/down/left/right as False
        up = False
        down = False
        left = False
        right = False

        #Build potential new states
        #Up
        if x.board.index(z) > 0:
            up = True
            stategen += 1
            new_up.board[x.board.index(z)][z.index(0)] = new_up.board[x.board.index(z)-1][z.index(0)]
            new_up.board[x.board.index(z)-1][z.index(0)] = 0
        #Left
        if z.index(0) > 0:
            left = True
            stategen += 1
            new_left.board[x.board.index(z)][z.index(0)] = new_left.board[x.board.index(z)][z.index(0)-1]
            new_left.board[x.board.index(z)][z.index(0)-1] = 0
        #Down
        if x.board.index(z) < gridsize_x - 1 and (x.down is not x.parent or x.parent is None):
            down = True
            stategen += 1
            new_down.board[x.board.index(z)][z.index(0)] = new_down.board[x.board.index(z)+1][z.index(0)]
            new_down.board[x.board.index(z)+1][z.index(0)] = 0
        #Right
        if z.index(0) < gridsize_y - 1 and (x.right is not x.parent or x.parent is None):
            right = True
            stategen += 1
            new_right.board[x.board.index(z)][z.index(0)] = new_right.board[x.board.index(z)][z.index(0)+1]
            new_right.board[x.board.index(z)][z.index(0)+1] = 0
        
        #For each of our (up to) four new states, add them to the graph if needed
        if up and new_up.depth < maximum:
            new_up.manh = calcmanh(new_up.board,goalstate) + new_up.depth
            if new_up.board not in seenboards:
                #Newly explored node, just link it to x
                x.up = new_up
                seenboards.append(new_up.board)
                heapq.heappush(openlist,new_up)
            #Otherwise, examine depth to see if it's shorter
            else:
                for l in closelist:
                    if new_up.board == l.board:
                        #We've found the node, now examine depths
                        if new_up.manh < l.manh:
                            new_up.parent.up = new_up
                            closelist.pop(closelist.index(l))
                            heapq.heappush(openlist,new_up)
                            seenboards.pop(seenboards.index(new_up.board))
                            #l.parent.up = None
                            #l.parent = None
                            break
                        else:
                            new_up.parent = None
                            break
        if left and new_left.depth < maximum:
            new_left.manh = calcmanh(new_left.board,goalstate) + new_left.depth
            if new_left.board not in seenboards:
                #Newly explored node, just link it to x
                x.left = new_left
                seenboards.append(new_left.board)
                heapq.heappush(openlist,new_left)
            #Otherwise, examine depth to see if it's shorter
            else:
                for l in closelist:
                    if new_left.board == l.board:
                        #We've found the node, now examine depths
                        if new_left.manh < l.manh:
                            new_left.parent.left = new_left
                            closelist.pop(closelist.index(l))
                            heapq.heappush(openlist,new_left)
                            seenboards.pop(seenboards.index(new_left.board))
                            #l.parent.left = None
                            #l.parent = None
                            break
                        else:
                            new_left.parent = None
                            break
        if down and new_down.depth < maximum:
            new_down.manh = calcmanh(new_down.board,goalstate) + new_down.depth
            if new_down.board not in seenboards:
                #Newly explored node, just link it to x
                x.down = new_down
                seenboards.append(new_down.board)
                heapq.heappush(openlist,new_down)
            #Otherwise, examine depth to see if it's shorter
            else:
                for l in closelist:
                    if new_down.board == l.board:
                        #We've found the node, now examine depths
                        if new_down.manh < l.manh:
                            new_down.parent.down = new_down
                            closelist.pop(closelist.index(l))
                            heapq.heappush(openlist,new_down)
                            seenboards.pop(seenboards.index(new_down.board))
                            #l.parent.down = None
                            #l.parent = None
                            break
                        else:
                            new_down.parent = None
                            break
        if right and new_right.depth < maximum:
            new_right.manh = calcmanh(new_right.board,goalstate) + new_right.manh
            if new_right.board not in seenboards:
                #Newly explored node, just link it to x
                x.right = new_right
                seenboards.append(new_right)
                heapq.heappush(openlist,new_right)
            #Otherwise, examine depth to see if it's shorter
            else:
                for l in closelist:
                    if new_right.board == l.board:
                        #We've found the node, now examine depths
                        if new_right.manh < l.manh:
                            new_right.parent.right = new_right
                            #Need to pop off CLOSED and re-add to OPEN
                            closelist.pop(closelist.index(l))
                            heapq.heappush(openlist,new_right)
                            seenboards.pop(seenboards.index(new_right.board))
                            #l.parent.right = None
                            #l.parent = None
                            break
                        else:
                            new_right.parent = None
                            break         
    #If we get here OPEN is empty, meaning no solutions are available.
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

stategen = 0
statevisit = 0
depth = 0
res = 0
solboard = []
solpath = []
openlist = []
closelist = []
seenboards = []
beftime = time.time()
tree = Tree(grid_start)
stategen += 1
tree.manh = calcmanh(tree.board,grid_goal)
heapq.heappush(openlist,tree)
seenboards.append(tree.board)
result = solsearch(depth,maxdepth+1,openlist,closelist,grid_goal)
aftime = time.time()
restime = aftime - beftime
if result == 1:
    print("Solution found!")
    for x in solpath:
        print(x,end=' ')
    print()
    print("Total time:",restime,"seconds")
    print("States generated:",stategen)
    print("States visited:",statevisit)
    for x in solboard:
        for y in x:
            print(y)
        print("------")
else:
    print("Nope")