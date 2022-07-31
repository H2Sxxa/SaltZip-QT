from os import popen
def debugmain(self):
    def debug(command):
        with popen(command) as pipe:
            msg=pipe.read()
            return msg
    try:
        self.myLog.infolog(f"{getcwd()}/{__file__}")
        msg=debug(f"{os.getcwd()}/saltzipqt.exe")
        with open("debug.log","w",encoding="utf-8") as f:
            f.write(msg)
        self.myLog.infolog("debug finish")
        self.myLog.infolog(f"已保存在 {getcwd()} 下 debug.log")
    except Exception as e:
        self.myLog.errorlog(str(e))
self.myLog.infolog("debug模式下,原窗口将会静默未响应")
self.myLog.infolog(f"{getcwd()}/Data/plugin/debug.py")
debugmain(self)