class Client:
    def __init__(self, websocket_connection, lives=3):
        self.lives = lives
        self.shots = 0
        self.websocket_connection = websocket_connection