from tarfile import TarFile
from pyzipper import AESZipFile
from zipfile import ZipFile
from rarfile import RarFile
import os
from Library.Quet.lite.LiteLog import LiteLog
from . import RarOSsupport
class Core():
    def __init__(self,ZipCore:str="SaltZip",isZip:bool=False,haspassword:bool=False,issplit:bool=False,bindlog:LiteLog=None,processbar=None) -> None:
        if bindlog != None:
            self.haslog=True
        else:
            self.haslog=False
        self.processbar=processbar
        self.ZipCore=ZipCore
        self.haspassword=haspassword
        self.issplit=issplit
        self.isZip=isZip
        self.bindlog=bindlog
        self.myLog=LiteLog(name=__name__)
    def setRarlocation(self,rarloction="rar.exe"):
        self.rar=RarOSsupport.RarOSsupport(rarloction)
    def GetStart(self,filepath,ungzip_call_password_method=None,gzip_call_password_method=None,gzip_call_gziptype=None):
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
        self.ext=ext
        self.add_log("Identify as "+ext)
        try:
            if ext == ".zip":
                if self.ZipCore == "SaltZip":
                    if self.check_zip(filepath):
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
            else:
                pass
        except Exception as e:
            self.add_errorlog(str(e))
            self.add_log("may be it is a illegal archive")
    def enzip(self):
        self.gzip_call_gziptype()
    #gzip
    def call_pwd_rar(self,pwd):
        zip_file=None
        if zip_file == None and not os.path.isdir(self.filepath):
            zip_file=self.filepath.replace(os.path.splitext(self.filepath)[-1],"")
        elif zip_file == None and os.path.isdir(self.filepath):
            zip_file=self.filepath
        msg=self.rar.mkrar(self.filepath,zip_file+".rar",pwd=pwd)
        print(msg)
        self.bindlog.appendtoQT(msg)
    def batch_rar(self,start_dir,zip_file=None):
        if zip_file == None and not os.path.isdir(start_dir):
            zip_file=start_dir.replace(os.path.splitext(start_dir)[-1],"")
        elif zip_file == None and os.path.isdir(start_dir):
            zip_file=start_dir
        target=zip_file+'.rar'
        msg=self.rar.mkrar(start_dir,target)
        self.bindlog.appendtoQT(msg)
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
            self.bindlog.logcache.append(msg)
            self.bindlog.appendtoQT(self.myLog.lastQTlog)
    def add_errorlog(self,msg):
        if self.bindlog != None:
            self.myLog.errorlog(msg)
            self.bindlog.logcache.append(msg)
            self.bindlog.appendtoQT(self.myLog.lastQTlog)
    #Ungzip
    def unzipfile(self,zip_file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(zip_file_path)
        zip_file = self.support_gbk(ZipFile(file=zip_file_path))
        aes_zip_file=self.support_gbk(AESZipFile(file=zip_file_path))
        zip_list = zip_file.namelist()
        for f in zip_list:
            self.add_log("Extract "+f)
            if pwd != None:
                try:
                    zip_file.extract(f,target_path,pwd.encode("utf-8"))
                except Exception as e:
                    if zip_list[0] == f:
                        self.add_errorlog(str(e))
                        self.add_log("Don't worry,it will try to use AES-256 to ungzip it.")
                    aes_zip_file.extract(f,target_path,pwd=pwd.encode("utf-8"))
                finally:
                    pass
            else:
                zip_file.extract(f,target_path)
        zip_file.close()
        self.add_log("All Successed!")
    def untarfile(self,file_path,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(file_path)
        rf = TarFile(file_path)
        rf_list=rf.getnames()
        for f in rf_list:
            self.add_log("Extract "+f)
            try:
                rf.extract(f,target_path)
            except Exception as e:
                self.add_errorlog(str(e))
                self.add_log("May be it is a illegal archive")
                break
        #rf.extractall(target_path)
        self.add_log("All Successed!")
    def unrarfile(self,file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=os.path.dirname(file_path)
        zip_file = RarFile(file=file_path)
        zip_list = zip_file.namelist()
        for f in zip_list:
            self.add_log("Extract "+f)
            try:
                if pwd != None:
                    zip_file.extract(f,target_path,pwd.encode("utf-8"))
                else:
                    zip_file.extract(f,target_path)
            except Exception as e:
                self.add_errorlog(str(e))
                self.add_log("May be it is a illegal archive")
                break
        zip_file.close()
        self.add_log("All Successed!")
        
    #check password
    
    def check_rar(self,file: str) -> bool:
        '''
        name: 
        des: 检测rar格式压缩包是否加密
        param {传入的文件名}
        return {True:文件加密 False:文件没加密}
        '''
        rf = RarFile(file)
        is_encrypted = rf.needs_password()
        if is_encrypted:
            return True
        else:
            return False
        
    def check_zip(self,file: str) -> bool:
        '''
        name: 
        des: 检测zip格式压缩保是否加密
        param {传入的文件名}
        return {True:文件加密 False：文件没加密}
    
        '''
        zf = ZipFile(file)
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
            real_name = name.encode('cp437').decode('gbk')
            if real_name != name:
                info.filename = real_name
                del name_to_info[name]
                name_to_info[real_name] = info
        return zip_file
