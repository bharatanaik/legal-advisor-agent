import json
import time
from channels.generic.websocket import WebsocketConsumer
from core.settings import app
from main.agent import query

from main.utils import LEGAL_ADVISOR_PROMPT

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.accept()
        print(LEGAL_ADVISOR_PROMPT)
        for chunk, checkpoint, is_stop in query(app, self.room_name, LEGAL_ADVISOR_PROMPT):
            self.send(text_data=json.dumps({"message": chunk, "checkpoint":checkpoint, "is_stop":is_stop}))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        for chunk, checkpoint, is_stop in query(app, self.room_name, message):
            self.send(text_data=json.dumps({"message": chunk, "checkpoint":checkpoint, "is_stop":is_stop}))