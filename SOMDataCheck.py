from FTPwork import myFtp
import pandas as pd

def SOMDataCheckProcess():
    SOMType = 'new'

    # 登入FTP(SOM)
    try:
        ftp = myFtp("192.168.0.50")
        ftp.Login("root", "")

        # 取得檢測名單資料
        WhiteListdf = pd.read_csv('ListLibrary/SOMWriteListData.csv')
        BlackListdf = pd.read_csv('ListLibrary/SOMBlackListData.csv')
        OtherFiledf = pd.read_csv('ListLibrary/OtherFileList.csv')

        WhiteListCheckPath = WhiteListdf['Dir'].unique()
        BlackListCheckPath = BlackListdf['Dir'].unique()

        WhiteListTypes = WhiteListdf['SOMType'].unique()
        BlacListTypes = BlackListdf['SOMType'].unique()
        OtherFileListType = OtherFiledf['SOMType'].unique()

        GrayFileCheck = {}

        # -------------------------------
        # 黑名單檢測流程
        # -------------------------------

        # 取得黑名單資料
        # 依目錄類型作循環檢測
        for BlackPath in BlackListCheckPath:
            # 取得SOM板目標目錄資料清單
            ftp.ChangeRount(BlackPath)
            GrayFileCheck[BlackPath] = ftp.CheckRountsFileName()
            # 比對黑名單資料
            if SOMType == 'new':
                # 不進行篩選,只要存在於黑名單的就刪除
                for BlackListFileName in BlackListdf[BlackListdf['Dir'] == BlackPath]['FileName']:
                    if BlackListFileName in GrayFileCheck[BlackPath]:
                        print('{}存在資料:{}!!!'.format(BlackPath, BlackListFileName))
                        # 刪除黑名單檔案
                        try:
                            ftp.DeleteFuc(BlackListFileName)
                        except:
                            print('刪除失敗!')
            elif SOMType == 'repair':
                # 只刪除必要刪的檔案
                for BlackListFileName in \
                BlackListdf[(BlackListdf['Dir'] == BlackPath) & (BlackListdf['SOMType'] == 'all')]['FileName']:
                    if BlackListFileName in GrayFileCheck[BlackPath]:
                        print('{}存在資料:{}!!!'.format(BlackPath, BlackListFileName))
                        # 刪除黑名單檔案
                        try:
                            ftp.DeleteFuc(BlackListFileName)
                        except:
                            print('刪除失敗!')
            else:
                print('SOMDataBlackTypeErr!!!!')

        # -------------------------------
        # 白名單檢測流程
        # -------------------------------
        # 依目錄類型作循環檢測
        for WhitePath in WhiteListCheckPath:
            # 取得SOM板目標目錄資料清單
            ftp.ChangeRount(WhitePath)
            GrayFileCheck[WhitePath] = ftp.CheckRountsFileName()
            # 比對白名單資料
            for WriteListFileName in WhiteListdf[WhiteListdf['Dir'] == WhitePath]['FileName']:
                if WriteListFileName not in GrayFileCheck[WhitePath]:
                    # 警示沒有該檔案
                    print('資料{},不存在!!'.format(WriteListFileName))
                    # 生成白名單異常名單
                    WriteListErrFile = open('WhiteErrList.text', 'a+', encoding='utf8')
                    WriteListErrFile.write(WriteListFileName + '\n')
                    WriteListErrFile.close()

                # 移除已檢測過的檔案名稱
                GrayFileCheck[WhitePath].remove(WriteListFileName)
        # -------------------------------
        # 灰名單檢測流程
        # -------------------------------

        for CheckPath in GrayFileCheck.keys():
            if len(GrayFileCheck[CheckPath]) > 0:
                # 待處理項目:新增警示資料
                # 檢測之前歷史資料是否有該檔案的定義
                for OtherFileName in OtherFiledf[OtherFiledf['Dir'] == CheckPath]['FileName']:
                    if OtherFileName in GrayFileCheck[CheckPath]:
                        GrayFileCheck[CheckPath].remove(OtherFileName)

                # 過濾後,仍有位定義資料名稱,則匯出灰名單
                if len(GrayFileCheck[CheckPath]) > 0:
                    print('存在未知檔案!!')
                    # 匯出灰名單
                    GrayFile = open('GrayFileList.text', 'a+', encoding='utf8')
                    for GrayFileName in GrayFileCheck[CheckPath]:
                        GrayFile.write(CheckPath + ',' + GrayFileName + '\n')
                    GrayFile.close()
        print('SOM板檢測完成')
        ftp.close()
    except:
        print('FTP登入失敗!')


if __name__ == '__main__':
    SOMDataCheckProcess()
