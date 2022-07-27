import ctypes
from PyQt5.QtGui import QIcon
from uuid import uuid4
boxicon="Data/box.png"
def setIcon(self):
    try:
        self.setWindowIcon(QIcon(boxicon))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.github.iaxretailer.box.%s"%uuid4())
    except:
        pass