import pyxel

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

Game()