class Requester:
    def __init__(self):
        self.response = None
        pass

    def send_request(self, body: dict):
        pass

    def get_response(self):
        return self.response

    def reset(self):
        self.response = None


class StubLoginRequester(Requester):
    def __init__(self):
        super().__init__()

    def send_request(self, body: dict) -> dict:
        self.response = {"token":"just-a-random-token"}

    def get_response(self):
        return self.response