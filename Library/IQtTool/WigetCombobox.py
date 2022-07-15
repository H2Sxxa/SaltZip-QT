from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from Library.Quet.lite.LiteLog import LiteLog
from .WigetComboboxGUI import Ui_Form
class WigetCombobox(QWidget,Ui_Form):
    def __init__(self,title="",parent=None,ChoiceList:list=[],calllog:LiteLog=None,callmethod=None,color:str="#00bcd4") -> None:
        super(WigetCombobox,self).__init__(parent=parent)
        self.m_flag=False
        self.myLog=LiteLog(name=__name__)
        self.calllog=calllog
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("ComboBox")
        self.title=title
        self.setColor(color)
        self.callmethod=callmethod
        if ChoiceList !=[]:
            for Choice,num in zip(ChoiceList,range(len(ChoiceList))):
                self.comboBox.addItem("")
                self.comboBox.setItemText(num, Choice)
        self.CloseBtn.clicked.connect(self.okchoice)
    def okchoice(self):
        if self.calllog != None:
            self.myLog.infolog("Chose as "+self.comboBox.itemText(self.comboBox.currentIndex()))
            self.calllog.appendtoQT(self.myLog.lastQTlog)
            self.calllog.logcache.append(self.myLog.lastlog)
        self.close()
        self.callmethod(self.comboBox.itemText(self.comboBox.currentIndex()))
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
