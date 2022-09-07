from __future__ import print_function
import ftplib
import os
from os.path import isfile, isdir




class myFtp:
    ftp = ftplib.FTP()
    
    def __init__(self, host, port=21):
        
        self.ftp.connect(host, port)
        self.ftp.encoding = 'utf8'
        
        self.FailPath=""
        self.RetryTimes=10
        self.FileSkipCount=0
        
        
        self.DownloadFailPath=""
        self.DownloadRetryTimes=10
        
        self.TotalDownloadAmount=0
        self.SuccesDownloadAmount=0
        
        self.FileSkipCount=0
        self.DownloadRetryCout=self.DownloadRetryTimes
        
        
        self.SuccessUploadAmount=0
        self.TotelUploadFile=0
        self.LocalFileAmount=0
        
        self.RetryCount=self.RetryTimes
        

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载单个文件
        file_handler = open(LocalFile, 'wb')
        #print(file_handler)
        # self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)#接收服务器上文件并写入本地文件
        self.ftp.retrbinary('RETR ' + RemoteFile, file_handler.write)
        file_handler.close()
        return True

    def DownLoadFileTree(self, LocalDir, RemoteDir,host,DeviceID):  # 下载整个目录下的文件               
        print("{},伺服端文件夹remoteDir:".format(DeviceID), RemoteDir)
        
        if not os.path.exists(LocalDir): #確認是否存在儲存路徑
            os.makedirs(LocalDir)
        
        
        try:
            
            self.ftp.cwd(RemoteDir)
            self.DownloadFailPath=RemoteDir
            
    
            while(self.DownloadRetryCout>0):
                RemoteNames = self.ftp.nlst()        
                print("伺服端文件項目數量：", len(RemoteNames))       
                 
                try:
                    for x in range(len(RemoteNames)):
                        
                        Local = os.path.join(LocalDir, RemoteNames[x])
                        
                        #print("正在下載", self.ftp.nlst(RemoteNames[x]))  
                        
                        if RemoteNames[x].find(".") == -1:
                            if not os.path.exists(Local):
                                os.makedirs(Local)
                            self.DownloadFailPath=RemoteNames[x]                                               
                            self.DownLoadFileTree(Local, RemoteNames[x],host,DeviceID)
                            
                        else:     
                            try:
                                self.DownLoadFile(Local, RemoteNames[x])
                                self.TotalDownloadAmount+=1
                                self.SuccesDownloadAmount+=1
                                
                            except:
                                
                                f=open("ErrReport.csv","a")
                                f.write("{},{},DownloadReTryPath\n".format(DeviceID,self.DownloadFailPath))
                                f.close()
                                
                                print("{} DownFail !".format(RemoteNames[x]))
                            
                    self.DownloadRetryCout=self.DownloadRetryTimes 
                    break
                except:
                    print("DownLoad Retry...")
                    self.DownloadRetryCout-=1 
                    
                    f=open("ErrReport.csv","a")
                    f.write("{},{},DownloadReTryPath\n".format(DeviceID,self.DownloadFailPath))
                    f.close()
                    
                    
                    ftp = myFtp(host)
                    ftp.Login("root", "root")              
                    
                    self.ftp.cwd(self.DownloadFailPath) #Turn back to Last step       
            
            print("此資料夾下載成功總數: ",self.SuccesDownloadAmount)
            print("目前下載總數: ",self.TotalDownloadAmount)        
            print()
            self.SuccesDownloadAmount=0
            #回到上一個目錄
            self.ftp.cwd("..")
            return
        except:
            print("遠端路徑不存在!")
    
    def Uploadfile(self,targetfile,targetfilefullpath):
        
        f = open(targetfilefullpath, 'rb') 
        self.ftp.storbinary("STOR {}".format(targetfile),f) 

        f.close()
        
    def UploadfileTree(self, LocalDir, RemoteDir):
        
        print("伺服端文件夹remoteDir:", RemoteDir)
               
        #移至目標資料夾或創建資料夾
        try:            
            self.ftp.cwd(RemoteDir)
            
        except:
            self.ftp.mkd(RemoteDir)
            self.ftp.cwd(RemoteDir)
            
        self.FailPath=LocalDir

        
        # 取得所有檔案與子目錄名稱
        files = os.listdir(LocalDir)
        print("目前處理本地端資料位置:",LocalDir)
        print("資料數量: ",len(files))
        
        # 以迴圈處理
        if(len(files)>0):
            for f in files:
              # 產生檔案的絕對路徑
              #fullpath = join(LocalDir, f)
              
              fullpath = "{}/{}".format(LocalDir,f)
              
              #print("全路徑:",fullpath)
              # 判斷 fullpath 是檔案還是資料夾
              if isfile(fullpath):
                  #self.Uploadfile(f)
                  #print("檔案：", f)
                  
                  while(self.RetryCount>0):
                      
                      try:
                          self.Uploadfile(f,fullpath)
                          print("上傳成功:",f)
                          self.SuccessUploadAmount+=1 
                          self.TotelUploadFile+=1
                          
                          self.RetryCount=self.RetryTimes 
                          break
                      except:                          
                          f=open("ErrReport.csv","a")
                          f.write("{},UpLoadFail\n".format(fullpath))
                          f.close()                          
                          
                          print("Retry Upload")
                          self.RetryCount-=1
                    
                  
              elif isdir(fullpath):
                  print("資料夾：", f)
                  self.UploadfileTree(fullpath,f)
                
        else:
            print("none")
        
        #print("回到上層..")
        
        self.ftp.cwd("..")
        print("此資料夾成功上傳數量: ",self.SuccessUploadAmount)
        print("目前上傳總數: ",self.TotelUploadFile)
        print()
        self.SuccessUploadAmount=0
        
        return
    
    
    
    def ChangeRount(self,RemoteDir):
        self.ftp.cwd(RemoteDir)
    
    def CreatFolder(self,FolderName):
        self.ftp.mkd(FolderName)
        
    def CheckFolderExist(self,FolderName):
        RemoteNameList = self.ftp.nlst()  
        for x in RemoteNameList:
            if(x==FolderName):
                return True
            else:
                return False
    
    def CheckRountsFileName(self):
        RemoteNames = self.ftp.nlst()        
        print("伺服端文件目錄：", RemoteNames)
        return RemoteNames
    
    def close(self):
        self.ftp.quit()