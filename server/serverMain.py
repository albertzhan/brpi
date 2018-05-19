import tornado.websocket, tornado.ioloop, tornado.web
import client
import time
clients = {} #each socket object points to [client object, face encoding, name]

ftimer = 0 #tracking time
ctdtimer = 0
stage = "fill" ##"countdown" "game"
def periodic_callback():
    global ftimer, ctdtimer
    print("hi")
    if ftimer > 1:
        ftimer -= 1
    elif ftimer == 1:
        stage = "countdown"
        ctdtimer = 11
        print("countdown started")
    if ctdtimer > 1:
        ctdtimer -= 1
    elif ctdtimer == 1:
        stage = "game"
        print("game started")
        
        
class wsHandler(tornado.websocket.WebSocketHandler):
    global ftimer,stage
    def open(self):
        if stage == "fill":
            clients[self] = [client.Client(self),null,null]
            ftimer = 31 #30sec delay to start the game
            print("one")
            self.write_message(str((0,stage)))
        else:
            self.write_message("you are too late")
    def on_message(self, message):
        ##first char determines types of messages:
        ##0training picture + name
        ##1picture "shots"
        message = pickle.loads(zlib.decompress(message)) #unpacking
        if message[0] == 0:# set sockets links to faces and names
            clients[self][1] = face_recognition.face_encodings(message[1])[0]
            clients[self][2] = message[2] #this is the name
            self.write_message("face registered")
        if message[1] == 0: #this is a picture shot
##            registerHit(self,message[1])
            
        
##        
            pass
    def on_close(self):
        del clients[self]

 
if __name__ == "__main__":
    app = tornado.web.Application([(r'/brpi', wsHandler)])
    app.listen(8888)
    tornado.ioloop.PeriodicCallback(periodic_callback,1000).start()
    print('callback started')
    tornado.ioloop.IOLoop.current().start()
