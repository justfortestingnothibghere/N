class MusicQueue:
    def __init__(self):
        self.list = []

    def add(self, file):
        self.list.append(file)

    def next(self):
        if not self.list:
            return None
        return self.list.pop(0)