import numpy as np
import pandas as pd
import Utility


# Pull latest SPP .csv's into pandas data frames
DAMCTable = pd.read_csv(Utility.pulllatestcsv('DAMC'))
#SUMTable = pd.read_csv(Utility.pulllatestcsv('RTMD')[0])

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
print(DAMCTrendTable)



#Correct the Summary Table
#SUMTable['Interval'] = pd.to_datetime(SUMTable['Interval'])

