# This file was created by: Harrison Manullang

# write a player class
import pygame as pg
from settings import *
from os import path
import math



vec = pg.math.Vector2

# needed for animated sprite
SPRITESHEET = "theBell.png"
SPRITESHEET2 = "dog.png"
# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# needed for animated sprite
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        #self.image.fill(GREEN)
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        #finds player spawn
        self.pos = vec(0,0)
        self.dir = vec(0,0)
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False
        #finds player spawn
    def detath(self):
        self.x = self.game.p1col*TILESIZE
        self.y = self.game.p1row*TILESIZE
        print("You Died")

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
           self.vx = -self.speed  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
           self.vx = self.speed  
        if keys[pg.K_UP] or keys[pg.K_w]:
           self.vy = -self.speed 
        if keys[pg.K_DOWN] or keys[pg.K_s]:
           self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
           self.vx *= 0.7071
           self.vy *= 0.7071
        if keys [pg.K_e]:
            self.shoot()
        
     
    def load_images(self):
        self.standing_frames = [self.spritesheet2.get_image(0,0, 32, 32), 
                                self.spritesheet2.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def shoot(self):
            p = Gun(self.game, self.rect.x, self.rect.y)
            print(p.rect.x)
            print(p.rect.y)
           
   
    def collide_with_walls(sprite, group, dir):
      if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
        if dir == 'y':
         hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

    #
    # player group collisions
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            # if str(hits[0].__class__.__name__) == "Projectile":
            #     self.moneybag += 1
            if str(hits[0].__class__.__name__) == "Deathblock":
                self.death()
            if str(hits[0].__class__.__name__) == "Speedboost":
                self.speed += 200
            if str(hits[0].__class__.__name__) == "Ratelimiter":
                self.speed -= 150
            if str(hits[0].__class__.__name__) == "Mob":
                self.death()
            if str(hits[0]._class_._name_) == "Mob2":
                self.hitpoints -= 1
                hits[0]. health -= 1
            

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0,32,32),self.spritesheet.get_image(32 ,0, 32, 32)]
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    
    # def Gun(self):
      #  p = Gun(self.game, self.rect.x, self.rect.y)
      #  print(p.rect.x)
       # print(p.rect.y)

    def update(self):
        self.get_keys()
        self.animate()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.deathblock, False)
        self.collide_with_group(self.game.speedboost, True)
        self.collide_with_group(self.game.ratelimiter,True)
        self.collide_with_group(self.game.mobs, False)
        

        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")


# classes for game

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        # self.image = self.game.mob_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = speed
        self.health = 32
        self.max_health = 32

        print("created mob at", self.rect.x, self.rect.y)
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def chasing(self):
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100

   

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')




class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
# class Projectile(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.projectiles
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(WHITE)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Ratelimiter (pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ratelimiter
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Speedboost (pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.speedboost
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Deathblock(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.deathblock
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Gun(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.gun
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        print("I created a pew pew...")
        # creating the design of the pew pew
        # when the pew pew is shot it will say it is shot to show that it is happening
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
    def update(self):
        self.collide_with_group(self.game.mobs, True)
        self.rect.y -= -self.speed
        # self.rect.x -= self.speed
        # will destory mobs when it hits it


class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(ORANGE)
        self.image = self.game.mob_img
    
        self.rect = self.image.get_rect()
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        # added
        self.speed = 150
        self.chasing = False
        # self.health = MOB_HEALTH
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    def update(self):
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            # self.image = pg.transform.rotate(self.image, 45)
            # self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            # self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            # self.rect.center = self.hit_rect.center
            # if self.health <= 0:
            #     self.kill(