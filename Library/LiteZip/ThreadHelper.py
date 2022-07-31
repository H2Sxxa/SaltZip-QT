import threading

import py7zr

from Library.Quet.lite.LiteLog import LiteLog

class ResThread(threading.Thread):
    def __init__(self, target, args):
        threading.Thread.__init__(self)
        self.func = target
        self.args = args
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return str(e)
class ThreadHooker:
    def __init__(self,Logger:LiteLog) -> None:
        self.Logger=Logger
        threading.excepthook=self.HookerArgs
    def HookerArgs(self,HookerInfo):
        self.exc_type=HookerInfo.exc_type
        self.exc_value=HookerInfo.exc_value
        self.exc_traceback=HookerInfo.exc_traceback
        self.thread=HookerInfo.thread
        self.Logger.errorlog(self.exc_value)
        if self.exc_type == py7zr.UnsupportedCompressionMethodError:
            self.Logger.errorlog("不支持的文件压缩方式,建议使用7zip Core")