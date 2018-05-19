import cv2, keyboardDisplay
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
name = ""
timesnr = font.Font("../BurbankBigCondensed-Bold.otf",35)
while running: #this will keep trying to connect the websocket if the websocket dc's
    for ws in websocket.connect(poll=0): # this is essentially the new event loop, it will stop running if the connection is broken
        if ws.name!='poll':
            print(ws.name)
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
            else:
                name += keyPress
            oldKey = keyPress
        elif keyPress == None:
            oldKey = ''
        display.flip()
        clockity.tick(30)
        draw.rect(screen,(180,180,180),(0,480,720,35))
        screen.blit(timesnr.render(name,True,(0,0,0)),(0,480))
cam.release()
quit()
