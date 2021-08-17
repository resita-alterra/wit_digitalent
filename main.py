import pygame,sys,random
from misc import get_all_fruits,get_all_sweets,asset_path
from pprint import pprint
pygame.init()
pygame.font.init()
class BuahOrPoison():
    def __init__(self,the_rect,score,image) -> None:
        self.rect = the_rect
        self.score = score
        self.pict = image
# 1 draw screen & init

SCREEN = pygame.display.set_mode((288,512)) # screen size 
pygame.display.set_caption("Yuk, Makan Buah") # set window title 
clock = pygame.time.Clock() # used for fps setting
game_font = pygame.font.Font("asset/font/emilys-candy/EmilysCandy-Regular.ttf", 36)
game_font_20 = pygame.font.Font("asset/font/emilys-candy/EmilysCandy-Regular.ttf", 24)
bg_surface = pygame.image.load("asset/misc/greenPortraitBg.png").convert()
bg_surface = pygame.transform.scale(bg_surface,(288,512))
FPS = 120 # FPS
START = False

# SOUNDS 
point_sound = pygame.mixer.Sound('asset/sound/power-up.mp3')
level_sound = pygame.mixer.Sound('asset/sound/get_point.mp3')
health_sound = pygame.mixer.Sound('asset/sound/lose_health.mp3')
over_sound = pygame.mixer.Sound('asset/sound/game_over.mp3')
# COLORS
BLUE = (15, 50, 138)

CHILD_MEASURE = 48
MIDDLE_SCREEN = (288 - CHILD_MEASURE)/2
SPAWNBUAH = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNBUAH,500)
buah_list=[]

# tidak berubah ubah
HIGH_SCORE = 0
ACCEL = 1
LEVEL_SCORE = 10

# direset tiap game baru
SCORE = 0
HEALTH = 3
LEVEL = 1
LEVEL_SPEED = 2


def reset_game():
    global SCORE
    global HEALTH
    global buah_list
    global child_rect
    global LEVEL
    global LEVEL_SPEED
    SCORE = 0
    HEALTH = 3
    LEVEL = 1
    LEVEL_SPEED = 2
    buah_list = []
    child_rect.centerx = 144

def display_up_bar():
    atas_image = pygame.image.load("asset/misc/g9254.png").convert_alpha()
    atas_surface = pygame.transform.scale(atas_image,(400,80))
    atas_rect = atas_surface.get_rect(center = (144,0))

    star_image = pygame.image.load("asset/misc/starOn.png").convert_alpha()
    star_surface = pygame.transform.scale(star_image,(20,20))
    star_rect = atas_surface.get_rect(topleft = (0,8))

    SCREEN.blit(atas_surface,atas_rect)
    SCREEN.blit(star_surface,star_rect)


def score_display(start = True, high = False):

    score = HIGH_SCORE if high else SCORE
    title = "High Score: " if high else "Score: "
    to_render = title + str(int(score)) if not start else str(int(score))
    score_surface = game_font_20.render(to_render,True,BLUE)
    if not start:
        if high:
            score_rect = score_surface.get_rect(midbottom = (144,500))
        else:
            score_rect = score_surface.get_rect(midtop = (144,12))
    else:
        if high:
            score_rect = score_surface.get_rect(topleft = (24,6))
        else:
            score_rect = score_surface.get_rect(midtop = (144,6))
 
    SCREEN.blit(score_surface,score_rect)
def init_display():
    ####### Enter to play
    cloud_image = pygame.image.load("asset/misc/g9236.png").convert_alpha()
    cloud_surface = pygame.transform.scale(cloud_image,(240,50))
    cloud_rect = cloud_surface.get_rect(center = (144,400))
    welcome_surface = game_font_20.render("Enter to Play",True,BLUE)
    welcome_rect = welcome_surface.get_rect(center = (144,400))

    ####### Judul
    frame_image = pygame.image.load("asset/misc/Framed_less_no_text.png").convert_alpha()
    frame_surface = pygame.transform.scale(frame_image,(264,100))
    frame_rect = frame_surface.get_rect(center=(144,256))
    title_surface = game_font_20.render("Yuk, Makan Buah",True,BLUE)
    title_rect = title_surface.get_rect(center = (144,250))

    SCREEN.blit(cloud_surface,cloud_rect)
    SCREEN.blit(welcome_surface,welcome_rect)
    SCREEN.blit(frame_surface,frame_rect)
    SCREEN.blit(title_surface,title_rect)

    score_display(start=False)
    score_display(high=True, start=False)
    
