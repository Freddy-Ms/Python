import pygame
import sys
import textwrap
pygame.font.init()
pygame.init()
FONT = pygame.font.SysFont("Arial", 40)
WIDTH = 1800
HEIGHT = 900
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (128,128,128)
PLAYERGAP = 100
XOFF = YOFF = 20
CATEGORIES = ["Matematyka","Fizyka","Muzyka","Astronomia","Chemia","cos0","cos3"]
PLAYERS = ["Daniel","Maciek","Kacper","Michał","As","xd"]
NUMBER_OF_PLAYERS = len(PLAYERS) 
PLAYER_WIDTH = 150
class Board:
    def read(self):
        try:
            index = 0
            q_board =[[[]for i in range(self.columns)] for j in range(self.rows)]
            a_board =[[[]for i in range(self.columns)] for j in range(self.rows)]
            with open("QuizQuestions.txt",'r') as file:
                words = file.read().splitlines()
            for column in range(self.columns):
                for row in range(self.rows):
                    question = words[index]
                    anserw = words[index+1]
                    q_board[row][column] = question
                    a_board[row][column] = anserw
                    index += 2
            return q_board, a_board
        except FileNotFoundError:
            print(f"File QuizQuestions.txt not found.")  
            return [] 
    def __init__(self,window, width, height, ctg_number):
        self.selected = False
        self.window = window
        self.width = width
        self.height = height
        self.columns = ctg_number 
        self.rows = 5
        self.questions, self.anserws = self.read()
        self.cubes = [[Cube(self.window,self.questions[i][j], self.anserws[i][j],i,j,width,height, value =(i +1)*100) for j in range(self.columns)] for i in range(self.rows)]
        self.player =[Player(window,PLAYERS[i],i,PLAYERGAP,((WIDTH/2)- (NUMBER_OF_PLAYERS * PLAYER_WIDTH / 2) + (PLAYER_WIDTH * i))) for i in range (NUMBER_OF_PLAYERS)]
    def draw(self):
        if not self.selected:
            width_gap = self.width/ self.columns
            height_gap = self.height / (self.rows + 1)
            for i in range(7):
                pygame.draw.line(self.window,BLACK,(XOFF,YOFF + i*height_gap),(XOFF + self.width,YOFF + i*height_gap),2)
            for j in range(self.columns+1):
                pygame.draw.line(self.window,BLACK,(XOFF +j*width_gap,YOFF),(XOFF + j*width_gap,self.height+YOFF),2)
            for x in range(NUMBER_OF_PLAYERS+1):
                pygame.draw.line(self.window,BLACK,((WIDTH/2)- (NUMBER_OF_PLAYERS * PLAYER_WIDTH / 2) + (PLAYER_WIDTH * x),HEIGHT-PLAYERGAP),((WIDTH/2)- (NUMBER_OF_PLAYERS * PLAYER_WIDTH / 2) + (PLAYER_WIDTH * x),HEIGHT),2)
            
            index = 0
            for category in CATEGORIES:
                display = FONT.render(category,BLACK,1)
                self.window.blit(display,((index * width_gap)+XOFF+(width_gap/2 - display.get_width()/2) , YOFF + (height_gap/2 - display.get_height()/2))) 
                index += 1
            
            for col in range(self.columns):
                for row in range(self.rows):
                    self.cubes[row][col].draw()
            for i in range(len(PLAYERS)):
                self.player[i].draw()
        else:
            row,column = self.selected
            self.cubes[row][column].draw()
            pygame.draw.line(self.window,BLACK,(self.player[0].x_pos,HEIGHT-PLAYERGAP),(self.player[NUMBER_OF_PLAYERS-1].x_pos+PLAYER_WIDTH,HEIGHT-PLAYERGAP),2)
            for x in range(NUMBER_OF_PLAYERS+1):
                pygame.draw.line(self.window,BLACK,((WIDTH/2)- (NUMBER_OF_PLAYERS * PLAYER_WIDTH / 2) + (PLAYER_WIDTH * x),HEIGHT-PLAYERGAP),((WIDTH/2)- (NUMBER_OF_PLAYERS * PLAYER_WIDTH / 2) + (PLAYER_WIDTH * x),HEIGHT),2)
            for i in range(len(PLAYERS)):
                self.player[i].draw()
    def click(self,position):
        x,y = position
        width_gap = self.width/ self.columns
        height_gap = self.height / (self.rows + 1)
        if x > XOFF  and x < WIDTH - XOFF and y > YOFF + height_gap and y < HEIGHT-PLAYERGAP:
            x -= XOFF
            y -= YOFF
            x = x // width_gap
            y = y // height_gap
            return(int(y-1),int(x))                                                                                                                   #
        else:
            return None
    def select(self,row,col):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row,col)
        self.selection_cube()
    def clear(self):
        self.selected = False
    def select_player(self,position):
        x,y = position
        if y < HEIGHT and y > HEIGHT-PLAYERGAP and x > self.player[0].x_pos and x < self.player[NUMBER_OF_PLAYERS-1].x_pos + PLAYER_WIDTH:
            x -= self.player[0].x_pos
            x = x // PLAYER_WIDTH
            return int(x)
        else:
            return -1
    def give_points(self,nr_of_player):
        row, col = self.selected
        if nr_of_player > NUMBER_OF_PLAYERS - 1:
            return None
        else:
            self.player[nr_of_player].score += self.cubes[row][col].value
    def selection_cube(self):
        row, col = self.selected
        self.cubes[row][col].selected = True
    def clear_cube(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].selected = False
                self.cubes[i][j].show_anserw = False
    def disable_cube(self):
        row, col = self.selected
        self.cubes[row][col].disabled = True
    def show_anserws(self):
        row,col = self.selected
        self.cubes[row][col].show_anserw = True

