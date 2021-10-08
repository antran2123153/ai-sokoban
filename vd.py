import heapq
import time
import collections
import numpy as np


def makeGameState(input):
    height = len(input)
    input = [x.replace('\n','') for x in input]
    input = [','.join(input[i]) for i in range(height)]
    input = [x.split(',') for x in input]
    maxCol = max([len(x) for x in input])

    for irow in range(height):
        for icol in range(len(input[irow])):
            if input[irow][icol] == ' ': input[irow][icol] = 0
            elif input[irow][icol] == '#': input[irow][icol] = 1
            elif input[irow][icol] == 'A': input[irow][icol] = 2
            elif input[irow][icol] == 'X': input[irow][icol] = 3
            elif input[irow][icol] == '_': input[irow][icol] = 4
            elif input[irow][icol] == 'O': input[irow][icol] = 5
            elif input[irow][icol] == 'E': input[irow][icol] = 6
        colsNum = len(input[irow])
        if colsNum < maxCol:
            input[irow].extend([1 for _ in range(maxCol-colsNum)])
    
    array = np.array(input)
    posWalls = tuple(tuple(x) for x in np.argwhere(array == 1))
    posGoals = tuple(tuple(x) for x in np.argwhere((array == 4) | (array == 5) | (array == 6)))
    initialBoxs = tuple(tuple(x) for x in np.argwhere((array == 3) | (array == 5)))
    initialActor = tuple(np.argwhere((array == 2) | (array == 6))[0])

    return (posWalls, posGoals, initialBoxs, initialActor)

def isWInGame(posBoxs):
    return sorted(posBoxs) == sorted(posGoals)

def isValidMove(move, posActor, posBoxs):
    xActor, yActor = posActor
    if move[-1]:
        xNext, yNext = xActor + 2 * move[0], yActor + 2 * move[1]
    else:
        xNext, yNext = xActor + move[0], yActor + move[1]
    return (xNext, yNext) not in posBoxs + posWalls

def nextMoves(posActor, posBoxs):
    xActor, yActor = posActor
    allNextMoves = []
    for move in [[-1, 0],[1, 0],[0, -1],[0, 1]]:
        xNext, yNext = xActor + move[0], yActor + move[1]
        if (xNext, yNext) in posBoxs:
            move.append(True)
        else:
            move.append(False) 
        if isValidMove(move, posActor, posBoxs):
            allNextMoves.append(move)
    return tuple(tuple(x) for x in allNextMoves)

def updateState(posActor, posBoxs, move):
    xActor, yActor = posActor
    newPosActor = [xActor + move[0], yActor + move[1]]
    posBoxs = [list(x) for x in posBoxs]

    if move[-1]:
        posBoxs.remove(newPosActor)
        posBoxs.append([xActor + 2 * move[0], yActor + 2 * move[1]])

    newPosBoxs = tuple(tuple(x) for x in posBoxs)
    newPosActor = tuple(newPosActor)
    return newPosActor, newPosBoxs

def isFailed(posBoxs):
    rotatePattern = [[0,1,2,3,4,5,6,7,8],
                    [2,5,8,1,4,7,0,3,6],
                    [0,1,2,3,4,5,6,7,8][::-1],
                    [2,5,8,1,4,7,0,3,6][::-1]]
    flipPattern = [[2,1,0,5,4,3,8,7,6],
                    [0,3,6,1,4,7,2,5,8],
                    [2,1,0,5,4,3,8,7,6][::-1],
                    [0,3,6,1,4,7,2,5,8][::-1]]
    allPattern = rotatePattern + flipPattern

    for box in posBoxs:
        if box not in posGoals:
            board = [(box[0] - 1, box[1] - 1), (box[0] - 1, box[1]), (box[0] - 1, box[1] + 1), 
                    (box[0], box[1] - 1), (box[0], box[1]), (box[0], box[1] + 1), 
                    (box[0] + 1, box[1] - 1), (box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)]
            for pattern in allPattern:
                newBoard = [board[i] for i in pattern]
                if newBoard[1] in posWalls and newBoard[5] in posWalls: 
                    return True
                elif newBoard[1] in posBoxs and newBoard[2] in posWalls and newBoard[5] in posWalls: 
                    return True
                elif newBoard[1] in posBoxs and newBoard[2] in posWalls and newBoard[5] in posBoxs: 
                    return True
                elif newBoard[1] in posBoxs and newBoard[2] in posBoxs and newBoard[5] in posBoxs: 
                    return True
                elif newBoard[1] in posBoxs and newBoard[6] in posBoxs and newBoard[2] in posWalls and newBoard[3] in posWalls and newBoard[8] in posWalls: 
                    return True
    return False

