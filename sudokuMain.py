from tkinter import *

def isComplete(board):
    for row in range(9):
        for col in range(9):
            if not board[row][col]:
                return False
    return True


def findEmpty(board):
    for row in range(9):
        for col in range(9):
            if not board[row][col]:
                return (row, col)
    return None


def checkCol(board, num, col):
    for eachNum in range(9):
        if board[eachNum][col] == num:
            return False
    return True


def checkRow(board, num, row):
    for eachNum in range(9):
        if board[row][eachNum] == num:
            return False
    return True


def checkSquare(board, num, row, col):
    for i in range((row // 3) * 3, (row // 3) * 3 + 3):
        for j in range((col // 3) * 3, (col // 3) * 3 + 3):
            if board[i][j] == num:
                return False
    return True


def validMove(board, num, pos):
    return checkCol(board, num, pos[1]) and checkRow(board, num, pos[0]) and checkSquare(board, num, pos[0], pos[1])


def draw(board, data, canvas):
    row = data.nextPos[0]
    col = data.nextPos[1]
    x1 = data.distanceBetweenLine * col
    y1 = data.distanceBetweenLine * row
    x2 = (data.distanceBetweenLine * col) + data.distanceBetweenLine
    y2 = (data.distanceBetweenLine * row) + data.distanceBetweenLine

    canvas.create_rectangle(x1, y1, x2, y2, outline="orange", width=1)

def initialDraw(canvas, data, color):
    for row in range(len(data.grid)):
        for col in range(len(data.grid[row])):
            if data.grid[row][col] != 0:
                canvas.create_text((data.distanceBetweenLine*col)+(data.distanceBetweenLine/2),
                                   (data.distanceBetweenLine*row)+(data.distanceBetweenLine/2),
                                   fill=color, text=data.grid[row][col], font="Arial 20")

def solve(board):
    if isComplete(board):
        return board
    nextPos = findEmpty(board)  # nextPos is a tuple of (row, col)
    for possibleNum in range(1, 10):
        currentNum = possibleNum
        if validMove(board, possibleNum, (nextPos[0], nextPos[1])):
            board[nextPos[0]][nextPos[1]] = possibleNum
            tmpSolution = solve(board)
            if tmpSolution != None:
                return tmpSolution
            board[nextPos[0]][nextPos[1]] = 0
    return None


####################################
# Tkinter functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.start = False
    data.grid = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                 [5, 2, 0, 0, 0, 0, 0, 0, 0],
                 [0, 8, 7, 0, 0, 0, 0, 3, 1],
                 [0, 0, 3, 0, 1, 0, 0, 8, 0],
                 [9, 0, 0, 8, 6, 3, 0, 0, 5],
                 [0, 5, 0, 0, 9, 0, 6, 0, 0],
                 [1, 3, 0, 0, 0, 0, 2, 5, 0],
                 [0, 0, 0, 0, 0, 0, 0, 7, 4],
                 [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    data.nextPos = (0, 0)
    data.currentNum = 0
    data.distanceBetweenLine = 0



def mousePressed(event, data):
    # use event.x and event.y
    pass


def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Return":
        data.start = True
        solve(data.grid)


def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    data.distanceBetweenLine = data.width / 9
    # print(distanceBetweenLine)
    for rowLine in range(1, 9):
        if rowLine % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        canvas.create_line(0, data.distanceBetweenLine * rowLine, data.height, data.distanceBetweenLine * rowLine,
                           fill="black", width=thickness)
        # print(distanceBetweenLine * rowLine)

    for colLine in range(1, 9):
        if colLine % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        canvas.create_line(data.distanceBetweenLine * colLine, 0, data.distanceBetweenLine * colLine, data.width,
                           fill="black", width=thickness)

    if data.start:
        initialDraw(canvas, data, "grey")
    else:
        initialDraw(canvas, data, "black")






####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


if __name__ == "__main__":
    run(800, 800)
def testCase():
    grid1 = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
             [5, 2, 0, 0, 0, 0, 0, 0, 0],
             [0, 8, 7, 0, 0, 0, 0, 3, 1],
             [0, 0, 3, 0, 1, 0, 0, 8, 0],
             [9, 0, 0, 8, 6, 3, 0, 0, 5],
             [0, 5, 0, 0, 9, 0, 6, 0, 0],
             [1, 3, 0, 0, 0, 0, 2, 5, 0],
             [0, 0, 0, 0, 0, 0, 0, 7, 4],
             [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    grid1answer = [[3, 1, 6, 5, 7, 8, 4, 9, 2],
                   [5, 2, 9, 1, 3, 4, 7, 6, 8],
                   [4, 8, 7, 6, 2, 9, 5, 3, 1],
                   [2, 6, 3, 4, 1, 5, 9, 8, 7],
                   [9, 7, 4, 8, 6, 3, 1, 2, 5],
                   [8, 5, 1, 7, 9, 2, 6, 4, 3],
                   [1, 3, 8, 9, 4, 7, 2, 5, 6],
                   [6, 9, 2, 3, 5, 1, 8, 7, 4],
                   [7, 4, 5, 2, 8, 6, 3, 1, 9]]

    grid2 = [[3, 1, 6, 5, 7, 8, 4, 9, 2],
             [5, 2, 9, 1, 3, 4, 7, 6, 8],
             [4, 8, 7, 6, 2, 9, 5, 3, 1],
             [2, 6, 3, 0, 1, 5, 9, 8, 7],
             [9, 7, 4, 8, 6, 0, 1, 2, 5],
             [8, 5, 1, 7, 9, 2, 6, 4, 3],
             [1, 3, 8, 0, 4, 7, 2, 0, 6],
             [6, 9, 2, 3, 5, 1, 8, 7, 4],
             [7, 4, 5, 0, 8, 6, 3, 1, 0]]

    grid2answer = [[3, 1, 6, 5, 7, 8, 4, 9, 2],
                   [5, 2, 9, 1, 3, 4, 7, 6, 8],
                   [4, 8, 7, 6, 2, 9, 5, 3, 1],
                   [2, 6, 3, 4, 1, 5, 9, 8, 7],
                   [9, 7, 4, 8, 6, 3, 1, 2, 5],
                   [8, 5, 1, 7, 9, 2, 6, 4, 3],
                   [1, 3, 8, 9, 4, 7, 2, 5, 6],
                   [6, 9, 2, 3, 5, 1, 8, 7, 4],
                   [7, 4, 5, 2, 8, 6, 3, 1, 9]]

    assert (solve(grid1) == grid1answer)
    assert (solve(grid2) == grid2answer)


