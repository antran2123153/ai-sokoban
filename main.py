from abc import abstractmethod
import heapq
import time
import collections
import numpy as np

####################################################################################################
# Hàm makeGameState
# Input: mảng các string tương ứng với các dòng ký tự thể hiện trong game
# Output: 4 tuple tương ứng với 4 đối tượng thể hiện vị trí của Wall, Goal, Box, Actor trong game 
####################################################################################################
def makeGameState(input): 
    height = len(input)
    input = [x.replace('\n','') for x in input] # xóa bỏ các ký tự xuống dòng nếu có
    input = [','.join(input[i]) for i in range(height)] # thêm dấu phẩy phân tách các ký tự trong từng chuỗi
    input = [x.split(',') for x in input] # chuyển các chuỗi tương ứng thành mảng các ký tự
    maxWeight = max([len(x) for x in input])

    saveWalls = []

    for i in range(height):
        for j in range(len(input[i])):
            if input[i][j] == ' ': 
                input[i][j] = 0 # ô trống
            elif input[i][j] == '#': 
                input[i][j] = 1 # wall
                saveWalls += [(i, j)]
            elif input[i][j] == 'A': 
                input[i][j] = 2 # actor
            elif input[i][j] == 'X': 
                input[i][j] = 3 # box
            elif input[i][j] == '_': 
                input[i][j] = 4 # goal
            elif input[i][j] == 'O': 
                input[i][j] = 5 # box đang đứng ở goal
            elif input[i][j] == 'E': 
                input[i][j] = 6 # actor đang đứng ở goal
        colsNum = len(input[i])
        if colsNum < maxWeight:
            input[i].extend([1 for _ in range(maxWeight-colsNum)]) # các ô trống phía ngoài wall được xem như wall
    
    array = np.array(input)
    posWalls = tuple(tuple(x) for x in np.argwhere(array == 1)) # tọa độ của các wall
    posGoals = tuple(tuple(x) for x in np.argwhere((array == 4) | (array == 5) | (array == 6))) # tọa độ của các goal
    initialBoxs = tuple(tuple(x) for x in np.argwhere((array == 3) | (array == 5))) # tọa độ của các box
    initialActor = tuple(np.argwhere((array == 2) | (array == 6))[0]) # toạn độ của actor

    return (posWalls, posGoals, initialBoxs, initialActor, saveWalls)

####################################################################################################
# Hàm isWInGame
# Input: vị trí của các Box
# Output: True nếu tất cả Box lần lượt được đặt tại Goal(trạng thái đích), False nếu ngược lại 
####################################################################################################
def isWInGame(posBoxs):
    return sorted(posBoxs) == sorted(posGoals)

####################################################################################################
# Hàm isValidMove
# Input: hướng di chuyển, vị trí của Actor và vị trí của các Box
# Output: True nếu sau nước di chuyển này vị trí mới của Actor và Box là hợp lệ, False nếu ngược lại
####################################################################################################
def isValidMove(move, posActor, posBoxs):
    xActor, yActor = posActor
    if move[-1]:
        xNext, yNext = xActor + 2 * move[0], yActor + 2 * move[1] # actor di chuyển đồng thời đẩy box
    else:
        xNext, yNext = xActor + move[0], yActor + move[1] # actor di chuyển không đẩy box
    return (xNext, yNext) not in posBoxs + posWalls

####################################################################################################
# Hàm nextMoves
# Input: vị trí của Actor và vị trí của các Box
# Output: trả về tất cả các nước đi hợp lệ có thể áp dụng để di chuyển tiếp cho trò chơi
####################################################################################################
def nextMoves(posActor, posBoxs):
    xActor, yActor = posActor
    allNextMoves = []
    for move in [[-1, 0],[1, 0],[0, -1],[0, 1]]: # 4 hướng di chuyển: trên - dưới - trái - phải
        xNext, yNext = xActor + move[0], yActor + move[1]
        if (xNext, yNext) in posBoxs: 
            move.append(True) # actor di chuyển đồng thời đẩy box
        else: 
            move.append(False) # actor di chuyển không đẩy box
        if isValidMove(move, posActor, posBoxs): # kiểm tra để chỉ nhận các nước đi hợp lệ
            allNextMoves.append(move)
    return tuple(tuple(x) for x in allNextMoves)

####################################################################################################
# Hàm updateState
# Input: vị trí của Actor, vị trí của các Box, hướng di chuyển
# Output: trả về 2 đối tượng là vị trí mới của Actor và Box sau khi được di chuyển theo hướng từ input
####################################################################################################
def updateState(posActor, posBoxs, move):
    xActor, yActor = posActor
    newPosActor = [xActor + move[0], yActor + move[1]]
    posBoxs = [list(x) for x in posBoxs]

    if move[-1]: # khi di chuyển có đẩy box, vị trí box đẩy này là vị trí mới cho actor
        posBoxs.remove(newPosActor)
        posBoxs.append([xActor + 2 * move[0], yActor + 2 * move[1]])

    newPosBoxs = tuple(tuple(x) for x in posBoxs)
    newPosActor = tuple(newPosActor)
    return newPosActor, newPosBoxs

