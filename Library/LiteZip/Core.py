from tarfile import TarFile,is_tarfile
import tarfile
from threading import Thread,activeCount
import multivolumefile
from pyzipper import AESZipFile
from zipencrypt import ZipFile as ENCZipFile
from zipfile import ZipFile
from rarfile import RarFile,is_rarfile
from py7zr import SevenZipFile
import os
from Library.Quet.lite.LiteLog import LiteLog
from Library.Warpper.Timeout import timeout
from . import RarOSsupport,Salt,VolumeUtils
#from ThreadHelper import ResThread

class Core():
    def __init__(self,ZipCore:str="SaltZip",isZip:bool=False,haspassword:bool=False,issplit:bool=False,bindlog:LiteLog=None,processbar=None) -> None:
        if bindlog != None:
            self.haslog=True
        else:
            self.haslog=False
        self.trueext=""
        self.salt=Salt.Salt()
        self.resptime=2
        self.maxThread=3
        self.processbar=processbar
        self.ZipCore=ZipCore
        self.haspassword=haspassword
        self.issplit=issplit
        self.isZip=isZip
        self.bindlog=bindlog
        self.myLog=LiteLog(name=__name__)
    def setRarlocation(self,rarloction="rar.exe"):
        self.rar=RarOSsupport.RarOSsupport(rarloction,self.bindlog)
        
    def setProcesssafe(self,app):
        self.processingEvents=app.processEvents
        
    def detect_ziptype(self,filepath):
        if is_tarfile(filepath):
            self.add_log("Detect as a tar")
            return ".tar"
        elif is_rarfile(filepath):
            self.add_log("Detect as a rar")
            return ".rar"
        else:
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
                if "invalid header data" in str(e):
                    try:
                        with multivolumefile.open(filepath.replace(self.trueext,"",-1), mode='rb') as target_archive:
                            with SevenZipFile(target_archive, 'r') as archive:
                                archive.testzip()
                                return "volume7z"
                    except Exception as e2:
                        if "Password is required for extracting given archive." in str(e2):
                            return "volume7z"
                    self.add_log(str(e2))
                self.add_log(str(e))
                if "Password is required for extracting given archive." in str(e):
                    return ".7z"
            if self.PK_checkzip(filepath):
                self.add_log("Attention!It's a obscure match!")
                return "volumezip"
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
            if "invalid header data" in str(e):
                try:
                    with multivolumefile.open(filepath.replace(self.trueext,"",-1), mode='rb') as target_archive:
                        with SevenZipFile(target_archive, 'r') as archive:
                            archive.testzip()
                            return "volume7z"
                except Exception as e2:
                    if "Password is required for extracting given archive." in str(e2):
                        return "volume7z"
                self.add_log(str(e2))
            self.add_log(str(e))
            if "Password is required for extracting given archive." in str(e):
                return ".7z"
        if self.PK_checkzip(filepath):
            self.add_log("Attention!It's a obscure match!")
            return "volumezip"
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
        if ext not in [".tar",".rar",".zip",".7z",".hk",".h2k"]:
            self.add_log("A unknown filetype,don't worry,it will detect for you")
            self.trueext=ext
            ext=self.detect_ziptype(filepath)
            if ext == None:
                return
        self.ext=ext
        self.add_log("Identify as "+ext)
        try:
            if ext == ".hk":
                try:
                    self.add_log("捕获为第1代SaltZip加密")
                    password,info=self.salt.get1hkpassword(self.filepath)
                    self.add_log("文件信息")
                    self.add_log("校验码%s"%info[0])
                    self.add_log("发布者%s"%info[1])
                    self.add_log("发布时间%s"%info[2])
                    if os.path.exists(self.filepath.replace(".hk",".zip",-1)):
                        self.unzipfile(self.filepath.replace(".hk",".zip",-1),password)
                    elif os.path.exists(self.filepath.replace(".hk",".sip",-1)):
                        self.unzipfile(self.filepath.replace(".hk",".sip",-1),password)
                    else:
                        self.add_errorlog(self.filepath.replace(".hk",".zip",-1)+" 不存在,检查是否有此文件")
                except Exception as e:
                    self.add_errorlog(str(e))
            if ext == ".h2k":
                try:
                    self.add_log("捕获为第2代SaltZip加密")
                    password,lenstr,info=self.salt.get2hkpassword(self.filepath)
                    self.add_log("文件信息")
                    self.add_log("校验码%s"%info[0])
                    self.add_log("发布者%s"%info[1])
                    self.add_log("发布时间%s"%info[2])
                    if os.path.exists(self.filepath.replace(lenstr+".h2k","sip",-1)):
                        self.unzipfile(self.filepath.replace(lenstr+".h2k","sip",-1),password)
                    else:
                        self.add_errorlog(self.filepath.replace(lenstr+".h2k","sip",-1)+" 不存在,检查是否有此文件")
                except Exception as e:
                    self.add_errorlog(str(e))
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
            elif ext == "volume7z":
                if self.ZipCore == "SaltZip":
                    if self.check_Volume7z(filepath):
                        self.ungzip_call_password_method()
                    else:
                        self.unVolume7zfile(filepath)
            elif ext == "volumezip":
                if self.ZipCore == "SaltZip":
                    self.filepath=VolumeUtils.combinefile(self.removefileext(filepath))
                    filepath=self.filepath
                    try:
                        tzipP=self.ck4_zip(filepath)
                    except Exception as e:
                        self.add_log(str(e))
                        tzipP=False
                    if tzipP or self.check_zip(filepath):
                        self.ungzip_call_password_method()
                    else:
                        self.unVolumeZip(filepath)
                elif self.ZipCore == "7Zip":
                    pass
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
        Thread(target=self.rar.mkVolumerar,args=(self.filepath,zip_file+".rar",pwd,blocksize)).start()
    def callfortarsplit(self,blocksize:str):
        blocksize=blocksize.lower().replace("k","000").replace("m","000000").replace("g","000000000")
        try:
            blocksize=int(blocksize)
        except Exception as e:
            self.add_errorlog(str(e))
            return
        self.volume_tar(self.filepath,None,blocksize)
    def setuppwdsplit(self,blocksize):
        self.blocksize=blocksize
        
    def callforpwdsplit(self,pwd):
        self.callforrarsplit(self.blocksize,pwd)
    
    def call_pwd_zip(self,pwd):
        self.batch_enzip(self.filepath,password=pwd)
    
    def call_pwd_rar(self,pwd):
        zip_file=None
        if zip_file == None and not os.path.isdir(self.filepath):
            zip_file=self.filepath.replace(os.path.splitext(self.filepath)[-1],"",-1)
        elif zip_file == None and os.path.isdir(self.filepath):
            zip_file=self.filepath
        Thread(target=self.rar.mkrar,args=(self.filepath,zip_file+".rar",pwd)).start()

    def batch_rar(self,start_dir,zip_file=None):
        if zip_file == None and not os.path.isdir(start_dir):
            zip_file=start_dir.replace(os.path.splitext(start_dir)[-1],"",-1)
        elif zip_file == None and os.path.isdir(start_dir):
            zip_file=start_dir
        target=zip_file+'.rar'
        Thread(target=self.rar.mkrar,args=(start_dir,target)).start()
        
    #TODO Check it safe
    def batch_enzip(self,start_dir,zip_file=None,password=None):
        if zip_file == None and not os.path.isdir(start_dir):
            zip_file=start_dir.replace(os.path.splitext(start_dir)[-1],"",-1)
        elif zip_file == None and os.path.isdir(start_dir):
            zip_file=start_dir
        if os.path.isdir(start_dir):
            with ENCZipFile(zip_file+'.zip','w') as target:
                for path, dirnames, filenames in os.walk(start_dir):
                    fpath=path.replace(start_dir,'',-1)
                    for dirs in dirnames:
                        self.add_log("Append %s"%dirs)
                        pathfile = os.path.join(path, dirs)
                        while activeCount() > self.maxThread:
                            self.processingEvents()
                        Thread(target=target.write,args=(pathfile,os.path.basename(pathfile),None,password.encode("utf-8"))).start()
                    for filename in filenames:
                        self.add_log("Append "+filename)
                        while activeCount() > self.maxThread:
                            self.processingEvents()
                        Thread(target=target.write,args=(os.path.join(path,filename),os.path.join(fpath,filename),None,password.encode("utf-8"))).start()
                while activeCount() != 1:
                    self.processingEvents()
                self.add_log("All Successed!")
        else:
            with ENCZipFile(zip_file+".zip","w") as target:
                self.add_log("Append "+os.path.basename(start_dir)+" to "+zip_file+".zip")
                Thread(target=target.write,args=(start_dir,os.path.basename(start_dir),None,password.encode("utf-8"))).start()

    #TODO Check it safe
    def batch_zip(self,start_dir,zip_file=None):
        if zip_file == None and not os.path.isdir(start_dir):
            zip_file=start_dir.replace(os.path.splitext(start_dir)[-1],"",-1)
        elif zip_file == None and os.path.isdir(start_dir):
            zip_file=start_dir
        if os.path.isdir(start_dir):
            with ZipFile(zip_file+'.zip','w') as target:
                for path, dirnames, filenames in os.walk(start_dir):
                    fpath=path.replace(start_dir,'',-1)
                    for dirs in dirnames:
                        self.add_log("Append %s"%dirs)
                        pathfile = os.path.join(path, dirs)
                        while activeCount() > self.maxThread:
                            self.processingEvents()
                        Thread(target=target.write,args=(pathfile,os.path.basename(pathfile))).start()
                    for filename in filenames:
                        self.add_log("Append "+filename)
                        while activeCount() > self.maxThread:
                            self.processingEvents()
                        Thread(target=target.write,args=(os.path.join(path,filename),os.path.join(fpath,filename))).start()
                while activeCount() != 1:
                    self.processingEvents()
                self.add_log("All Successed!")
        else:
            with ZipFile(zip_file+".zip","w") as target:
                self.add_log("Append "+os.path.basename(start_dir)+" to "+zip_file+".zip")
                Thread(target=target.write,args=(start_dir,os.path.basename(start_dir))).start()
                
    def batch_tar(self,source_dir,zip_file=None):
        if zip_file == None and not os.path.isdir(source_dir):
            zip_file=source_dir.replace(os.path.splitext(source_dir)[-1],"",-1)
        elif zip_file == None and os.path.isdir(source_dir):
            zip_file=source_dir
        if os.path.isdir(source_dir):
            tar = tarfile.open(zip_file+".tar","w")
            for root,dirs,files in os.walk(source_dir):
                for adir in dirs:
                    self.add_log("Append %s"%adir)
                    pathfile = os.path.join(root, adir)
                    while activeCount() > self.maxThread:
                        self.processingEvents()
                    Thread(target=tar.add,args=(pathfile,os.path.basename(pathfile))).start()
                for afile in files:
                    self.add_log("Append %s"%afile)
                    pathfile = os.path.join(root, afile)
                    while activeCount() > self.maxThread:
                        self.processingEvents()
                    Thread(target=tar.add,args=(pathfile,os.path.basename(pathfile))).start()
        else:
            tar = tarfile.open(zip_file+".tar","w")
            pathfile = os.path.join(source_dir)
            Thread(target=tar.add,args=(pathfile,os.path.basename(pathfile))).start()
        while activeCount() != 1:
            self.processingEvents()
        self.add_log("All Successed!")
        tar.close()
    def volume_tar(self,start_dir,zip_file=None,volume_size=None):
        self.batch_tar(start_dir,zip_file)
        self.add_log("Start to split")
        if zip_file == None and not os.path.isdir(start_dir):
            zip_file=start_dir.replace(os.path.splitext(start_dir)[-1],"",-1)
        elif zip_file == None and os.path.isdir(start_dir):
            zip_file=start_dir
        volume=1
        if volume_size != None:
            with open(zip_file+".tar","rb") as archive:
                volume_con=archive.read(volume_size)
                while volume_con != b"":
                    self.processingEvents()
                    with open(zip_file+f".tar.{str(volume).zfill(3)}","wb") as volume_file:
                        volume_file.write(volume_con)
                    volume_con=archive.read(volume_size)
                    volume+=1
        os.unlink(zip_file+".tar")
        self.add_log("All Successed!")

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
    def unVolume7zfile(self,zip_file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(zip_file_path)
        if pwd == None:
            with multivolumefile.open(self.removefileext(zip_file_path), mode='rb') as target_archive:
                with SevenZipFile(target_archive, 'r') as zip_file:
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
                    self.add_log("All Successed!")
        else:
            with multivolumefile.open(self.removefileext(zip_file_path), mode='rb') as target_archive:
                with SevenZipFile(target_archive, 'r',password=pwd) as zip_file:
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
                    self.add_log("All Successed!")
    def unVolumeZip(self,zip_file_path,pwd=None,target_path=None):
        self.unzipfile(zip_file_path,pwd,target_path)
        os.unlink(zip_file_path)
    def unzipfile(self,zip_file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(zip_file_path)
        zip_file = self.support_gbk(ZipFile(file=zip_file_path))
        self.processingEvents()
        aes_zip_file=self.support_gbk(AESZipFile(file=zip_file_path))
        zip_list = zip_file.namelist()
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
        for f in zip_list:
            if pwd != None:
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
    def unVolumetarfile(self,file_path,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(file_path)
        res=VolumeUtils.combinefile(self.removefileext(file_path))
        rf=TarFile(res)
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
        os.unlink(res)

    def untarfile(self,file_path,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(file_path)
        try:
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
                    self.add_log("May be it is a illegal archive")
                    break
            while activeCount() != 1:
                self.processingEvents()
            self.add_log("All Successed!")
            rf.close()
        except Exception as e:
            if "unexpected end of data" in str(e):
                Thread(self.unVolumetarfile(file_path,target_path)).start()
                return
            self.add_errorlog(str(e))
    def unrarfile(self,file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(file_path)
        zip_file = RarFile(file=file_path)
        zip_list = zip_file.namelist()
        if pwd != None:
            try:
                zip_file.testrar(pwd=pwd)
            except Exception as e:
                self.add_errorlog(str(e))
                self.add_errorlog("ERROR PASSWORD")
                return
        for f in zip_list:
            self.add_log("Extract "+f)
            try:
                if pwd != None:
                    '''
                    try:
                        self.te_rar(zip_file,f,target_path,pwd=pwd)
                    except Exception as e:
                        if ...
                        self.add_log("Test extract error,turn to ROS")
                        self.rar.extractrar(file_path,target_path,pwd=pwd)
                        return
                    '''
                    while activeCount() > self.maxThread:
                        self.processingEvents()
                    myThread = Thread(target=zip_file.extract,args=(f,target_path,pwd.encode("utf-8")))
                    myThread.start()
                else:
                    while activeCount() > self.maxThread:
                        self.processingEvents()
                    myThread = Thread(target=zip_file.extract,args=(f,target_path))
                    myThread.start()
            except Exception as e:
                self.add_errorlog(str(e))
                self.add_log("May be it is a illegal archive,dont worry,it will use unrar.exe to handle it")
                Thread(self.rar.extractrar(file_path,target_path,pwd)).start()
                break
        while activeCount() != 1:
            self.processingEvents()
        self.add_log("All Successed!")
        zip_file.close()
    #check password
    def PK_checkzip(self,mfile:str) -> bool:
        with open(mfile,"rb") as f:
            if f.read(2) == b"PK":
                return True
            else:
                return False
    def check_7z(self,mfile:str) -> bool:
        sf=SevenZipFile(mfile)
        return sf.needs_password()
    def check_Volume7z(self,mfile:str) -> bool:
        with multivolumefile.open(self.removefileext(mfile), mode='rb') as target_archive:
            with SevenZipFile(target_archive, 'r') as archive:
                return archive.needs_password()
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
    @timeout(2)
    def te_rar(self,IRarfile:RarFile,f,tp,pwd) -> bool:
        IRarfile.extract(f,tp,pwd=pwd)
    @timeout(2)
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
    @timeout(2)
    def ck4_zip_password(self,zipfile:ZipFile,pwd:bytes) -> str:
        Izipfile=zipfile
        Izipfile.setpassword(pwd)
        try:
            Izipfile.testzip()
            return "Correct Password!"
        except Exception as e:
            return str(e)
        
    @timeout(2)
    def det4_zip(self,mfile:str):
        ZipFile(mfile).testzip()
    
    #utils
    def removefileext(self,filepath) -> str:
        return filepath.replace(os.path.splitext(filepath)[-1],"",-1)