import pygame
import random
import time

# Initialize Pygame
pygame.init()
running = True
game_solved = False
coins_need = 5

# Set up the display
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Robot Collect Golden Coins')

# Load images
robot_image = pygame.image.load('robot.png')
coin_image = pygame.image.load('coin.png')
monster_image = pygame.image.load('monster.png')


# Robot sprite class
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = robot_image
        self.rect = self.image.get_rect()
        self.rect.center = (300, 200)
        self.speed = 1

    def move(self, dx, dy):
        if self.rect.x + robot_image.get_width() + dx <= 600 and self.rect.x + dx >= 0:
            self.rect.x += dx
        if self.rect.y + robot_image.get_height() + dy <= 400 and self.rect.y + dy >= 0:
            self.rect.y += dy


# Coin sprite class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(10, 590), random.randint(10, 390))

    def move_to_random_location(self):
        self.rect.center = (random.randint(10, 590), random.randint(10, 390))


# Monster sprite class
class Monster(pygame.sprite.Sprite):
    def __init__(self, height):
        super().__init__()
        self.image = monster_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 600), height)
        self.speed = 1

    def move(self):
        if not game_solved:
            self.rect.x += self.speed
        if self.rect.right > 600:
            self.speed = -self.speed
            self.rect.right = 600
        if self.rect.left < 0:
            self.speed = -self.speed
            self.rect.left = 0


def show_text(text1: str):
    text_show = font.render(text1, True, (255, 255, 255))
    text_rect = text_show.get_rect()
    text_rect.center = (300, 200)
    screen.blit(text_show, text_rect)
    text_show2 = font.render('Press SPACE to exit the game.', True, (255, 255, 255))
    text_rect2 = text_show2.get_rect()
    text_rect2.center = (300, 220)
    screen.blit(text_show2, text_rect2)
    for EVENT in pygame.event.get():
        if EVENT.type == pygame.QUIT:
            exit()
        if EVENT.type == pygame.KEYDOWN:
            if EVENT.key == pygame.K_SPACE:
                exit()
        continue


# Create sprites instances
robot = Robot()
coin = Coin()
monsters = [Monster(100), Monster(350)]

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(robot)
all_sprites.add(coin)
all_sprites.add(monsters)

# Initialize game variables
coins_collected = 0
start_time = time.time()

to_right = False
to_left = False
to_up = False
to_down = False
elapsed_time = 0

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True
            if event.key == pygame.K_UP:
                to_up = True
            if event.key == pygame.K_DOWN:
                to_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False
            if event.key == pygame.K_RIGHT:
                to_right = False
            if event.key == pygame.K_UP:
                to_up = False
            if event.key == pygame.K_DOWN:
                to_down = False

    if to_left:
        robot.move(-robot.speed, 0)
    if to_right:
        robot.move(robot.speed, 0)
    if to_up:
        robot.move(0, -robot.speed)
    if to_down:
        robot.move(0, robot.speed)

    # Update game state
    if pygame.sprite.collide_rect(robot, coin):
        coin.move_to_random_location()
        coins_collected += 1
    for monster in monsters:
        monster.move()
    if pygame.sprite.spritecollide(robot, monsters, False):
        running = False

    # Render game display
    screen.fill((41, 158, 217))
    all_sprites.draw(screen)

    # Render text
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f'Coins collected: {coins_collected}', True, (255, 255, 255))
    screen.blit(text, (10, 10))
    if not game_solved:
        elapsed_time = time.time() - start_time
    text = font.render(f'Time elapsed: {elapsed_time:.1f} seconds', True, (255, 255, 255))
    screen.blit(text, (10, 40))

    if coins_collected >= coins_need:
        show_text('Challenge success!')
        game_solved = True
    if not running:
        show_text('Challenge failed!')
        game_solved = True

    pygame.display.flip()