####################################################################################################
# Hàm isFailed
# Input: vị trí của các Box
# Output: True nếu có ít nhất 1 box ở vị trí không an toàn(gây ra trạng thái bí), False nếu ngược lại
####################################################################################################
def isFailed(posBoxs):
    for box in posBoxs: # duyệt qua các box để kiểm tra
        if box in posGoals: # nếu box đã nằm ở goal thì không xét
            continue
        
        if (box[0] + 1, box[1]) in posWalls: # bên phải box là wall
            if ((box[0], box[1] + 1) in posWalls) or ((box[0], box[1] - 1) in posWalls): # phía trên hoặc dưới box là tường
                return True
            if ((box[0], box[1] + 1) in posBoxs) and (box[0] + 1, box[1] + 1) in posWalls: # phía trên có box khác(box này bên phải cũng có wall)
                return True
            if ((box[0], box[1] - 1) in posBoxs) and (box[0] + 1, box[1] - 1) in posWalls: # phía dưới có box khác(box này bên phải cũng có wall)
                return True

        if (box[0] - 1, box[1]) in posWalls: # bên trái box là wall
            if ((box[0], box[1] + 1) in posWalls) or ((box[0], box[1] - 1) in posWalls): # phía trên hoặc dưới box là tường
                return True
            if ((box[0], box[1] + 1) in posBoxs) and (box[0] - 1, box[1] + 1) in posWalls: # phía trên có box khác(box này bên trái cũng có wall)
                return True
            if ((box[0], box[1] - 1) in posBoxs) and (box[0] - 1, box[1] - 1) in posWalls: # phía trên có box khác(box này bên trái cũng có wall)
                return True

        if (box[0], box[1] + 1) in posWalls: # phía trên box là wall
            if ((box[0] + 1, box[1]) in posBoxs) and (box[0] + 1, box[1] + 1) in posWalls: # bên phải có box khác(box này phía trên cũng có wall)
                return True
            if ((box[0] - 1, box[1]) in posBoxs) and (box[0] - 1, box[1] + 1) in posWalls: # bên trái có box khác(box này phía trên cũng có wall)
                return True

        if (box[0], box[1] - 1) in posWalls: # phía dưới box là wall
            if ((box[0] + 1, box[1]) in posBoxs) and (box[0] + 1, box[1] - 1) in posWalls: # bên phải có box khác(box này phía dưới cũng có wall)
                return True
            if ((box[0] - 1, box[1]) in posBoxs) and (box[0] - 1, box[1] - 1) in posWalls: # bên trái có box khác(box này phía dưới cũng có wall)
                return True
    return False

####################################################################################################
# Hàm heuristicFunction
# Input: vị trí của các Box
# Output: giá trị ước tính để có thể từ trạng thái hiện tại đến trạng thái đích, 
# xấp xỉ sử dụng khoảng cách Manhattan
####################################################################################################
def heuristicFunction(posBoxs):
    distance = 0
    completes = set(posGoals) & set(posBoxs) # lấy ra các vị trí mà box và goal trùng nhau
    sortedPosBoxs = list(set(posBoxs).difference(completes)) # bỏ đi các vị trí trùng với goal
    sortedPosGoals = list(set(posGoals).difference(completes)) # bỏ đi các vị trí trùng với box

    for i in range(len(sortedPosBoxs)):
        distance += (abs(sortedPosBoxs[i][0] - sortedPosGoals[i][0])) + (abs(sortedPosBoxs[i][1] - sortedPosGoals[i][1]))
    return distance

####################################################################################################
# Hàm costFunction
# Input: mảng lưu trữ các trạng thái của game từ trạng thái đầu đến trạng thái hiện tại
# Output: chi phí để đi từ trạng thái đầu đến hiện tại = số bước đã đi = độ dài của mảng input
####################################################################################################
def costFunction(node):
    return len(node)

