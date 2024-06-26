#Three Features Consisting My Game
#Created by Harrison Manullang
#Credits to Chris Bradfield
#
#Speed Boost
#Deathblock
'''
Sources: https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2001 
blackbox.ai
Chatgpt
'''
import pygame as pg
from settings import *
from sprites import *
import sys
from os import path
from random import randint
from math import floor
from utils import *
import random

#cooldown class
# class Cooldown():
#     def __init__(self):
#         self.current_time = 0
#         self.event_time = 0
#         self.delta = 0
#     def ticking(self):
#         self.current_time = floor((pg.time.get_ticks())/1000)
#         self.delta = self.current_time - self.event_time
#     def countdown(self, x):
#         x = x - self.delta
#         if x != None:
#             return x
#     def event_reset(self):
#         self.event_time = floor((pg.time.get_ticks())/1000)
#     def timer(self):
#         self.current_time = floor((pg.time.get_ticks())/1000)

# create a game class 
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.mob_spawn_time = pg.time.get_ticks()
        self.mob_spawn_interval = 4000  # Interval in milliseconds between spawns
       #Chat gpt helped me create this
        # Your existing initialization code...
        # List of coin respawn timers
        
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        # pull images from folders 
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'tank.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, 'dog.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    # Create run method which runs the whole GAME
    def new(self):
        self.load_data()
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.gun = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.deathblock = pg.sprite.Group()
        self.speedboost = pg.sprite.Group()
        self.ratelimiter= pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.autolock = pg.sprite.Group()
        self.cooldown = Timer(self)
        # Add more coins as needed
         # Create coins and their respawn timers
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'p':
                    #finds thepalyers starting coordinates
                    self.p1col = col
                    self.p1row = row
                    self.player = Player(self, self.p1col, self.p1row)
                if tile == 'd':
                    Deathblock(self, col, row)
                    (self, col, row)
                if tile == 'S':
                    Speedboost(self, col, row)
                if tile == 'B':
                    Ratelimiter(self, col, row)
                if tile == 'U':
                    Mob(self, col, row,)  
                if tile == 'A':
                    Autolock(self, col, row)

    
    def init_coins(self):
        all_coin_positions = [(5, 5), (10, 10), (15, 15)]  # Example positions
        # Create coins at the predetermined positions
        chosen_positions = random.sample(all_coin_positions, 2)
        for pos in chosen_positions:
            Coin(self, pos[0], pos[1])
            
    
    
    def run(self):
        # runs game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        
    def quit(self):
         pg.quit()
         sys.exit()

    
    def update(self):
        self.all_sprites.update()
        self.spawn_mobs()
        # Check if all coins are collected
        if len(self.coins) == 0:
        # Reset the level with a new set of coins
            self.init_coins()
    # makes grid appear on screen
    
    def spawn_mobs(self):
        now = pg.time.get_ticks()
        if now - self.mob_spawn_time >= self.mob_spawn_interval:
            # Generate random coordinates for the mob
            x = randint(0, (WIDTH // TILESIZE) - 1)
            y = randint(0, (HEIGHT // TILESIZE) - 1)
            # Ensure mobs do not spawn inside walls
            if not any([wall.rect.collidepoint(x * TILESIZE, y * TILESIZE) for wall in self.walls]):
                Mob(self, x, y)
            self.mob_spawn_time = now
    


    # makes grid appear on screen
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

     #start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Press any button to begin/shoot the other player can collect coins to to win", 24, WHITE, 2, 3)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    # shows clock on screen
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
            pg.display.flip()
            self.clock.tick(60)
    


    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
    
    def show_start_screen(self):
        pass

    def show_game_over_screen(self):
        pass
    
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
####################### Instantiate game... ###################
g = Game()

# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()



