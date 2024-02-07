import pandas as pd
import Utility
import matplotlib.pyplot as plt

def loadgentrend():
    # Pull latest SPP .csv's into pandas data frames
    DAMCTable = pd.read_csv(Utility.pulllatestcsv('DAMC'))
    SUMTable = pd.read_csv(Utility.pulllatestcsv('RTMD')[0])

    #Correct the Day Ahead Table
    DAMCTable['Interval'] = pd.to_datetime(DAMCTable['Interval'])
    DAMCTable.set_index(keys=DAMCTable['Interval'], inplace=True)
    DAMCTable.drop('GMTIntervalEnd', axis=1, inplace=True)
    DAMCTable['Cap Minus Reserve'] = DAMCTable['Capacity Available'] - (DAMCTable['Spin'] + DAMCTable['Supp'])
    print(DAMCTable)

    #Correct the Summary Table
    SUMTable['Interval'] = pd.to_datetime(SUMTable['Interval'])
    SUMTable.set_index(keys=SUMTable['Interval'], inplace=True)
    SUMTable.sort_index(inplace=True)
    SUMTable.drop('GMTIntervalEnd', axis=1, inplace=True)
    SUMTable.ffill(inplace=True)
    print(SUMTable)

    #Create a single load line before forward fill (334 5 Min periods before using MTLF)
    LoadTrend = pd.DataFrame(index=SUMTable['Interval'], columns=['Load'])
    x = 0
    for i in LoadTrend.index:
        x += 1
        if x < 334:
            LoadTrend.loc[i, 'Load'] = SUMTable.loc[i, 'STLF']
        else:
            LoadTrend.loc[i, 'Load'] = SUMTable.loc[i, 'MTLF']

    #Create New DAMC Table to integrate with SUM table
    DAMCTrendTable = pd.DataFrame(index=SUMTable['Interval'], columns=['Capacity Available', 'Cap Minus Reserve'])
    #Match values from DAMCTable to DAMCTrendTable
    for i in DAMCTrendTable.index:
        if i in DAMCTable.index:
            DAMCTrendTable.loc[i, 'Capacity Available'] = DAMCTable.loc[i, 'Capacity Available']
            DAMCTrendTable.loc[i, 'Cap Minus Reserve'] = DAMCTable.loc[i, 'Cap Minus Reserve']
        else:
            pass

    #Remove NaN values using forward fill
    DAMCTrendTable.ffill(inplace=True)
    print(DAMCTrendTable)

    #Create combined table
    CombinedTrendTable = pd.DataFrame(index=SUMTable['Interval'], columns=['Load', 'MTWF', 'Capacity Available', 'Cap Minus Reserve'])
    for i in CombinedTrendTable.index:
        CombinedTrendTable.loc[i, 'Load'] = LoadTrend.loc[i, 'Load']
        CombinedTrendTable.loc[i, 'MTWF'] = SUMTable.loc[i, 'MTWF']
        CombinedTrendTable.loc[i, 'Capacity Available'] = DAMCTrendTable.loc[i, 'Capacity Available']
        CombinedTrendTable.loc[i, 'Cap Minus Reserve'] = DAMCTrendTable.loc[i, 'Cap Minus Reserve']
    CombinedTrendTable['Total Gen'] = CombinedTrendTable['Capacity Available'] + SUMTable['MTWF']
    CombinedTrendTable.ffill(inplace=True)
    print(CombinedTrendTable)
    #CombinedTrendTable.to_csv(path_or_buf='C:/Users/###/OneDrive/Documents/test.csv')
    CombinedTrendTable.plot()
    plt.show()
    return CombinedTrendTable



loadgentrend()
