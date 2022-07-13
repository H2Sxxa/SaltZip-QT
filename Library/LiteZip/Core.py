import tarfile
import zipfile
from threading import Thread
from os.path import splitext,dirname
from Library.Quet.lite.LiteLog import LiteLog

class Core():
    def __init__(self,ZipCore:str="SaltZip",isZip:bool=False,haspassword:bool=False,issplit:bool=False,bindlog:LiteLog=None,fatheruse=None) -> None:
        if bindlog != None:
            self.haslog=True
        else:
            self.haslog=False
        self.ZipCore=ZipCore
        self.haspassword=haspassword
        self.issplit=issplit
        self.isZip=isZip
        self.bindlog=bindlog
        self.father=fatheruse
        self.myLog=LiteLog(name=__name__)
    def GetStart(self,filepath) -> Thread:
        self.filepath=filepath
        if self.isZip:
            self.enzip(filepath)
        else:
            self.add_log("Get Threading...")
            self.unzip(filepath)
    
    def unzip(self,filepath):
        if type(filepath)==tuple:
            filepath=filepath[0]
            self.filepath=filepath
        ext=splitext(filepath)[-1]
        self.add_log("Identify as "+ext)
        if ext == ".zip":
            if self.ZipCore == "SaltZip":
                if self.check_zip(filepath):
                    self.father.callforapassword()
                else:
                    self.Eunzip(filepath)
            else:
                pass
        elif ext == ".tar":
            if self.ZipCore == "SaltZip":
                '''
                tar无法加密
                '''
                self.untarfile(filepath)
            else:
                pass
        else:
            pass
            
    def enzip(self,filepath):
        pass
    def add_log(self,msg):
        if self.bindlog != None:
            self.myLog.infolog(msg)
            self.bindlog.appendtoQT(self.myLog.lastQTlog)
            
    def Eunzip(self,zip_file_path,pwd=None,target_path=None):
        if target_path == None:
            target_path=dirname(zip_file)
        zip_file = self.support_gbk(zipfile.ZipFile(zip_file_path))
        zip_list = zip_file.namelist()
        for f in zip_list:
            if pwd != None:
                zip_file.extract(f,target_path,pwd.encode("utf-8"))
            else:
                zip_file.extract(f,target_path)
        zip_file.close()
        self.add_log("All Successed!")
        
        
    def untarfile(self,file_path,target_path=None):
        if target_path == None:
            target_path=dirname(file_path)
        rf = tarfile.TarFile(file_path)
        rf.extractall(target_path)
        self.add_log("All Successed!")
        
        
    def check_gz_tar(file: str) -> bool:
        '''
        name: 
        des: 检测gz格式压缩包是否加密，注：gz文件一一般不加密的，检测得是.tar.gz是否加密
        param {传入的文件名}
        return {True: 文件加密 False: 文件没加密}
    
        '''       
        try:
            zf = tarfile.open(file)
            return False
        except Exception as e:
            return True
        
    def check_rar(file: str) -> bool:
        '''
        name: 
        des: 检测rar格式压缩包是否加密
        param {传入的文件名}
        return {True:文件加密 False:文件没加密}
    
        '''
        rf = tarfile.RarFile(file)
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
        zf = zipfile.ZipFile(file)
        for zinfo in zf.infolist():
            is_encrypted = zinfo.flag_bits & 0x1
            if is_encrypted:
                return True
            else:
                return False
    def support_gbk(self,zip_file: zipfile.ZipFile):
        name_to_info = zip_file.NameToInfo
        # copy map first
        for name, info in name_to_info.copy().items():
            real_name = name.encode('cp437').decode('gbk')
            if real_name != name:
                info.filename = real_name
                del name_to_info[name]
                name_to_info[real_name] = info
        return zip_file