import pygame

class Tank:

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        
        self.image = pygame.image.load('Graphics/Tiger1.bmp').convert()
        self.image = pygame.transform.scale(self.image, (164, 60))
        self.rect = self.image.get_rect()
        self.collideRect =  pygame.rect.Rect((0, 0), (164, 34)) 
        self.collideRect.midbottom = self.rect.midbottom


        self.rect.midleft = self.screen_rect.midleft
        self.collideRect.midleft = self.screen_rect.midleft
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)


    def update(self):
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= 3
            self.collideRect.y -= 3

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += 3
            self.collideRect.y += 3

