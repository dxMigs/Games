import pygame
import random
from pygame.sprite import Sprite
from enemy_bullet import EnemyBullet




class EnemyTank(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.previous_time = pygame.time.get_ticks()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.moving = True
        self.moving_up = False
        self.moving_down = False
        
        self.side_move = False

        self.image = pygame.image.load('Graphics/sherman.bmp')
        self.image = pygame.transform.scale(self.image, (132, 60))
        self.rect = self.image.get_rect()
        self.collideRect =  pygame.rect.Rect((0, 0), (132, 28)) 
        self.collideRect.midbottom = self.rect.midbottom

        self.rect.midright = self.screen_rect.midright
        self.collideRect.midright = self.screen_rect.midright
 


        

    def draw_enemy_tank(self):
        self.screen.blit(self.image, self.rect)

        

    def update(self):    

        if self.moving:
            if not self.moving_up and not self.moving_down:
                self.randomint = random.randint(0,1)

                if self.randomint == 0:
                    self.moving_up = True
                else:
                    self.moving_down = True

            if self.moving_up and self.rect.top > 0:
                if self.moving_up:
                    self.rect.y -=  self.settings.enemy_moving_vertical_speed
                    self.collideRect.y -= self.settings.enemy_moving_vertical_speed
               
            if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                if self.moving_down:
                    self.rect.y += self.settings.enemy_moving_vertical_speed
                    self.collideRect.y += self.settings.enemy_moving_vertical_speed
                            
            self.current_time = pygame.time.get_ticks()

            if self.moving_up and self.current_time - self.previous_time > random.randint(self.settings.start_enemy_dodge_time_min, self.settings.start_enemy_dodge_time_max):
                self.previous_time = self.current_time
                self.moving_up = False
                self.moving_down = True

            if self.moving_down and self.current_time - self.previous_time > random.randint(self.settings.start_enemy_dodge_time_min, self.settings.start_enemy_dodge_time_max):
                self.previous_time = self.current_time
                self.moving_up = True
                self.moving_down = False

       

        
   