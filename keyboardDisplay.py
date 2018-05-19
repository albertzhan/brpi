from pygame import *

init()
font.init()

height = 60
screen = display.set_mode((720,height*4))
screen.fill((180,180,180))
running = True

timesnr = font.SysFont("Times New Roman",15)

def keyboard(height,x,y,mx,my,mb):
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ._")
    numpad = list("123456789#0*")
    for i in range(4):
        for j in range(7):
            l = letters[i*7+j]
            col = (230,230,230) #colour of key, different if highlighted
            if Rect(x+1+j*60,y+1+i*height,58,height-2).collidepoint(mx,my):
                col = (200,200,200)
                if mb:
                    return str(l) #if it's pressed it returns a string
            draw.rect(screen,col,(x+1+j*60,y+1+i*height,58,height-2))
            textSurface = timesnr.render(l,True,(0,0,0))
            screen.blit(textSurface,(30-textSurface.get_width()//2+j*60,height//2-textSurface.get_height()//2+i*height))
    for i in range(4):
        for j in range(3):
            n = numpad[i*3+j]
            col = (230,230,230)
            if Rect(x+541+j*60,y+1+i*height,58,height-2).collidepoint(mx,my):
                col = (200,200,200)
                if mb:
                    return str(n) #if it's pressed it returns a string
            draw.rect(screen,col,(x+541+j*60,y+1+i*height,58,height-2))
            textSurface = timesnr.render(n,True,(0,0,0))
            screen.blit(textSurface,(571-textSurface.get_width()//2+j*60,height//2-textSurface.get_height()//2+i*height))
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    clicked = 0 if mb == (0,0,0) else 1
    keyboard(height,0,0,mx,my,clicked)
    
    display.flip()
quit()