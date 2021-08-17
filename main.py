import pygame,sys,random
from misc import get_all_fruits,get_all_sweets
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
pygame.display.set_caption("Yuk Makan Sehat") # set window title 
clock = pygame.time.Clock() # used for fps setting
game_font = pygame.font.Font("asset/font/emilys-candy/EmilysCandy-Regular.ttf", 36)
bg_surface = pygame.image.load("asset/misc/greenPortraitBg.png").convert()
bg_surface = pygame.transform.scale(bg_surface,(288,512))
FPS = 120 # FPS
START = False

# COLORS
BLUE = (10, 231, 255)

#menambah variabel kiri kanan
CHILD_MEASURE = 48
MIDDLE_SCREEN = (288 - CHILD_MEASURE)/2
SPAWNBUAH = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNBUAH,500)
buah_list=[]

HIGH_SCORE = 0
SCORE = 0
HEALTH = 3

def reset_game():
    global SCORE
    global HEALTH
    SCORE = 0
    HEALTH = 3

def score_display(start = True, high = False):
    score = HIGH_SCORE if high else SCORE
    title = "High Score: " if high else "Score :"
    to_render = title + str(int(score)) if not start else str(int(score))
    score_surface = game_font.render(to_render,True,BLUE)
    if not start:
        if high:
            score_rect = score_surface.get_rect(midbottom = (144,512))
        else:
            score_rect = score_surface.get_rect(midtop = (144,0))
    else:
        if high:
            score_rect = score_surface.get_rect(topleft = (0,0))
        else:
            score_rect = score_surface.get_rect(midtop = (144,0))
            

    
    # score_surface = game_font.render(str(int(score)),True,(0,0,0))
    # score_rect = score_surface.get_rect(topleft = topleft)
    SCREEN.blit(score_surface,score_rect)
def init_display():
    cloud_image = pygame.image.load("asset/misc/cloud.png").convert_alpha()
    cloud_surface = pygame.transform.scale(cloud_image,(288,220))
    cloud_rect = cloud_surface.get_rect(center = (144,256))
    welcome_surface = game_font.render("Enter to Play",True,BLUE)
    welcome_rect = welcome_surface.get_rect(center = (144,256))
    SCREEN.blit(cloud_surface,cloud_rect)
    SCREEN.blit(welcome_surface,welcome_rect)
    score_display(start=False)
    score_display(high=True, start=False)
    
def health_display():
    health_surface = game_font.render(str(int(HEALTH)),True,(0,0,255))
    health_rect = health_surface.get_rect(topright = (288,0))
    SCREEN.blit(health_surface,health_rect)
def create_buah():
    random_pos = random.choice(posisi_buah)
    random_score = random.choice([-1,1,1])
    random_pict = random.choice([0,1,2,3,4])
    if random_score == 1:
        image = buah_images[random_pict]
        
    else:
        image = poison_images[random_pict]
        # buah_rect = BuahOrPoison(poison_images[random_pict].get_rect(topleft = (MIDDLE_SCREEN + (random_pos*CHILD_MEASURE),0)),random_score,random_pict)
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
        buah.rect.centery += 2
    visible_buah = [buah for buah in buahs if buah.rect.bottom <= 512+CHILD_MEASURE] 
    return visible_buah
def check_collision(buahs):
    global SCORE
    global HEALTH
    for i in range(len(buahs)):
        if child_rect.colliderect(buahs[i].rect):
            if buahs[i].score == 1:
                SCORE += buahs[i].score
            else:
                HEALTH += buahs[i].score
            buahs.pop(i)
            return HEALTH > 0
    return HEALTH > 0
            

###### ANAKNYA #####
child_image = pygame.image.load('asset/sprites_splitted/child.png').convert_alpha() 
child_image = pygame.transform.scale(child_image, (CHILD_MEASURE, CHILD_MEASURE))
child_rect = child_image.get_rect(topleft = (MIDDLE_SCREEN,464))

########### Buah #########
buah_images = [pygame.image.load(i) for i in get_all_fruits()]
buah_images = [pygame.transform.scale(i,(CHILD_MEASURE,CHILD_MEASURE)) for i in buah_images]
poison_images = [pygame.image.load('asset/sprites_splitted/snack{}.png'.format(i)).convert_alpha() for i in range(5)]
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
        score_display(start= True, high=False)
        score_display(start= True, high=True)
        health_display()
    else:
        if SCORE > HIGH_SCORE:
            HIGH_SCORE = SCORE
        for event in pygame.event.get(): # get list of event
            if event.type == pygame.QUIT: 
                pygame.quit() #quit 
                sys.exit() #exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    START = True
                    reset_game()
        init_display()
    pygame.display.update() # update render
#ini komen