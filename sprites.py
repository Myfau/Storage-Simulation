import pygame as pg
import random
import time
from settings import *
from collections import deque
from state_search import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('./assets/cart.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rotation = 0
        self.cart_loaded = False
        self.loaded_box = ''
        self.movelist = []
        self.last_box_colided = None
        self.last_shelf_colided = None

    def rotate_right(self):
        if self.rotation >= 270:
            self.rotation = 0
        else:
            self.rotation += 90  

    def rotate_left(self):
        if self.rotation <= 0:
            self.rotation = 270
        else:
            self.rotation -= 90

    def move_forward(self):
        if self.rotation == 0:
            self.move(dy=-1)
        elif self.rotation == 90:
            self.move(dx=1)
        elif self.rotation == 180:
            self.move(dy=1)
        elif self.rotation == 270:
            self.move(dx=-1)   

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
        self.collide_with_boxes()
        self.collide_with_shelves()

    def pickup(self):
        if self.collide_with_boxes() and not self.cart_loaded:
            self.cart_loaded = True
            box = self.ret_collided_box_and_del()    
            self.loaded_box = box.type
            self.image = pg.image.load(f'./assets/cart_box_{self.loaded_box}.png')
    
    def put_down(self):
        if self.collide_with_shelves():
            self.shelf = self.ret_collided_shelf()
            if self.shelf.type == self.loaded_box and not self.shelf.is_loaded:
                self.shelf.image = pg.image.load(f'./assets/box_{self.shelf.type}.png')
                self.image = pg.image.load('./assets/cart.png')
                self.loaded_box = ''
                self.shelf.is_loaded = True
                self.cart_loaded = False

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def collide_with_boxes(self):
        for box in self.game.boxes:
            if box.x == self.x and box.y == self.y:
                self.last_box_colided = box
                print("\nCurrent object:\nObject: box\nType: " + box.type + "\nWeight: " + str(box.weight))
                return True
        return False
    
    def ret_collided_box_and_del(self):
        for box in self.game.boxes:
            if box.x == self.x and box.y == self.y:
                box_ret = box
                box.kill()
                return box_ret

    def collide_with_shelves(self):
        for shelf in self.game.shelves:
            if shelf.x == self.x and shelf.y == self.y:
                self.last_shelf_colided = shelf
                print("\nCurrent object:\nObject: shelf\nType: " + shelf.type + "\nWeight: " + str(shelf.max_weight))
                return True
        return False

    def ret_collided_shelf(self):
        for shelf in self.game.shelves:
            if shelf.x == self.x and shelf.y == self.y:
                return shelf

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def serch_init(self, cert_object, search_type = 1):
        goal = []
        if not cert_object.is_loaded:
            goal.append(State(cert_object.x, cert_object.y, 180))
            goal.append(State(cert_object.x, cert_object.y, 90))
            goal.append(State(cert_object.x, cert_object.y, 270))
            goal.append(State(cert_object.x, cert_object.y, 0))

        istate = State(self.x, self.y, self.rotation)
        search_obj = Search(istate, goal, self.game.walls, self.game.padles)
        print("Start search")
        if search_type == 1:
            self.movelist = search_obj.greedy_search()
        else:
            self.movelist = search_obj.search()
        
        print(self.movelist)

    def move_cart_by_movelist(self):
        for move in self.movelist:
            if move == "forward":
                self.move_forward()
            if move == "rotate_right":
                self.rotate_right()
            if move == "rotate_left":
                self.rotate_left()
            self.update()
            self.game.draw()
            time.sleep(0.1)
        self.movelist = []
        self.rotation = 0


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(f'./assets/wall.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Shelf(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.groups = game.all_sprites, game.shelves
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.is_loaded = False
        self.type = img
        self.image = pg.image.load(f'./assets/{img}.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.max_weight = random.randint(3,5)

class Box(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.groups = game.all_sprites, game.boxes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.is_loaded = False
        self.type = img
        self.image = pg.image.load(f'./assets/{img}Box.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.weight = random.randint(3,5)

class Padle(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.groups = game.all_sprites, game.padles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = img
        self.image = pg.image.load(f'./assets/padle.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

