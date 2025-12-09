from telethon.tl.functions.phone import CreateGroupCallRequest, JoinGroupCallRequest
from telethon.tl.types import DataJSON

class VCSignaling:
    def __init__(self, client):
        self.client = client

    async def ensure_group_call(self, chat_id):
        info = await self.client(GetFullChannelRequest(chat_id))
        gc = info.full_chat.call

        if gc:
            return gc

        return await self.client(CreateGroupCallRequest(
            peer=chat_id,
            random_id=0
        ))

    async def join(self, chat_id, sdp_offer):
        gc = await self.ensure_group_call(chat_id)

        return await self.client(JoinGroupCallRequest(
            call=gc.call,
            params=DataJSON(sdp_offer),
            muted=False,
            video_stopped=True
        ))