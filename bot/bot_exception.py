class IncorrectData(Exception):
    def __init__(self, text):
        self.text = text
