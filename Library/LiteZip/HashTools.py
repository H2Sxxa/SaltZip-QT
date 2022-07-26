import pyDes
import base64
def getStringhash(string,key,iv):
	des=pyDes.des(key,pyDes.ECB,iv,pad=None,padmode=pyDes.PAD_PKCS5)
	res=des.encrypt(string.encode('utf-8'))
	return str(base64.b64encode(res).decode("utf-8"))

def decodeStringhash(string,key,iv):
	import pyDes,base64
	string=base64.b64decode(string)
	des=pyDes.des(key,pyDes.ECB,iv,pad=None,padmode=pyDes.PAD_PKCS5)
	res=des.decrypt(string)
	return res.decode('utf-8')

def b64d(obj):
	return base64.b64decode(obj).decode("utf-8")

def b64e(obj):
    return base64.b64encode(obj.encode("utf-8")).decode('utf-8')


import random
import string
def genrds(length):
	resultlist=[]
	sample=[]
	for i in string.ascii_uppercase:
		sample.append(i)
	for i in string.digits:
		sample.append(i)
	while len(resultlist) < length:
		resultlist.append(random.choice(sample))
	for i in resultlist:
		try:
			res=res+i 
		except:
			res=i 
	return res


from xxhash import xxh64
def getfilehash(file,blocksize,size):
	hasher=xxh64()
	blocksize=int(blocksize)
	size2=int(size)
	with open(file,"rb") as f:
		while True:
			size2-=65565
			process=str(round(((size-size2)/size)*100,4))+"%"+" 计算中xxhash中，剩余"+str(size2)
			print("\r"+process,end="")
			buf=f.read(blocksize)
			if not buf:
				print("\nOver")
				break
			hasher.update(buf)
	return hasher.hexdigest()

import struct
def writetobin(binPath,string):
    slist=list(string)
    data = struct.pack(f"i",ord(slist[0]))
    with open(binPath, 'w+b') as f:
        f.write(data)
    slist.pop(0)
    for i in slist:
        data=struct.pack(f"i",ord(i))
        with open(binPath, 'a+b') as f:
            f.write(data)

def readrbtostring(filepath,lenstr):
    rbcon=open(filepath,"rb").read()
    data=str(lenstr)+"i"
    ms=struct.unpack(data,rbcon)
    res=""
    for i in ms:
        res=res+chr(i)
    return res