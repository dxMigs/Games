import pygame, random, math, time

#initilize pygame
pygame.init()

class Flak(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.vehicle_image = pygame.image.load("flakvehicle.png").convert_alpha()
        self.vehicle_image = pygame.transform.scale_by(self.vehicle_image, 0.2)
        self.rect = self.vehicle_image.get_rect(center = pos)

        self.gun_image = pygame.image.load("flakgun.png").convert_alpha()
        self.gun_image = pygame.transform.scale_by(self.gun_image, 0.2)
        self.gun_rect = self.gun_image.get_rect()
        self.gun_rect.centerx = self.rect.centerx
        self.gun_rect.centery = self.rect.centery - 30

        self.angle = 0
        self.mouse_position = (0, 0)

        self.rotated_gun_rect = self.gun_image.get_rect(center = pos)

        self.dy = 0
        self.dx = 0
    
    def get_mouse_position(self):
        self.mouse_position = pygame.mouse.get_pos()
        self.vektor_a1 = (self.mouse_position[0] - self.rotated_gun_rect.centerx)
        self.vektor_a2 = (self.mouse_position[1] - self.rotated_gun_rect.centery)

    def calculate_angle(self):
        self.angle = math.degrees(math.atan2(self.vektor_a1, self.vektor_a2))-180
        
    def gun_rotation(self):
        if self.angle > -270 and self.angle < -90: 
            self.rotated_gun_rect = self.rotated_gun_image.get_rect(center = self.rotated_gun_rect.center)
            self.rotated_gun_rect.centerx = self.rect.centerx
            self.rotated_gun_rect.centery = self.rect.centery - 30
        else:
            self.rotated_gun_image = pygame.transform.rotate(self.gun_image, self.angle)
            self.rotated_gun_rect = self.rotated_gun_image.get_rect(center = self.rotated_gun_rect.center)
            self.rotated_gun_rect.centerx = self.rect.centerx 
            self.rotated_gun_rect.centery = self.rect.centery - 30 

    def gun_position(self):
        if self.angle <= 0 and self.angle >= -90:
            self.dx = self.rotated_gun_rect.bottomleft[0] - self.rect.centerx + 5
            self.dy = self.rotated_gun_rect.bottomleft[1] - self.rect.centery   

        if self.angle < -270 and self.angle > -360:
            self.dx = abs(self.rotated_gun_rect.bottomleft[0] - self.rect.centerx) -5
            self.dy = self.rotated_gun_rect.bottomleft[1] - self.rect.centery
               
        self.rotated_gun_rect.centerx -= self.dx
        self.rotated_gun_rect.centery -= self.dy
                  
    def update(self):
        self.gun_rotation()
        self.get_mouse_position()
        self.calculate_angle()
        self.gun_position()
    
class Cloud(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.i = random.randint(1, 4)
        self.cloud = pygame.image.load(f"Clouds/{self.i}.png").convert_alpha()
        self.cloud = pygame.transform.scale_by(self.cloud, 1)
        self.cloud_rect = self.cloud.get_rect(center = pos)
    
class Bullet(pygame.sprite.Group):
    def __init__(self, pos):
        super().__init__()
        self.bullet_size = 5
        self.bullet_surface = pygame.Surface((self.bullet_size, self.bullet_size))
        self.bullet_surface.fill(BLACK)
        self.bullet_rect = self.bullet_surface.get_rect(center = pos)
        
        self.bullet_speed_x = 0
        self.bullet_speed_y = 0
        self.speed = bullet_speed
        self.directiony = 0
        self.directionx = 0
        self.calculate_bullet_direction()

        self.x = pos[0]
        self.y = pos[1]

    def calculate_bullet_direction(self):
        self.directionx = math.cos(math.radians(90 - abs(playervehicle.angle))) 
        self.directiony = -math.sin(math.radians(90 - abs(playervehicle.angle))) 

    def calculate_velocity(self):
        self.bullet_speed_x = self.directionx * self.speed 
        self.bullet_speed_y = self.directiony * self.speed 
        
    def move_bullet(self):
        self.x += self.bullet_speed_x
        self.y += self.bullet_speed_y
        self.bullet_rect.x = int(self.x)
        self.bullet_rect.y = int(self.y)

    def update(self):
        self.calculate_velocity()
        self.move_bullet()
        
class EnemyBomber(pygame.sprite.Sprite):
    def __init__(self, pos, hp, speed):
        super().__init__() 
        self.x_speed = -speed
        self.y_speed = 0

        self.i = random.randint(1,3)
        self.enemy_image = pygame.image.load(f"Planes/bomber{self.i}.jpg").convert_alpha()
        if self.i == 2:
            self.enemy_image = pygame.transform.scale(self.enemy_image, (200, 70))
        elif self.i == 1:
            self.enemy_image = pygame.transform.scale(self.enemy_image, (220, 76))
        elif self.i == 3:
            self.enemy_image = pygame.transform.scale(self.enemy_image, (200, 70))
        self.enemy_rect = self.enemy_image.get_rect(center = pos)
        self.collide_rect = pygame.Rect(self.enemy_rect.left, self.enemy_rect.centery - 5, 195, 24)

        self.max_hp = hp
        self.hp = self.max_hp

        self.x = pos[0]
        self.y = pos[1]

    def display_health(self):
        self.ratio = self.hp / self.max_hp
        if self.hp < self.max_hp:
            pygame.draw.rect(screen, RED, (self.collide_rect.left, self.collide_rect.bottom + 15, self.collide_rect.width, 5))
            pygame.draw.rect(screen, GREEN, (self.collide_rect.left, self.collide_rect.bottom + 15, self.collide_rect.width * self.ratio, 5))
        
    def movement(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.enemy_rect.x = int(self.x)
        self.enemy_rect.y = int(self.y)
        self.collide_rect.x = int(self.enemy_rect.left) 
        self.collide_rect.y = int(self.enemy_rect.centery)

class Base(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.base_image = pygame.image.load("Bases/HouseBase.png").convert_alpha()
        self.base_image = pygame.transform.scale_by(self.base_image, 0.5)
        self.base_rect = self.base_image.get_rect(bottomleft = pos)
        self.collide_rect = pygame.Rect(self.base_rect.left, self.base_rect.centery, self.base_rect.width, 20)
        self.max_hp = 100
        self.hp = self.max_hp

    def display_health(self):
        self.ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, RED, (self.base_rect.left + 21, self.base_rect.bottom + 10, 250, 25))
        pygame.draw.rect(screen, GREEN, (self.base_rect.left + 21, self.base_rect.bottom + 10, 250 * self.ratio, 25))

class Bomb(pygame.sprite.Group):
    def __init__(self, pos, bomber_speed):
        super().__init__()

        self.bomb_image = pygame.image.load("Bombs/bomb1.png").convert_alpha()
        self.bomb_image = pygame.transform.scale_by(self.bomb_image, 0.2)
        self.angle = 90
        self.bomb_image = pygame.transform.rotate(self.bomb_image, self.angle)
        self.bomb_rect = self.bomb_image.get_rect(center = pos)


        self.x_speed = bomber_speed

        self.t0 = time.time()
        self.t1 = 0

        self.x = pos[0]
        self.y = pos[1]

        self.rotated_bomb_rect = self.bomb_image.get_rect(center = pos)

    def calculate_angle(self):
        try:
            self.angle = math.degrees(math.atan(self.x_speed/self.y_speed))
        except ZeroDivisionError:
            self.angle = -90
      
        self.rotated_bomb_image = pygame.transform.rotate(self.bomb_image, self.angle)
        self.rotated_bomb_rect = self.rotated_bomb_image.get_rect(center = self.rotated_bomb_rect.center)

    def physics(self):
        self.drag_force = 0.5 * p0 * self.x_speed**2

        self.acceleration = self.drag_force/bombmass
        self.x_speed = self.acceleration * self.dt + self.x_speed
        self.y_speed = gravity * self.dt

        self.x += self.x_speed
        self.y += self.y_speed
        self.bomb_rect.x = int(self.x)
        self.bomb_rect.y = int(self.y)

        self.rotated_bomb_rect.center = self.bomb_rect.center

    def get_time(self):
        self.t1 = time.time()
        self.dt = self.t1 - self.t0
              
    def reset_timer(self):
        self.t0 = self.t1

class EnemyBattleBomber(pygame.sprite.Sprite):
    def __init__(self, pos, hp, lowest, highest):
        super().__init__() 
        self.random_speed = random.randint(lowest, highest)
        self.random_speed /= 10
        self.x_speed = -self.random_speed
        self.y_speed = 0

        self.i = random.randint(1,3)
        self.enemy_image = pygame.image.load(f"Planes/battlebomber{self.i}.jpg").convert_alpha()
        if self.i == 2:
            self.enemy_image = pygame.transform.scale(self.enemy_image, (150, 60))
        elif self.i == 1:
            self.enemy_image = pygame.transform.scale(self.enemy_image, (140, 46))
        elif self.i == 3:
            self.enemy_image = pygame.transform.scale(self.enemy_image, (130, 51))
        self.enemy_rect = self.enemy_image.get_rect(center = pos)
        self.collide_rect = pygame.Rect(self.enemy_rect.left, self.enemy_rect.centery, 130, 20)

        self.max_hp = hp
        self.hp = self.max_hp

        self.x = pos[0]
        self.y = pos[1]

    def display_health(self):
        self.ratio = self.hp / self.max_hp
        if self.hp < self.max_hp:
            pygame.draw.rect(screen, RED, (self.collide_rect.left + 5, self.collide_rect.bottom + 15, self.collide_rect.width, 5))
            pygame.draw.rect(screen, GREEN, (self.collide_rect.left + 5, self.collide_rect.bottom + 15, self.collide_rect.width * self.ratio, 5))
        
    def movement(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.enemy_rect.x = int(self.x)
        self.enemy_rect.y = int(self.y)
        self.collide_rect.x = int(self.enemy_rect.left) 
        self.collide_rect.y = int(self.enemy_rect.centery)

class Crosshair():
    def __init__(self):
        self.i = 62
        self.image = pygame.image.load(f"Crosshairs/PNG/Black/crosshair0{self.i}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
    
    def position(self):
        self.mouse_position = pygame.mouse.get_pos()
        self.rect.x = self.mouse_position[0] - 18
        self.rect.y = self.mouse_position[1]

#screen settings
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 600
FPS = 120

#colors
GREEN = (0, 240, 0)
BLUE = (0, 0, 240)
RED = (240, 0, 0)
LIGHT_BLUE = (80, 140, 190)
GRASS_COLOR = (86, 125, 70)
BULLET_COLOR = (234, 184, 35)
BLACK = (0, 0, 0)

#window settings
icon = pygame.image.load("Icon/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Flak Defender") 

#fonts
fontsize = 30
upgrades_size = 20
font = pygame.font.Font("freesansbold.ttf", fontsize)
upgrade_font = pygame.font.Font("freesansbold.ttf", upgrades_size)

#game variables
reload_time = 600
bullet_demage = 1
bullet_speed = 2
p0 = 1
bombmass = 100
gravity = 1.5
game_paused = False
money = 0
score = 0
upgrades = 1
enemybomber_hp = 5
enemybattlebomber_hp = 1
buying_phase = False
prize = 200
enemybomber_speed = 0.4
enemybattlebomber_speed_lowest = 8
enemybattlebomber_speed_highest = 15
max_enemybomber_hp = 25
max_enemybattlebomber_hp = 5
shoots_fired = 0
shoots_hits = 0

#sounds
shoot_sound = pygame.mixer.Sound("Sounds/shoot_sound.mp3")
shoot_sound.set_volume(0.1)

enemybattlebomber_sound = pygame.mixer.Sound("Sounds/plane_sound1.mp3")
enemybattlebomber_sound.set_volume(0.05)

hitmarker = pygame.mixer.Sound("Sounds/hitmarker.mp3")
hitmarker.set_volume(0.06)

#music
random_music = random.randint(1,3)
pygame.mixer.music.load(f"Music/music{random_music}.mp3")
pygame.mixer.music.set_volume(0.45)
pygame.mixer.music.play()

def backgroundmusic():
    if not pygame.mixer.music.get_busy():
        randommusic()

def randommusic():
    random_music1 = random.randint(1,3)
    pygame.mixer.music.load(f"Music/music{random_music1}.mp3")
    pygame.mixer.music.set_volume(0.45)
    pygame.mixer.music.play()

#bombers
bombers = []

#clock
clock = pygame.time.Clock()
previous_time = pygame.time.get_ticks()

#initilising screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

#ground
grass_height = 80
grass = pygame.Rect(screen_rect.left, screen_rect.bottom - grass_height, SCREEN_WIDTH, grass_height)

#initilizing player
y_pos_player = grass.top - 20
x_pos_player = SCREEN_WIDTH//2
playervehicle = Flak((x_pos_player, y_pos_player))
bullets = []

#crosshair
mouse_visible = False
crosshair = Crosshair()
pygame.mouse.set_visible(mouse_visible)

#randomizing clouds
clouds = []
for i in range(25):
    x_pos_cloud = random.randint(30, SCREEN_WIDTH - 30)
    y_pos_cloud = random.randint(0, SCREEN_HEIGHT - grass_height - 200)
    cloud = Cloud((x_pos_cloud, y_pos_cloud))
    clouds.append(cloud)

def spawn_enemy_bomber():
    global enemybomber
    hp = enemybomber_hp
    speed = enemybomber_speed
    x_pos_enemy = SCREEN_WIDTH + 100
    y_pos_enemy = random.randint(50, SCREEN_HEIGHT - grass_height - 300)
    enemybomber = EnemyBomber((x_pos_enemy, y_pos_enemy), hp, speed)    
    bombers.append(enemybomber)

def spawn_enemy_battlebomber():
    global enemybattlebomber
    hp = enemybattlebomber_hp
    lowest = enemybattlebomber_speed_lowest
    highest = enemybattlebomber_speed_highest
    x_pos_enemy = SCREEN_WIDTH + 100
    y_pos_enemy = random.randint(50, SCREEN_HEIGHT - grass_height - 300)
    enemybattlebomber = EnemyBattleBomber((x_pos_enemy, y_pos_enemy), hp, lowest, highest)    
    bombers.append(enemybattlebomber)

#bombs
bombs = []
bomb_spawner = True
t0 = time.time()
t1 = 0
def spawn_bombs(bomber):
    get_time()
    if dt >= 0.6:
        bomb = Bomb((bomber.enemy_rect.centerx, bomber.enemy_rect.centery), bomber.x_speed)
        bombs.append(bomb)
        reset_timer()

def check_bombs():
    global base
    for bomb in bombs:
        if bomb.bomb_rect.colliderect(base.collide_rect):
            bombs.remove(bomb)
            base.hp -= 2
        if bomb.bomb_rect.colliderect(grass):
            bombs.remove(bomb)

def get_time():
    global dt, t1
    t1 = time.time()
    dt = t1 - t0
              
def reset_timer():
    global t0
    t0 = t1

#base
x_pos_base = 20
y_pos_base = grass.top + 20
base = Base((x_pos_base, y_pos_base))

#function for keydown events
def keydown_events(event):
    global running, previous_time, current_time, money, upgrades, reload_time, bullet_speed, bullet_demage, buying_phase, prize, score, total_time
    if event.key == pygame.K_ESCAPE:
        running = False
    elif event.key == pygame.K_SPACE:
        current_time = pygame.time.get_ticks()
        if current_time - previous_time > reload_time:
            previous_time = current_time
            new_bullet = Bullet((playervehicle.rotated_gun_rect.centerx, playervehicle.rotated_gun_rect.centery))
            bullets.append(new_bullet)

    elif event.key == pygame.K_F1 and buying_phase == True and reload_time > 200:
        money -= prize
        upgrades += 1
        reload_time_upgrade()
        buying_phase = False
        prize += upgrades * 100
    elif event.key == pygame.K_F2 and buying_phase == True and bullet_demage < 6:
        money -= prize
        upgrades += 1
        bullet_demage_upgrade()
        buying_phase = False
        prize += upgrades * 100
    elif event.key == pygame.K_F3 and buying_phase == True and bullet_speed < 5:
        money -= prize
        upgrades += 1
        bullet_speed_upgrade()
        buying_phase = False
        prize += upgrades * 100
    #elif event.key == pygame.K_F11:
    #    money += 1000000

def reload_time_upgrade():
    global reload_time
    if reload_time > 200:
        reload_time -= 100

def bullet_demage_upgrade():
    global bullet_demage
    if bullet_demage < 6:
        bullet_demage += 0.5

def bullet_speed_upgrade():
    global bullet_speed
    if bullet_speed < 5:
        bullet_speed += 1

def mouse_events():
    global previous_time, current_time,shoots_fired
    mouse_position = pygame.mouse.get_pos()
    if mouse_position[1] < grass.top - 35:
        if pygame.mouse.get_pressed()[0]:
            current_time = pygame.time.get_ticks()
            if current_time - previous_time > reload_time:
                previous_time = current_time
                new_bullet = Bullet((playervehicle.rotated_gun_rect.centerx, playervehicle.rotated_gun_rect.centery))
                bullets.append(new_bullet) 
                pygame.mixer.Sound.play(shoot_sound) 
                shoots_fired += 1

def bullet_collisions():
    global bullets, shoots_hits
    for bomber in bombers:
        for bullet in bullets:
            if bullet.bullet_rect.colliderect(bomber.collide_rect):
                bullets.remove(bullet)
                bomber.hp -= bullet_demage
                pygame.mixer.Sound.play(hitmarker)
                shoots_hits += 1


def check_bullets():
    for bullet in bullets:
        if len(bullets) > 0:
            if bullet.bullet_rect.x >= SCREEN_WIDTH or bullet.bullet_rect.x <= 0:
                try:
                    bullets.remove(bullet)
                except ValueError:
                    pass
            if bullet.bullet_rect.y >= SCREEN_HEIGHT or bullet.bullet_rect.y <= 0:
                try:
                    bullets.remove(bullet)
                except ValueError:
                    pass

def display_score():
    score_display = font.render(f"Score: {score}", True, BLACK)
    money_display = font.render(f"Money: {money}", True, BLACK)
    screen.blit(score_display, (screen_rect.topleft))
    screen.blit(money_display, (screen_rect.topleft[0], screen_rect.topleft[1] + fontsize))

def update_upgrades():
    global buying_phase
    if reload_time > 200:
        f1 = upgrade_font.render(f"(F1) Firerate Upgrade Prize: {prize}", True, BLACK)
    else: 
        f1 = upgrade_font.render(f"Max Firerate reached", True, BLACK)
    if bullet_demage < 6:
        f2 = upgrade_font.render(f"(F2) Demage Upgrade Prize: {prize}", True, BLACK)
    else:
        f2 = upgrade_font.render(f"Max Bullet Demage reached", True, BLACK)
    if bullet_speed < 5:
        f3 = upgrade_font.render(f"(F3) Bullet Speed Upgrade Prize: {prize}", True, BLACK)
    else:
        f3 = upgrade_font.render(f"Max Bullet Speed reached", True, BLACK)

    if prize <= money:
        buying_phase = True
        screen.blit(f1, (screen_rect.topleft[0], screen_rect.topleft[1] + 2 * fontsize))
        screen.blit(f2, (screen_rect.topleft[0], screen_rect.topleft[1] + 2 * fontsize + upgrades_size))
        screen.blit(f3, (screen_rect.topleft[0], screen_rect.topleft[1] + 2 * fontsize + 2 * upgrades_size))
        
#updating the screen
def update_screen():
    screen.fill(LIGHT_BLUE)
    for cloud in clouds:
        screen.blit(cloud.cloud, cloud.cloud_rect)
    
    for bullet in bullets:
        screen.blit(bullet.bullet_surface, bullet.bullet_rect)
        bullet.update()

    screen.blit(playervehicle.vehicle_image, playervehicle.rect)
    screen.blit(playervehicle.rotated_gun_image, playervehicle.rotated_gun_rect)

    for bomb in bombs:
        screen.blit(bomb.rotated_bomb_image, bomb.rotated_bomb_rect)

    for bomber in bombers:
        screen.blit(bomber.enemy_image, bomber.enemy_rect)
        
    screen.blit(base.base_image, base.base_rect)

    screen.blit(crosshair.image, crosshair.rect)

    try:
        hit_percentage = round(shoots_hits/shoots_fired * 100, 2)        
    except ZeroDivisionError:
        hit_percentage = 0.0
    
    display_hit_percentage = upgrade_font.render(f"Hit Rate: {hit_percentage}%", True, BLACK)


#events
enemybomber_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(enemybomber_spawn, 12000)

bombs_spawn = pygame.USEREVENT + 2

battlebomber_spawn = pygame.USEREVENT + 3

battlebomber_spawn_time = random.randint(9, 15)
def battle_bomber_spawn():
    global battlebomber_spawn_time, lowest_time, highest_time
    lowest_time = 5
    highest_time = 15
    if total_time % battlebomber_spawn_time == 0:
        pygame.event.post(pygame.event.Event(battlebomber_spawn))
        battlebomber_spawn_time = random.randint(lowest_time, highest_time)

def total_game_time():
    global total_time
    total_time = pygame.time.get_ticks()/1000
    total_time = round(total_time, 2)

spawn_enemy_bomber()        
running = True
while running:
    playervehicle.update()
    update_screen()
    pygame.draw.rect(screen, GRASS_COLOR, grass)
    base.display_health()
    mouse_events()
    bullet_collisions()
    check_bullets()
    check_bombs() 
    crosshair.position()
    display_score()
    total_game_time()
    update_upgrades()
    battle_bomber_spawn()
    backgroundmusic()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keydown_events(event)
        if event.type == enemybomber_spawn:
            spawn_enemy_bomber()
        if event.type == battlebomber_spawn:
            spawn_enemy_battlebomber()

    for bomber in bombers:
        bomber.movement()
        bomber.display_health()
        if bomber.enemy_rect.right < 0:
            bombers.remove(bomber)
            enemybattlebomber_sound.stop()
        if bomber.hp <= 0:
            if bomber.x_speed == enemybomber.x_speed:
                bombers.remove(bomber) 
                money += 200
            else: 
                bombers.remove(bomber) 
                money += 50

    #game getting harder
    if total_time % 5 == 0:
        score += 50

    #hp increase
    if total_time % 45 == 0 and enemybattlebomber_hp < max_enemybattlebomber_hp:
        enemybattlebomber_hp += 1
    if total_time % 45 == 0 and enemybomber_hp < max_enemybomber_hp:
        enemybomber_hp += 2

    #speed increase
    if total_time % 30 == 0 and enemybomber_speed < 0.8:
        enemybomber_speed += 0.1
    if total_time % 30 == 0 and enemybattlebomber_speed_lowest < 12:
        enemybattlebomber_speed_highest += 1 
        enemybattlebomber_speed_lowest += 1

    #spawnrate increase 
    if score % 1000 == 0 and highest_time > 8:
        highest_time -= 1
    if score % 1500 == 0 and lowest_time > 2:
        lowest_time -= 1

    #hit percentage
    try:
        hit_percentage = round(shoots_hits/shoots_fired * 100, 1)        
    except ZeroDivisionError:
        hit_percentage = 0.0
    
    display_hit_percentage = upgrade_font.render(f"Hit Percentage: {hit_percentage}%", True, BLACK)
    screen.blit(display_hit_percentage, (playervehicle.rect.bottomleft[0]-56, playervehicle.rect.bottomleft[1]+20))

    if bomb_spawner:
        for bomber in bombers:
            distance = math.sqrt(2*bomber.enemy_rect.bottom / gravity) * abs(bomber.x_speed)
            if bomber.enemy_rect.centerx - base.collide_rect.right <= distance + abs(bomber.x_speed)*55 and bomber.enemy_rect.centerx - (base.collide_rect.left + base.collide_rect.centerx)/2 >= 0 + abs(bomber.x_speed)*35 :
                spawn_bombs(bomber)



    if base.hp <= 0:
        running = False

    for bomb in bombs:
        bomb.get_time()
        bomb.physics()
        bomb.calculate_angle()

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
