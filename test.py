import heapq
import time

import numpy as np


class PriorityQueue: # priority queue whose priority is estimated from the heuristic function
    def  __init__(self):
        self.queue = [] 
        self.count = 0 # number of all elements in priority queue

    def push(self, element, priority):# Push new element item onto the queue
        newElement = (priority, self.count, element)
        heapq.heappush(self.queue, newElement) 
        self.count += 1

    def pop(self):# Pop and return the smallest element from the queue
        (_, _, item) = heapq.heappop(self.queue) 
        return item

    def isEmpty(self):
        return len(self.queue) == 0

def transferToState(input):
    input = [x.replace('\n','') for x in input]
    input = [','.join(input[i]) for i in range(len(input))]
    input = [x.split(',') for x in input]
    maxColsNum = max([len(x) for x in input])

    for irow in range(len(input)):
        for icol in range(len(input[irow])):
            if input[irow][icol] == ' ': input[irow][icol] = 0   # free space
            elif input[irow][icol] == '#': input[irow][icol] = 1 # wall
            elif input[irow][icol] == 'A': input[irow][icol] = 2 # actor
            elif input[irow][icol] == 'X': input[irow][icol] = 3 # box
            elif input[irow][icol] == '_': input[irow][icol] = 4 # goal
            elif input[irow][icol] == 'O': input[irow][icol] = 5 # box on goal
            elif input[irow][icol] == 'E': input[irow][icol] = 6 # actor on goal
        colsNum = len(input[irow])
        if colsNum < maxColsNum:
            input[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 
    return np.array(input)

def actorPosition(state):
    return tuple(np.argwhere((state == 2) | (state == 6))[0])

def boxPosition(state):
    return tuple(tuple(x) for x in np.argwhere((state == 3) | (state == 5))) 

def wallPosition(state):
    return tuple(tuple(x) for x in np.argwhere(state == 1))

def goalPosition(state):
    return tuple(tuple(x) for x in np.argwhere((state == 4) | (state == 5) | (state == 6)))

def isWInGame(posBox):
    return sorted(posBox) == sorted(posGoals) # check the positions of the boxes are fully located at the position of the goal

def isValidMove(move, posActor, posBox):
    xActor, yActor = posActor
    if move[-1]: # actor push the box
        xNext, yNext = xActor + 2 * move[0], yActor + 2 * move[1]
    else: # move to empty space
        xNext, yNext = xActor + move[0], yActor + move[1]
    return (xNext, yNext) not in posBox + posWalls # the location must not coincide with the wall or box

def nextMoves(posActor, posBox):
    xActor, yActor = posActor # current coordinates of actor
    allNextMoves = []
    for move in [[-1, 0],[1, 0],[0, -1],[0, 1]]: # left, top, down, right move
        xNext, yNext = xActor + move[0], yActor + move[1] # actor move
        if (xNext, yNext) in posBox: # actor push the box
            move.append(True)
        else:
            move.append(False) 
        if isValidMove(move, posActor, posBox):
            allNextMoves.append(move)
    return tuple(tuple(x) for x in allNextMoves) # return all next valid moves

def updateState(posActor, posBox, move):
    xActor, yActor = posActor # previous position of actor
    newPosActor = [xActor + move[0], yActor + move[1]] # current position of Actor
    posBox = [list(x) for x in posBox]

    if move[-1]: # if actor push the box, update position of box
        posBox.remove(newPosActor) # remove the pushed box
        posBox.append([xActor + 2 * move[0], yActor + 2 * move[1]]) # add box in new position pushed

    posBox = tuple(tuple(x) for x in posBox)
    newPosActor = tuple(newPosActor)
    return newPosActor, posBox # return new position of actor and boxs

def isFailed(posBox):
    rotatePattern = [[0,1,2,3,4,5,6,7,8],
                    [2,5,8,1,4,7,0,3,6],
                    [0,1,2,3,4,5,6,7,8][::-1],
                    [2,5,8,1,4,7,0,3,6][::-1]]
    flipPattern = [[2,1,0,5,4,3,8,7,6],
                    [0,3,6,1,4,7,2,5,8],
                    [2,1,0,5,4,3,8,7,6][::-1],
                    [0,3,6,1,4,7,2,5,8][::-1]]
    allPattern = rotatePattern + flipPattern

    for box in posBox:
        if box not in posGoals:
            board = [(box[0] - 1, box[1] - 1), (box[0] - 1, box[1]), (box[0] - 1, box[1] + 1), 
                    (box[0], box[1] - 1), (box[0], box[1]), (box[0], box[1] + 1), 
                    (box[0] + 1, box[1] - 1), (box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)]
            for pattern in allPattern:
                newBoard = [board[i] for i in pattern]
                if newBoard[1] in posWalls and newBoard[5] in posWalls: return True
                elif newBoard[1] in posBox and newBoard[2] in posWalls and newBoard[5] in posWalls: return True
                elif newBoard[1] in posBox and newBoard[2] in posWalls and newBoard[5] in posBox: return True
                elif newBoard[1] in posBox and newBoard[2] in posBox and newBoard[5] in posBox: return True
                elif newBoard[1] in posBox and newBoard[6] in posBox and newBoard[2] in posWalls and newBoard[3] in posWalls and newBoard[8] in posWalls: return True
    return False

def heuristic(posActor, posBox): # h(n) heuristic function that estimates the cost of the cheapest path from n to the goal
    distance = 0
    completes = set(posGoals) & set(posBox) # positions box at goal 
    sortposBox = list(set(posBox).difference(completes)) # positions box not at goal
    sortposGoals = list(set(posGoals).difference(completes)) # positions goal not contain box

    for i in range(len(sortposBox)):
        distance += (abs(sortposBox[i][0] - sortposGoals[i][0])) + (abs(sortposBox[i][1] - sortposGoals[i][1]))
    return distance

def cost(node): # g(n) the cost of the path from the start node to n
    return len(node)

def aSearchAlgorithm(): 
    beginBox = boxPosition(state) # get position of boxs
    beginActor = actorPosition(state) # get position of actor
    priorityQueue = PriorityQueue() 
    priorityQueue.push([(beginActor, beginBox)], heuristic(beginActor, beginBox)) 
    exploredSet = set()

    while priorityQueue:
        node = priorityQueue.pop()
        if isWInGame(node[-1][-1]):
            return node
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            gCost = cost(node)
            allNextMoves = nextMoves(node[-1][0], node[-1][1]) 
            for move in allNextMoves:
                newPosActor, newPosBox = updateState(node[-1][0], node[-1][1], move)
                if not isFailed(newPosBox):
                    priorityQueue.push(node + [(newPosActor, newPosBox)], heuristic(newPosActor, newPosBox) + gCost)
    return []


def printResult(node, name):   
    maxHeight = len(initial) # max width display of game
    maxWidth = max(len(i) for i in initial) - 1 # max height display of game
    with open("solutions/" + filename, "w") as f:
        for nd in node:
            for i in range(0, maxWidth):
                for j in range(0, maxHeight):
                    ch = ' '
                    position = (i, j)
                    if position in posGoals:
                        if position in nd[1]:
                            ch = 'O'
                        elif position == nd[0]:
                            ch = 'B'
                        else:
                            ch = '_'
                    elif position in posWalls:
                        ch = '#'
                    elif position in nd[1]:
                        ch = 'X'
                    elif position == nd[0]:
                        ch = 'A'
                    f.write(ch)
                f.write('\n')
            f.write('\n')
   


if __name__ == '__main__':
    # select type input of game
    while True:
        type = input("Select input type (1 - Mini Comos, 2 - Mirco Comos): ")
        if type in ["1", "2"]:
            break

    # select lever input of game
    while True:
        lever = input("Select lever (1 - 60): ")
        if lever in ["1", "2"]:
            break

    filename = "{0}-{1}.txt".format("mini" if type == "1" else "micro", lever)
    # read game input from files in folder test/
    with open("test/" + filename,"r") as f:
        initial = f.readlines()

    state = transferToState(initial)
    posWalls = wallPosition(state)
    posGoals = goalPosition(state)

    startTime = time.time()
    result = aSearchAlgorithm()
    endTime=time.time()

    print("Runtime: {0} second.".format(endTime - startTime))

    if result:
        printResult(result, filename)
    else:
        print("Can't find the solution")