import cv2, keyboardDisplay, zlib, pickle, face_recognition
from lomond import websocket
from pygame import *
init()
font.init()
websocket = websocket.WebSocket("ws://localhost:8888/brpi")
running = True
screen = display.set_mode((720,480))
cam = cv2.VideoCapture(0)
clockity = time.Clock()
oldKey = ""
tries = 0
stage = 1
buttonFont = font.Font("../BurbankBigCondensed-Bold.otf",30)
connectScreen = transform.smoothscale(image.load('HomeScr-Scaled.png').convert(),screen.get_size())
connectButton = Rect(230, 200, 260,100)
name = ""
pictureTaken = False
face = None
timesnr = font.Font("../BurbankBigCondensed-Bold.otf",35)
camButton = transform.smoothscale(image.load('purple_square.png').convert_alpha(), (80,100))
takePicButton = Rect(640, 190, 80, 100)
connected = False
while running: #this will keep trying to connect the websocket if the websocket dc's
    screen.fill((0, 0, 0))
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()[0]
    if stage != 1:
        for ws in websocket.connect(poll=0): # this is essentially the new event loop, it will stop running if the connection is broken
            screen.fill((0, 0, 0))
            if ws.name=='poll':
                pass
            elif ws.name == 'connected':
                connected = True
            elif ws.name == 'disconnected':
                connected = False
            else:
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
                if pictureTaken:
                    screen.fill((130, 130, 230))
                    keyPress = keyboardDisplay.keyboard(screen, 50, 0, 280, mx, my, mb)
                    if keyPress != None and keyPress != oldKey:
                        print(keyPress)
                        if keyPress == "backspace":
                            if len(name) > 0:
                                name = name[:len(name) - 1]
                        elif keyPress == 'enter':
                            out = zlib.compress(pickle.dumps((0,frame, name)))
                            websocket.send_binary(out)
                            print('face sent')
                        else:
                            name += keyPress
                        oldKey = keyPress
                    elif keyPress == None:
                        oldKey = ''
                    draw.rect(screen, (255, 255, 255), (0, 245, 720, 35))
                    screen.blit(timesnr.render(name, True, (0, 0, 0)), (0, 245))
                    screen.blit(face, (360-face.get_width()//2, 10))
                    drawFont = timesnr.render("Name:", True, (255,255,255))
                    screen.blit(drawFont, (360-drawFont.get_width()//2, 200))
                else:
                    stuff, frame = cam.read()
                    pySurf = transform.rotate(surfarray.make_surface(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), -90)
                    screen.blit(pySurf, (0, 240-pySurf.get_height()//2))
                    screen.blit(camButton, takePicButton.topleft)
                    if takePicButton.collidepoint(mx,my):
                        if mb:
                            faces = face_recognition.face_locations(frame)
                            if len(faces)>0:
                                fPos = faces[0]
                                pictureTaken = True
                                print(fPos)
                                box = Rect(640 - fPos[1], fPos[0], fPos[1] - fPos[3], fPos[2] - fPos[0]).move(-10,-10).inflate(20,20)
                                newWidth = int(box.width*185/box.height)
                                face = transform.smoothscale(pySurf.subsurface(box),(newWidth,185))
            elif stage == 3:
                pass
            elif stage == 4:
               pass
            print(connected)
            if connected:
                display.flip()
                clockity.tick(30)
        screen.fill((0, 0, 0))
        connectText = buttonFont.render("Connecting...", True, (255,255,255))
        screen.blit(connectText, (360-connectText.get_width()//2,240-connectText.get_height()//2))
        tries+=1
        if tries == 5:
            print('failed to connect')
            tries = 0
            stage = 1
        display.flip()
        clockity.tick(30)
    else:
        pictureTaken = False
        name = ''
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
