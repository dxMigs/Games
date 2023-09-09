import pygame
from pygame import mixer
class Settings:

    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (35, 118, 7)
        mixer.music.load('Music/perpertuummobile.mp3')
        mixer.music.play(-1)
        self.border = pygame.Surface([10, self.screen_height])
        self.border.fill((240, 0, 0))
        self.enemy_wall = pygame.Surface([10, 60])
        self.enemy_wall.set_alpha(270)
        self.enemy_wall.fill((0, 0, 200))
       

        self.bullet_speed = 18.0
        self.bullet_width = 18
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        self.reload_time = 300

        self.enemy_moving_vertical_speed = round(float(1) * 100) / 100
        self.start_enemy_dodge_time_max = 7000
        self.start_enemy_dodge_time_min = 3000       

         
        
