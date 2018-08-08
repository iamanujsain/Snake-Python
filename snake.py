import pygame
import random as r
from os import path

pygame.init()
pygame.mixer.init()

'''Widnow size'''
WIDTH = 500
HEIGHT = 400

'''Colours'''
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)

'''Controls frames per second'''
clock = pygame.time.Clock()

''' Sounds '''
sound_dir = path.join(path.dirname(__file__), 'sound_fx')

up = pygame.mixer.Sound(path.join(sound_dir, 'up.wav'))
down = pygame.mixer.Sound(path.join(sound_dir, 'down.wav'))
left = pygame.mixer.Sound(path.join(sound_dir, 'left.wav'))
right = pygame.mixer.Sound(path.join(sound_dir, 'right.wav'))
key_press = pygame.mixer.Sound(path.join(sound_dir, 'keypress.wav'))
eat = pygame.mixer.Sound(path.join(sound_dir, 'eat.wav'))
collision = pygame.mixer.Sound(path.join(sound_dir, 'collision.wav'))

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Snake")
running = True

''' Draws a rectangle '''
def drawRect(x, y, w, h, colour):
    pygame.draw.rect(screen, colour, pygame.Rect(x, y, w, h))

''' Draws text on the screen '''
def drawText(text, x, y, font_size, colour):
    my_font = pygame.font.SysFont("Consolas", font_size)
    text_surface = my_font.render(text, False, colour)
    screen.blit(text_surface, (x, y)) 

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.start_size = 7
        self.start_x = 100
        self.start_y = 100
        self.block_size = 7
        self.dx = 0
        self.dy = 0
        self.isMoving = False
        self.elongate = False
        self.score = 0
        self.snakePoints = []
        for i in range(1, self.start_size+1):
            self.snakePoints.append(Point(self.start_x - (i*self.block_size), self.start_y))

    def draw(self):
        for i in range(len(self.snakePoints)):
            drawRect(self.snakePoints[i].x, self.snakePoints[i].y, self.block_size, self.block_size, WHITE)

    def update(self):
        if self.isMoving:
            first = self.snakePoints[0]
            last = self.snakePoints[len(self.snakePoints)-1]
            new_block = Point(first.x+(self.dx*self.block_size), first.y+(self.dy*self.block_size))
            for i in range((len(self.snakePoints)-1), 0, -1):
                self.snakePoints[i].x = self.snakePoints[i-1].x
                self.snakePoints[i].y = self.snakePoints[i-1].y
            first.x = new_block.x
            first.y = new_block.y
            if self.elongate:
                self.snakePoints.append(Point((last.x + (self.dx*self.block_size)), (last.y + (self.dy*self.block_size))))
                self.elongate = False
                
            if self.snakePoints[0].x < 0 and self.dx == -1:
                self.snakePoints[0].x = WIDTH
            if self.snakePoints[0].x > WIDTH-self.block_size and self.dx == 1:
                self.snakePoints[0].x = -self.block_size
            if self.snakePoints[0].y < 0 and self.dy == -1:
                self.snakePoints[0].y = HEIGHT
            if self.snakePoints[0].y > HEIGHT-self.block_size and self.dy == 1:
                self.snakePoints[0].y = -self.block_size

            self.suicide()
    
    def suicide(self):
        '''The snake dies if it bites itself.'''
        head_x = self.snakePoints[0].x + self.block_size/2
        head_y = self.snakePoints[0].y + self.block_size/2
        for i in range(1, len(self.snakePoints)):
            if head_x >= self.snakePoints[i].x  and head_x <= self.snakePoints[i].x + self.block_size:
                if head_y >= self.snakePoints[i].y and head_y <= self.snakePoints[i].y + self.block_size:
                    collision.play()
                    self.isMoving = False

    def reset(self):
        self.snakePoints = []
        for i in range(1, self.start_size+1):
            self.snakePoints.append(Point(self.start_x - (i*self.block_size), self.start_y))
        self.dx = 1
        self.dy = 0

class Food:
    def __init__(self):
        self.block_size = 7
        self.score = 0
        self.x = r.randrange(self.block_size, WIDTH-self.block_size)
        self.y = r.randrange(self.block_size, HEIGHT-self.block_size)
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, pygame.Rect(self.x, self.y, self.block_size, self.block_size))
    
    def update(self):
        if self.collision():
            eat.play()
            self.score += 1
            self.reset()
            snake.elongate = True

    def reset(self):
        '''New position for the food.'''
        self.x = r.randrange(self.block_size, WIDTH-self.block_size)
        self.y = r.randrange(self.block_size, HEIGHT-self.block_size)

    def collision(self):
        '''Returns True if the snake's head has collided with the food.'''
        head_x = snake.snakePoints[0].x + snake.block_size/2
        head_y = snake.snakePoints[0].y + snake.block_size/2
        if head_x >= self.x and head_y >= self.y and head_x <= self.x + self.block_size and head_y <= self.y + self.block_size:
            return True
        else:
            return False


def drawRect(x, y, w, h, col):
    pygame.draw.rect(screen, col, pygame.Rect(x, y, w, h), 2)

snake = Snake()
food = Food()

def draw():
    food.draw()
    snake.draw()
    drawText(str(food.score), 450, 30, 19, PINK)

def update():
    food.update()
    snake.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake.dy != 1 and snake.isMoving:
                    up.play()
                    snake.dx = 0
                    snake.dy = -1
            elif event.key == pygame.K_DOWN:
                if snake.dy != -1 and snake.isMoving:
                    down.play()
                    snake.dx = 0
                    snake.dy = 1
            elif event.key == pygame.K_LEFT:
                if snake.dx != 1 and snake.isMoving:
                    left.play()
                    snake.dy = 0
                    snake.dx = -1
            elif event.key == pygame.K_RIGHT:
                if snake.dx != -1 and snake.isMoving:
                    right.play()
                    snake.dy = 0
                    snake.dx = 1
            elif event.key == pygame.K_SPACE:
                if not snake.isMoving:
                    key_press.play()
                    food.score = 0
                    snake.reset()
                    snake.isMoving = True

    clock.tick(30)
    screen.fill(BLACK)
    draw()
    update()
    pygame.display.flip()


pygame.quit()
        