from json import dumps
from uuid import UUID,getnode
import time
import HashTools

class AuthHandle():
    def __init__(self) -> None:
        self.encert={
            "data":{
                "version":"",
                "signature":{
                    "releaser":"",
                    "contact":"",
                    "mac":self.mac_address
                },
                "information":{
                    "filename":"",
                    "filetime":self.now_time,
                    "filetips":"",
                    "filepawd":HashTools.genrds(16)
                }
            }
        }
        self.decert=""
  
    @staticmethod
    def drop10to2(string):
        return ' '.join(format(ord(c), 'b') for c in string)
    
    @staticmethod
    def repair2to10(string):
        rawlist=string.split(" ")
        return ''.join(format(chr(int(b1n,2))) for b1n in rawlist)
    
    @property
    def encodeCert(self):
        pwd=HashTools.genrds(8)
        res={"key":pwd,"code":HashTools.getStringhash(dumps(self.encert),pwd,None)}
        return self.drop10to2(HashTools.b64e(dumps(res)))
        
    @property
    def mac_address(self):
        mac=UUID(int = getnode()).hex[-12:]
        mac=mac.replace(mac[1],"",1).replace(mac[1],"",1).replace(mac[-1],"",-1).replace(mac[-1],"",-1)
        mac=mac.upper()
        mac=HashTools.b64e(mac)
        return mac
    
    @property
    def now_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())