import tornado.websocket, tornado.ioloop, tornado.web
import client
clients = {}
stage = "fill"
class WebsocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients[self] = client.Client(self)
        self.write_message((0,stage))
    def on_message(self, message):
        pass
    def on_close(self):
        del clients[self]
if __name__ == "__main__":
    app = tornado.web.Application(['r/brpi', WebsocketHandler])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()