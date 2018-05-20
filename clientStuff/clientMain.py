# noinspection PyUnresolvedReferences
import cv2, keyboardDisplay, zlib, pickle, face_recognition
from lomond import websocket
from pygame import *
import time as tm
init()
font.init()
websocket = websocket.WebSocket("ws://192.168.137.102:8888/brpi")
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
camButton = transform.smoothscale(image.load('purple_square.png').convert_alpha(), (80,480))
camButton.fill((130,130,230))
takePicButton = Rect(640, 0, 80, 480)
connected = False
headOutline = image.load('Head.png').convert_alpha()
headRatio = headOutline.get_width()/headOutline.get_height()
headOutline = transform.smoothscale(headOutline, (int(headRatio*400), 400))
takePicImage = transform.smoothscale(image.load('cartooncamera.png').convert_alpha(),(68,45))
timeRemaining = 30
awaitcountDownStarted = False
countDownstarted = False
lives = 3
lastPicTime = 0
killQueue = []
isHit = 0
hitTarget = 0
dead = False
hitMarker = transform.smoothscale(image.load('redhitmark.png').convert_alpha(), (100,100))
lifeCounter = transform.smoothscale(image.load('redHeart.png').convert_alpha(), (70,70))
awaiting = transform.smoothscale(image.load('Awaiting.png').convert_alpha(), (720,480))
while running: #this will keep trying to connect the websocket if the websocket dc's
    screen.fill((0, 0, 0))
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()[0]
    if stage != 1:
        for ws in websocket.connect(poll=0): # this is essentially the new event loop, it will stop running if the connection is broken
            screen.fill((0, 0, 0))
            if ws.name=='poll':
                pass
            elif ws.name == 'text':
                tDat = ws.text.split()
                if tDat[0] == 'awaitcountdown':
                    awaitcountDownStarted = True
                    timeRemaining = int(tDat[1])
                elif tDat[0] == 'countdown':
                    countDownstarted = True
                    timeRemaining = int(tDat[1])
                elif tDat[0] == 'gamestart':
                    stage =4
                elif tDat[0] == 'kill':
                    killQueue.append((tDat[0], tDat[1],60))
                elif tDat[0] == 'hitted':
                    isHit = 150
                    lives-=1
                elif tDat[0] == 'hit':
                    hitTarget = 15
                print(ws.text)
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
                            stage = 3
                            print('face sent')
                            print('welcome, %s'%name)
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
                    screen.blit(headOutline, (360-headOutline.get_width()//2, 240-headOutline.get_height()//2))
                    screen.blit(camButton, takePicButton.topleft)
                    screen.blit(takePicImage, (takePicButton.centerx-takePicImage.get_width()//2, takePicButton.centery-takePicImage.get_height()//2))
                    if takePicButton.collidepoint(mx,my):
                        if mb:
                            faces = face_recognition.face_locations(frame)
                            if len(faces)>0:
                                fPos = faces[0]
                                pictureTaken = True
                                box = Rect(640 - fPos[1], fPos[0], fPos[1] - fPos[3], fPos[2] - fPos[0]).move(-10,-10).inflate(20,20)
                                newWidth = int(box.width*185/box.height)
                                face = transform.smoothscale(pySurf.subsurface(box),(newWidth,185))
            elif stage == 3:
                for e in event.get():
                    if e.type==QUIT:
                        running = False
                        websocket.close()
                screen.blit(awaiting, (0,0))
                if countDownstarted:
                    waitingText = timesnr.render("Game Starts in", True, (255, 255, 255))
                    screen.blit(waitingText, (360 - waitingText.get_width() // 2, 240 - waitingText.get_height() // 2))
                    awaitingCountDownText = buttonFont.render(str(timeRemaining), True, (255, 255, 255))
                    screen.blit(awaitingCountDownText, (360-awaitingCountDownText.get_width()//2, 270-awaitingCountDownText.get_height()//2))
                    awaitingCountDownText = buttonFont.render("Use this time to hide!", True, (255, 255, 255))
                    screen.blit(awaitingCountDownText, (360-awaitingCountDownText.get_width()//2, 300-awaitingCountDownText.get_height()//2))
                elif awaitcountDownStarted:
                    waitingText = timesnr.render("Awaiting Countdown...", True, (255, 255, 255))
                    screen.blit(waitingText, (360 - waitingText.get_width() // 2, 240 - waitingText.get_height() // 2))
                    awaitingCountDownText = buttonFont.render(str(timeRemaining), True, (255, 255, 255))
                    screen.blit(awaitingCountDownText, (360-awaitingCountDownText.get_width()//2, 270-awaitingCountDownText.get_height()//2))
                else:
                    waitingText = timesnr.render("Waiting for more players...", True, (255, 255, 255))
                    screen.blit(waitingText, (360 - waitingText.get_width() // 2, 240 - waitingText.get_height() // 2))
            elif stage == 4:
                mx, my = mouse.get_pos()
                mb = mouse.get_pressed()[0]
                for e in event.get():
                    if e.type==QUIT:
                        running = False
                        websocket.close()
                stuff, frame = cam.read()
                screen.fill((130,130,230))
                pySurf = transform.rotate(surfarray.make_surface(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), -90)
                uiTransparent = Surface((720,480), SRCALPHA)
                uiTransparent.set_alpha(20)
                draw.circle(uiTransparent, (200, 200, 200), (100,380), 100,3)
                screen.blit(pySurf, (0, 240 - pySurf.get_height() // 2))
                screen.blit(uiTransparent, (0,0))
                if len(killQueue) > 0:
                    if killQueue[0][2] > 0:
                        if killQueue[0][0] == name:
                            stage = 5
                            dead = True
                        killText = buttonFont.render('%-10s killed %10s'%(killQueue[0][1], killQueue[0][0]), True, (255,255,255),(130,130,230))
                        screen.blit(killText,(360-killText.get_width()//2, 0))
                        killQueue[0][2]-=1
                    else:
                        del killQueue[0]
                if hitTarget> 0:
                    screen.blit(hitMarker, (360-hitMarker.get_width()//2,240-hitMarker.get_height()//2))
                    hitTarget-=1
                #print(((100-mx)**2)+(380-my)**2, tm.time()-lastPicTime, lastPicTime)
                if ((100-mx)**2)+(380-my)**2 <= 10000 and tm.time()-lastPicTime >3:
                    if mb:
                        out = zlib.compress(pickle.dumps((1,frame)))
                        websocket.send_binary(out)
                        lastPicTime = tm.time()
                        print('bang')
                for i in range(lives):
                    screen.blit(lifeCounter, (645,i*90+90))
                if isHit > 0:
                    isHit-=1
                    uiTransparent = Surface((720,480),SRCALPHA)
                    uiTransparent.set_alpha(40)
                    uiTransparent.fill((0,0,0))
                    invulnFont = timesnr.render("You've been hit!", True, (255,255,255))
                    screen.blit(invulnFont, (360-invulnFont.get_width()//2,240-invulnFont.get_height()//2))
                    timeRemainingInv = buttonFont.render('Invulnerability ends in %d'%(isHit//30+1), True, (255,255,255))
                    screen.blit(timeRemainingInv, (360 - timeRemainingInv.get_width() // 2, 280 - timeRemainingInv.get_height() // 2))
            elif stage == 5:
                for e in event.get():
                    if e.type==QUIT:
                        running = False
                        websocket.close()
                screen.fill((0,0,0))

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
