import pandas as pd
import numpy as np
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
            # Dataframes
            self.tempDf = None
            self.allData2G = None
            self.allData3G = None
            self.allData4G = None
            self.sinImei4g = None
            self.dfIncidentales = None

            # Processing ans state
            self.processing = False
            self.threadProcessor = ThreadingUtils()
            self.saverThread = ThreadingUtils()
            self.uniqueColumnValues = dict()
            PandasDataLoader.__instance = self

    def concatDfs(self, dfs: list):
        return pd.concat(dfs)

    def getAllData(self):
        df = pd.concat([self.allData2G, self.allData3G, self.allData4G])
        print(f"All data shape {df.shape}")
        return df

    def setTempDf(self, df: pd.DataFrame):
        print(f"PANDAS UTILS: setting new temp df {df.shape}")
        self.tempDf = df

    def setUniqueColumnValues(self, df: pd.DataFrame, column: str):
        # Adds to the state dictionary the unique values of a column from the df
        self.uniqueColumnValues[column] = df[column].unique().tolist()

    def getCantidadDatos(self, df, columna, filtros=[]):
        groupedData = df.groupby(columna)

        dfs = []
        try:
            # [groupedData.get_group(gn) for gn in filtros]
            for gn in filtros:
                dfs.append(groupedData.get_group(gn))
        except Exception as e:
            print(e)
            return 0
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
            dfsList = []
            """
            Reads each excel file and saves all the sheets into a list with the specified columns
            """
            COLS = ["RAT", "OPERATOR", "CHANNEL", "IMEI", "IMSI", "TMSI",
                    "MS POWER", "TA", "LAST LAC", "NAME", "HITS", "DATE-TIME"]
            for filePath in pathList:
                temd_df = pd.read_excel(f"{filePath}", usecols=COLS)
                dfsList.append(temd_df)
            # Puts all the general and raw data into a df
            allData = pd.concat(dfsList)
            allData.dropna(how='all', inplace=True)

            # Asigna nueva columna DATE_TIME ya formateado y quita la vieja
            allData['DATE_TIME'] = allData['DATE-TIME'].apply(self.toDatetime)
            allData.drop('DATE-TIME', axis=1, inplace=True)
            # Cambia el nombre de las columnas a estandar con _ en lugar de espacios
            cols = allData.columns
            cols = cols.map(lambda x: x.strip().replace(
                ' ', '_').strip() if isinstance(x, (str, )) else x)
            allData.columns = cols

            # Intenta convertir cada columna y si no pone NaN
            allData['MS_POWER'] = pd.to_numeric(allData['MS_POWER'], errors='coerce')

            # Sacar los incidentales
            self.dfIncidentales = self.getDfDatosIncidentales(allData, hitsMin=1)
            allData = self.getDifferenceBetweenDataFrames(allData,  self.dfIncidentales)
            self.dividirDfEnRats(allData)

            self.sinImei4g = self.allData4G[self.allData4G['IMEI'].isnull()]
            self.processing = False
        self.threadProcessor.setWorker(loadDataWrapper)
        self.threadProcessor.start(QThread.HighestPriority)
        self.threadProcessor.finished.connect(callback)
        # ThreadingUtils.doInThread(loadDataWrapper, callback)

    def dividirDfEnRats(self, allData: pd.DataFrame):
        self.allData2G = self.filterByRat(allData, "2G")
        self.allData3G = self.filterByRat(allData, "3G")
        self.allData4G = self.filterByRat(allData, "4G")

    def getDfImeisFaltantes(self, df: pd.DataFrame):
        return df[df['IMEI'].isnull()]

    def asignarIMEIS(self, allDataP: pd.DataFrame, dfImeisFaltantes: pd.DataFrame):
        """ Assigns Emais for the columns where the emais is null based on the historical data"""
        def joinValues(values):
            # print(f"{type(values)}")
            return ','.join(map(str, values))

        def obtenerEmai(x: str):
            # X is the IMSI value
            rCoincide = allDataP[allDataP['IMSI'].isin(x.values)]['IMEI']
            imeis = joinValues(rCoincide[rCoincide.notnull()].unique())
            return imeis
        nuevosValores = dfImeisFaltantes.groupby('IMSI')['IMSI'].transform(obtenerEmai)
        allDataP.loc[dfImeisFaltantes.index, 'IMEI'] = nuevosValores
        # Retorna serie con nuevos valores de IMEI separados por coma
        return allDataP



    def getDfDatosIncidentales(self, df: pd.DataFrame, hitsMin: int = 1):
        print(f"Empieza obtencion incidentales df arg {df.shape}")
        groupedDfHitsMin = df.groupby('IMEI').filter(lambda x: x['HITS'].sum() <= hitsMin)
        print(f"Grouped hits min {groupedDfHitsMin.shape}")
        # print("Agrupados por hits igual a 1\n ", groupedDfHitsMin)
        groupedDfNullVals = df.loc[df['MS_POWER'].isnull() | df['DATE_TIME'].isnull() | df['HITS'].isnull()]
        print(f"Grouped nulls {groupedDfNullVals.shape}")
        incidentales = pd.concat([groupedDfHitsMin, groupedDfNullVals]).drop_duplicates()
        # Sin IMEI ni IMSI
        print(f"Finaliza obtencion de incidentales df arg {incidentales.shape}")
        return incidentales

    def getDifferenceBetweenDataFrames(self, dfLeft: pd.DataFrame, dfRight: pd.DataFrame):
        print(f"Empieza proceso de diferencia entre dfs left {dfLeft.shape} right {dfRight.shape}")
        dfRes = dfLeft.merge(dfRight, indicator=True, how='left').loc[lambda x: x['_merge'] != 'both']
        dfRes.drop(columns=['_merge'], inplace=True)
        print(f"New df after merge-drop {dfRes.shape}")
        return dfRes

    def getGroupedByEmais(self, df: pd.DataFrame):
        # Returns a df with grouped and aggregated values
        def joinValues(series):
            return ','.join(map(str, series[series.notnull()].unique()))
        groupedDf = df.groupby('IMEI').agg(
            IMEI=pd.NamedAgg(column='IMEI', aggfunc=joinValues),
            RAT=pd.NamedAgg(column='RAT', aggfunc=joinValues),
            OPERATOR=pd.NamedAgg(column='OPERATOR', aggfunc=joinValues),
            CHANNEL=pd.NamedAgg(column='CHANNEL', aggfunc=joinValues),
            IMSI=pd.NamedAgg(column='IMSI', aggfunc=joinValues),
            TMSI=pd.NamedAgg(column='TMSI', aggfunc=joinValues),
            MS_POWER=pd.NamedAgg(column='MS_POWER', aggfunc=joinValues),
            TA=pd.NamedAgg(column='TA', aggfunc=joinValues),
            LAST_LAC=pd.NamedAgg(column='LAST_LAC', aggfunc=joinValues),
            NAME=pd.NamedAgg(column='NAME', aggfunc=joinValues),
            HITS=pd.NamedAgg(column='HITS', aggfunc='sum'),
            DATE_TIME=pd.NamedAgg(column='DATE_TIME', aggfunc=joinValues),
        )
        return groupedDf.reset_index(drop=True)


    def getGroupedByIMSI(self, df: pd.DataFrame):
        # Returns a df with grouped and aggregated values
        def joinValues(series):
            return ','.join(map(str, series[series.notnull()].unique()))
        groupedDf = df.groupby('IMSI').agg(
            IMSI=pd.NamedAgg(column='IMSI', aggfunc=joinValues),
            RAT=pd.NamedAgg(column='RAT', aggfunc=joinValues),
            OPERATOR=pd.NamedAgg(column='OPERATOR', aggfunc=joinValues),
            CHANNEL=pd.NamedAgg(column='CHANNEL', aggfunc=joinValues),
            IMEI=pd.NamedAgg(column='IMEI', aggfunc=joinValues),
            TMSI=pd.NamedAgg(column='TMSI', aggfunc=joinValues),
            MS_POWER=pd.NamedAgg(column='MS_POWER', aggfunc=joinValues),
            TA=pd.NamedAgg(column='TA', aggfunc=joinValues),
            LAST_LAC=pd.NamedAgg(column='LAST_LAC', aggfunc=joinValues),
            NAME=pd.NamedAgg(column='NAME', aggfunc=joinValues),
            HITS=pd.NamedAgg(column='HITS', aggfunc='sum'),
            DATE_TIME=pd.NamedAgg(column='DATE_TIME', aggfunc=joinValues),
        )
        return groupedDf.reset_index(drop=True)


    def getGroupedByEmaisHorario(self, df: pd.DataFrame):
        # Returns a df with grouped and aggregated values
        def joinValues(series):
            return ','.join(map(str, series[series.notnull()].unique()))
        groupedDf = df.groupby('IMEI').agg(
            IMEI=pd.NamedAgg(column='IMEI', aggfunc=joinValues),
            IMSIS=pd.NamedAgg(column='IMSI', aggfunc=joinValues),
            HITS=pd.NamedAgg(column='HITS', aggfunc='sum'),
            DATE_TIME=pd.NamedAgg(column='DATE_TIME', aggfunc=joinValues)
        )
        return groupedDf.reset_index(drop=True)

    def getGroupedByEmaisIMSIS(self, df: pd.DataFrame):
        # Returns a df with grouped and aggregated values
        def joinValues(series):
            return ','.join(map(str, series[series.notnull()].unique()))
        groupedDf = df.groupby('IMEI').agg(
            IMEI=pd.NamedAgg(column='IMEI', aggfunc=joinValues),
            IMSIS=pd.NamedAgg(column='IMSI', aggfunc=joinValues),
            CANTIDAD=pd.NamedAgg(column='IMSI', aggfunc=pd.Series.nunique),
            DATE_TIMEs=pd.NamedAgg(column='DATE_TIME', aggfunc=joinValues)
        )
        return groupedDf.reset_index(drop=True)

    def getGroupedByEmaisDates(self, df: pd.DataFrame):
        # Returns a df with grouped and aggregated values
        def joinValues(series):
            return ','.join(map(str, series[series.notnull()].unique()))
        groupedDf = df.groupby('IMEI').agg(
            IMEI=pd.NamedAgg(column='IMEI', aggfunc=joinValues),
            DATE_TIMES=pd.NamedAgg(column='DATE_TIME', aggfunc=joinValues),
            CANTIDAD=pd.NamedAgg(column='IMSI', aggfunc=pd.Series.nunique),
        )
        return groupedDf.reset_index(drop=True)

    def getGroupedByEmaisCanales(self, df: pd.DataFrame):
        # Returns a df with grouped and aggregated values
        def joinValues(series):
            return ','.join(map(str, series[series.notnull()].unique()))
        groupedDf = df.groupby('IMEI').agg(
            IMEI=pd.NamedAgg(column='IMEI', aggfunc=joinValues),
            CHANNELS=pd.NamedAgg(column='CHANNEL', aggfunc=joinValues),
            CANTIDAD=pd.NamedAgg(column='CHANNEL', aggfunc=pd.Series.nunique),
        )
        return groupedDf.reset_index(drop=True)

    def getGroupedByEmaisOps(self, df: pd.DataFrame):
        # Returns a df with grouped and aggregated values
        def joinValues(series):
            return ','.join(map(str, series[series.notnull()].unique()))
        groupedDf = df.groupby('IMEI').agg(
            IMEI=pd.NamedAgg(column='IMEI', aggfunc=joinValues),
            OPERATORS=pd.NamedAgg(column='OPERATOR', aggfunc=joinValues),
            CANTIDAD=pd.NamedAgg(column='OPERATOR', aggfunc=pd.Series.nunique),
        )
        return groupedDf.reset_index(drop=True)


    def filtroHoras(self, df: pd.DataFrame, fromTime, toTime):
        return df[(df['DATE_TIME'].dt.hour >= fromTime) & (df['DATE_TIME'].dt.hour < toTime)]

    def saveToExcelFile(self, df: pd.DataFrame, newFilePath: str, index=False, callbackSave=None):
        def saveFunctionWrapper():
            df.to_excel((newFilePath if newFilePath.endswith(
                ".xlsx") else (newFilePath+".xlsx")), index=index)
        self.saverThread.setWorker(saveFunctionWrapper)
        self.saverThread.start(QThread.HighestPriority)
        self.saverThread.finished.connect(callbackSave)

    def tiempoAvanceFilterTA(self, df: pd.DataFrame, valuesList: list = []):
        """ Filters the df by the values on the TA column"""
        return (df[df['TA'].isin(valuesList)] if len(valuesList) > 0 else df)

    def filtroDatetimes(self, df: pd.DataFrame, fromDate, toDate):
        return df.loc[(df['DATE_TIME'] >= fromDate) & (df['DATE_TIME'] <= toDate)]

    def filterByRat(self, df: pd.DataFrame, rat: str):
        """ Returns a df with the seleccted rats """
        return df[df['RAT'] == rat]

    def filterByHitsAmount(self, df: pd.DataFrame, amount: int = 0):
        """ Filters the df where the hits amount are greater or equal to the given amount """
        return df[df['HITS'] >= amount]

    def filterByHitsAmountMin(self, df: pd.DataFrame, amount: int):
        """ Filters the df where the hits amount are greater or equal to the given amount """
        return df[df['HITS'] <= amount]

    def msPowerRangeFilter(self, df: pd.DataFrame, fromN: float, toN: float):
        """ Filters the df in the column MS POWER with the given boundaries"""
        print(f"PANDAS UTILS: Ms power filter from {fromN} to {toN}")
        return (df[df['MS_POWER'].between(fromN, toN)] if fromN is not None and toN is not None else df)

    def filtroLastLacValor(self, df: pd.DataFrame, value: float = None):
        # return (df[df['LAST_LAC'] == float(value)] if value is not None else df)
        df = (df[df['LAST_LAC'] == float(value)] if value is not None else df)
        return {key: val for key, val in df.itertuples()}

    def lastLacFrecuenciaSeries(self, df: pd.DataFrame):
        groupedDf = df.groupby('LAST_LAC').size().sort_values(ascending=False)
        return groupedDf

    def hitsByDate(self, df: pd.DataFrame):
        print(f"Pandas Utils: Df to group by date shape {df.shape} info  {df.info()} Index {df.index}")
        dfT = df[df['DATE_TIME'].notnull()]
        series = dfT.set_index('DATE_TIME').groupby(pd.Grouper(freq='D'))['HITS'].apply(sum)
        return series
    def dfLastLacFrecuencia(self, df: pd.DataFrame):
        groupedDf = df.groupby('LAST_LAC')['LAST_LAC'].agg(FRECUENCIA=pd.NamedAgg(column='LAST_LAC', aggfunc='size'))
        groupedDf['LAST_LAC'] = groupedDf.index
        groupedDf = groupedDf[['LAST_LAC', 'FRECUENCIA']]
        return groupedDf.sort_values(ascending=False, by='FRECUENCIA')

    def setUniqueNameIdColumn(self, dfEmaisOk: pd.DataFrame):
        """ Updates the NAME with a unique KEY for a EMAI groups and returns that new DataFrame"""
        import hashlib
        def fn(x): return hashlib.md5(str(x).encode()).hexdigest()[0:10]
        df1 = dfEmaisOk.groupby('IMEI')['IMEI'].transform(fn)
        return dfEmaisOk.assign(NAME=df1)

    def filterDfByEmai(self, df: pd.DataFrame = None, imei: float = None):
        return (df[df['IMEI'].astype(float) == float(imei)] if imei is not None else df)

    def getDfCompletoEmaisOk(self, df: pd.DataFrame):
        """
        Returns the df where the EMAIS are not null
        """
        return df.loc[df['IMEI'].notnull()]

    def filterDfByColumnValues(self, df: pd.DataFrame, column: str, columnValues: list=[]):
        """
        Groups the df by the column parameters and gets the groups in the columnValues list
        """
        return df[df[column].isin(columnValues)] if len(columnValues) > 0 else df

    def filterByHitsGrouping(self, df: pd.DataFrame, columnToGroupBy: str = 'IMEI', hitsMin: int = 0):
        """ Returns all the rows that in the group acomplish the filter of min of hits"""
        print(f"Hits by grouping df shape{df.info()} column {columnToGroupBy}")
        return df.groupby(columnToGroupBy).filter(lambda x: x['HITS'].sum() >= hitsMin)

    def getMonthInt(self, strMonth):
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

    def toDatetime(self, dateStr):
        try:
            # Date string example-> ma. dic. 31 23:50:11 2019
            _, month, t_year = list(map(str.strip, dateStr.split('.')))
            day, t, year = t_year.split(' ')
            month = self.getMonthInt(month)
            dateStr = f"{year}-{month}-{day} {t}"
            return pd.to_datetime(dateStr, format="%Y-%m-%d %X")
        except Exception as e:
            print(e)
            return np.NaN

    def isFloat(self, strNumber: str):
        try:
            float(strNumber)
            return True
        except ValueError as ve:
            return False


class ThreadingUtils_:

    @staticmethod
    def doInThread(worker=None, callback=None):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(worker)
            future.add_done_callback(callback)
            return future


class ThreadingUtils(QThread):
    """ Thread class processor to do hard work """
    updateSignal = pyqtSignal()

    def __init__(self, worker=None):
        super(QThread, self).__init__()
        self.worker = worker

    def setWorker(self, worker):
        self.worker = worker

    def run(self):
        # Starts the worker and then emits the signal
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