def health_display():
    health_image = pygame.image.load("asset/misc/health{}.png".format(str(HEALTH))).convert_alpha()
    health_surface = pygame.transform.scale(health_image,(22*3,22))
    health_rect = health_surface.get_rect(topright = (286,6))

    SCREEN.blit(health_surface,health_rect)
    
def display_level():
    bawah_image = pygame.image.load("asset/misc/g9254.png").convert_alpha()
    bawah_surface = pygame.transform.scale(bawah_image,(400,60))
    bawah_rect = bawah_surface.get_rect(center = (144,512))
    level_surface = game_font_20.render("lvl:"+str(int(LEVEL)),True,BLUE)
    level_rect = level_surface.get_rect(bottomleft = (2,510))
    SCREEN.blit(bawah_surface,bawah_rect)
    SCREEN.blit(level_surface,level_rect)

def create_buah():
    random_pos = random.choice(posisi_buah)
    random_score = random.choice([-1,1,1])
    random_pict = random.choice([0,1,2,3,4])
    if random_score == 1:
        image = buah_images[random_pict]
        
    else:
        image = poison_images[random_pict]
    buah_rect = BuahOrPoison(image.get_rect(topleft = (MIDDLE_SCREEN + (random_pos*CHILD_MEASURE),0)),random_score,image)
    return [buah_rect]
def draw_buah(buahs):
    for buah in buahs:
        if buah.score == 1:
            SCREEN.blit(buah.pict,buah.rect)
        else:
            SCREEN.blit(buah.pict,buah.rect)
def move_buah(buahs): 
    for buah in buahs:
        buah.rect.centery += LEVEL_SPEED
    visible_buah = [buah for buah in buahs if buah.rect.bottom <= 512+CHILD_MEASURE] 
    return visible_buah
def check_collision(buahs):
    global SCORE
    global HEALTH
    global LEVEL
    global LEVEL_SPEED
    for i in range(len(buahs)):
        if child_rect.colliderect(buahs[i].rect):
            if buahs[i].score == 1:
                point_sound.play()
                SCORE += buahs[i].score
            else:
                health_sound.play()
                HEALTH += buahs[i].score
            buahs.pop(i)
            if SCORE >= LEVEL * LEVEL_SCORE:
                level_sound.play()
                LEVEL +=1
                LEVEL_SPEED += ACCEL
            if HEALTH<= 0:
                over_sound.play() 
            return HEALTH > 0
    return HEALTH > 0
            

###### ANAKNYA #####
child_image = pygame.image.load('asset/player/row-1-column-2.png').convert_alpha() 
child_image = pygame.transform.scale(child_image, (CHILD_MEASURE, CHILD_MEASURE))
child_rect = child_image.get_rect(topleft = (MIDDLE_SCREEN,434))

########### Buah #########
buah_images = [pygame.image.load(i) for i in get_all_fruits()]
buah_images = [pygame.transform.scale(i,(CHILD_MEASURE,CHILD_MEASURE)) for i in buah_images]
poison_images = [pygame.image.load(i) for i in get_all_sweets()]
poison_images = [pygame.transform.scale(i,(CHILD_MEASURE,CHILD_MEASURE)) for i in poison_images]
posisi_buah = [-2,-1,0,1,2]


while True:
    SCREEN.blit(bg_surface,(0,0))

    if START:
        START = check_collision(buah_list)
        location = 0
        clock.tick(FPS) # ensure the event only at FPS setting 
        for event in pygame.event.get(): # get list of event
            # if window close -> 'x' was clicked
            if event.type == pygame.QUIT: 
                pygame.quit() #quit 
                sys.exit() #exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    location -= 1
                if event.key == pygame.K_RIGHT:
                    location += 1
            if event.type == SPAWNBUAH:
                buah_list += create_buah()
        new_x_center = child_rect.centerx + (location*CHILD_MEASURE)
        # Check apakah new_x_center berada antara 48 dan 240 (inklusif)
        if new_x_center >= 48 and new_x_center <= 240:
            # kalau ngga berada di nilai itu, lewatin aja
            child_rect.centerx += (location*CHILD_MEASURE)

            
        
        # Fill the background with white
        SCREEN.blit(child_image,child_rect)
        buah_list = move_buah(buah_list)
        draw_buah(buah_list)
        display_up_bar()
        score_display(start= True, high=False)
        score_display(start= True, high=True)
        health_display()
        display_level()
    else:
        if SCORE > HIGH_SCORE:
            HIGH_SCORE = SCORE
        for event in pygame.event.get(): # get list of event
            if event.type == pygame.QUIT: 
                pygame.quit() #quit 
                sys.exit() #exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    START = True
                    reset_game()
        init_display()
    pygame.display.update() # update render
#ini komen