####################################################################################################
# Hàm aStarAlgorithm
# Input: 
# Output: trả về mảng lưu trữ tất cả trạng thái từ trạng thái đầu đến trạng thái đích, nếu
# tìm thấy trang thái đích, trả về mảng rỗng nếu không tìm thấy trạng thái đích
####################################################################################################
def aStarAlgorithm():
    priorityQueue = [] # danh sách được sử dụng như priority queue để hỗ trợ giải thuật
    initialNode = [(initialActor, initialBoxs)] # trạng thái ban đầu của game, chỉ lưu các thành phần động
    priority = heuristicFunction(initialBoxs) 
    heapq.heappush(priorityQueue,(priority, initialNode)) # thêm 1 node vào queue
    exploredSet = set() # bảng hashing để lưu các trạng thái đã từng đi qua

    while priorityQueue:
        (_, node) = heapq.heappop(priorityQueue) # lấy 1 node ra khỏi queue
        if isWInGame(node[-1][-1]):
            return node
        if node[-1] in exploredSet: # bor qua node nếu nó đã từng đi qua
            continue
        exploredSet.add(node[-1]) # đánh dấu node là đã đi qua
        cost = costFunction(node) # g(n)
        allNextMoves = nextMoves(node[-1][0], node[-1][1]) # các bước di chuyển hợp lệ tiếp theo
        for move in allNextMoves:
            newPosActor, newPosBox = updateState(node[-1][0], node[-1][1], move) 
            if not isFailed(newPosBox): # bỏ qua nếu vị trí mới của box dẫn đến trạng thái bí
                saveNode = node + [(newPosActor, newPosBox)] 
                priority = heuristicFunction(newPosBox) + cost # priority = h(n) + g(n)
                heapq.heappush(priorityQueue,(priority, saveNode)) # thêm node vào queue 
    return []

####################################################################################################
# Hàm DFSalgorithm
# Input: 
# Output: trả về mảng lưu trữ tất cả trạng thái từ trạng thái đầu đến trạng thái đích, nếu
# tìm thấy trang thái đích, trả về mảng rỗng nếu không tìm thấy trạng thái đích
####################################################################################################
def DFSalgorithm():
    queue = collections.deque([[(initialActor, initialBoxs)]]) # queue để lưu trữ các trạng thái game
    exploredSet = set() # bảng hashing để lưu các trạng thái đã từng đi qua

    while queue:
        node = queue.pop() # lấy 1 node ra khỏi queue
        if isWInGame(node[-1][-1]):
            return node
        if node[-1] not in exploredSet: # duyệt node nếu chưa đi qua node này
            exploredSet.add(node[-1]) # đánh dấu node là đã duyệt
            for action in nextMoves(node[-1][0], node[-1][1]): # kiểm tra các bước đi hợp lệ tiếp theo
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)
                if not isFailed(newPosBox): # bỏ qua nếu vị trí mới của box dẫn đến trạng thái bí
                    queue.append(node + [(newPosPlayer, newPosBox)]) # thêm node vào queue để chờ duyệt
    return []

####################################################################################################
# Hàm printResult
# In ra kết quả mô tả các bước đi để có thể giải được bài toán sokoban ban đấu
####################################################################################################
def printResult():
    maxHeight = len(initial)
    maxWidth = max([len(i) for i in initial])

    # print(len(posWalls))

    # print(saveWalls)

    with open("outputs/" + filename, "w") as f:
        for rs in result:
            for i in range(maxHeight):
                for j in range(maxWidth - 1):
                    ch = ' '
                    position = (i, j)
                    if position in posGoals:
                        if position in rs[1]:
                            ch = 'O'
                        elif position == rs[0]:
                            ch = 'E'
                        else:
                            ch = '_'
                    elif position in saveWalls:
                        ch = '#'
                    elif position in rs[1]:
                        ch = 'X'
                    elif position == rs[0]:
                        ch = 'A'
                    f.write(ch)
                f.write('\n')
            f.write('\n')
   
####################################################################################################
# MAIN
####################################################################################################
if __name__ == '__main__':
    while True:
        type = input("Select input type (1 - Mini Comos, 2 - Micro Comos): ")
        if type in ["1", "2"]:
            break
    while True:
        lever = input("Select lever (1 - 30): ")
        if int(lever) > 0 and int(lever) <= 30:
            break
    while True:
        alg = input("Select search algorithm (1 - DFS algorithm, 2 - A start algorithm): ")
        if alg in ["1", "2"]:
            break

    filename = "{0}/{1}.txt".format("mini" if type == "1" else "micro", lever)
    with open("inputs/" + filename,"r") as f:
        initial = f.readlines()

    (posWalls, posGoals, initialBoxs, initialActor, saveWalls)  = makeGameState(initial)

    startTime = time.time()
    if alg == "1":
        print("Using the DFS algorithm to solve...")
        result = DFSalgorithm()
    else:
        print("Using the A star algorithm to solve...")
        result = aStarAlgorithm()
    endTime=time.time()

    print("Runtime: {0} second.".format(endTime - startTime))

    if result:
        print("Total step: ", len(result))
        printResult()
    else:
        print("Can't find the solution")