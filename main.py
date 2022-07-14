import sys
from os import getcwd
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from Library.LiteZip.RarOSsupport import RarOSsupport

from gui import Ui_MainWindow
from Library.Quet.lite import LiteLog
from Library.IQtTool import WigetMessagebox,WigetVerifyBox,WigetInputbox,WigetCombobox
from Library.LiteZip import Core


from qt_material import apply_stylesheet
class SALTZIP(QMainWindow,Ui_MainWindow):
    def __init__(self,myLog=LiteLog.LiteLog(name=__name__), parent=None) -> None:
        super(SALTZIP,self).__init__(parent)
        self.myLog=myLog
        self.rar=RarOSsupport("rar.exe")
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
        self.FixRar.triggered.connect(lambda:self.rar.fixrar(QFileDialog.getOpenFileName(self,"选择压缩包",getcwd())[0],self.myLog,QFileDialog.getExistingDirectory(self,"保存压缩包(取消则默认保存在程序目录)",getcwd())))
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
        self.wvb=WigetVerifyBox.WigetVerifybox(desc=["您确认关闭吗"],title="退出确认",callmethod=self.close)
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
            self.myCoreOpearte=Core.Core(self.myCore,False,self.haspassword,self.ifsplit,self.myLog)
            self.myCoreOpearte.setRarlocation("rar.exe")
            self.myCoreOpearte.GetStart(QFileDialog.getOpenFileName(self,"选择解压文件",getcwd()),ungzip_call_password_method=self.callforapassword)
        elif self.myMode == "压缩":
            self.TaskLabel.setText("当前任务：压缩")
            self.myCoreOpearte=Core.Core(self.myCore,True,self.haspassword,self.ifsplit,self.myLog)
            self.myCoreOpearte.setRarlocation("rar.exe")
            self.callforisdir()
    def callforisdir(self):
        self.wcb=WigetCombobox.WigetCombobox("选择模式",ChoiceList=["选择文件夹","选择文件"],calllog=self.myLog,callmethod=self.getisdir)
        self.wcb.show()
    def getisdir(self,choice:str):
        if choice == "选择文件夹":
            self.myCoreOpearte.GetStart(QFileDialog.getExistingDirectory(self,"选择压缩文件夹",getcwd()),gzip_call_gziptype=self.callforgziptype)
        else:
            self.myCoreOpearte.GetStart(QFileDialog.getOpenFileName(self,"选择压缩文件",getcwd()),gzip_call_gziptype=self.callforgziptype)
            
    def callforapassword(self):
        self.TaskLabel.setText("当前任务：需要密码")
        self.wib=WigetInputbox.WigetInputbox(title="该文件受到加密,请输入密码",calllog=self.myLog,callmethod=self.getpassword)
        self.wib.show()
        
    def callforgziptype(self):
        self.wcb=WigetCombobox.WigetCombobox("选择模式",ChoiceList=["zip","tar","rar"],calllog=self.myLog,callmethod=self.getgziptype)
        self.wcb.show()
        
    def getgziptype(self,gziptype:str):
        if gziptype == "zip":
            if self.haspassword and self.myCoreOpearte.ZipCore == "SaltZip":
                self.Qmb=WigetMessagebox.WigetMessagebox(desc=["ZipFile加密无法实现,您无法使用此内核制作加密Zip","解决方案:尝试使用7Zip内核并重试以创建加密Zip"],title="警告")
                self.Qmb.show()
            elif self.ifsplit and self.myCoreOpearte.ZipCore == "SaltZip":
                self.Qmb=WigetMessagebox.WigetMessagebox(desc=["由于管道流特性导致ZipFile分卷压缩无法实现","解决方案:尝试使用7Zip内核并重试以创建分卷Zip"],title="警告")
                self.Qmb.show()
            else:
                self.myCoreOpearte.batch_zip(self.myCoreOpearte.filepath)
        if gziptype == "tar":
            if self.haspassword and self.myCoreOpearte.ZipCore == "SaltZip":
                self.Qmb=WigetMessagebox.WigetMessagebox(desc=["tar无法加密"],title="警告")
                self.Qmb.show()
            elif self.ifsplit and self.myCoreOpearte.ZipCore =="SaltZip":
                self.Qmb=WigetMessagebox.WigetMessagebox(desc=["由于管道流特性导致TarFile分卷压缩无法实现","解决方案:尝试使用7Zip内核并重试以创建分卷Tar"],title="警告")
                self.Qmb.show()
            else:
                self.myCoreOpearte.batch_tar(self.myCoreOpearte.filepath)
        if gziptype == "rar":
            if self.haspassword and self.myCoreOpearte.ZipCore == "SaltZip":
                self.wib=WigetInputbox.WigetInputbox("输入压缩密码",calllog=self.myLog,callmethod=self.myCoreOpearte.call_pwd_rar)
                self.wib.show()
                
            elif self.ifsplit and self.myCoreOpearte.ZipCore =="SaltZip":
                self.Qmb=WigetMessagebox.WigetMessagebox(desc=["由于管道流特性导致RarFile分卷压缩无法实现","解决方案:尝试使用7Zip内核并重试以创建分卷Rar"],title="警告")
                self.Qmb.show()
            else:
                self.myCoreOpearte.batch_rar(self.myCoreOpearte.filepath)
    def getpassword(self,password):
        if self.myCoreOpearte.isZip:
            pass
        else:
            try:
                if self.myCoreOpearte.ZipCore == "SaltZip":
                    self.myLog.infolog("Rerun the unarchive with the password")
                    if self.myCoreOpearte.ext == ".zip":
                        self.myCoreOpearte.unzipfile(self.myCoreOpearte.filepath,password)
                    else:
                        self.myCoreOpearte.unrarfile(self.myCoreOpearte.filepath,password)
                    self.TaskLabel.setText("当前任务：完成")
                else:
                    pass
            except Exception as e:
                self.TaskLabel.setText("当前任务：密码错误")
                self.myLog.errorlog(str(e))
                if "Bad password" in str(e):
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