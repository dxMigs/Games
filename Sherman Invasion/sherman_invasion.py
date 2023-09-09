import sys
import pygame
import random
from settings import Settings
from tank import Tank
from bullet import Bullet
from pygame import mixer
from enemy_tank import EnemyTank
from enemy_bullet import EnemyBullet


class ShermanInvasion:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sherman Invasion")
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.tank = Tank(self) 
        self.enemy_tank = EnemyTank(self)
        self.i = 1
        self.loops = 0
        self.level = 0
        self.lives = 3
        self.border_x = 180
        self.enemy_wall_x = self.settings.screen_width - 155
        self.enemy_wall_y = self.settings.screen_height / 2 - 30

       
        

        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemy_tanks = pygame.sprite.Group()
        
         

        self.clock = pygame.time.Clock()
        self.previous_time = pygame.time.get_ticks()

        self.move_side_event = pygame.USEREVENT + 1
        self.enemy_tank_shoot_event = pygame.USEREVENT + 2
        self.enemy_tank_spawn_event = pygame.USEREVENT + 3
        self.enemy_tank_getting_faster_event = pygame.USEREVENT + 4
        self.enemy_level_up_event = pygame.USEREVENT + 5


        pygame.time.set_timer(self.move_side_event, 25)
        pygame.time.set_timer(self.enemy_tank_shoot_event, 1800)
        pygame.time.set_timer(self.enemy_tank_spawn_event, 4000)
        pygame.time.set_timer(self.enemy_tank_getting_faster_event, 8000)
        

        self.previous_time = pygame.time.get_ticks()

        self.enemy_moving_horizontal_speed = round(float(1) * 100) / 100
        self._spawn_enemy_tank() 
        self.font = pygame.font.Font("freesansbold.ttf", 25)
        
           



    def run_game(self):
        while True:
            self._update_screen()
            self._check_events()
            self.bullets.update() 
            self.enemy_bullets.update()
            self.tank.update()
            
            
           

            self.enemy_tanks.update()

            self.collisions = pygame.sprite.groupcollide(self.bullets, self.enemy_tanks, True, True)
            

            
           
            
            
            for bullet in self.bullets.copy():
                if bullet.rect.right >= self.settings.screen_width:
                    self.bullets.remove(bullet)
                if bullet.rect.right >= self.enemy_wall_x and bullet.rect.bottom >= self.enemy_wall_y and bullet.rect.top <= self.enemy_wall_y + 60:
                    self.bullets.remove(bullet)

            for enemytank in self.enemy_tanks.copy():
                if enemytank.rect.left <= self.border_x:
                    self.enemy_tanks.remove(enemytank)
                    self.lives -= 1
            if self.lives < 0:
                sys.exit()

            self.clock.tick(60) 
            pygame.display.flip() 
       

    def _check_events(self):

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    elif event.key == pygame.K_DOWN:
                        self.tank.moving_up = False 
                        self.tank.moving_down = True
                    elif event.key == pygame.K_UP:
                        self.tank.moving_up = True 
                        self.tank.moving_down = False
                    elif event.key == pygame.K_s:
                        self.tank.moving_up = False
                        self.tank.moving_down = False
                        self.enemy_tanks.moving = False
                        

                    
                    elif event.key == pygame.K_SPACE:
                        self.current_time = pygame.time.get_ticks()
                          
                        if self.current_time - self.previous_time > 1600:
                            self.previous_time = self.current_time
                            self._fire_bullet()

                if event.type == self.move_side_event:
                    self.move_enemy_tank()

               # if event.type == self.enemy_tank_shoot_event:     
                    #self._fire_bullet_enemy()

                if event.type == self.enemy_tank_spawn_event:
                    self._spawn_enemy_tank()
                
                if event.type == self.enemy_level_up_event:
                    self._enemy_level_up
     

        

    def _enemy_level_up(self): 
       
        self.current_time = pygame.time.get_ticks()
                          
        if len(self.enemy_tanks) == 0 and self.current_time - self.previous_time > 100:
            self.previous_time = self.current_time
            self.level += 1
            self.loops = 0
            self._enemy_get_faster()
            self._spawn_enemy_tank()
            
       

    
    def _spawn_enemy_tank(self):
        self.loops += 1
        if self.loops <= 5:
            self.new_enemytank = EnemyTank(self)
            self.enemy_tanks.add(self.new_enemytank)
        else:
            self._enemy_level_up()
            
        
    def move_enemy_tank(self):
        for self.new_enemytank in self.enemy_tanks:
            self.new_enemytank.rect.x -= self.enemy_moving_horizontal_speed 
            self.new_enemytank.collideRect.x -= self.enemy_moving_horizontal_speed 

    def _enemy_get_faster(self):
        self.enemy_moving_horizontal_speed += 0.26
        self.settings.enemy_moving_vertical_speed += 0.26

        if self.level % 2 == 0:
            if self.settings.start_enemy_dodge_time_max >= 2500 and self.settings.start_enemy_dodge_time_min >= 800:
                self.settings.start_enemy_dodge_time_max -= 600
                self.settings.start_enemy_dodge_time_min -= 600
        


    def _fire_bullet_enemy(self):
        for self.new_enemytank in self.enemy_tanks:
            new_enemybullet = EnemyBullet(self)

            self.bullets.add(new_enemybullet)

            self.bullet_sound = mixer.Sound('Sounds/cannonshot.mp3')  
            self.bullet_sound.set_volume(0.3) 
            self.bullet_sound.play()

                    

    def _fire_bullet(self):
        
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            self.bullet_sound = mixer.Sound('Sounds/cannonshot.mp3')  
            self.bullet_sound.set_volume(0.3) 
            self.bullet_sound.play()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.settings.border, (self.border_x, 0))
        self.screen.blit(self.settings.enemy_wall, (self.enemy_wall_x, self.enemy_wall_y))
        self.leveldisplay = self.font.render(f"Level: {self.level}", False, (60,60,60))
        self.livedisplay = self.font.render(f" You have {self.lives} Lives", False, (60, 60, 60))
        self.screen.blit(self.leveldisplay, ((self.settings.screen_width / 2) - 30, (self.settings.screen_height / 2) - 250))
        self.screen.blit(self.livedisplay, ((self.settings.screen_width / 2) - 85, (self.settings.screen_height / 2) - 220))
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for enemybullet in self.bullets.sprites():
            enemybullet.draw_bullet()
        
        for enemytank in self.enemy_tanks.sprites():
            enemytank.draw_enemy_tank()
        
        
       
        self.tank.blitme()
        pygame.display.flip()
        
            



if __name__ == '__main__':
    ai = ShermanInvasion()
    ai.run_game()
  
 