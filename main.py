#Three Features Consisting My Game

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
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        # pull images from folders 
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'tank2.png')).convert_alpha()
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
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.deathblock = pg.sprite.Group()
        self.speedboost = pg.sprite.Group()
        self.ratelimiter= pg.sprite.Group()
        self.mobs = pg.sprite.Group()
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
                    self.p1 = Player(self, self.p1col, self.p1row)
                if tile == 'd':
                    Deathblock(self, col, row)
                    (self, col, row)
                if tile == 'S':
                    Speedboost(self, col, row)
                if tile == 'B':
                    Ratelimiter(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)

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
        # self.test_timer.ticking()

    # makes grid appear on screen
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

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
            self.draw_text(self.screen, str(self.p1.moneybag), 64, WHITE, 1, 1)
            #self.draw_text(self.screen, str(self.test_timer.countdown(45)), 24, WHITE, WIDTH/2 - 32, 2)
            pg.display.flip()


    # def draw_text(self, surface, text, size, color, x, y):
    #     font_name = pg.font.match('arial')
    #     font = pg.font.Font(font_name, size)
    #     text_surface = font.render(text, True, color)
    #     text_rect = text_surface.get_rect()
    #     text_rect.topleft = (x,y)
    #     surface.blit(text_surface, text_rect)

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
    
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



