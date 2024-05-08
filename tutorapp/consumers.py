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
        #print(text_data_json)
        message = text_data_json["roomName"]
        sent_type = text_data_json["type"]
        message_sdp = text_data_json.get("sdp", "")

        print("Received message (room name): ", message)
        print("Received type: ", sent_type)
        print("Received sdp: ", message_sdp)

        if (sent_type == "offer") or (sent_type == "answer"):
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message",
                                       "text_data_json": text_data_json}
            )
            return

        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "chat.message",
        #                            "text_data_json": text_data_json}
        # )

    async def chat_message(self, event):
        message = event["text_data_json"]
        sent_type = message["type"]
        message_sdp = message["sdp"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                "type": sent_type,
                "message_sdp": message_sdp,})
        )