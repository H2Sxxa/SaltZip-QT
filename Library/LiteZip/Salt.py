from . import HashTools
class Salt():
    def __init__(self) -> None:
        pass
    
    def get1hkpassword(self,filepath):
        with open(filepath,"r",encoding="utf-8") as f:
            con=f.read()
        if "saltzip://" in con:
            cklist=con.replace("saltzip://","").split("|")
        else:
            cklist=con.split("|")
        key,iv=HashTools.b64d(cklist[1]).split("/!")
        rxxhash,releaser,rtime=HashTools.b64d(cklist[2]).split("/!")
        password=HashTools.decodeStringhash(cklist[0],key,iv)
        return(password,[rxxhash,releaser,rtime])
    def get2hkpassword(self,filepath):
        lenstr=filepath.replace(".h2k","").split(".")[-1]
        res=HashTools.readrbtostring(filepath,lenstr=int(lenstr)+64+10)
        password=HashTools.decodeStringhash(res[:32],res[32:40],res[40:48])
        rxxhash=res[48:64]
        releaser=res[64:64+int(lenstr)]
        rtime=res[64+int(lenstr):]
        return(password,lenstr,[rxxhash,releaser,rtime])