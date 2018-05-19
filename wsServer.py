import tornado.ioloop
import tornado.web
import tornado.websocket
import zlib, pickle, numpy, random, face_recognition
from pygame import *

faceData = []
names = []

CAPTURE_FACES = 0
TRAIN_MODEL = 1
class MainHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('socket opened')
    def on_message(self, message):
        if len(message) <2000:
            print(message)
        else:
            print(len(message))
            message = pickle.loads(zlib.decompress(message))#unpack message
            if message[0] == CAPTURE_FACES:
                face_locations = face_recognition.face_locations(message[1])
                unknown_encodings = face_recognition.face_encodings(message[1],known_face_locations=face_locations)
                for i,j in zip(unknown_encodings, face_locations):
                    results = face_recognition.compare_faces(faceData, i, tolerance=0.4125)
                    found = []
                    for k,l in zip(names, results):
                        if l:
                            print('found %s'%k)
                            found.append(k)
                    self.write_message("faces found, %s"%', '.join(found))
                self.write_message('face_captured')
            elif message[0] == TRAIN_MODEL:
                names.append(message[2])
                faceData.append(face_recognition.face_encodings(message[1])[0])
                self.write_message('face_trained')
    def on_close(self):
        print('socket closed')
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
