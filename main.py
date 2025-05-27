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

        self.méchenx = 40
        self.mécheny = 40
        self.umechant = 64
        self.vmechant = 64
        self.canon=Boulets()
        self.direction="haut"
        pyxel.load("theme.pyxres")
        pyxel.run(self.update, self.draw)

    def move(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.direction = "haut"
            self.y -= self.speed
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
            self.direction = "bas"
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.direction = "gauche"
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.direction = "droite"
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.canon.lancer_boule(130, 130, self.direction)


    def update(self):
        self.canon.update()
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

        tileU = camX // TILE_SIZE
        tileV = camY // TILE_SIZE
        pyxel.bltm(0, 0, 0, tileU, tileV, SCREEN_WIDTH, SCREEN_HEIGHT)

        drawX = SCREEN_WIDTH // 2
        drawY = SCREEN_HEIGHT // 2

        pyxel.blt(drawX, drawY, img=0, u=self.prev_u, v=self.prev_v, w=16, h=16)


        if drawX > self.méchenx and drawY > self.mécheny:
            self.méchenx +=1
            self.mécheny +=1
            self.umechant = 112
            self.vmechant = 80
        elif drawX > self.méchenx and drawY < self.mécheny:
            self.méchenx += 1
            self.mécheny -= 1
            self.umechant = 112
            self.vmechant = 64
        elif drawX > self.méchenx:
            self.méchenx += 1
            self.umechant = 64
            self.vmechant = 80
        if drawX < self.méchenx and drawY > self.mécheny:
            self.méchenx -=1
            self.mécheny +=1
            self.umechant = 96
            self.vmechant = 80
        elif drawX < self.méchenx and drawY < self.mécheny:
            self.méchenx -= 1
            self.mécheny -= 1
            self.umechant = 96
            self.vmechant = 64
        elif drawX < self.méchenx:
            self.méchenx -=1
            self.umechant = 64
            self.vmechant = 64

        pyxel.blt(self.méchenx, self.mécheny, img=0, u=self.umechant, v=self.vmechant, w=16, h=16)
        self.canon.draw()
        print(self.x, self.y)


class Boulets:
    def __init__(self):
        self.boules = []


    def lancer_boule(self, x, y, direction):


        dx, dy = 0, 0
        if direction == "haut":
            dy = -1
        elif direction == "bas":
            dy = 1
        elif direction == "gauche":
            dx = -1
        elif direction == "droite":
            dx = 1


        self.boules.append({"x": x, "y": y, "dx": dx, "dy": dy})

    def update(self):



        for boule in self.boules:
            boule["x"] += boule["dx"]
            boule["y"] += boule["dy"]

        self.boules = [
            b for b in self.boules
            if 0 <= b["x"] <= pyxel.width and 0 <= b["y"] <= pyxel.height
        ]

        if pyxel.frame_count % 30 == 0:
            try:
                self.boules.pop(0)
            except :
                pass

    def draw(self):
        for boule in self.boules:
            pyxel.circ(boule["x"], boule["y"], 2, 0)



if __name__ == "__main__":
    Game()