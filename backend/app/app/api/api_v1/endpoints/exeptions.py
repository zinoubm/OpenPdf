class MaxBodySizeException(Exception):
    def __init__(self, body_len: str):
        self.body_len = body_len
