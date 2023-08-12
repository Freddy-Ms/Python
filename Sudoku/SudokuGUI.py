import requests
import pygame
import time
pygame.font.init()
pygame.init()
#Global - Customize
#________________________________________
FONT = pygame.font.SysFont("Arial", 40) #|
BLACK = (0,0,0)                         #|
RED = (255,0,0)                         #|
WHITE = (255,255,255)                   #|
GREEN = (0,128,0)                       #|
GRAY = (128,128,128)                    #|
WIDTH = 940                             #|
HEIGHT = 980                            #|
XOFF =  20                              #|
TXTGAP = 60                             #|
#________________________________________
class Board:
    def get_sudoku(self):
        url = f"https://sudoku-api.vercel.app/api/dosuku"
        data = requests.get(url).json().get("newboard").get("grids")
        game = data[0]["value"]
        solution = data[0]["solution"]
        return game, solution
    
    
    def __init__(self,window,rows,columns,width,height):
        self.board, self.solution = self.get_sudoku()
        self.window = window
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.selected = None
        self.cubes = [[Cube(self.board[i][j],i,j,width,height) for j in range(columns)] for i in range(rows)]
    def draw(self):
        width_gap = self.width / 9
        height_gap = self.height / 9
        for i in range(10):
            if i % 3 == 0:
                thick = 5
            else:
                thick = 2
            pygame.draw.line(self.window, BLACK, (XOFF + i*width_gap, XOFF), (XOFF + i*width_gap, HEIGHT - TXTGAP), thick)
            pygame.draw.line(self.window,BLACK,(XOFF,XOFF + i * height_gap),(WIDTH- XOFF,XOFF + i*height_gap),thick)
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].draw(self.window)
    def chose(self,position):
        s,t = position
        if s < XOFF or s > WIDTH - XOFF or t<XOFF or t > HEIGHT - TXTGAP:
            return None
        else:
            s = s-XOFF
            t = t-XOFF
            width_gap = self.width / 9
            height_gap = self.height / 9
            x = s // width_gap
            y = t // height_gap
            return(int(y),int(x)) 
    def select(self,row,col):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row,col) 
    def sketch(self,value):
        row, col = self.selected
        self.cubes[row][col].set_temp(value)   
    def clear(self):
        row,col = self.selected
        self.cubes[row][col].set_temp(0)   
    def place(self,value):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            if self.cubes[row][col].temp == self.solution[row][col]:
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                return False 
    def end_game(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.cubes[i][j].value == 0:
                    return False
        return True        

class Cube:
    rows = 9
    columns = 9
    def __init__(self, value,row,col,width,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
    def draw(self,window):
        width_gap = self.width / 9
        height_gap = self.height / 9
        x = self.col * width_gap
        y = self.row * height_gap
        if self.temp != 0 and self.value == 0:
            display = FONT.render(str(self.temp),1,GRAY)
            window.blit(display,(x+10+XOFF,y+10+XOFF))
        elif not(self.value == 0):
            display = FONT.render(str(self.value),1, BLACK)  
            window.blit(display,(x+XOFF+(width_gap/2 - display.get_width()/2),y+XOFF + (height_gap/2 - display.get_height()/2)))     
       
        if self.selected:
            pygame.draw.rect(window,GREEN,(x+XOFF,y+XOFF,width_gap, height_gap),5)
    def set(self,value):
        self.value = value
    def set_temp(self,value):
        self.temp = value    
def draw_whole_window(window,board,time,fails):
    window.fill(WHITE)
    
    display = FONT.render("Time: " + time_display(time),1,BLACK)
    window.blit(display,(WIDTH - 200,(HEIGHT - TXTGAP)+(TXTGAP/2 - display.get_height()/2)))

    display = FONT.render("X " * fails,1,RED)
    window.blit(display,(60,(HEIGHT - TXTGAP)+(TXTGAP/2 - display.get_height()/2)))

    board.draw()
def time_display(seconds):
    sec = seconds % 60
    minutes = (seconds // 60) % 60
    hours = seconds // 3600
    if hours == 0:
        time = f"{minutes}:{sec}"
    else:
        time =f"{hours}:{minutes}:{sec}"
    return time
def main():
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    window.fill(WHITE)
    pygame.display.set_caption("Sudoku")
    board = Board(window,9,9,WIDTH - 2*XOFF, HEIGHT - TXTGAP - XOFF)
    running = True
    key = None
    start = time.time()
    fails = 0
    while running:
        time_play = round(time.time()- start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                if board.selected and event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if board.selected and event.key == pygame.K_RETURN or event.key == pygame.KSCAN_RETURN:
                    i,j = board.selected  
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            board.cubes[i][j].set(board.cubes[i][j].temp) 
                        else:
                            if board.cubes[i][j].value == 0:
                                fails +=1
                        key = None  
                        

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = pygame.mouse.get_pos()
                chosen = board.chose(position) 
                if chosen:
                    board.select(chosen[0],chosen[1])      
                    key = None  
        if board.selected and key != None:
            board.sketch(key)
        draw_whole_window(window,board,time_play,fails)
        pygame.display.update()   
        if board.end_game() == True:             
            running = False 
            window.fill(GREEN)
            display = FONT.render("Congratulations! Do you wanna play again?", RED, True)
            window.blit(display,(WIDTH/2 - display.get_width()/2,HEIGHT/2 - display.get_height()/2))
            display = FONT.render("Press R - Restart",RED,1)
            window.blit(display,(WIDTH/2 - display.get_width()/2,HEIGHT/2+ display.get_height()))
            display = FONT.render("Press Q - Quit", RED,1)
            window.blit(display,(WIDTH/2 - display.get_width()/2,HEIGHT/2+ 2* display.get_height()))
            pygame.display.update()  
    run = True
    while run and board.end_game() == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                   run = False
                   main()
                if event.key == pygame.K_q:
                    run = False
                    
            
if __name__ == "__main__":
    main()
    pygame.quit()

