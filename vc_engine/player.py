import asyncio
import av

class AudioGenerator:
    def __init__(self, file_path):
        self.file_path = file_path

    async def get_frame(self):
        if not hasattr(self, "container"):
            self.container = av.open(self.file_path)
            self.stream = self.container.streams.audio[0]

        for frame in self.container.decode(self.stream):
            return frame
        await asyncio.sleep(0.02)