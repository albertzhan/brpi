import cv2, keyboardDisplay, zlib, pickle
from lomond import websocket
from pygame import *
init()
font.init()
websocket = websocket.WebSocket("ws://localhost:8888/brpi")
running = True
screen = display.set_mode((720,515))
cam = cv2.VideoCapture(0)
clockity = time.Clock()
oldKey = ""
stage = 1
tries = 0
buttonFont = font.Font("../BurbankBigCondensed-Bold.otf",30)
connectScreen = transform.smoothscale(image.load('HomeScr-Scaled.png').convert(),screen.get_size())
connectButton = Rect(230, 200, 260,100)
name = ""
timesnr = font.Font("../BurbankBigCondensed-Bold.otf",35)
while running: #this will keep trying to connect the websocket if the websocket dc's
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()[0]
    if stage != 1:
        screen.fill((0,0,0))
        for ws in websocket.connect(poll=0): # this is essentially the new event loop, it will stop running if the connection is broken
            if ws.name!='poll':
                print(ws.name)
            mx, my = mouse.get_pos()
            mb = mouse.get_pressed()[0]
            for e in event.get():
                if e.type == QUIT:
                    running = False
                    websocket.close()
            if stage == 2:
                for e in event.get():
                    if e.type == QUIT:
                        running = False
                        websocket.close()
                mx, my = mouse.get_pos()
                mb = mouse.get_pressed()[0]
                stuff, frame = cam.read()
                pySurf = transform.rotate(surfarray.make_surface(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ),-90)
                screen.blit(pySurf, (0,0))
                keyPress = keyboardDisplay.keyboard(screen, 50, 0, 280,mx,my,mb)
                if keyPress!=None and keyPress!=oldKey:
                    print(keyPress)
                    if keyPress == "backspace":
                        if len(name) > 0:
                            name = name[:len(name)-1]
                    elif keyPress == "enter":
                        pass #do stuff with enter here
                    else:
                        name += keyPress
                    oldKey = keyPress
                elif keyPress == None:
                    oldKey = ''
                draw.rect(screen,(180,180,180),(0,480,720,35))
                screen.blit(timesnr.render(name,True,(0,0,0)),(0,480))
                display.flip()
                clockity.tick(30)
            elif stage == 3:
                pass
            elif stage == 4:
                pass
        connectText = buttonFont.render("Connecting...", True, (255,255,255))
        screen.blit(connectText, (360-connectText.get_width()//2,240-connectText.get_height()//2))
        tries+=1
        if tries == 5:
            print('failed to connect')
            tries = 0
            stage = 1
    else:
        for e in event.get():
            if e.type == QUIT:
                running = False
                websocket.close()
        screen.blit(connectScreen, (0,0))
        if connectButton.collidepoint(mx,my):
            draw.rect(screen, (255,255,0), connectButton)
            if mb:
                stage = 2
        else:
            draw.rect(screen, (140,120,220), connectButton)
        connectRender = buttonFont.render("Connect", True, (255,255,255))
        screen.blit(connectRender, (connectButton.centerx-connectRender.get_width()//2, connectButton.centery-connectRender.get_height()//2))
        display.flip()
        clockity.tick(30)
cam.release()
quit()
