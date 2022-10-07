from FTPwork import myFtp
from  SerialTest import SerialCtrl
import time
import winsound
#運行流程
#-----------------------------------

# 持續取得Debug訊息
# 當程序完成ActionFlag+1
# 當所有程序完整完成 ActionFlag=0

#------------------------------------

#系統音設置
duration = 500  # millisecond
freq = 880  # Hz

#全套
# ActionList=['run 1','CheckIsDone','CheckAble','run 2','CheckIsDone','CheckAble','Reset',
#              'CheckAble2','LoadingTLS','untar','CheckAble','RemoveTar','Reboot','CheckWorking',
#             'StopProcess','SetIP']

#刪資料用
ActionList=['CheckWorking','RemoveTransferd','CheckAble','StopProcess','SetIP']


CheckAction=['WriteListCheck']
#ActionList=['SetIP','LoadingTLS','untar','CheckAble','RemoveTar']
ActionFlag=0

#上傳TLS資料
def LoadingTLSFile(IP_Position):
    ftp = myFtp("192.168.0.{}".format(IP_Position))
    ftp.Login("root", "")
    #設定於根目錄
    ftp.ChangeRount('/')

    print("上傳含TLS的linuxrc")
    #上傳用於自動掛載CF卡的linuxrc檔
    ftp.Uploadfile("linuxrc","linuxrc")
    print("成功")

    print("上傳SSL_update資料夾")
    local_path = 'SSL_update'
    romte_path = 'bv'

    ftp.UploadfileTree(local_path,romte_path)
    print("成功")
    ftp.close()

def SOMAction(case,DebugInfo):

# def CheckWriteList(FTP,SOMType):


    #用於等待可正常輸入

    if case=='run 1':
        if DebugInfo.find('Hit') != -1:
            ser.SerialWrite("\r\n".encode())
            ser.SerialWrite("run 1\r\n".encode())
            return 1
        elif DebugInfo.find('ARP Retry') != -1:
            return 3

    elif case=='CheckIsDone':
        if DebugInfo.find('done')!= -1:
            return 1


    elif case=='CheckAble':
        if DebugInfo.find('bv')!= -1:
            return 1
    elif case=='CheckAble2':
        if DebugInfo.find('/ #')!= -1:
            return 1

    elif case=='CheckWorking':
        if DebugInfo.find('Local IP=')!= -1:
            return 1

    elif case=='run 2':
        ser.SerialWrite("run 2\r\n".encode())
        return 1

    elif case == 'Reset':
        ser.SerialWrite("reset\r\n".encode())
        return 1

    elif case == 'Reboot':
        ser.SerialWrite("reboot -f\r\n".encode())
        return 1

    elif case=='LoadingTLS':
        try:
            LoadingTLSFile(50)
            return 1
        except:
            print("FTP Fail")
            return 4

    elif case == 'StopProcess':
        ser.SerialWrite("killall Mitac_BV\r\n".encode())
        return 1

    elif case=='untar':
        ser.SerialWrite("cd bv\r\n".encode())
        ser.SerialWrite("tar zxvf openssl.tar.gz\r\n".encode())
        return 1

    elif case=="RemoveTransferd":
        ser.SerialWrite("rm rm Transfered -rf\r\n".encode())
        return 1

    elif case=="RemoveTar":
        ser.SerialWrite("rm openssl.tar.gz\r\n".encode())
        return 1

    elif case=="SetIP":
        ser.SerialWrite("ifconfig eth0 192.168.0.50 up \r\n".encode())
        return 2




if __name__ == "__main__":
    #連接COM port
    ser = SerialCtrl()
    TimeoutCounter=0
    StepTimeList=[]
    StartTime = time.time()
    while(1):
        #持續取得資訊
        try:
            Debugdata = ser.GetDebugInfo()
        except:
            print("有異常字元~~~")
        print('|',end='')


        try:

            if SOMAction(ActionList[ActionFlag],Debugdata)==1:
                print('-------------------------------------------')
                print('NowAction:', ActionList[ActionFlag])
                print('ActionFlag:', ActionFlag)
                print('-------------------------------------------')
                EndTime = time.time()
                TotalTime = round(EndTime - StartTime, 2)
                print("花費時間", TotalTime)
                StepTimeList.append(TotalTime)
                ActionFlag+=1
                StartTime = time.time()
                TimeoutCounter=0

            elif SOMAction(ActionList[ActionFlag],Debugdata)==2:
                print(StepTimeList)
                EntreTime=0
                for x in StepTimeList:
                    EntreTime+=x
                print('總時間:',EntreTime)
                StepTimeList.clear()
                ActionFlag = 0
                TimeoutCounter = 0
                # time.sleep(10)
                winsound.Beep(freq, duration)
                a = input("流程完成,請更換下一片")
            elif SOMAction(ActionList[ActionFlag], Debugdata) == 3:
                print(Debugdata)
                print("SOM板異常!")
                ActionFlag = 0
                TimeoutCounter = 0
            elif SOMAction(ActionList[ActionFlag], Debugdata) == 4:
                winsound.Beep(freq, duration)
                a=input("重試")


        except:
            SerialCtrl.SerialClose()
            a=input('Unknow Err')
