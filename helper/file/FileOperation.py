import glob, os
import re
from datetime import datetime,timedelta
import logging

from helper.ip.IPChecker import IPChecker
import data.holder.LogVisitorFromFile 
from data.holder.LogVisitorFromFile import LogVisitorFromFile




class FileOperation(object):

    def __init__(self,folderName):
        self.__data         = []
        self.__log          = logging.getLogger(__name__)
        self.__folderName   = folderName
        self.readFolder(folderName)
        
        
       
    def readFolder(self,folderName):
        print("Scanning folder '{}'".format(folderName))
        os.chdir(folderName)
        i = 1
        for file in glob.glob("*.access.log*"):
            excludeFile = ["gz", "php", "nginx"]
            if any(x in file for x in excludeFile):
                continue 
            print("{}.Reading file '{}'".format(i,file))
            self.__log.info("{}.Reading file '{}'".format(i,file))
            self.readFile(file)
            i +=1

            
    def readFile(self, file):
        with open(file) as fp:
            line = fp.readline()
            cnt = 1
            datetimeobject = ''
            while line:
                line = fp.readline()
                data = line.strip().split(" ")
                dataLen = len(data)
                if dataLen < 5:
                    continue
                method = data[5].replace('"','')
                browser = ''
                ipObj = IPChecker(data[0].strip())
                if ipObj.isValid() == True:
                    ipValid = ipObj.getIPAddr()
                    #print("Valid ip : {} {}".format(ipObj.getIPAddr(), ipObj.getIPVersion()))
         
                byDoubleQuotes = re.findall("\"(.+?)\"", line)
                if byDoubleQuotes:
                    browser = byDoubleQuotes[2].strip()
                    url = byDoubleQuotes[0].replace(method,'').strip()
                    urlComplete = byDoubleQuotes[1].strip()
                    
                
                byBracket = re.search("\[(.+?)\]", line)
                dTime =''
                if byBracket:
                   dTime = str(byBracket.group(0)[1:-6]).strip()
                if dTime == '':
                    continue    
               
                datetimeobject = datetime.strptime(dTime,'%d/%b/%Y:%H:%M:%S')
                date_time = datetimeobject.strftime("%Y-%m-%d %H:%M:%S")
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                five_minute = str(datetime.now() - timedelta(minutes=5))[:-7]

                
                if date_time > five_minute:
                    self.__log.info("{} {}".format(ipValid,urlComplete))
                    self.__data.append(LogVisitorFromFile(cnt,ipValid,date_time,method,browser,url,urlComplete))
                    
                cnt +=1
    
    
    def deleteFile(self, file):
        f = "{}{}".format(self.__folderName,file)
        os.remove(file)

    def getData(self):
      return self.__data
    
   
