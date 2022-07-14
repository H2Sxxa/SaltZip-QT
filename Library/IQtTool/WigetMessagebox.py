from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from .WigetMessageboxGUI import Ui_Form
class WigetMessagebox(QWidget,Ui_Form):
    def __init__(self,desc=[""],title="",parent=None) -> None:
        super(WigetMessagebox,self).__init__(parent=parent)
        self.m_flag=False
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("MessageBox")
        self.title=title
        self.setColor()
        for descline in desc:
            self.textBrowser.append(descline)
        self.CloseBtn.clicked.connect(self.close)
    def setColor(self,color:str="#4DD0E1"):
        self.label.setText("<font color='#4DD0E1'>"+self.title+"<font>")
        self.label_2.setStyleSheet("border: 2px solid #4DD0E1;")
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
