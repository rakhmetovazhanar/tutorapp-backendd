import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ConferenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connecting')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"conference_{self.room_name}"
        print("room name: ", self.room_name)
        print("group name: ", self.room_group_name)

        try:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print(f"User: {self.channel_name} added in group: {self.room_group_name}")
        except Exception as e:
            print(f"Error while adding user in group: {e}")

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
            try:
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "chat.message",
                                           "text_data_json": text_data_json
                                           }
                )
                print(f"Send message to group: {self.room_group_name}")
            except Exception as e:
                print(f"Error while sending message to group: {e}")

    async def chat_message(self, event):
        text_data_json = event["text_data_json"]

        sent_type = text_data_json["type"]
        message_room_name = text_data_json["roomName"]
        message_sdp = text_data_json["sdp"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                "type": sent_type,
                "roomName": message_room_name,
                "sdp": message_sdp
                })
        )