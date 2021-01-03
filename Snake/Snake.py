import sys
import pygame
from pygame.math import Vector2
import random

#################
cell_size = 35
cell_number = 20
#################
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
rabbit = pygame.image.load('Assets/Graphics/food.png').convert_alpha()
font = pygame.font.Font('Assets/Font/PoetsenOne-Regular.ttf', 20)

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.dire = Vector2(0, 0)
        self.new_block = False
        self.head_up = pygame.image.load('Assets/Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Assets/Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Assets/Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Assets/Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Assets/Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Assets/Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Assets/Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Assets/Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Assets/Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Assets/Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Assets/Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Assets/Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Assets/Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Assets/Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Assets/Sound/crunch.wav')

    def head_graphic(self):
        head_rotate = self.body[1] - self.body[0]
        if head_rotate == Vector2(1, 0):
            self.head = self.head_left
        elif head_rotate == Vector2(-1, 0):
            self.head = self.head_right
        elif head_rotate == Vector2(0, 1):
            self.head = self.head_up
        elif head_rotate == Vector2(0, -1):
            self.head = self.head_down

    def tail_graphic(self):
        tail_rotate = self.body[-2] - self.body[-1]
        if tail_rotate == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_rotate == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_rotate == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_rotate == Vector2(0, -1):
            self.tail = self.tail_down

    def draw_snake(self):
        self.head_graphic()
        self.tail_graphic()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            snake_rec = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, snake_rec)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rec)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, snake_rec)
                elif previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, snake_rec)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, snake_rec)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, snake_rec)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, snake_rec)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, snake_rec)

            # else:
            #     pygame.draw.rect(screen, (150, 100, 100), snake_rec)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.dire)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.dire)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.dire = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.re_position()

    def draw_fruit(self):
        pos_x = int(self.pos.x * cell_size)
        pos_y = int(self.pos.y * cell_size)
        fruit_rec = pygame.Rect(pos_x, pos_y, cell_size - 5, cell_size - 5)
        screen.blit(rabbit, fruit_rec)

    def re_position(self):
        self.x = random.randint(0, cell_number - 5)
        self.y = random.randint(0, cell_number - 5)
        self.pos = Vector2(self.x, self.y)


class Game:  # game logic
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.collision_food()
        self.collision()

    def draw(self):
        self.draw_grass()
        self.score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def collision_food(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.crunch_sound.play()
            self.fruit.re_position()
            self.snake.add_block()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.re_position()

    def collision(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def game_over(self):
        self.snake.reset()

    def score(self):
        score_txt = str(len(self.snake.body) - 3)
        score_sur = font.render(score_txt, True, (255, 255, 255))
        score_x = int(45)
        score_y = int(20)
        score_rec = score_sur.get_rect(center=(score_x, score_y))
        food_rec = rabbit.get_rect(midright=(score_rec.left, score_rec.centery))
        screen.blit(rabbit, food_rec)
        screen.blit(score_sur, score_rec)


running = True
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

game_logic = Game()

while running:  # Main loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game_logic.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_UP:
                if game_logic.snake.dire.y != 1:
                    game_logic.snake.dire = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if game_logic.snake.dire.x != -1:
                    game_logic.snake.dire = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if game_logic.snake.dire.x != 1:
                    game_logic.snake.dire = Vector2(-1, 0)
            if event.key == pygame.K_DOWN:
                if game_logic.snake.dire.y != -1:
                    game_logic.snake.dire = Vector2(0, 1)

    pygame.display.update()
    screen.fill((100, 100, 100))
    game_logic.draw()
    clock.tick(60)
