from os import popen

from Library.Quet.lite.LiteLog import LiteLog

class SevenZipOSsupport():
    def __init__(self,szlocation,logger:LiteLog) -> None:
        self.logger=logger
        self.szLC=szlocation

    def cmdhandle(self,command):
        with popen(self.szLC+" "+command) as papi:
            msg=papi.read()
            try:
                self.logger.infolog(msg)
            except:
                pass
            return msg

    def make7z(self,location,out,pwd=None):
        if pwd != None:
            return self.cmdhandle("a -t7z -r \"%s\" -p\"%s\" \"%s\"" % (out,pwd,location))
        else:
            return self.cmdhandle("a -t7z -r \"%s\" \"%s\"" % (out,location))

    def makeVolume7z(self,location,out,blocksize,pwd=None):
        if pwd != None:
            return self.cmdhandle("a -t7z -r -v%s \"%s\" -p\"%s\" \"%s\"" % (blocksize,out,pwd,location))
        else:
            return self.cmdhandle("a -t7z -r -v%s \"%s\" \"%s\"" % (blocksize,out,location))

    def extractall(self,location,out,pwd=None):
        if pwd != None:
            return self.cmdhandle("x \"%s\" -p\"%s\" -o\"%s\"" % (location,pwd,out))
        else:
            return self.cmdhandle("x \"%s\" -o\"%s\"" % (location,out))

    def batch(self,ziptype,location,out,pwd=None):
        if pwd != None:
            return self.cmdhandle("a -t%s -r \"%s\" -p\"%s\" \"%s\"" % (ziptype,out,pwd,location))
        else:
            return self.cmdhandle("a -t%s -r \"%s\" \"%s\"" % (ziptype,out,location))

    def batchVolume(self,ziptype,location,out,blocksize,pwd=None):
        if pwd != None:
            return self.cmdhandle("a -t%s -r -v%s \"%s\" -p\"%s\" \"%s\"" % (ziptype,blocksize,out,pwd,location))
        else:
            return self.cmdhandle("a -t%s -r -v%s \"%s\" \"%s\"" % (ziptype,blocksize,out,location))
