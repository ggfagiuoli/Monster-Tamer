from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

# Merely meant to be used like an enum
class ORIENTATION:
    class ENUM:
        def __init__(self, o):
            self.o = o

        def __eq__(self, other):
            return self.o == other.o

    HORIZONTAL = ENUM(0)
    VERTICAL = ENUM(1)



def subWidget(wids: list[QWidget], orientation: ORIENTATION.ENUM):
    qw = QWidget()
    lay = QHBoxLayout() if orientation == ORIENTATION.HORIZONTAL else QVBoxLayout()
    for wid in wids:
        lay.addWidget(wid)
    qw.setLayout(lay)
    return qw