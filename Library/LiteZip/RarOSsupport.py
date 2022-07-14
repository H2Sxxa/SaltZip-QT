from os import popen
from os.path import basename
from shutil import move
from Library.Quet.lite.LiteLog import LiteLog
class RarOSsupport():
    def __init__(self,Rarexelocation) -> None:
        self.RarLC=Rarexelocation
    def cmdhandle(self,command):
        with popen(self.RarLC+" "+command) as pipe:
            msg=pipe.read()
            return msg
        
    def mkrar(self,location,out,pwd=None):
        if pwd != None:
            return self.cmdhandle(f"a -r -o+ -p{pwd} \"{out}\" \"{location}\"")
        else:
            return self.cmdhandle(f"a -r \"{out}\" \"{location}\"")
    def mkVolumerar(self,location,out,pwd=None,blocksize=None):
        return
    def fixrar(self,location,bindlog:LiteLog=None,callsavepath=""):
        if location == "":
            bindlog.warnlog("A illegal file path!")
            return
        msg=self.cmdhandle(f"r -o+ \"{location}\"")
        bsn=basename(location)
        
        if callsavepath != "":
            try:
                move("rebuilt."+bsn,callsavepath+"/rebuilt."+bsn)
            except Exception as e:
                bindlog.errorlog(str(e))
        if bindlog != None:
            bindlog.appendtoQT(msg)
            bindlog.logcache.append(msg)
'''
<Commands>
  a             添加文件到压缩文档
  c             添加压缩文档注释
  ch            更改压缩文档参数
  cw            写入压缩文档注释到文件
  d             从压缩文档删除文件
  e             提取文件不带压缩路径
  f             刷新压缩文档中的文件
  i[par]=<str>  在压缩文档里查找字符串
  k             锁定压缩文档
  l[t[a],b]     列出压缩文档内容 [technical[all], bare]
  m[f]          移动到压缩文档 [仅文件]
  p             打印文件到 stdout
  r             修复压缩文档
  rc            重新构建丢失的卷
  rn            重命名归档的文件
  rr[N]         添加数据恢复记录
  rv[N]         创建恢复卷
  s[name|-]     转换压缩文档到或从 SFX
  t             测试压缩文档的文件
  u             更新压缩文档中的文件
  v[t[a],b]     详细列出压缩文档的内容 [technical[all],bare]
  x             解压文件带完整路径

'''