board =[[0,8,7,0,1,5,9,0,0],
        [0,0,2,7,6,3,1,0,0],
        [5,0,0,9,0,0,0,4,0],
        [9,4,0,0,0,0,5,0,3],
        [0,7,5,0,0,0,6,9,0],
        [0,3,0,5,0,9,8,7,2],
        [0,0,0,1,0,0,0,6,9],
        [0,0,0,3,0,6,2,0,0],
        [0,6,0,0,8,4,7,3,0]]

def valid(row,col,value):
    global board
    #Checking for number in row
    for i in range(9):
        if board[row][i] == value:
            return False
    #Checking for number in column
    for i in range(9):
        if board[i][col] == value:
            return False    
    #Checking for number in square 3x3
    x0 = (row // 3) * 3
    y0 = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[x0+i][y0+j] == value:
                return False
    return True        

def solve_sudoku():
    global board
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for value in range(10):
                    if valid(row,col,value):
                        board[row][col] = value
                        solve_sudoku()
                        board[row][col] = 0
                return
    for i in range(9):
        print(board[i])


solve_sudoku()        