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
    #Create New DAMC Table to integrating with SUM table
    NewDAMCTimeRange = pd.date_range(start=DAMCTable['Interval'][0], end=DAMCTable['Interval'][23], freq="5min")
    DAMCTrendTable = pd.DataFrame(index=NewDAMCTimeRange, columns=['Capacity Available', 'Cap Minus Reserve'])
    #Match values from DAMCTable to DAMCTrendTable
    for i in DAMCTrendTable.index:
        if i in DAMCTable['Interval']:
            DAMCTrendTable.loc[i, 'Capacity Available'] = DAMCTable.loc[i, 'Capacity Available']
            DAMCTrendTable.loc[i, 'Cap Minus Reserve'] = DAMCTable.loc[i, 'Cap Minus Reserve']
        else:
            pass
    #Remove NaN values using forward fill
    DAMCTrendTable.ffill(inplace=True)

    #Correct the Summary Table
    SUMTable['Interval'] = pd.to_datetime(SUMTable['Interval'])
    SUMTable.set_index(keys=SUMTable['Interval'], inplace=True)
    SUMTable.drop('GMTIntervalEnd', axis=1, inplace=True)

    #Create combined table
    CombinedTrendTable = pd.DataFrame(index=NewDAMCTimeRange, columns=['STLF', 'MTLF', 'Capacity Available', 'Cap Minus Reserve'])
    for i in CombinedTrendTable.index:
        CombinedTrendTable.loc[i, 'STLF'] = SUMTable.loc[i, 'STLF']
        CombinedTrendTable.loc[i, 'MTLF'] = SUMTable.loc[i, 'MTLF']
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
