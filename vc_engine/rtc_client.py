import json
from aiortc import RTCPeerConnection, MediaStreamTrack

class AudioTrack(MediaStreamTrack):
    kind = "audio"
    def __init__(self, generator):
        super().__init__()
        self.generator = generator

    async def recv(self):
        frame = await self.generator.get_frame()
        return frame

class RTCClient:
    def __init__(self, audio_generator):
        self.pc = RTCPeerConnection()
        self.track = AudioTrack(audio_generator)
        self.pc.addTrack(self.track)

    async def create_offer(self):
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        return json.dumps({"sdp": offer.sdp, "type": offer.type})

    async def set_answer(self, ans):
        data = json.loads(ans)
        await self.pc.setRemoteDescription(
            RTCSessionDescription(sdp=data["sdp"], type=data["type"])
        )