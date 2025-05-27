from platform import python_revision

import pyxel

#CONSTANTS
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
TILE_SIZE = 8

default_x = 128
default_y = 128

class GameObject:
    def __init__(self, x, y, w, h, u, v, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.u = u
        self.v = v
        self.img = img

    def draw(self, cam_x, cam_y):
        screen_x = cam_x - self.x
        screen_y = cam_y - self.y
        if (screen_x + self.w) > 0 and screen_x < SCREEN_WIDTH and (screen_y + self.h) > 0 and screen_y < SCREEN_HEIGHT:
            pyxel.blt(screen_x, screen_y, self.img, self.u, self.v, self.x, self.h, 0)

    def get_rect(self):
        return self.x, self.y, self.w, self.h

    def check_collision(self, other_rect):
        ax, ay, aw, ah = self.get_rect()
        bx, by, bw, bh = other_rect
        return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)


class Game:
    def __init__(self):
        pyxel.init(256,256, title="Gold n Powder", fps=30, quit_key=pyxel.KEY_ESCAPE)
        self.x = 128
        self.y = 128
        self.speed = 10

        self.prev_u = 0
        self.prev_v = 64

        pyxel.load("theme.pyxres")
        pyxel.run(self.update, self.draw)

    def move(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed

        self.x = max(0,min(self.x,SCREEN_WIDTH - TILE_SIZE))
        self.y = max(0,min(self.y,SCREEN_HEIGHT - TILE_SIZE))


    def update(self):
        self.move()

        if pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_LEFT):
            self.prev_u = 32
            self.prev_v = 80
        elif pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_RIGHT):
            self.prev_u = 32
            self.prev_v = 64
        elif pyxel.btn(pyxel.KEY_UP):
            self.prev_u = 0
            self.prev_v = 64
        elif pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_LEFT):
            self.prev_u = 48
            self.prev_v = 80
        elif pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_RIGHT):
            self.prev_u = 48
            self.prev_v = 64
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.prev_u = 16
            self.prev_v = 80
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.prev_u = 16
            self.prev_v = 64
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.prev_u = 0
            self.prev_v = 80

    def draw(self):
        pyxel.cls(0)

        camX = self.x - SCREEN_WIDTH // 2
        camY = self.y - SCREEN_HEIGHT // 2

        camX = max(0, min(camX, pyxel.width - SCREEN_WIDTH))
        camY = max(0, min(camY, pyxel.height - SCREEN_HEIGHT))

        tileU = camX // TILE_SIZE
        tileV = camY // TILE_SIZE
        pyxel.bltm(0, 0, 0, tileU, tileV, SCREEN_WIDTH, SCREEN_HEIGHT)

        drawX = SCREEN_WIDTH // 2
        drawY = SCREEN_HEIGHT // 2

        pyxel.blt(drawX, drawY, img=0, u=self.prev_u, v=self.prev_v, w=16, h=16)

        print(self.x, self.y)



    def méchen(self):
        pyxel.rect(40,40,8,9,col=9)
    def méchen_move(self):


Game()