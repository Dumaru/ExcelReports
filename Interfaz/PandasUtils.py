import pandas as pd
import concurrent.futures
import time

class PandasDataLoader:
    def __init__(self):
        self.processing = False
    def loadDataframes(pathList=[], callback=None):
        def loadDataWrapper():
            self.processing=True
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
            self.processing=False
            return dfs
        ThreadingUtils.doInThread(loadDataWrapper(), callback)
    
class ThreadingUtils:

    @staticmethod
    def doInThread(worker=None, callback=None, *args):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(worker, *args)
            future.add_done_callback(callback)
            return future


# Testing
def worker():
    time.sleep(5)
    return "Worker done"

def callBack(future):
    print(f"Se ejecuta callback {future} {future.result()}")

if(__name__=='__main__'):
    ThreadingUtils.doInThread(worker, callBack)