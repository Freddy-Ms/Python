import pygame
import random
import time
pygame.font.init()

WIDTH = 1600
HEIGHT = 1000
BODY_SIZE = SNAKE_SPEED = 50
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
FONT = pygame.font.SysFont("Arial", 40)

class Snake:
    def __init__(self):
        self.size = 2
        self.coordinates =[(WIDTH//2,HEIGHT//2),(WIDTH//2 - BODY_SIZE,HEIGHT//2)]
        self.direction = "right"
    def change_direction(self,direction):
        if direction == "right" and self.direction != "left":
            self.direction = "right"
        if direction == "left" and self.direction != "right":
            self.direction = "left"
        if direction == "down" and self.direction != "up":
            self.direction = "down"        
        if direction == "up" and self.direction != "down":
            self.direction = "up"
    def move(self):
        x,y = self.coordinates[0]
        if self.direction == "right":
            x += SNAKE_SPEED
        if self.direction == "left":
            x -= SNAKE_SPEED
        if self.direction == "up":
            y -= SNAKE_SPEED
        if self.direction == "down":
            y += SNAKE_SPEED
        self.coordinates.insert(0,(x,y))
        self.coordinates.pop()
    def check_collisions(self):
        head = self.coordinates[0]
        if head in self.coordinates[1:]:
            return True
        if head[0] < BODY_SIZE or head[0] > WIDTH - BODY_SIZE or head[1] < BODY_SIZE or head[1] > HEIGHT - BODY_SIZE:
            return True
        return False
    def draw(self,window,score):
        for segment in self.coordinates:
            pygame.draw.rect(window,GREEN,pygame.Rect(segment[0],segment[1],BODY_SIZE-0.1,BODY_SIZE-0.1))
        display = FONT.render(str(score),1, (255,255,255))
        window.blit(display,(WIDTH- 50, HEIGHT - 50))
class Food:
    def __init__(self):
        self.position= (random.randint(0, (WIDTH // BODY_SIZE)-1) * BODY_SIZE, random.randint(0, (HEIGHT// BODY_SIZE)-1) * BODY_SIZE)
    def new_position(self):
        self.position= (random.randint(0, (WIDTH // BODY_SIZE)-1) * BODY_SIZE, random.randint(0, (HEIGHT// BODY_SIZE)-1) * BODY_SIZE)
    def draw(self,window):
        pygame.draw.rect(window, RED, pygame.Rect(self.position[0], self.position[1], BODY_SIZE, BODY_SIZE))            
def main():
    running = True
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Snake")
    timee = pygame.time.Clock()
    snake = Snake()
    food = Food()
    SCORE = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake.change_direction("up")
                elif event.key == pygame.K_s:
                    snake.change_direction("down")
                elif event.key == pygame.K_d:
                    snake.change_direction("right")
                elif event.key == pygame.K_a:
                    snake.change_direction("left")
        snake.move()
        if snake.coordinates[0] == food.position:
            SCORE += 1
            last_segment = snake.coordinates[-1]
            snake.coordinates.append((last_segment[0],last_segment[1]))
            food.new_position()
        if snake.check_collisions():
            running = False
        snake.food = False
        window.fill(BLACK)
        snake.draw(window,SCORE)
        food.draw(window)
        pygame.display.update()
        timee.tick(20)
    main()

if __name__ == "__main__":
    main()
    pygame.quit()
