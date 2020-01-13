import pandas as pd


def loadDataframes(pathList=[]):
    """
    Reads each excel file and saves all the sheets into a list with the specified columns
    """
    dfs = []
    COLS = ["RAT","OPERATOR","CHANNEL","IMEI","IMSI","TMSI",
            "MS POWER","TA","LAST LAC","NAME","HITS","DATE-TIME"]
    for filePath in pathList:
        temd_dfs = [pd.read_excel(f"{filePath}", sheet_name=0, usecols=COLS), #2G
                    pd.read_excel(f"{filePath}", sheet_name=1, usecols=COLS), #3G
                    pd.read_excel(f"{filePath}", sheet_name=2, usecols=COLS)] #4G
        dfs.append(temd_dfs)
    return dfs
