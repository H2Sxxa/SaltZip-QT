import ctypes
from PyQt5.QtGui import QIcon
boxicon="Data/box.png"
def setIcon(self):
    try:
        self.setWindowIcon(QIcon(boxicon))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.github.iaxretailer.saltzip.mainwindows")
    except:
        pass