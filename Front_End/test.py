import time 

nowtime = int(time.time())

def writedata(nowtime,data):
    f = open(str(nowtime)+'.txt', "a")
    #f.write(str(data['input'])+'\n'+str(data['time']))
    f.write(data)
    f.close()

def newfile(nowtime):
    f = open(str(nowtime)+'.txt', 'w')
    f.close()

newfile(nowtime)
writedata(nowtime,'adb')
