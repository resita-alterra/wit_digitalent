import pygame,sys,random 
pygame.init()
pygame.font.init()
class BuahOrPoison():
    def __init__(self,the_rect,score) -> None:
        self.rect = the_rect
        self.score = score
# 1 draw screen & init

SCREEN = pygame.display.set_mode((288,512)) # screen size 
pygame.display.set_caption("Yuk Makan Sehat") # set window title 
clock = pygame.time.Clock() # used for fps setting
game_font = pygame.font.SysFont("Arial", 36)
FPS = 120 # FPS
START = False

#menambah variabel batas atas

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

def score_display(topleft = (0,0),high = False):
    score = HIGH_SCORE if high else SCORE
    score_surface = game_font.render(str(int(score)),True,(0,0,0))
    score_rect = score_surface.get_rect(topleft = topleft)
    SCREEN.blit(score_surface,score_rect)
def init_display():
    init_surface = game_font.render("Hello, pencet spasi dong", True,(0,0,0))
    init_rect = init_surface.get_rect(center = (144,256))
    SCREEN.blit(init_surface,init_rect)
    score_display()
    score_display((144,0),True)
    
def health_display():
    health_surface = game_font.render(str(int(HEALTH)),True,(0,0,255))
    health_rect = health_surface.get_rect(topright = (288,0))
    SCREEN.blit(health_surface,health_rect)
def create_buah():
    random_pos = random.choice(posisi_buah)
    random_score = random.choice([-1,1])
    if random_score == 1:
        buah_rect = BuahOrPoison(buah_image.get_rect(topleft = (MIDDLE_SCREEN + (random_pos*CHILD_MEASURE),0)),random_score )
    else:
        buah_rect = BuahOrPoison(poison_image.get_rect(topleft = (MIDDLE_SCREEN + (random_pos*CHILD_MEASURE),0)),random_score )
    return [buah_rect]
def draw_buah(buahs):
    for buah in buahs:
        if buah.score == 1:
            SCREEN.blit(buah_image,buah.rect)
        else:
            SCREEN.blit(poison_image,buah.rect)
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
buah_image =  pygame.image.load('asset/sprites_splitted/buah.png').convert_alpha() 
buah_image = pygame.transform.scale(buah_image, (CHILD_MEASURE, CHILD_MEASURE))
poison_image =  pygame.image.load('asset/sprites_splitted/poison.png').convert_alpha() 
poison_image = pygame.transform.scale(poison_image, (CHILD_MEASURE, CHILD_MEASURE))
posisi_buah = [-2,-1,0,1,2]


while True:
    SCREEN.fill((255, 255, 255))
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
        score_display()
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