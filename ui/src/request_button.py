from PySide6.QtWidgets import QPushButton
from src.requesters import Requester
from src.body_getters import BodyGetter

# When actually writing the real buttons i may have to use async requests and check the response in update()
class RequestButton(QPushButton):
    def __init__(self, requester: Requester, bodyGetter: BodyGetter, responseAction = lambda _: None):
        super().__init__()
        self.requester = requester
        self.bodyGetter = bodyGetter
        self.responseAction = responseAction
        self.clicked.connect(self.clickMethod)

    def setTextB(self, lab):
        self.setText(lab)
        return self

    def clickMethod(self):
        self.requester.send_request(self.bodyGetter.get())
        self.responseAction(self.requester.get_response())

    def reset(self):
        self.requester.reset()
