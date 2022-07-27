from PyQt5.QtWidgets import QApplication,QWidget,QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor,QIcon
import sys


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        height = 300
        width = 500
        padding = 20
        self.m_flag=False
        self.setFixedSize(width+2*padding, height+2*padding)

        self.center_widget = QWidget(self)
        self.center_widget.setGeometry(padding, padding, width, height)
        self.setAccessibleName('center-widget')
        self.center_widget.setAttribute(Qt.WA_StyledBackground, True)
        self.center_widget.setStyleSheet('QWidget{background-color: rgba(255, 255, 255, 1); border-radius:8px}')

        shadow_effect = QGraphicsDropShadowEffect(self.center_widget)
        shadow_effect.setOffset(0, 0)
        shadow_effect.setColor(Qt.gray)
        shadow_effect.setBlurRadius(10)
        self.center_widget.setGraphicsEffect(shadow_effect)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
