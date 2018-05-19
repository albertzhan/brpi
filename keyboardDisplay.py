from pygame import *

init()
font.init()

height = 60
screen = display.set_mode((720,height*4))
screen.fill((180,180,180))
running = True

timesnr = font.SysFont("Times New Roman",15)
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ._")
numpad = list("123456789#0*")
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    mx,my = mouse.get_pos()

    for i in range(4):
        for j in range(7):
            l = letters[i*7+j]
            col = (230,230,230) #colour of key, different if highlighted
            if Rect(1+j*60,1+i*height,58,height-2).collidepoint(mx,my):
                col = (200,200,200)
            draw.rect(screen,col,(1+j*60,1+i*height,58,height-2))
            textSurface = timesnr.render(l,True,(0,0,0))
            screen.blit(textSurface,(30-textSurface.get_width()//2+j*60,30-textSurface.get_height()//2+i*60))
    for i in range(4):
        for j in range(3):
            n = numpad[i*3+j]
            col = (230,230,230)
            if Rect(541+j*60,1+i*height,58,height-2).collidepoint(mx,my):
                col = (200,200,200)
            draw.rect(screen,col,(541+j*60,1+i*height,58,height-2))
            textSurface = timesnr.render(n,True,(0,0,0))
            screen.blit(textSurface,(571-textSurface.get_width()//2+j*60,30-textSurface.get_height()//2+i*60))
    display.flip()
quit()
