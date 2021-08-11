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
while True:
    clock.tick(FPS) # ensure the event only at FPS setting 
    for event in pygame.event.get(): # get list of event
        # if window close -> 'x' was clicked
        if event.type == pygame.QUIT: 
            pygame.quit() #quit 
            sys.exit() #exit
        
    
    # Fill the background with white
    SCREEN.fill((255, 255, 255))
    pygame.draw.rect(SCREEN, (0, 0, 255), pygame.Rect(120,464,CHILD_MEASURE,CHILD_MEASURE))
    pygame.display.update() # update render
