import pygame as pg
from set_and_const import *


pg.init()


class Player:
    def __init__(self, pos, size, speed):
        self.rect = pg.Rect(pos, size)
        self.size = size
        self.x = float(pos[0])
        self.y = float(pos[1])
        self.speed = speed

        self.right_pressed = False
        self.left_pressed = False

        self.vel = pg.math.Vector2(0,0)

        

    def check_if_stuck_in_ground(self):
        if self.y > SCREEN_HEIGHT - self.size[1]:
            self.y = SCREEN_HEIGHT - self.size[1]

    def check_gravity(self):
        if self.y < SCREEN_HEIGHT - self.size[1]:
            self.vel[1] += gravity
        else:
            self.vel[1] = 0

    def update_pos(self):
        if self.y >= SCREEN_HEIGHT - self.size[1]:
            if self.right_pressed and not self.left_pressed:
                self.vel[0] = self.speed
            elif self.left_pressed and not self.right_pressed:
                self.vel[0] = -self.speed
            if not self.right_pressed and not self.left_pressed:
                self.vel[0] = 0

        if self.x >= 0 and self.x <= SCREEN_WIDTH - self.size[0]:
            self.x += self.vel[0]
        elif self.x < 0:
            self.x = 0
            self.vel[0] = 0
        elif self.x > SCREEN_WIDTH - self.size[0]:
            self.x = SCREEN_WIDTH - self.size[0]
            self.vel[0] = 0

        if self.y >= 0 :
            self.y += self.vel[1]
        elif self.y < 0:
            self.y = 0
            self.vel[1] = self.vel[1] * -0.1

        self.rect = pg.Rect((self.x, self.y), self.size)

    def draw(self):
        pg.draw.rect(screen, BLACK, self.rect)
    
    
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


clock = pg.time.Clock()
player = Player((100, 100), (player_width, player_height), player_speed)

def update_player():
    player.check_gravity()
    player.update_pos()
    player.check_if_stuck_in_ground()
    player.draw()

def update_screen():
    #pg.display.update()
    pg.display.flip()
    screen.fill(WHITE)





running = True        
def main():
    global running
    while running:
        clock.tick(FPS)
        update_screen()
        update_player()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_a:
                    player.left_pressed = True
                if event.key == pg.K_d:
                    player.right_pressed = True
                if event.key == pg.K_SPACE:
                    if player.y <= SCREEN_HEIGHT - player.size[1]:
                        player.vel[1] -= jump_height
                        player.y -= 2
            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    player.left_pressed = False
                if event.key == pg.K_d:
                    player.right_pressed = False
                          

    pg.quit()   


if __name__ == '__main__':
    main()