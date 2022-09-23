#確認USB資料更新資料與BV內容相同大小
#

from FTPwork import myFtp
import csv

def GetFileCheckListDict(ListFileName):
    FilePath='./ListLibrary/{}'.format(ListFileName)

    WriteDict={}

    with open(FilePath, newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if WriteDict.__contains__(row['Dir'])==False:
                WriteDict[row['Dir']]=[]
            WriteDict[row['Dir']].append(row['FileName'])
    return WriteDict



if __name__ == '__main__':
    #登入FTP(SOM)
    try:
        ftp = myFtp("192.168.1.250")
        ftp.Login("root", "")
        #-------------------------------
        #白名單檢測流程
        #-------------------------------
        # 取得白名單資料
        WriteDict = GetFileCheckListDict('SOMWriteListData.csv')
        # 依目錄類型作循環檢測
        for WritePath in WriteDict.keys():
            # 取得SOM板目標目錄資料清單
            ftp.ChangeRount(WritePath)
            SOMDataList=ftp.CheckRountsFileName()
            # 比對白名單資料
            for WriteListFileName in WriteDict[WritePath]:
                if WriteListFileName not in SOMDataList:
                    # 警示沒有該檔案
                    print('資料{},不存在!!'.format(WriteListFileName))
                    #生成白名單異常名單
                    WriteListErrFile=open('WriteErrList.text','a+',encoding='uft8')
                    WriteListErrFile.write(WriteListFileName)
                    WriteListErrFile.close()

        #-------------------------------
        #黑名單檢測流程
        #-------------------------------
        # 取得黑名單資料
        BlackDict = GetFileCheckListDict('SOMBlackListData.csv')
        # 依目錄類型作循環檢測
        for BlackPath in BlackDict.keys():
            # 取得SOM板目標目錄資料清單
            ftp.ChangeRount(BlackPath)
            SOMDataList=ftp.CheckRountsFileName()
            # 比對黑名單資料
            for BlackListFileName in WriteDict[BlackPath]:
                if BlackListFileName in SOMDataList:
                    print('存在資料:{}!!!'.format(BlackListFileName))
                    #刪除黑名單檔案
                    try:
                        ftp.DeleteFoldersFlies()




    except:
        print('FTP登入失敗!')


