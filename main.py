import pygame,sys,random 
pygame.init()
# 1 draw screen & init
SCREEN = pygame.display.set_mode((288,512)) # screen size 
pygame.display.set_caption("Yuk Makan Sehat") # set window title 
clock = pygame.time.Clock() # used for fps setting
FPS = 120 # FPS
CHILD_MEASURE = 48
#end1
#2 loop
# main loop of game Infinite loop 
# child_rect = pygame.Rect(120,464,CHILD_MEASURE,CHILD_MEASURE)
#3 let's add the bird
child_image = pygame.image.load('asset/sprites_splitted/child.png').convert_alpha() 
child_image = pygame.transform.scale(child_image, (CHILD_MEASURE, CHILD_MEASURE))
# bg_surface = pygame.image.load('assets/background-day.png').convert()
#rect for the position
child_rect = child_image.get_rect(topleft = (120,464))
while True:
    clock.tick(FPS) # ensure the event only at FPS setting 
    for event in pygame.event.get(): # get list of event
        # if window close -> 'x' was clicked
        if event.type == pygame.QUIT: 
            pygame.quit() #quit 
            sys.exit() #exit
        
    
    # Fill the background with white
    SCREEN.fill((255, 255, 255))
    SCREEN.blit(child_image,child_rect)
    pygame.display.update() # update render
