import collections
import heapq
import sys
import time

import numpy as np


class PriorityQueue:
    """data structure implement priority queue"""
    def  __init__(self):
        """initial structure with queue empty and element number = 0"""
        self.queue = [] # priority queue whose priority is estimated from the heuristic function
        self.count = 0 # number of all elements in priority queue

    def push(self, element, priority):
        """add a element"""
        newElement = (priority, self.count, element)
        heapq.heappush(self.queue, newElement) # Push new element item onto the queue
        self.count += 1

    def pop(self):
        """get a element from """
        (_, _, item) = heapq.heappop(self.queue) # Pop and return the smallest element from the queue
        return item

    def isEmpty(self):
        """check if queue is empty"""
        return len(self.queue) == 0


def transferToGameState(layout):
    """Transfer the layout of initial puzzle"""
    layout = [x.replace('\n','') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    maxColsNum = max([len(x) for x in layout])

    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == ' ': layout[irow][icol] = 0   # free space
            elif layout[irow][icol] == '#': layout[irow][icol] = 1 # wall
            elif layout[irow][icol] == '&': layout[irow][icol] = 2 # Actor
            elif layout[irow][icol] == 'B': layout[irow][icol] = 3 # box
            elif layout[irow][icol] == '.': layout[irow][icol] = 4 # goal
            elif layout[irow][icol] == 'X': layout[irow][icol] = 5 # box on goal
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 
    return np.array(layout)


def actorPosition(gameState):
    """get position of Actor"""
    return tuple(np.argwhere(gameState == 2)[0]) # e.g. (2, 2)


def boxPosition(gameState):
    """get positions of boxes"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 3) | (gameState == 5))) # e.g. ((2, 3), (3, 4), (4, 4), (6, 1), (6, 4), (6, 5))


def wallPosition(gameState):
    """get positions of walls"""
    return tuple(tuple(x) for x in np.argwhere(gameState == 1)) # e.g. like those above


def goalPosition(gameState):
    """get positions of goals"""
    return tuple(tuple(x) for x in np.argwhere((gameState == 4) | (gameState == 5))) # e.g. like those above


def isWInGame(posBox):
    """check if the game was won"""
    return sorted(posBox) == sorted(posGoals) # check the positions of the boxes are fully located at the position of the goal


def isValidMove(move, posActor, posBox):
    """check if the move is valid or not"""
    xActor, yActor = posActor
    if move[-1].isupper(): # actor push the box
        xNext, yNext = xActor + 2 * move[0], yActor + 2 * move[1]
    else: # move to empty space
        xNext, yNext = xActor + move[0], yActor + move[1]
    return (xNext, yNext) not in posBox + posWalls # the location must not coincide with the wall or box


def nextMoves(posActor, posBox):
    """check and return all next valid moves"""
    xActor, yActor = posActor # current coordinates of actor
    allNextMoves = []
    for move in [[-1, 0, 'u', 'U'],[1, 0, 'd', 'D'],[0, -1, 'l', 'L'],[0, 1, 'r', 'R']]: # left, top, down, right move
        xNext, yNext = xActor + move[0], yActor + move[1] # actor move
        if (xNext, yNext) in posBox: # actor push the box
            move.pop(2) # delete lower case character
        else:
            move.pop(3) # delete upper case character
        if isValidMove(move, posActor, posBox):
            allNextMoves.append(move)
    return tuple(tuple(x) for x in allNextMoves) # return all next valid moves


def updateState(posActor, posBox, move):
    """updated state after moving"""
    xActor, yActor = posActor # previous position of actor
    newPosActor = [xActor + move[0], yActor + move[1]] # current position of Actor
    posBox = [list(x) for x in posBox]
    if move[-1].isupper(): # if actor push the box, update position of box
        posBox.remove(newPosActor) # remove the pushed box
        posBox.append([xActor + 2 * move[0], yActor + 2 * move[1]]) # add box in new position pushed
    posBox = tuple(tuple(x) for x in posBox)
    newPosActor = tuple(newPosActor)
    return newPosActor, posBox # return new position of actor and boxs


def isFailed(posBox):
    """observe if the state is potentially failed, then prune the search"""
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


def heuristic(posActor, posBox):
    """estimate the total distance from the boxes to the  goals"""
    distance = 0
    completes = set(posGoals) & set(posBox) # positions box at goal 
    sortposBox = list(set(posBox).difference(completes)) # positions box not at goal
    sortposGoals = list(set(posGoals).difference(completes)) # positions goal not contain box
    for i in range(len(sortposBox)):
        distance += (abs(sortposBox[i][0] - sortposGoals[i][0])) + (abs(sortposBox[i][1] - sortposGoals[i][1]))
    return distance


def cost(moves):
    """costs calculation from start to current state"""
    return len([x for x in moves if x.islower()])


def aSearchAlgorithm():
    """A* search algorithm"""
    beginBox = boxPosition(gameState) # get position of boxs
    beginActor = actorPosition(gameState) # get position of actor

    initial = (beginActor, beginBox)
    priorityQueue = PriorityQueue() 
    priorityQueue.push([initial], heuristic(beginActor, beginBox)) 
    exploredSet = set()
    moves = PriorityQueue()
    moves.push([0], heuristic(beginActor, initial[1]))
    while priorityQueue:
        node = priorityQueue.pop()
        node_move = moves.pop()
        if isWInGame(node[-1][-1]):
            print(','.join(node_move[1:]).replace(',',''))
            break
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            Cost = cost(node_move[1:])
            for move in nextMoves(node[-1][0], node[-1][1]):
                newPosActor, newPosBox = updateState(node[-1][0], node[-1][1], move)
                if isFailed(newPosBox):
                    continue
                Heuristic = heuristic(newPosActor, newPosBox)
                priorityQueue.push(node + [(newPosActor, newPosBox)], Heuristic + Cost) 
                moves.push(node_move + [move[-1]], Heuristic + Cost)


"""Read command"""
def readCommand(argv):
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option('-l', '--level', dest='sokobanLevels',
                      help='level of game to play', default='level1.txt')
    parser.add_option('-m', '--method', dest='agentMethod',
                      help='research method', default='bfs')
    args = dict()
    options, _ = parser.parse_args(argv)
    with open('test/' + options.sokobanLevels,"r") as f: 
        layout = f.readlines()
    args['layout'] = layout
    args['method'] = options.agentMethod
    return args

if __name__ == '__main__':
    time_start = time.time()
    layout, method = readCommand(sys.argv[1:]).values()

    gameState = transferToGameState(layout)
    posWalls = wallPosition(gameState)
    posGoals = goalPosition(gameState)

    if method == 'astar':
        aSearchAlgorithm()
    else:
        raise ValueError('Invalid method.')

    time_end=time.time()
    print('Runtime of %s: %.2f second.' %(method, time_end-time_start))
