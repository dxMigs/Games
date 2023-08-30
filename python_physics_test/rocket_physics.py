
import pygame, math, time, random


class Rocket(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        #reset time event
        self.reset_time_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.reset_time_event, 100)
        
        #rocket settings
        self.pictures = []
        self.player_speed_x = 0
        self.player_speed_y = 0
        self.directionx = 0
        self.directiony = 0
        self.velx = 0
        self.vely = 0
        self.acceleration = 2
        self.dt = 0
        self.t0 = time.time()
        self.t1 = 0

        #variables
        self.clicked = False
        self.moved = False
        self.rotated = False
        self.accelerating = False

        #angle
        self.angle = 0
        self.mouse_position = (0, 0)

        #load picture
        picture = pygame.image.load("spaceship.png").convert_alpha()
        picture_2 = pygame.image.load("spaceship_2.png").convert_alpha()

        #create a rocket
        self.original_rocket_picture = pygame.transform.scale(picture, (100, 220))
        self.original_rocket_picture_2 = pygame.transform.scale(picture_2, (100, 279))
        self.collide_rect =  pygame.rect.Rect((pos), (100, 100))
        self.pictures.append(self.original_rocket_picture)
        self.pictures.append(self.original_rocket_picture_2)

        # Initialize the rotated_rects with a default value
        self.rotated_rect = self.original_rocket_picture.get_rect(center = pos)
        self.rotated_rect_fire = self.original_rocket_picture_2.get_rect(center = pos)
        
    #rotate picture
    def player_rotation(self):
        self.rotated_picture = pygame.transform.rotate(self.pictures[0], self.angle)
        self.rotated_picture_fire = pygame.transform.rotate(self.pictures[1], self.angle)
        self.rotated_rect = self.rotated_picture.get_rect(center = self.rotated_rect.center)
        self.rotated_rect_fire = self.rotated_picture_fire.get_rect(center = self.rotated_rect_fire.center) 

    #get mouse position and calculate vektor
    def get_mouse_position(self):
        self.mouse_position = pygame.mouse.get_pos()
        self.vektor_a1 = (self.mouse_position[0] - self.rotated_rect.centerx + camera_group.offset[0])
        self.vektor_a2 = (self.mouse_position[1] - self.rotated_rect.centery + camera_group.offset[1])
       

    #calculate angle
    def calculate_angle(self):
        self.angle = math.degrees(math.atan2(self.vektor_a1, self.vektor_a2))-180

    #calculate the x and y compenents of the direction vector 
    def calculate_player_direction(self):
        self.directionx = math.cos(math.radians(90 - abs(self.angle))) 
        self.directiony = -math.sin(math.radians(90 - abs(self.angle))) 

        self.calculate_velocity()

    #calculate velocity with accelaration
    def calculate_velocity(self):
        self.player_speed_x += self.directionx * self.acceleration * self.dt
        self.player_speed_y += self.directiony * self.acceleration * self.dt

    #mouse input
    def input(self):
        if pygame.mouse.get_pressed()[0]:
            self.calculate_player_direction()
            self.get_time()
            self.accelerating = True
        else:
            self.reset_timer()
            self.accelerating = False

    #move the rocket
    def move_rocket(self):
        self.rotated_rect.x += self.player_speed_x
        self.rotated_rect.y += self.player_speed_y
        self.rotated_rect_fire.x += self.player_speed_x
        self.rotated_rect_fire.y += self.player_speed_y
        self.collide_rect.x += self.player_speed_x
        self.collide_rect.y += self.player_speed_y

    #accelaration time
    def get_time(self):
        self.t1 = time.time()
        self.dt = self.t1 - self.t0

    #reset time if not accelarating        
    def reset_timer(self):
        self.t0 = self.t1

    def wall_collision(self):
        if self.collide_rect.top <= -25000 or self.collide_rect.bottom >= 25000:
            self.player_speed_y *= -0.9
        if self.collide_rect.right >= 25000 or self.collide_rect.left <= -25000:
            self.player_speed_x *= -0.9
            
    def update(self):
        self.player_rotation() 
        self.get_mouse_position()
        self.calculate_angle()
        self.wall_collision()
        self.get_time()
        self.move_rocket()
        self.input()
        
class CameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
    
        self.space_surface = pygame.image.load("space_3.jpg")
        self.space_rect = self.space_surface.get_rect()

        #camera offset
        self.offset = pygame.math.Vector2()

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.random_star = random.randint(0, 3)

        self.space_surface_width = self.space_surface.get_width()
        self.tiles = math.ceil(SCREEN_WIDTH / self.space_surface_width)

        pygame.draw.rect(self.display_surface, RED, (-25000, -25000, 50000, 50000), 100)

    def center_target_camera(self,target):
        self.offset.x = target.rotated_rect.centerx - self.half_width
        self.offset.y = target.rotated_rect.centery - self.half_height
        self.offset.x = target.rotated_rect_fire.centerx - self.half_width
        self.offset.y = target.rotated_rect_fire.centery - self.half_height

    def costom_draw(self, player_rocket, asteroid):
        self.display_surface.fill("#030b15")
        self.display_surface.blit(self.space_surface, self.space_rect)

 
        pygame.draw.rect(self.display_surface, RED, (-25000 - self.offset[0], -25000 - self.offset[1], 50000, 50000), 100)

        self.center_target_camera(player_rocket)

        for asteroid in asteroids:
            offset_pos_asteroid = asteroid.rect.topleft - self.offset 
            self.display_surface.blit(asteroid.image, offset_pos_asteroid)

        for bullet in bullets:
            offset_pos_bullet = bullet.bullet_rect.topleft - self.offset
            self.display_surface.blit(bullet.lazer_bullet_image, offset_pos_bullet)
    
        if player_rocket.accelerating:
            offset_pos = player_rocket.rotated_rect_fire.topleft - self.offset
            self.display_surface.blit(player_rocket.rotated_picture_fire, offset_pos)
        else:
            offset_pos = player_rocket.rotated_rect.topleft - self.offset
            self.display_surface.blit(player_rocket.rotated_picture, offset_pos)  

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.random_angle = random.randint(0, 360)        
        self.random_size = random.randint(200, 400)
        self.image = pygame.image.load("Star_images/asteroid.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.random_size,  self.random_size))
        self.image = pygame.transform.rotate(self.image, self.random_angle)
        self.rect = self.image.get_rect(topleft = pos)        
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.lazer_bullet_image = pygame.image.load("Laser_bullets/Laser Sprites/14.png").convert_alpha()
        self.lazer_bullet_image = pygame.transform.rotate(self.lazer_bullet_image, player_rocket.angle + 90)
        self.lazer_bullet_image = pygame.transform.scale_by(self.lazer_bullet_image, 0.8)
        self.bullet_rect = self.lazer_bullet_image.get_rect(center = pos)
        self.initial_rect_x = self.bullet_rect.x
        self.initial_rect_y = self.bullet_rect.y

        
        self.bullet_speed_x = 0
        self.bullet_speed_y = 0
        self.speed = 9

        self.directionx, self.directiony = 0, 0
        self.calculate_bullet_direction()

    def calculate_bullet_direction(self):
        self.directionx = math.cos(math.radians(90 - abs(player_rocket.angle))) 
        self.directiony = -math.sin(math.radians(90 - abs(player_rocket.angle))) 

    def calculate_velocity(self):
        self.bullet_speed_x += self.directionx * self.speed 
        self.bullet_speed_y += self.directiony * self.speed   
       
    def move_bullet(self):
        self.bullet_rect.x += self.bullet_speed_x + player_rocket.player_speed_x
        self.bullet_rect.y += self.bullet_speed_y + player_rocket.player_speed_y
        
    def update(self):
        self.calculate_velocity()
        self.move_bullet()
            
#Initilize pygame
pygame.init()

#screen settings
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000
FPS = 60

#colors
BLUE = (0, 0, 240)
RED = (240, 0, 0)
GREEN = (0, 240, 0)
LIGHT_GREY = (169,169,169)
GREY = (135,135,135)
BLACK = (0, 0, 0)

#clock
clock = pygame.time.Clock()

#initilising screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

#font
font = pygame.font.Font("freesansbold.ttf", 25)

#setup
camera_group = CameraGroup()
player_rocket = Rocket((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), camera_group)
asteroids = []
for i in range (2000):
    x = random.randint(-25000 , 25000)
    y = random.randint(-25000, 25000)
    asteroid = Asteroid((x, y), camera_group)
    asteroids.append(asteroid)
bullets = []
for bullet in bullets:
    bullet.update()
    
background_music = pygame.mixer.music.load('Music/space_background.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

def engine_sound():
    if player_rocket.accelerating:
        rocket_sound = pygame.mixer.Sound("Music/rocket_sound.mp3")
        rocket_sound.set_volume(0.3) 
        rocket_sound.play(1)

#show information about the rocket in the top left corner
def display_velocity():
    speed = math.sqrt(player_rocket.player_speed_x**2 + player_rocket.player_speed_y**2)
    speed_x_display = font.render(f"Horizontal velocity: {round(player_rocket.player_speed_x, 2)}", True, LIGHT_GREY)
    speed_y_display = font.render(f"Vertical velocity: {round(player_rocket.player_speed_y, 2)}", True, LIGHT_GREY)
    speed_display = font.render(f"Overall speed: {round(speed, 2)}", True, LIGHT_GREY)
    time_display = font.render(f"Time: {round(player_rocket.dt, 1)}", True, LIGHT_GREY)
    acceleration_display = font.render(f"Acceleration: {player_rocket.acceleration}", True, LIGHT_GREY)
    coordinatesxy = font.render(f"X: {player_rocket.rotated_rect.centerx}, Y: {player_rocket.rotated_rect.centery}", True, LIGHT_GREY)
    screen.blit(speed_x_display, (screen_rect.topleft[0], screen_rect.topleft[1]))
    screen.blit(speed_y_display, (screen_rect.topleft[0], screen_rect.topleft[1] + 30))
    screen.blit(speed_display, (screen_rect.topleft[0], screen_rect.topleft[1] + 60))
    screen.blit(time_display, (screen_rect.topleft[0], screen_rect.topleft[1] + 90))
    screen.blit(acceleration_display, (screen_rect.topleft[0], screen_rect.topleft[1] + 120))
    screen.blit(coordinatesxy, (screen_rect.topleft[0], screen_rect.topleft[1] + 150))

def border():
    pygame.draw.rect(screen, RED, (-25000, -25000, 50000, 50000), 100)


     
#function for keypress events
def keypress_events(event):
    global running, new_bullet
    if event.key == pygame.K_ESCAPE:
        running = False
    if event.key == pygame.K_t:
        player_rocket.get_time()
    if event.key == pygame.K_r:
        player_rocket.rotated_rect.center = screen_rect.center
        player_rocket.rotated_rect_fire.center = screen_rect.center
    if event.key == pygame.K_UP:
        player_rocket.acceleration += 1
    if event.key == pygame.K_DOWN:
        player_rocket.acceleration -= 1   
    if event.key == pygame.K_e:
        player_rocket.acceleration = 5
    if event.key == pygame.K_s:
        player_rocket.player_speed_x, player_rocket.player_speed_y = 0, 0
    if event.key == pygame.K_SPACE:
        new_bullet = Bullet(player_rocket.rotated_rect.center, camera_group)
        bullets.append(new_bullet)
        
  
#Game loop
running = True
while running:  

    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keypress_events(event)
        if event.type == player_rocket.reset_time_event:
            player_rocket.reset_timer()
            

    
    camera_group.update()
    player_rocket.update()
    camera_group.costom_draw(player_rocket, asteroid)
    display_velocity()
    border()

    try:
        for bullet in bullets.copy():
            if abs(bullet.bullet_rect.right) >= 25000 or abs(bullet.bullet_rect.left) <= -25000:
                bullets.remove(bullet)
            if abs(bullet.bullet_rect.top) <= -25000 or abs(bullet.bullet_rect.bottom) >= 25000:
                bullets.remove(bullet)
    except ValueError:
        pass

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()

    
                