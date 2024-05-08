import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ConferenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connecting')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"conference_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["roomName"]
        sent_type = text_data_json["type"]
        message_sdp = text_data_json.get("sdp", "")

        print("Message sdp: ", message_sdp)
        print("Message room name: ", message)
        print("Message type: ", sent_type)

        if (sent_type == "offer") or (sent_type == "answer"):
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message",
                                       "sent_type": sent_type,
                                       "roomName": message,
                                       "sdp": message_sdp}
            )
            return

    async def chat_message(self, event):
        sent_type = event["sent_type"]
       # message_sdp = event["message_sdp"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                "type": sent_type,
                #"message_sdp": message_sdp,
                })
        )