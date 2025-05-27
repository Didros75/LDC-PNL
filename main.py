import pyxel
import math

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
TILE_SIZE = 8
PLAYER_IMG_BANK = 0
ENEMY_IMG_BANK = 0

PLAYER_START_X = 128
PLAYER_START_Y = 128
PLAYER_SPEED = 1
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16

YELLOW_TILE_COLOR = 10


def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    return (x1 < x2 + w2 and x1 + w1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.u = 0
        self.v = 64
        self.direction = "up"
        self.is_active = True
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 10

    def reset(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.u = 0
        self.v = 64
        self.direction = "up"
        self.is_active = True
        self.shoot_cooldown = 0

    def check_tile_collision_at(self, check_x, check_y):
        tile_x = int(check_x / TILE_SIZE)
        tile_y = int(check_y / TILE_SIZE)
        if tile_x >= 0 and tile_y >= 0:
            try:
                tile_val = pyxel.tilemap(0).pget(tile_x, tile_y)
                if tile_val == YELLOW_TILE_COLOR:
                    return True
            except IndexError:
                pass
        return False

    def update(self):
        if not self.is_active:
            return

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        prev_x = self.x
        prev_y = self.y

        dist_x_input = 0
        dist_y_input = 0

        target_x = self.x
        target_y = self.y

        if pyxel.btn(pyxel.KEY_LEFT):
            target_x -= self.speed
            self.direction = "left"
            dist_x_input = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            target_x += self.speed
            self.direction = "right"
            dist_x_input = 1
        if pyxel.btn(pyxel.KEY_UP):
            target_y -= self.speed
            self.direction = "up"
            dist_y_input = -1
        if pyxel.btn(pyxel.KEY_DOWN):
            target_y += self.speed
            self.direction = "down"
            dist_y_input = 1

        points_to_check_future = [
            (target_x + self.w // 4, target_y + self.h // 4),
            (target_x + self.w * 3 // 4, target_y + self.h // 4),
            (target_x + self.w // 4, target_y + self.h * 3 // 4),
            (target_x + self.w * 3 // 4, target_y + self.h * 3 // 4)
        ]

        collided_with_tile = False
        for p_x, p_y in points_to_check_future:
            if self.check_tile_collision_at(p_x, p_y):
                collided_with_tile = True
                break

        if collided_with_tile:
            self.is_active = False
        else:
            self.x = target_x
            self.y = target_y

        if dist_x_input == -1 and dist_y_input == -1:
            self.u = 32
            self.v = 80
            self.direction = "up_left"
        elif dist_x_input == 1 and dist_y_input == -1:
            self.u = 32
            self.v = 64
            self.direction = "up_right"
        elif dist_x_input == -1 and dist_y_input == 1:
            self.u = 48
            self.v = 80
            self.direction = "down_left"
        elif dist_x_input == 1 and dist_y_input == 1:
            self.u = 48
            self.v = 64
            self.direction = "down_right"
        elif dist_x_input == -1:
            self.u = 16
            self.v = 64
            self.direction = "left"
        elif dist_x_input == 1:
            self.u = 0
            self.v = 80
            self.direction = "right"
        elif dist_y_input == -1:
            self.u = 0
            self.v = 64
            self.direction = "up"
        elif dist_y_input == 1:
            self.u = 16
            self.v = 80
            self.direction = "down"

        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0

    def draw(self, cam_x, cam_y):
        if not self.is_active:
            return
        draw_x = self.x - cam_x
        draw_y = self.y - cam_y
        pyxel.blt(draw_x, draw_y, PLAYER_IMG_BANK, self.u, self.v, self.w, self.h, 0)

    def get_rect(self):
        return self.x, self.y, self.w, self.h

    def can_shoot(self):
        return self.shoot_cooldown == 0

    def shoot(self):
        self.shoot_cooldown = self.shoot_cooldown_max


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.speed = 0.5
        self.u = 64
        self.v = 64
        self.is_active = True

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.u = 64
        self.v = 64
        self.is_active = True

    def update(self, player_x, player_y):
        if not self.is_active:
            return

        target_center_x = player_x + PLAYER_WIDTH / 2
        target_center_y = player_y + PLAYER_HEIGHT / 2
        enemy_center_x = self.x + self.w / 2
        enemy_center_y = self.y + self.h / 2

        dist_x = target_center_x - enemy_center_x
        dist_y = target_center_y - enemy_center_y
        dist = math.sqrt(dist_x * dist_x + dist_y * dist_y)

        if dist > self.speed:
            move_x = (dist_x / dist) * self.speed
            move_y = (dist_y / dist) * self.speed
            self.x += move_x
            self.y += move_y
        elif dist > 0:
            self.x += dist_x
            self.y += dist_y

        threshold = self.speed * 2

        if abs(dist_x) > abs(dist_y) + threshold:
            if dist_x > 0:
                self.u = 64
                self.v = 80
                if dist_y > threshold:
                    self.u = 112
                    self.v = 80
                elif dist_y < -threshold:
                    self.u = 112
                    self.v = 64
            else:
                self.u = 64
                self.v = 64
                if dist_y > threshold:
                    self.u = 96
                    self.v = 80
                elif dist_y < -threshold:
                    self.u = 96
                    self.v = 64
        elif abs(dist_y) > abs(dist_x) + threshold:
            if dist_y > 0:
                if dist_x > threshold:
                    self.u = 112
                    self.v = 80
                elif dist_x < -threshold:
                    self.u = 96
                    self.v = 80
                else:
                    self.u = 96
                    self.v = 80
            else:
                if dist_x > threshold:
                    self.u = 112
                    self.v = 64
                elif dist_x < -threshold:
                    self.u = 96
                    self.v = 64
                else:
                    self.u = 96
                    self.v = 64
        elif dist > self.speed:
            if dist_x > 0 and dist_y > 0:
                self.u = 112
                self.v = 80
            elif dist_x < 0 and dist_y > 0:
                self.u = 96
                self.v = 80
            elif dist_x > 0 and dist_y < 0:
                self.u = 112
                self.v = 64
            elif dist_x < 0 and dist_y < 0:
                self.u = 96
                self.v = 64
        else:
            self.u = 64
            self.v = 64

    def draw(self, cam_x, cam_y):
        if not self.is_active:
            return
        draw_x = self.x - cam_x
        draw_y = self.y - cam_y
        pyxel.blt(draw_x, draw_y, ENEMY_IMG_BANK, self.u, self.v, self.w, self.h, 0)

    def get_rect(self):
        return self.x, self.y, self.w, self.h


class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.radius = 2
        self.speed = 4
        self.color = 0
        self.is_active = True
        self.dx = 0
        self.dy = 0

        if "up" in direction: self.dy = -1
        if "down" in direction: self.dy = 1
        if "left" in direction: self.dx = -1
        if "right" in direction: self.dx = 1

        if self.dx == 0 and self.dy == 0:
            if direction == "up":
                self.dy = -1
            elif direction == "down":
                self.dy = 1
            elif direction == "left":
                self.dx = -1
            elif direction == "right":
                self.dx = 1

        if self.dx != 0 and self.dy != 0:
            length = math.sqrt(self.dx ** 2 + self.dy ** 2)
            self.dx = (self.dx / length)
            self.dy = (self.dy / length)

    def update(self):
        if not self.is_active:
            return
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        if self.x < -self.radius or self.x > SCREEN_WIDTH + self.radius or self.y < -self.radius or self.y > SCREEN_HEIGHT + self.radius:
            self.is_active = False

    def draw(self, cam_x, cam_y):
        if not self.is_active:
            return
        draw_x = self.x - cam_x
        draw_y = self.y - cam_y
        pyxel.circ(draw_x, draw_y, self.radius, self.color)

    def get_rect(self):
        return self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2


class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Beginner Game", fps=30)
        pyxel.load("theme.pyxres")
        self.game_state = "playing"  # "playing", "game_over"
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.cam_x = 0
        self.cam_y = 0
        self.coffres = [(4, 18), (40, 33), (80, 81), (128, 41), (40, 137), (136, 121), (100, 106), (114, 33), (81, 137)]
        self.time_near_coffre = 0
        self.max_time = 100
        self.spawn_enemy()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.player.reset()
        self.enemies.clear()
        self.bullets.clear()
        self.score = 0
        self.time_near_coffre = 0
        self.spawn_enemy()
        self.game_state = "playing"

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def check_proximite_coffre(self):
        for i in self.coffres:
            dist = self.distance(self.player.x / 10 + 1, self.player.y / 10 + 4, i[0], i[1])

            if dist < 6:
                self.time_near_coffre += 1
                if self.time_near_coffre >= self.max_time:
                    self.score += 3
                    self.time_near_coffre = 0
            else:
                self.time_near_coffre = 0
            break

    def spawn_enemy(self):
        enemy_w = 16
        enemy_h = 16
        ex = pyxel.rndi(0, SCREEN_WIDTH - enemy_w)
        ey = pyxel.rndi(0, SCREEN_HEIGHT - enemy_h)
        # Ensure enemy doesn't spawn on player
        while self.player.is_active and check_collision(ex, ey, enemy_w, enemy_h, self.player.x, self.player.y,
                                                        self.player.w, self.player.h):
            ex = pyxel.rndi(0, SCREEN_WIDTH - enemy_w)
            ey = pyxel.rndi(0, SCREEN_HEIGHT - enemy_h)
        self.enemies.append(Enemy(ex, ey))

    def update_playing(self):
        self.check_proximite_coffre()
        self.player.update()

        if not self.player.is_active:
            self.game_state = "game_over"
            return

        if pyxel.btnp(pyxel.KEY_SPACE) and self.player.can_shoot():
            self.player.shoot()
            bullet_x = self.player.x + self.player.w // 2
            bullet_y = self.player.y + self.player.h // 2
            self.bullets.append(Bullet(bullet_x, bullet_y, self.player.direction))

        for enemy in self.enemies:
            enemy.update(self.player.x, self.player.y)

        for bullet in self.bullets:
            bullet.update()

        active_bullets = []
        for b in self.bullets:
            if b.is_active:
                active_bullets.append(b)
        self.bullets = active_bullets

        active_enemies = []
        for e in self.enemies:
            if e.is_active:
                active_enemies.append(e)
        self.enemies = active_enemies

        for bullet_idx in range(len(self.bullets) - 1, -1, -1):
            bullet = self.bullets[bullet_idx]
            if not bullet.is_active: continue
            for enemy_idx in range(len(self.enemies) - 1, -1, -1):
                enemy = self.enemies[enemy_idx]
                if not enemy.is_active: continue
                br = bullet.get_rect()
                er = enemy.get_rect()
                if check_collision(br[0], br[1], br[2], br[3], er[0], er[1], er[2], er[3]):
                    bullet.is_active = False
                    enemy.is_active = False
                    self.score += 10
                    break

        for enemy_idx in range(len(self.enemies) - 1, -1, -1):
            enemy = self.enemies[enemy_idx]
            if not enemy.is_active: continue
            pr = self.player.get_rect()
            er = enemy.get_rect()
            if check_collision(pr[0], pr[1], pr[2], pr[3], er[0], er[1], er[2], er[3]):
                self.player.is_active = False
                self.game_state = "game_over"
                break

        if len(self.enemies) == 0:
            self.spawn_enemy()

        self.cam_x = self.player.x - SCREEN_WIDTH / 2
        self.cam_y = self.player.y - SCREEN_HEIGHT / 2

    def update_game_over(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

    def update(self):
        if self.game_state == "playing":
            self.update_playing()
        elif self.game_state == "game_over":
            self.update_game_over()

    def draw_playing(self):
        self.player.draw(self.cam_x, self.cam_y)
        for enemy in self.enemies:
            enemy.draw(self.cam_x, self.cam_y)
        for bullet in self.bullets:
            bullet.draw(self.cam_x, self.cam_y)
        bar_x = 5
        bar_y = 15
        bar_width = 100
        pyxel.text(5, 5, "Score: " + str(self.score), 7)
        progress = 0
        if self.max_time > 0:
            progress = min(self.time_near_coffre / self.max_time, 1.0)
        filled_width = int(bar_width * progress)
        pyxel.rect(bar_x, bar_y, bar_width, 6, 1)
        pyxel.rect(bar_x, bar_y, filled_width, 6, 11)
        pyxel.rectb(bar_x, bar_y, bar_width, 6, 7)

    def draw_game_over(self):
        pyxel.text(SCREEN_WIDTH // 2 - 28, SCREEN_HEIGHT // 2 - 10, "GAME OVER", pyxel.COLOR_RED)
        pyxel.text(SCREEN_WIDTH // 2 - 38, SCREEN_HEIGHT // 2 + 5, "Press R to Replay", 7)
        pyxel.text(5, 5, "Final Score: " + str(self.score), 7)

    def draw(self):
        pyxel.cls(1)
        pyxel.bltm(0, 0, 0, self.cam_x, self.cam_y, SCREEN_WIDTH, SCREEN_HEIGHT, 0)

        if self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()


if __name__ == "__main__":
    Game()