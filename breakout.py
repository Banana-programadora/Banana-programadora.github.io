import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

font = pygame.font.SysFont('Costantia', 70)

bg = (234, 218, 185)
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)
paddle_colour = (142, 135, 123)
paddle_outline = (100, 100, 100)
text_colour = (78, 81, 139)

cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False 
game_over = 0

def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))

class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.block = []
        block_individual = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.block.append(block_row)

    def draw_wall(self):
        for row in self.block:
            for block in row:
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)

class paddle():
    def __init__(self):
        self.reset()

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] or key[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_colour, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        collision_threshold = 5

        wall_destroyed = 1
        row_count = 0
        for row in wall.block:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision_threshold and self.speed_y > 0:
                        self.speed_y *= -1

                    if abs(self.rect.top - item[0].bottom) < collision_threshold and self.speed_y < 0:
                        self.speed_y *= -1

                    if abs(self.rect.right - item[0].left) < collision_threshold and self.speed_x > 0:
                        self.speed_x *= -1

                    if abs(self.rect.left - item[0].right) < collision_threshold and self.speed_x < 0:
                        self.speed_x *= -1
                    
                    if wall.block[row_count][item_count][1] > 1:
                        wall.block[row_count][item_count][1] -= 1
                    else:
                        wall.block[row_count][item_count][0] = (0, 0, 0, 0)

                if wall.block[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                item_count += 1
            row_count += 1
        if wall_destroyed == 1:
            self.game_over = 1

        if self.rect.left < 0:
            self.speed_x *= -1

        if self.rect.right > screen_width:
            self.speed_x *= -1

        if self.rect.top < 0:
            self.speed_y *= -1

        if self.rect.bottom > screen_height:
            self.game_over = -1

        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_threshold and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1
 
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over
        
    def draw(self):
        pygame.draw.circle(screen, paddle_colour, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad ), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline,(self.rect.x + self.ball_rad, self.rect.y + self.ball_rad ), self.ball_rad, 3)
    
    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y 
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

wall = wall()
wall.create_wall()

player_paddle = paddle()

ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
while run:

    clock.tick(fps)

    screen.fill(bg)

    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if live_ball:
        player_paddle.move()
        game_over = ball.move()
        if game_over != 0:
            live_ball = False

    if not live_ball:
        if game_over == 0:
            draw_text('CLICK TO START', font, text_colour, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text('YOU WON!', font, text_colour, 240, screen_height // 2 + 50)
            draw_text('CLICK TO RESTART', font, text_colour, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('YOU LOST!', font, text_colour, 240, screen_height // 2 + 50)
            draw_text('CLICK TO RESTART', font, text_colour, 100, screen_height // 2 + 100)
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()

    pygame.display.update()

pygame.quit()