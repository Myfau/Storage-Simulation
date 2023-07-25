import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
import decision_tree as dt
#from functions import *
import joblib

# Żeby program działał poprawnie wymagane są biblioteki:
# - pygame (pip install pygame)
# - scikit (pip install scikit-learn)
# - pandas (pip install pandas)
# - matplotlib (pip install matplotlib)
# - numpy (pip install numpy)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.tree = None
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, './maps/map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        try:
            self.tree = joblib.load('tree_utils/tree_model')
        except:
            print("No decision tree found! Press l to learn a tree")
        

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.shelves = pg.sprite.Group()
        self.boxes = pg.sprite.Group()
        self.padles = pg.sprite.Group()

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                if tile == 'P':
                    self.cart = Player(self, col, row)
                if tile == 'D':
                    Shelf(self, col, row, "dang")
                if tile == "R":
                    Shelf(self, col, row, "radi")
                if tile == "N":
                    Shelf(self, col, row, "norm")
                if tile == "F":
                    Shelf(self, col, row, "frag")
                if tile == "L":
                    Shelf(self, col, row, "flam")
                if tile == "n":
                    Box(self, col, row, "norm")
                if tile == "i":
                    Padle(self, col, row, "norm")
                if tile == 'd':
                    Box(self, col, row, "dang")
                if tile == "r":
                    Box(self, col, row, "radi")
                if tile == "f":
                    Box(self, col, row, "frag")
                if tile == "l":
                    Box(self, col, row, "flam")
                self.col_before_tile = tile
            self.row_before_tiles = tiles
        

    def run(self):
        # game loop - set self.playing = False to end the game
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
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.cart.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.cart.move(dx=1)
                if event.key == pg.K_UP:
                    self.cart.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.cart.move(dy=1)
                if event.key == pg.K_SPACE:
                    self.cart.pickup()
                    self.cart.put_down()
                if event.key == pg.K_TAB:    
                    self.cart.move_cart_by_movelist()
                if event.key == pg.K_s:
                    for current_box in self.boxes:
                        if self.tree == None:
                            print ('Error: no decision tree found')
                            break
                        for current_shelf in self.shelves:
                            if dt.decision_initialisation(self.tree, current_box, current_shelf, self.cart.cart_loaded):
                                self.cart.serch_init(current_box)
                                self.cart.move_cart_by_movelist()
                                self.cart.pickup()
                                self.cart.serch_init(current_shelf)
                                self.cart.move_cart_by_movelist()
                                self.cart.put_down()
                                break
                if event.key == pg.K_l:
                    self.tree = dt.treelearn()
                    dt.visualize_decision_tree(self.tree)
                    print("Decision tree learned!")
                    joblib.dump(self.tree, 'tree_utils/tree_model')

# create the game object
g = Game()

while True:
    g.new()
    g.run()