class Cube:
    def __init__(self,window,question,anserw,row,column,width,height,value):
        self.window = window
        self.question = question
        self.anserw = anserw
        self.row = row+1
        self.column = column
        self.width = width
        self.height = height
        self.selected = False
        self.show_anserw = False
        self.value = value
        self.disabled = False
    def draw(self):
        width_gap = self.width/ len(CATEGORIES)
        height_gap = self.height / 6
        x = self.column * width_gap
        y = self.row * height_gap
        if not self.selected:
            if not self.disabled:
                display = FONT.render(str(self.value),1,BLACK)
                self.window.blit(display,(x+XOFF+(width_gap/2 - display.get_width()/2),y+YOFF + (height_gap/2 - display.get_height()/2)))   
            else:
                display = FONT.render(str(self.value),1,GRAY)
                self.window.blit(display,(x+XOFF+(width_gap/2 - display.get_width()/2),y+YOFF + (height_gap/2 - display.get_height()/2))) 
        else:
            display = FONT.render(self.question,BLACK,1)
            y_pos = 50
            display = wrap_text(self.question,FONT,display.get_width())
            for line in display:
                self.window.blit(line,(WIDTH/2-line.get_width()/2,y_pos))
                y_pos +=  line.get_height() + 10
        if self.show_anserw:
            display = FONT.render(self.anserw,BLACK,1)
            self.window.blit(display,(WIDTH/2 - display.get_width()/2,y_pos+30))
class Player:
    def __init__(self,window,name,counter,height,x):
        self.window = window
        self.name = name
        self.score = 0
        self.player_number = counter
        self.width = PLAYER_WIDTH
        self.height = height
        self.x_pos = x
    def draw(self):
        display = FONT.render(str(self.name),BLACK,1)
        self.window.blit(display,(self.x_pos+PLAYER_WIDTH/2 - display.get_width()/2,HEIGHT-self.height))
        display = FONT.render(str(self.score),BLACK,1)
        self.window.blit(display,(self.x_pos+PLAYER_WIDTH/2 - display.get_width()/2,HEIGHT- (self.height/2)))
            
def wrap_text(text,font,txt_width):
    nr_of_lines = (txt_width // (WIDTH - 20)) + 1
    center = int(txt_width / nr_of_lines)
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word #if current_line else word
        test_width, _ = font.size(test_line)
        
        if test_width <= center:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    
    lines.append(current_line)
    rendered_lines = [font.render(line, True, BLACK) for line in lines]
    return rendered_lines
   


def draw_whole_window(window,board):
    window.fill(WHITE)
    board.draw()

def main():
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Quiz")
    board = Board(window,WIDTH-2*XOFF, HEIGHT - PLAYERGAP - YOFF,len(CATEGORIES))
    running = True
    while running:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                chosen_question = board.click(pos)
                if chosen_question and board.selected == False:
                    if chosen_question:
                        board.select(chosen_question[0],chosen_question[1])
                        board.disable_cube()
                elif board.selected:
                    click = board.select_player(pos)
                    if click >= 0 and click< NUMBER_OF_PLAYERS:
                        board.give_points(click)
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.clear()
                    board.clear_cube()
                if event.key == pygame.K_SPACE and board.selected:
                    board.show_anserws()

       # print(board.selected)
        draw_whole_window(window,board)  
        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()