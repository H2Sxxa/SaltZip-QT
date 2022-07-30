self.myLog.infolog(f"{getcwd()}/Data/plugin/debug.py")
def debug(command):
    with popen(command) as pipe:
        msg=pipe.read()
        self.myLog.infolog(msg)
    with open("debug.log","w",encoding="utf-8") as f:
        f.write(msg)
try:
    self.myLog.infolog(f"{getcwd()}/{__file__}")
    debug(f"{os.getcwd()}/{__file__}")
    self.myLog.infolog(f"已保存在 {getcwd()} 下 debug.log")
    system("pause")
except Exception as e:
    self.myLog.errorlog(str(e))