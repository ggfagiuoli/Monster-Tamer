from src.window import Window
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

window = Window()
window.show()

app.exec()