import pygame,sys,random 
pygame.init()
# 1 draw screen & init
SCREEN = pygame.display.set_mode((288,512)) # screen size 
pygame.display.set_caption("Yuk Makan Sehat") # set window title 
clock = pygame.time.Clock() # used for fps setting
FPS = 120 # FPS
CHILD_MEASURE = 48
MIDDLE_SCREEN = (288 - CHILD_MEASURE)/2
SPAWNBUAH = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNBUAH,500)
buah_list=[]
def create_buah():
    random_pos = random.choice(posisi_buah)
    buah_rect = buah_image.get_rect(topleft = (MIDDLE_SCREEN + (random_pos*CHILD_MEASURE),0)) 
    return [buah_rect]
def draw_buah(buahs):
    for buah in buahs:
        SCREEN.blit(buah_image,buah)
def move_buah(buahs): 
    for buah in buahs:
        buah.centery += 2
    visible_buah = [buah for buah in buahs if buah.bottom <= 512+CHILD_MEASURE] 
    return visible_buah

###### ANAKNYA #####
child_image = pygame.image.load('asset/sprites_splitted/child.png').convert_alpha() 
child_image = pygame.transform.scale(child_image, (CHILD_MEASURE, CHILD_MEASURE))
child_rect = child_image.get_rect(topleft = (MIDDLE_SCREEN,464))

########### Buah #########
buah_image =  pygame.image.load('asset/sprites_splitted/buah.png').convert_alpha() 
buah_image = pygame.transform.scale(buah_image, (CHILD_MEASURE, CHILD_MEASURE))
posisi_buah = [-2,-1,0,1,2]
# buah_list += create_buah()

while True:
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
    child_rect.centerx += (location*CHILD_MEASURE)
        
    
    # Fill the background with white
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(child_image,child_rect)
    buah_list = move_buah(buah_list)
    draw_buah(buah_list)
    pygame.display.update() # update render
