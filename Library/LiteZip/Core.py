from tarfile import TarFile,is_tarfile
from threading import Thread,activeCount
from pyzipper import AESZipFile
from zipfile import ZipFile,is_zipfile
from rarfile import RarFile,is_rarfile
from py7zr import SevenZipFile,is_7zfile
import os
from Library.Quet.lite.LiteLog import LiteLog
from Library.Warpper.Timeout import timeout
from . import RarOSsupport
#from ThreadHelper import ResThread

class Core():
    def __init__(self,ZipCore:str="SaltZip",isZip:bool=False,haspassword:bool=False,issplit:bool=False,bindlog:LiteLog=None,processbar=None) -> None:
        if bindlog != None:
            self.haslog=True
        else:
            self.haslog=False
        self.maxThread=1
        self.processbar=processbar
        self.ZipCore=ZipCore
        self.haspassword=haspassword
        self.issplit=issplit
        self.isZip=isZip
        self.bindlog=bindlog
        self.myLog=LiteLog(name=__name__)
    def setRarlocation(self,rarloction="rar.exe"):
        self.rar=RarOSsupport.RarOSsupport(rarloction)
        
    def setProcesssafe(self,app):
        self.processingEvents=app.processEvents
        
    def detect_ziptype(self,filepath):
        if is_tarfile(filepath):
            self.add_log("Detect as a tar")
            return ".tar"
        elif is_rarfile(filepath):
            self.add_log("Detect as a rar")
            return ".rar"
        elif is_zipfile and is_7zfile:
            return self.detect2type(filepath)
        elif is_zipfile:
            self.add_log("Detect as a zip")
            return ".zip"
        elif is_7zfile:
            self.add_log("Detect as a 7z")
            return ".7z"
        else:
            self.add_errorlog("Unknown format")
            return None
    def detect2type(self,filepath):
        try:
            self.det4_zip(filepath)
            return ".zip"
        except Exception as e:
            self.add_log(str(e))
            if "password required for extraction" in str(e):
                return ".zip"
        try:
            SevenZipFile(filepath).testzip()
            return ".7z"
        except Exception as e:
            self.add_log(str(e))
            if "Password is required for extracting given archive." in str(e):
                return ".7z"
    def GetStart(self,filepath,ungzip_call_password_method=None,gzip_call_password_method=None,gzip_call_gziptype=None):
        self.add_log("Max thread is "+str(self.maxThread))
        self.gzip_call_gziptype=gzip_call_gziptype
        self.ungzip_call_password_method=ungzip_call_password_method
        self.gzip_call_password_method=gzip_call_password_method
        if type(filepath)==tuple:
            filepath=filepath[0]
        if filepath == "":
            self.myLog.warnlog("A illegal file path")
            self.bindlog.appendtoQT(self.myLog.lastQTlog)
            return
        self.filepath=filepath
        if self.isZip:
            self.add_log("Start gzip now...")
            self.enzip()
        else:
            self.add_log("Start ungzip now...")
            self.unzip(filepath)
            
    def unzip(self,filepath):
        self.filepath=filepath
        ext=os.path.splitext(filepath)[-1] 
        if ext not in [".tar",".rar",".zip",".7z"]:
            self.add_log("A unknown filetype,don't worry,it will detect for you")
            ext=self.detect_ziptype(filepath)
            if ext == None:
                return
        self.ext=ext
        self.add_log("Identify as "+ext)
        try:
            if ext == ".zip":
                if self.ZipCore == "SaltZip":
                    try:
                        tzipP=self.ck4_zip(filepath)
                    except Exception as e:
                        self.add_log(str(e))
                        tzipP=False
                    if tzipP or self.check_zip(filepath):
                        self.ungzip_call_password_method()
                    else:
                        self.unzipfile(filepath)
                elif self.ZipCore == "7Zip":
                    pass
            elif ext == ".tar" or ext == ".gz":
                if self.ZipCore == "SaltZip":
                    '''
                    tar无法加密
                    '''
                    self.untarfile(filepath)
                elif self.ZipCore == "7Zip":
                    pass
            elif ext == ".rar":
                if self.ZipCore == "SaltZip":
                    if self.check_rar(filepath):
                        self.ungzip_call_password_method()
                    else:
                        self.unrarfile(filepath)
                elif self.ZipCore == "7Zip":
                    pass
            elif ext == ".7z":
                if self.ZipCore == "SaltZip":
                    if self.check_7z(filepath):
                        self.ungzip_call_password_method()
                    else:
                        self.un7zfile(filepath)
            else:
                pass
        except Exception as e:
            self.add_errorlog(str(e))
            self.add_log("may be it is a illegal archive")
    def enzip(self):
        self.gzip_call_gziptype()
    #gzip
    def callforrarsplit(self,blocksize,pwd=None):
        zip_file=None
        if zip_file == None and not os.path.isdir(self.filepath):
            zip_file=self.filepath.replace(os.path.splitext(self.filepath)[-1],"")
        elif zip_file == None and os.path.isdir(self.filepath):
            zip_file=self.filepath
        msg=self.rar.mkVolumerar(self.filepath,zip_file+".rar",pwd=pwd,blocksize=blocksize)
        self.bindlog.appendtoQT(msg)
        self.bindlog.logcache.append(msg)
    def setuppwdsplit(self,blocksize):
        self.blocksize=blocksize
        
    def callforpwdsplit(self,pwd):
        self.callforrarsplit(self.blocksize,pwd)
        
    def call_pwd_rar(self,pwd):
        zip_file=None
        if zip_file == None and not os.path.isdir(self.filepath):
            zip_file=self.filepath.replace(os.path.splitext(self.filepath)[-1],"")
        elif zip_file == None and os.path.isdir(self.filepath):
            zip_file=self.filepath
        msg=self.rar.mkrar(self.filepath,zip_file+".rar",pwd=pwd)
        self.bindlog.appendtoQT(msg)
        self.bindlog.logcache.append(msg)
    def batch_rar(self,start_dir,zip_file=None):
        if zip_file == None and not os.path.isdir(start_dir):
            zip_file=start_dir.replace(os.path.splitext(start_dir)[-1],"")
        elif zip_file == None and os.path.isdir(start_dir):
            zip_file=start_dir
        target=zip_file+'.rar'
        msg=self.rar.mkrar(start_dir,target)
        self.bindlog.appendtoQT(msg)
        self.bindlog.logcache.append(msg)
    def batch_zip(self,start_dir,zip_file=None):
        if zip_file == None and not os.path.isdir(start_dir):
            zip_file=start_dir.replace(os.path.splitext(start_dir)[-1],"")
        elif zip_file == None and os.path.isdir(start_dir):
            zip_file=start_dir
        if os.path.isdir(start_dir):
            with ZipFile(zip_file+'.zip','w') as target:
                for path, dirnames, filenames in os.walk(start_dir):
                    fpath=path.replace(start_dir,'')
                    for filename in filenames:
                        self.add_log("Append "+filename)
                        target.write(os.path.join(path,filename),os.path.join(fpath,filename))
        else:
            with ZipFile(zip_file+".zip","w") as target:
                self.add_log("Append "+os.path.basename(start_dir)+" to "+zip_file+".zip")
                target.write(start_dir,os.path.basename(start_dir))
                
    def batch_tar(self,start_dir,zip_file=None):
        if zip_file == None and not os.path.isdir(start_dir):
            zip_file=start_dir.replace(os.path.splitext(start_dir)[-1],"")
        elif zip_file == None and os.path.isdir(start_dir):
            zip_file=start_dir
        if os.path.isdir(start_dir):
            with TarFile(zip_file+'.tar','w') as target:
                for path, dirnames, filenames in os.walk(start_dir):
                    fpath=path.replace(start_dir,'')
                    for filename in filenames:
                        self.add_log("Append "+filename)
                        target.add(os.path.join(path,filename),os.path.join(fpath,filename))
        else:
            with TarFile(zip_file+".tar","w") as target:
                self.add_log("Append "+os.path.basename(start_dir)+" to "+zip_file+".tar")
                target.add(start_dir,os.path.basename(start_dir))
    #log
    def add_log(self,msg):
        if self.bindlog != None:
            self.myLog.infolog(msg)
            self.bindlog.logcache.append(self.myLog.lastlog)
            self.bindlog.appendtoQT(self.myLog.lastQTlog)
    def add_errorlog(self,msg):
        if self.bindlog != None:
            self.myLog.errorlog(msg)
            self.bindlog.logcache.append(self.myLog.lastlog)
            self.bindlog.appendtoQT(self.myLog.lastQTlog)
    #Ungzip
    def un7zfile(self,zip_file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(zip_file_path)
        if pwd == None:
            zip_file = SevenZipFile(zip_file_path)
        else:
            zip_file = SevenZipFile(zip_file_path,password=pwd)
            try:
                zip_file.testzip()
            except Exception as e:
                self.add_errorlog(str(e))
                self.add_errorlog("ERROR PASSWORD")
                return
        zip_list = zip_file.getnames()
        
        for f in zip_list:
            self.add_log("Extract "+f)
            while activeCount() > self.maxThread:
                self.processingEvents()
            zip_file.reset()
            myThread=Thread(target=zip_file.extract,args=(target_path,[f]))
            myThread.start()
        while activeCount() != 1:
            self.processingEvents()
        zip_file.close()
        self.add_log("All Successed!")
    def unzipfile(self,zip_file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(zip_file_path)
        zip_file = self.support_gbk(ZipFile(file=zip_file_path))
        self.processingEvents()
        aes_zip_file=self.support_gbk(AESZipFile(file=zip_file_path))
        zip_list = zip_file.namelist()
        for f in zip_list:
            if pwd != None:
                try:
                    callback=self.ck4_zip_password(zip_file,pwd.encode("utf-8"))
                    self.add_log(callback)
                    if "Bad password" in callback:
                        self.add_errorlog("ERROR PASSWORD")
                        print("Return main")
                        return
                except:
                    pass
                try:
                    while activeCount() > self.maxThread:
                        self.processingEvents()
                    myThread = Thread(target=zip_file.extract,args=(f,target_path,pwd.encode("utf-8")))
                    myThread.start()
                    self.add_log("Extract "+f)
                except Exception as e:
                    self.add_errorlog(str(e))
                    self.add_log("Don't worry,it will try to use AES-256 to ungzip it.")
                    self.add_log("Extract "+f)
                    while activeCount() > self.maxThread:
                        self.processingEvents()
                    myThread = Thread(target=aes_zip_file.extract,args=(f,target_path,pwd.encode("utf-8")))
                    myThread.start()
                finally:
                    pass
            else:
                while activeCount() > self.maxThread:
                    self.processingEvents()
                myThread = Thread(target=zip_file.extract,args=(f,target_path))
                myThread.start()
                self.add_log("Extract "+f)
        while activeCount() != 1:
            self.processingEvents()
        self.add_log("All Successed!")
        zip_file.close()
    def untarfile(self,file_path,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(file_path)
        rf = TarFile(file_path)
        rf_list=rf.getnames()
        for f in rf_list:
            self.add_log("Extract "+f)
            try:
                while activeCount() > self.maxThread:
                    self.processingEvents()
                myThread = Thread(target=rf.extract,args=(f,target_path))
                myThread.start()
            except Exception as e:
                self.add_errorlog(str(e))
                self.add_log("May be it is a illegal archive")
                break
        while activeCount() != 1:
            self.processingEvents()
        self.add_log("All Successed!")
        rf.close()
    def unrarfile(self,file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(file_path)
        zip_file = RarFile(file=file_path)
        zip_list = zip_file.namelist()
        for f in zip_list:
            self.add_log("Extract "+f)
            try:
                if pwd != None:
                    try:
                        #zip_file.testrar(pwd=pwd)
                        pass
                    except Exception as e:
                        self.add_errorlog(str(e))
                        self.add_errorlog("ERROR PASSWORD")
                        return
                    while activeCount() > self.maxThread:
                        self.processingEvents()
                    myThread = Thread(target=zip_file.extract,args=(f,target_path,pwd.encode("utf-8")))
                    myThread.start()
                else:
                    while activeCount() > self.maxThread:
                        self.processingEvents()
                    myThread = Thread(target=zip_file.extract,args=(f,target_path))
                    myThread.start()
                    #zip_file.extract(f,target_path)
            except Exception as e:
                self.add_errorlog(str(e))
                self.add_log("May be it is a illegal archive,dont worry,it will use unrar.exe to handle it")
                msg=self.rar.extractrar(file_path,target_path,pwd)
                self.bindlog.appendtoQT(msg)
                self.bindlog.logcache.append(msg)
                break
        while activeCount() != 1:
            self.processingEvents()
        self.add_log("All Successed!")
        zip_file.close()
    #check password
    def check_7z(self,mfile:str) -> bool:
        sf=SevenZipFile(mfile)
        return sf.needs_password()
    def check_rar(self,mfile: str) -> bool:
        '''
        name: 
        des: 检测rar格式压缩包是否加密
        param {传入的文件名}
        return {True:文件加密 False:文件没加密}
        '''
        rf = RarFile(mfile)
        return rf.needs_password()
    def check_zip(self,mfile: str) -> bool:
        zf = ZipFile(mfile)
        for zinfo in zf.infolist():
            is_encrypted = zinfo.flag_bits & 0x1
            if is_encrypted:
                return True
            else:
                return False
    def support_gbk(self,zip_file: ZipFile):
        name_to_info = zip_file.NameToInfo
        # copy map first
        for name, info in name_to_info.copy().items():
            try:
                real_name = name.encode('cp437')
                real_name = real_name.decode('gbk')
            except Exception as e:
                self.add_log(str(e))
                return zip_file
            if real_name != name:
                info.filename = real_name
                del name_to_info[name]
                name_to_info[real_name] = info
        return zip_file
    
    @timeout(3)
    def ck4_zip(self,mfile:str) -> bool:
        with ZipFile(mfile) as f:
            try:
                f.testzip()
                return False
            except Exception as e:
                if "password required" in str(e):
                    return True
                else:
                    return False
    @timeout(3)
    def ck4_zip_password(self,zipfile:ZipFile,pwd:bytes) -> str:
        Izipfile=zipfile
        Izipfile.setpassword(pwd)
        try:
            Izipfile.testzip()
            return ""
        except Exception as e:
            return str(e)
        
    @timeout(3)
    def det4_zip(self,mfile:str):
        ZipFile(mfile).testzip()