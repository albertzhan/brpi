import lomond, cv2
from pygame import *

running = True
screen = display.set_mode((720,480))
cam = cv2.VideoCapture(0)
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    mx, my = mouse.get_pos()
    stuff, frame = cam.read()
    pySurf = transform.rotate(surfarray.make_surface(cv2.COLOR_BGR2RGB(frame)),-90)
cam.release()
quit()
