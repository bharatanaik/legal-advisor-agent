import json
from channels.generic.websocket import WebsocketConsumer
from core.settings import app
from main.agent import query

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        for chunk in query(app, self.room_name, message):
            self.send(text_data=json.dumps({"message": chunk}))