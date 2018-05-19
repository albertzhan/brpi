import tornado.websocket, tornado.ioloop, tornado.web
class WebsocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('socket opened')
    def on_message(self, message):
        self.write_message("echo! "+message)
    def on_close(self):
        print("socket closed")
if __name__ == "__main__":
    app = tornado.web.Application(['r/brpi', WebsocketHandler])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    