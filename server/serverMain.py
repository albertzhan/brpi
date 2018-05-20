import tornado.websocket, tornado.ioloop, tornado.web
import client
import time, face_recognition
import pickle, zlib
clients = {} #each socket object points to [client object, face encoding, name]
faces = []
names = []
healths = []#1,2 or 3 hearts left. once dead, -1
submitted = []
hit = []
kills = []
lastHitTime = []

rank = 1

ftimer = 0 #tracking time
ctdtimer = 0
stage = "fill" ##"countdown" "game" "end"
klog = ""
def registerHit(facestuffs):
    global faces, names
    face_locations = face_recognition.face_locations(facestuffs)#figure out the location of faces
    unknown_encodings = face_recognition.face_encodings(facestuffs,knows_face_locations=face_locations)
    found = []
    for i,j in zip(unknown_encodings,face_locations):
        results = face_recognition.compare_faces(faceData, i, tolerance = 0.4125)
        for k,l in zip(names,results):
            if l:
                print('hit %s'%k)
                found.append(k)
    return found

def checkGameEnd():
    c = 0
    for k in healths:
        if k > 0:
            c += 1
    if c <2 : #game is ended
        for c in clients:
            myi = names.index(clients[c][2])
            #rank, kills, hits, submitted(fired)
            c.write_message("endgame rank "+str(-1*rank[myi])+" kills "+str(kills[myi])+" hits "+str(hits[myi])+" submitted "+str(submitted[myi]))
            stage = "endgame"        
        
                
def periodic_callback():
    global ftimer, ctdtimer, faces, names

    checkGameEnd()
    
    if ftimer > 1:
        ftimer -= 1
        print(ftimer)
        for c in clients:
            c.write_message("awaitcountdown "+str(ftimer-1))
            
    allFaced = True
    for c in clients:
        if str(clients[c][1]) == "0":
            allFaced = False
    if len(clients) < 2:
        allFaced = False
    if ftimer == 0 and allFaced:
        ftimer = 31
    if not allFaced:
        ftimer = 0
    elif ftimer == 1 and allFaced:
        stage = "countdown"

        
        for c in clients:
            faces.append(clients[c][1]) #create the indexed faces names
            names.append(clients[c][2])
            healths.append(3)
            submitted.append(0)
            hit.append(0)
            lastHitTime.append(0)
            kills.append(0)

            
        ftimer = -1
        ctdtimer = 11
        print("countdown started")
    if ctdtimer > 1:
        ctdtimer -= 1
        for c in clients:
            c.write_message("countdown "+str(ctdtimer-1))
        print(ctdtimer)
    elif ctdtimer == 1:
        stage = "game"
        ctdtimer-=1
        print("game started", faces,names)
        for c in clients:
            c.write_message("gamestart")        
        
class wsHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global ftimer,stage
        if stage == "fill":
            clients[self] = [client.Client(self),0,None]
            self.write_message(str((0,stage)))
        else:
            self.write_message("you are too late")
            self.close()
    def on_message(self, message):
        global ftimer,stage, names, faces, rank
        ##first char determines types of messages:
        ##0training picture + name
        ##1picture "shots"
        message = pickle.loads(
                zlib.decompress(message)) #unpacking
        if message[0] == 0:# set sockets links to faces and names
            clients[self][1] = face_recognition.face_encodings(message[1])[0]
            clients[self][2] = message[2] #this is the name
            ##if 2 guys with face, ftimer = 30
            self.write_message("face registered")
        if message[0] == 1: #this is a picture shot
            hit = registerHit(clients[self][2],message[1])#returns all the members that were hit
            submitted[names.index(clients[self][2])] += 1
            if len(hit) > 0:
                hit[names.index(clients[self][2])] += 1
                self.write_message("hit")
            rank += len(hit)
            for c in clients: #loop through the names
                i = names.index(clients[c][2])
                if names[i] in hit: #check if this mans got hit
                    if time.time() - lastHitTime[i]> 5.5: #actually deal damage to the guy
                        lastHitTime[i] = time.time() #invulnerability
                        c.write_message("hitted")
                        healths[i] -= 1
                        if healths[i] == 0: #killed someone
                            healths[i] = 0-rank
                            for c in clients:
                                c.write_message("kill killed " + names[i] + " killer " + clients[self][2])
                                klog = klog + clients[self][2] + " killed " + names[i] + "\n"
                                kills[names.index(clients[self][2])] += 1
    def on_close(self):
        del clients[self]

 
if __name__ == "__main__":
    app = tornado.web.Application([(r'/brpi', wsHandler)])
    app.listen(8888)
    tornado.ioloop.PeriodicCallback(periodic_callback,1000).start()
    print('callback started')
    tornado.ioloop.IOLoop.current().start()
