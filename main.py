import sys
from os import getcwd
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from gui import Ui_MainWindow
from Library.Quet.lite import LiteLog
from Library.IQtTool import WigetMessagebox,WigetVerifyBox,WigetInputbox
from Library.LiteZip import Core


from qt_material import apply_stylesheet
class SALTZIP(QMainWindow,Ui_MainWindow):
    def __init__(self,myLog=LiteLog.LiteLog(name=__name__), parent=None) -> None:
        super(SALTZIP,self).__init__(parent)
        self.myLog=myLog
        self.m_flag=False
        self.passwordcache=""
        self.setupUi(self)
        self.setWindowTitle("SaltZip")
        self.mainsetup()
        self.TaskLabel.setText("当前任务：启动")
        self.myLog.bindQTlog(self.LogText)
        self.myLog.infolog("Setup UI successfully")
        #bind Menu
        self.DarkTheme.triggered.connect(lambda:self.myTheme("Dark"))
        self.LightTheme.triggered.connect(lambda:self.myTheme("Light"))
        self.MenuFullScreen.triggered.connect(self.showFullScreen)
        self.MenuExitFullScreen.triggered.connect(self.showNormal)
        self.MenuAbout.triggered.connect(self.about)
        self.MenuSponsor.triggered.connect(self.sponsor)
        self.MenuExit.triggered.connect(self.choseVerify)
        self.MenuwtLog.triggered.connect(lambda:myLog.write_cache_log(QFileDialog.getExistingDirectory(self,"选择日志输出目录",getcwd()),True))
        #button
        self.ExitBT.clicked.connect(self.choseVerify)
        self.BTcontinue.clicked.connect(self.loadAll)
    def mainsetup(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
    def myTheme(self,theme:str="Dark"):
        if theme == "Dark":
            apply_stylesheet(app, theme='dark_cyan.xml')
        else:
            apply_stylesheet(app, theme='light_cyan_500.xml')
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton and not self.isFullScreen():
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag and not self.isFullScreen():  
            self.move(QMouseEvent.globalPos()-self.m_Position)
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        if not self.isFullScreen():
            self.m_flag=False
            self.setCursor(QCursor(Qt.ArrowCursor))
    def mouseDoubleClickEvent(self, QMouseEvent):
       if self.isFullScreen():
           self.showNormal()
       else:
           self.showFullScreen()
    def choseVerify(self) ->None:
        self.wvb=WigetVerifyBox.WigetVerifybox(desc=["您确认关闭吗"],title="退出确认",Sobject=self)
        self.wvb.show()
    def closeEvent(self, event) -> None:
        try:
            self.Qmb.close()
            self.wvb.close()
        except:
            pass
    def sponsor(self):
        self.Qmb=WigetMessagebox.WigetMessagebox(desc=["如果您觉得这个项目不错，不妨打个赏","https://afdian.net/@H2Sxxa"],title="赞助")
        self.Qmb.show()
    def about(self):
        self.Qmb=WigetMessagebox.WigetMessagebox(desc=["本软件于Github使用GPL3.0协议免费开源","仓库地址https://github.com/IAXRetailer/SaltZip-QT","使用时请务必遵循协议"],title="关于")
        self.Qmb.show()
    def loadAll(self):
        self.TaskLabel.setText("当前任务：初始化")
        self.myCore=self.ZipCore.itemText(self.ZipCore.currentIndex())
        self.myMode=self.ChoseMode.itemText(self.ChoseMode.currentIndex())
        self.myLog.infolog("Core is "+self.myCore+";Mode is "+self.myMode)
        self.haspassword=self.hasPassword.isChecked()
        self.ifsplit=self.isSplit.isChecked()
        self.myLog.infolog("split mode:"+str(self.ifsplit)+";has password:"+str(self.haspassword))
        
        if self.myMode == "解压":
            self.TaskLabel.setText("当前任务：解压")
            self.myCoreOpearte=Core.Core(self.myCore,False,self.haspassword,self.ifsplit,self.myLog,self)
            self.myCoreOpearte.GetStart(QFileDialog.getOpenFileName(self,"选择解压文件",getcwd()))
        else:
            self.TaskLabel.setText("当前任务：压缩")
            self.myCoreOpearte=Core.Core(self.myCore,True,self.haspassword,self.ifsplit,self.myLog,self)
            self.myCoreOpearte.GetStart(QFileDialog.getOpenFileName(self,"选择压缩文件",getcwd()))
    def callforapassword(self):
        self.TaskLabel.setText("当前任务：需要密码")
        self.wib=WigetInputbox.WigetInputbox(title="该文件受到加密,请输入密码",Sobject=self)
        self.wib.show()
    def getpassword(self,password):
        if self.myCoreOpearte.isZip:
            pass
        else:
            try:
                self.myLog.infolog("Rerun the unarchive with the password")
                self.myCoreOpearte.Eunzip(self.myCoreOpearte.filepath,password)
                self.TaskLabel.setText("当前任务：完成")
            except Exception as e:
                self.TaskLabel.setText("当前任务：密码错误")
                self.myLog.errorlog(str(e))
                self.myLog.errorlog("ERROR Password")
if __name__ == '__main__':
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        app = QApplication(sys.argv)
        apply_stylesheet(app, theme='light_cyan_500.xml')
        ui = SALTZIP()
        ui.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
        ui.myLog.errorlog(str(e))
    finally:
        pass