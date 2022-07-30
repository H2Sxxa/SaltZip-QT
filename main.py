import sys
import ctypes
from os import getcwd,environ, system,listdir
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor,QIcon
from Library.LiteZip.RarOSsupport import RarOSsupport
from gui import Ui_MainWindow
from Library.Quet.lite import LiteLog
from Library.IQtTool import WigetMessagebox,WigetVerifyBox,WigetInputbox,WigetCombobox
from Library.LiteZip import Core

from qt_material import apply_stylesheet,list_themes
class SALTZIP(QMainWindow,Ui_MainWindow):
    def __init__(self,myLog=LiteLog.LiteLog(name=__name__), parent=None) -> None:
        super(SALTZIP,self).__init__(parent)
        self.maxthread=1
        self.myLog=myLog
        self.rar=RarOSsupport("rar.exe",self.myLog)
        self.m_flag=False
        self.passwordcache=""
        self.setupUi(self)
        self.setWindowTitle("SaltZip")
        self.mainsetup()
        try:
            self.setWindowIcon(QIcon("Data/main.png"))
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.github.iaxretailer.saltzip.mainwindows")
        except Exception as e:
            self.myLog.errorlog(e)
        self.TaskLabel.setText("当前任务：启动")
        self.myLog.bindQTlog(self.LogText)
        self.myLog.infolog("Setup UI successfully")
        #bind Menu
        self.MenuswichDL.triggered.connect(self.myTheme)
        self.MenuswichTheme.triggered.connect(self.swichTheme)
        self.MenuSetThread.triggered.connect(self.setupwibtothread)
        self.MenuFullScreen.triggered.connect(self.showFullScreen)
        self.MenuExitFullScreen.triggered.connect(self.showNormal)
        self.MenuAbout.triggered.connect(self.about)
        self.MenuSponsor.triggered.connect(self.sponsor)
        self.MenuExit.triggered.connect(self.choseVerify)
        self.MenuDebug.triggered.connect(self.debugon)
        self.FixRar.triggered.connect(lambda:self.rar.fixrar(QFileDialog.getOpenFileName(self,"选择压缩包",getcwd())[0],self.myLog,QFileDialog.getExistingDirectory(self,"保存压缩包(取消则默认保存在程序目录)",getcwd())))
        self.MenuwtLog.triggered.connect(lambda:myLog.write_cache_log(QFileDialog.getExistingDirectory(self,"选择日志输出目录",getcwd()),True))
        #button
        self.ExitBT.clicked.connect(self.choseVerify)
        self.BTcontinue.clicked.connect(self.loadAll)
        #info
        self.wmb=WigetMessagebox.WigetMessagebox(["此版本为DEMO版本","请勿于正常生产开发中使用","如遇BUG,前往https://github.com/IAXRetailer/SaltZip-QT/issues反馈"],title="警告",color=environ["QTMATERIAL_PRIMARYCOLOR"])
        self.wmb.show()
    def debugon(self):
        if "debug.exe" not in listdir("Data"):
            self.myLog.errorlog(f"No debug module,install from 'https://github.com/IAXRetailer/SaltZip-QT/blob/main/Data/debug.exe' and put it in '{getcwd()}\Data'")
            return
        system(f"start Data/debug {sys.argv[0]}")
        self.close()
    def mainsetup(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
    def swichTheme(self):
        themelist=list_themes()
        themelist.remove(environ["QTMATERIAL_THEME"])
        themelist.insert(0,environ["QTMATERIAL_THEME"])
        self.wmb=WigetCombobox.WigetCombobox(title="主题选择",ChoiceList=themelist,calllog=self.myLog,callmethod=self.runSwichTheme,color=environ["QTMATERIAL_PRIMARYCOLOR"])
        self.wmb.show()
    def runSwichTheme(self,themename):
        apply_stylesheet(app=app,theme=themename)
    def myTheme(self):
        nowTheme=environ["QTMATERIAL_THEME"]
        themelist=list_themes()
        if "dark" in nowTheme:
            targetTheme=nowTheme.replace("dark","light",1)
            if targetTheme not in themelist:
                self.wmb=WigetMessagebox.WigetMessagebox([f"目标主题{targetTheme}未找到"],title="错误",color=environ["QTMATERIAL_PRIMARYCOLOR"])
                self.wmb.show()
                return
            else:
                apply_stylesheet(app=app,theme=targetTheme)
                return
        if "light" in nowTheme:
            if "_500" in nowTheme:
                nowTheme=nowTheme.replace("_500","")
            targetTheme=nowTheme.replace("light","dark",1)
            if targetTheme not in themelist:
                self.wmb=WigetMessagebox.WigetMessagebox([f"目标主题{targetTheme}未找到"],title="错误",color=environ["QTMATERIAL_PRIMARYCOLOR"])
                self.wmb.show()
                return
            else:
                apply_stylesheet(app=app,theme=targetTheme)
                return
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
        self.wvb=WigetVerifyBox.WigetVerifybox(desc=["您确认关闭吗"],title="退出确认",callmethod=self.close,color=environ["QTMATERIAL_PRIMARYCOLOR"])
        self.wvb.show()
    def closeEvent(self, event) -> None:
        try:
            self.Qmb.close()
            self.wvb.close()
        except:
            pass
        exit(0)
    def sponsor(self):
        self.Qmb=WigetMessagebox.WigetMessagebox(desc=["如果您觉得这个项目不错，不妨打个赏","https://afdian.net/@H2Sxxa"],title="赞助",color=environ["QTMATERIAL_PRIMARYCOLOR"])
        self.Qmb.show()
    def about(self):
        self.Qmb=WigetMessagebox.WigetMessagebox(desc=["本软件于Github使用GPL3.0协议免费开源","仓库地址https://github.com/IAXRetailer/SaltZip-QT","使用时请务必遵循协议"],title="关于",color=environ["QTMATERIAL_PRIMARYCOLOR"])
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
            self.myCoreOpearte.maxThread=self.maxthread
            self.myCoreOpearte.setProcesssafe(app=app)
            self.myCoreOpearte.setRarlocation("rar.exe")
            self.myCoreOpearte.GetStart(QFileDialog.getOpenFileName(self,"选择解压文件",getcwd()),ungzip_call_password_method=self.callforapassword)
        elif self.myMode == "压缩":
            self.TaskLabel.setText("当前任务：压缩")
            self.myCoreOpearte=Core.Core(self.myCore,True,self.haspassword,self.ifsplit,self.myLog)
            self.myCoreOpearte.maxThread=self.maxthread
            self.myCoreOpearte.setProcesssafe(app=app)
            self.myCoreOpearte.setRarlocation("rar.exe")
            self.callforisdir()
    def callforisdir(self):
        self.wcb=WigetCombobox.WigetCombobox("选择模式",ChoiceList=["选择文件夹","选择文件"],calllog=self.myLog,callmethod=self.getisdir,color=environ["QTMATERIAL_PRIMARYCOLOR"])
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
    def callforrarpwdsplit(self,blksize):
        self.myCoreOpearte.setuppwdsplit(blksize)
        self.wib=WigetInputbox.WigetInputbox("输入压缩密码",calllog=self.myLog,callmethod=self.myCoreOpearte.callforpwdsplit)
        self.wib.show()
    def getgziptype(self,gziptype:str):
        if gziptype == "zip":
            if self.haspassword and self.myCoreOpearte.ZipCore == "SaltZip":
                self.wib=WigetInputbox.WigetInputbox("输入压缩密码",calllog=self.myLog,callmethod=self.myCoreOpearte.call_pwd_zip,color=environ["QTMATERIAL_PRIMARYCOLOR"])
                self.wib.show()
            elif self.ifsplit and self.myCoreOpearte.ZipCore == "SaltZip":
                self.Qmb=WigetMessagebox.WigetMessagebox(desc=["SB zipfile","解决方案:尝试使用7Zip内核并重试以创建分卷Zip"],title="警告",color=environ["QTMATERIAL_PRIMARYCOLOR"])
                self.Qmb.show()
            else:
                self.myCoreOpearte.batch_zip(self.myCoreOpearte.filepath)
        if gziptype == "tar":
            if self.ifsplit and self.myCoreOpearte.ZipCore =="SaltZip":
                self.wib=WigetInputbox.WigetInputbox("输入分卷大小(1024k,1024m...)",calllog=self.myLog,callmethod=self.myCoreOpearte.callfortarsplit,color=environ["QTMATERIAL_PRIMARYCOLOR"])
                self.wib.show()
            else:
                self.myCoreOpearte.batch_tar(self.myCoreOpearte.filepath)
        if gziptype == "rar":
            if self.haspassword and self.myCoreOpearte.ZipCore == "SaltZip" and not self.ifsplit:
                self.wib=WigetInputbox.WigetInputbox("输入压缩密码",calllog=self.myLog,callmethod=self.myCoreOpearte.call_pwd_rar,color=environ["QTMATERIAL_PRIMARYCOLOR"])
                self.wib.show()
            elif self.ifsplit and self.myCoreOpearte.ZipCore =="SaltZip":
                if self.haspassword:
                    self.wib=WigetInputbox.WigetInputbox("输入分卷大小(1024k,1024m...)",calllog=self.myLog,callmethod=self.callforrarpwdsplit,color=environ["QTMATERIAL_PRIMARYCOLOR"])
                    self.wib.show()
                else:
                    self.wib=WigetInputbox.WigetInputbox("输入分卷大小(1024k,1024m...)",calllog=self.myLog,callmethod=self.myCoreOpearte.callforrarsplit,color=environ["QTMATERIAL_PRIMARYCOLOR"])
                    self.wib.show()
            else:
                self.myCoreOpearte.batch_rar(self.myCoreOpearte.filepath)
    def setMaxThread(self,threadnum):
        if threadnum == "":
            return
        try:
            threadnum=int(threadnum)
        except Exception as e:
            self.myLog.errorlog(str(e))
            return
        if threadnum < 1:
            self.myLog.warnlog("Max thread must > 1")
            return
        self.maxthread=threadnum
        try:
            self.myCoreOpearte.maxThread=self.maxthread
        except:
            pass
    def setupwibtothread(self):
        self.wib=WigetInputbox.WigetInputbox(title="当前最大线程数 %s" % self.maxthread,calllog=self.myLog,callmethod=self.setMaxThread,color=environ["QTMATERIAL_PRIMARYCOLOR"])
        self.wib.show()
        self.wmb=WigetMessagebox.WigetMessagebox(title="警告",desc=["对于.7z线程修改至2+,可能会出现死锁并而在后端抛出错误,而前端不会显示","https://github.com/miurahr/aqtinstall/issues/86","如果需要提高解压速度,建议使用7Zip内核"],color=environ["QTMATERIAL_PRIMARYCOLOR"])
        self.wmb.show()
    def getpassword(self,password):
        if password == "":
            self.myLog.errorlog("None password")
            return
        if self.myCoreOpearte.isZip:
            pass
        else:
            try:
                if self.myCoreOpearte.ZipCore == "SaltZip":
                    self.myLog.infolog("Rerun the unarchive with the password")
                    if self.myCoreOpearte.ext == ".zip":
                        self.myCoreOpearte.unzipfile(self.myCoreOpearte.filepath,password)
                    elif self.myCoreOpearte.ext == ".rar":
                        self.myCoreOpearte.unrarfile(self.myCoreOpearte.filepath,password)
                    elif self.myCoreOpearte.ext == ".7z":
                        self.myCoreOpearte.un7zfile(self.myCoreOpearte.filepath,pwd=password)
                    elif self.myCoreOpearte.ext == "volume7z":
                        self.myCoreOpearte.unVolume7zfile(self.myCoreOpearte.filepath,pwd=password)
                    elif self.myCoreOpearte.ext == "volumezip":
                        self.myCoreOpearte.unVolumeZip(self.myCoreOpearte.filepath,password)
                    self.TaskLabel.setText("当前任务：完成")
                else:
                    pass
            except Exception as e:
                self.TaskLabel.setText("当前任务：错误")
                self.myLog.errorlog(str(e))
                if "Bad password" in str(e):
                    self.myLog.errorlog("ERROR Password")
if __name__ == '__main__':
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        app = QApplication(sys.argv)
        apply_stylesheet(app, theme='light_cyan_500.xml')
        ui = SALTZIP()
        #print(environ["QTMATERIAL_PRIMARYCOLOR"])
        ui.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
        #ui.myLog.errorlog(str(e))
    finally:
        pass