def heuristicFunction(posActor, posBoxs):
    distance = 0
    completes = set(posGoals) & set(posBoxs)
    sortedPosBoxs = list(set(posBoxs).difference(completes))
    sortedPosBoxs = list(set(posGoals).difference(completes))

    for i in range(len(sortedPosBoxs)):
        distance += (abs(sortedPosBoxs[i][0] - sortedPosBoxs[i][0])) + (abs(sortedPosBoxs[i][1] - sortedPosBoxs[i][1]))
    return distance

def costFunction(node):
    return len([nd for nd in node if nd[-1]])

def aStarAlgorithm(): 
    priorityQueue = []
    saveNode = [(initialActor, initialBoxs)]
    priority = heuristicFunction(initialActor, initialBoxs)
    heapq.heappush(priorityQueue,(priority, saveNode)) 
    exploredSet = set()

    while priorityQueue:
        (_, node) = heapq.heappop(priorityQueue) 
        if isWInGame(node[-1][-1]):
            return node
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            cost = costFunction(node)
            allNextMoves = nextMoves(node[-1][0], node[-1][1]) 
            for move in allNextMoves:
                newPosActor, newPosBox = updateState(node[-1][0], node[-1][1], move)
                if not isFailed(newPosBox):
                    saveNode = node + [(newPosActor, newPosBox)]
                    priority = heuristicFunction(newPosActor, newPosBox) + cost
                    heapq.heappush(priorityQueue,(priority, saveNode)) 
    return []

def DFSalgorithm():
    startState = (initialActor, initialBoxs)
    frontier = collections.deque([[startState]])
    exploredSet = set()
    actions = [[0]]

    while frontier:
        node = frontier.pop()
        node_action = actions.pop()
        if isWInGame(node[-1][-1]):
            return node
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            for action in nextMoves(node[-1][0], node[-1][1]):
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)
                if not isFailed(newPosBox):
                    frontier.append(node + [(newPosPlayer, newPosBox)])
                    actions.append(node_action + [action[-1]])
    return []

def printResult():
    maxHeight = len(initial)
    maxWidth = max([len(i) for i in initial]) - 1
    with open("solutions/" + filename, "w") as f:
        for rs in result:
            for i in range(0, maxWidth):
                for j in range(0, maxHeight):
                    ch = ' '
                    position = (i, j)
                    if position in posGoals:
                        if position in rs[1]:
                            ch = 'O'
                        elif position == rs[0]:
                            ch = 'B'
                        else:
                            ch = '_'
                    elif position in posWalls:
                        ch = '#'
                    elif position in rs[1]:
                        ch = 'X'
                    elif position == rs[0]:
                        ch = 'A'
                    f.write(ch)
                f.write('\n')
            f.write('\n')
   
   
if __name__ == '__main__':
    while True:
        type = input("Select input type (1 - Mini Comos, 2 - Mirco Comos): ")
        if type in ["1", "2"]:
            break
    while True:
        lever = input("Select lever (1 - 60): ")
        if lever in ["1", "2"]:
            break
    while True:
        alg = input("Select search algorithm (1 - DFS algorithm, 2 - A start algorithm): ")
        if alg in ["1", "2"]:
            break

    filename = "{0}-{1}.txt".format("mini" if type == "1" else "micro", lever)
    with open("test/" + filename,"r") as f:
        initial = f.readlines()

    (posWalls, posGoals, initialBoxs, initialActor)  = makeGameState(initial)

    startTime = time.time()
    if alg == "1":
        print("Using the DFS algorithm to solve...")
        result = DFSalgorithm()
    else:
        print("Using the A start algorithm to solve...")
        result = aStarAlgorithm()
    endTime=time.time()

    print("Runtime: {0} second.".format(endTime - startTime))

    if result:
        print("Total step: ", len(result))
        printResult()
    else:
        print("Can't find the solution")