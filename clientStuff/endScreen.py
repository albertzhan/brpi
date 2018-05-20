from pygame import *

init()
font.init()

medTxt = font.Font("../BurbankBigCondensed-Bold.otf",60)
bigTxt = font.Font("../BurbankBigCondensed-Bold.otf",80)
def drawEndScreen(surface,data):
    #0. rank
    #1. kills
    #2. hits
    #3. submitted
    titleRender = bigTxt.render("Results",True,(255,255,255))
    surface.blit(titleRender,(360-titleRender.get_width()//2,60))
    stats = ["Rank: ","Kills: ","Hits: ","Submitted: "]
    for i in range(4):
        statTxt = medTxt.render(stats[i],True,(255,255,255))
        surface.blit(statTxt,(100,150+70*i))
        resTxt = medTxt.render(str(data[i]),True,(255,255,255))
        surface.blit(resTxt,(620-resTxt.get_width(),150+70*i))
if __name__=="__main__":
    screen = display.set_mode((720, 480))
    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        drawEndScreen(screen,[0,0,0,0])
        display.flip()
    quit()
