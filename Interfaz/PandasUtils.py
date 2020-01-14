import pandas as pd
import concurrent.futures
import time
from PyQt5.QtCore import QThread, pyqtSignal


class PandasDataLoader:
    """
    A class that acts as a container for the dataframe and manages all the operations
    with the data
    """
    __instance = None
    @staticmethod
    def getInstance():
        if PandasDataLoader.__instance is None:
            PandasDataLoader()
        return PandasDataLoader.__instance

    def __init__(self):
        if PandasDataLoader.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.dfsList = []
            self.allData = None
            self.processing = False
            self.threadProcessor = ThreadingUtils()
            self.uniqueColumnValues = dict()
            PandasDataLoader.__instance = self

    def setUniqueColumnValues(self, df, column):
        self.uniqueColumnValues[column] = df[column].unique().tolist()

    def getCantidadDatos(self, df, columna, filtros=[]):
        groupedData = df.groupby(columna)
        dfs = [groupedData.get_group(gn) for gn in filtros]
        return pd.concat(dfs).shape[0]
    
    def getRowCountForColumn(self, df, columna):
        # returns the number of non-NaN values in the column
        return df[columna].count()

    def getUniqueColumnValues(self, column):
        """
        Returns a list of all the diferent values for a column
        """
        return self.uniqueColumnValues[column]

    def loadDataframes(self, pathList=[], callback=None):
        def loadDataWrapper():
            print("Empieza carga de datos desde thread")
            self.processing = True
            """
            Reads each excel file and saves all the sheets into a list with the specified columns
            """
            COLS = ["RAT", "OPERATOR", "CHANNEL", "IMEI", "IMSI", "TMSI",
                    "MS POWER", "TA", "LAST LAC", "NAME", "HITS", "DATE-TIME"]
            for filePath in pathList:
                temd_dfs = [pd.read_excel(f"{filePath}", sheet_name=0, usecols=COLS),  # 2G
                            pd.read_excel(
                                f"{filePath}", sheet_name=1, usecols=COLS),  # 3G
                            pd.read_excel(f"{filePath}", sheet_name=2, usecols=COLS)]  # 4G
                self.dfsList.append(temd_dfs)
            # Puts all the general and raw data into a df
            self.allData = pd.concat(
                [df for dflist in self.dfsList for df in dflist])

            # TODO: HACER REEMPLAZO DE UNA
            self.allData['DATE-TIME'] = self.allData['DATE-TIME'].apply(self.toDatetime)
            self.allData['DATE'] = pd.to_datetime(self.allData['DATE-TIME'], format="%Y-%m-%d").dt.date
            self.allData['TIME'] = pd.to_datetime(self.allData['DATE-TIME']).dt.time
            self.allData.sort_values(by=["DATE"], inplace=True, ascending=True)
            # Borra columna
            self.allData.drop('DATE-TIME', axis=1, inplace=True)
            # Cambia el nombre de las columnas a estandar
            cols = self.allData.columns
            cols = cols.map(lambda x: x.strip().replace(' ', '_').strip() if isinstance(x, (str, )) else x)
            self.allData.columns = cols
            self.processing = False
        self.threadProcessor.setWorker(loadDataWrapper)
        self.threadProcessor.start(QThread.HighestPriority)
        self.threadProcessor.finished.connect(callback)
        # ThreadingUtils.doInThread(loadDataWrapper, callback)

    def getMonthInt(self,strMonth):
        if(strMonth.lower() in ["ene"]):
            return 1
        elif(strMonth.lower() in ["feb"]):
            return 2
        elif(strMonth.lower() in ["mar"]):
            return 3
        elif(strMonth.lower() in ["abr"]):
            return 4
        elif(strMonth.lower() in ["may"]):
            return 5
        elif(strMonth.lower() in ["jun"]):
            return 6
        elif(strMonth.lower() in ["jul"]):
            return 7
        elif(strMonth.lower() in ["ago"]):
            return 8
        elif(strMonth.lower() in ["sep"]):
            return 9
        elif(strMonth.lower() in ["oct"]):
            return 10
        elif(strMonth.lower() in ["nov"]):
            return 11
        elif(strMonth.lower() in ["dic"]):
            return 12

    def toDatetime(self,dateStr):
        # Date string example-> ma. dic. 31 23:50:11 2019
        _, month,t_year = list(map(str.strip, dateStr.split('.')))
        day, t, year = t_year.split(' ') 
        month = self.getMonthInt(month)
        dateStr = f"{year}-{month}-{day} {t}"
        return pd.to_datetime(dateStr, format="%Y-%m-%d %X")

class ThreadingUtils_:

    @staticmethod
    def doInThread(worker=None, callback=None):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(worker)
            future.add_done_callback(callback)
            return future


class ThreadingUtils(QThread):
    updateSignal = pyqtSignal()

    def __init__(self, worker=None):
        super(QThread, self).__init__()
        self.worker = worker

    def setWorker(self, worker):
        self.worker = worker

    def run(self):
        self.worker()
        self.updateSignal.emit()


# Testing
def worker():
    time.sleep(5)
    return "Worker done"


def callBack(future):
    print(f"Se ejecuta callback {future} {future.result()}")


if(__name__ == '__main__'):
    ThreadingUtils.doInThread(worker, callBack)
