import cv2, numpy, zlib, pickle
from pygame import *
from lomond import WebSocket
from lomond.persist import persist
#font.init()
connected = False
websocket = WebSocket('ws://localhost:8888/brpi')
clockity=time.Clock()
screen = display.set_mode((640,480))
#text = font.SysFont('consolas',30)
cam = cv2.VideoCapture(0)
for evt in websocket.connect(poll=0):
    if evt.name=='text':
        print('received:', evt.text)
    elif evt.name == 'ready':
        connected = True
        #websocket.send_text('hi')
    elif evt.name == 'poll':
        pass
    elif evt.name == 'closed' or evt.name=='connect_fail' or evt.name=='disconnected':
        print(evt.name)
        cam.release()
        websocket.close()
        quit()
        break
    else:
        print('unknown event:',evt.name)
    suc, frame = cam.read()
    frameConv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    for e in event.get():
        if e.type==QUIT:
            cam.release()
            websocket.close()
            quit()
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                out = zlib.compress(pickle.dumps((0, frameConv)))#prepare image for sending
                print(len(out))
                websocket.send_binary(out)#send image to server
            elif e.key == K_t:
                out = zlib.compress(pickle.dumps((1, frameConv, input('name?\n>>> '))))
                print(len(out))
                websocket.send_binary(out)
    screen.blit(transform.rotate(surfarray.make_surface(frameConv),-90),(0,0))
    display.set_caption(str(clockity.get_fps()))
    display.flip()
    clockity.tick(30)
