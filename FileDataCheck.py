import csv
def WriteListCheck():
    FilePath='./ListLibrary/SOMWriteListData.csv'

    WriteDict={}

    with open(FilePath, newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if WriteDict.__contains__(row['Dir'])==False:
                WriteDict[row['Dir']]=[]
            WriteDict[row['Dir']].append(row['FileName'])
    return WriteDict



if __name__ == '__main__':
    #取得白名單資料
    WriteDict=WriteListCheck()
    #取得bv檔案資料清單

    #比對白名單資料

    #警示沒有該檔案
