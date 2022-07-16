from os import popen,system,getcwd
from sys import argv
def debug(command):
    with popen(command) as pipe:
        msg=pipe.read()
        print(msg)
    with open("debug.log","w",encoding="utf-8") as f:
        f.write(msg)

input("确认原GUI关闭以回车开始")
print(argv[1])
debug(argv[1])
print(f"已保存为 {getcwd()}\debug.log")
system("pause")