import tornado.websocket, tornado.ioloop, tornado.web
import client
clients = {}
stage = "fill"
def periodic_callback():
    print("hi")
class wsHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients[self] = client.Client(self)
        self.write_message(str((0,stage)))
    def on_message(self, message):
        pass
    def on_close(self):
        del clients[self]
if __name__ == "__main__":
    app = tornado.web.Application([(r'/brpi', wsHandler)])
    app.listen(8888)
    tornado.ioloop.PeriodicCallback(periodic_callback,1000).start()
    print('callback started')
    tornado.ioloop.IOLoop.current().start()