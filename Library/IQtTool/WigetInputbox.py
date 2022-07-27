from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from .WigetInputboxGUI import Ui_Form
class WigetInputbox(QWidget,Ui_Form):
    def __init__(self,title="",parent=None,calllog=None,callmethod=None,color:str="#00bcd4") -> None:
        super(WigetInputbox,self).__init__(parent=parent)
        self.setupUi(self)
        from .IconTool import setIcon
        setIcon(self=self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("InputBox")
        self.title=title
        self.setColor(color)
        self.calllog=calllog
        self.callmethod=callmethod
        self.CloseBtn.clicked.connect(self.okchoice)
    def okchoice(self):
        if self.calllog != None:
            self.calllog.infolog("Input as "+self.lineEdit.text())
        self.close()
        self.callmethod(self.lineEdit.text())
    def setColor(self,color:str="#00bcd4"):
        self.label.setText(f"<font color='{color}'>"+self.title+"<font>")
        self.label_2.setStyleSheet(f"border: 2px solid {color};")
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
