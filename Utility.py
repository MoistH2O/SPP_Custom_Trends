import os
import shutil
import datetime
import requests
import math

# Get user info and generate path strings
UserName = os.getlogin()
SPPDocPath = 'C:/Users/' + UserName + '/Onedrive/Documents/SPP'
SPPSubDirs = ['DAMC', 'OPDATA', 'RTBM', 'RTMD']

def getcurrtime():
    global CMinute
    global CHour
    global CHourL1
    global CHourP1
    global CDay
    global CDayL1
    global CDayP1
    global YestMonth
    global CMonth
    global TomMonth
    global YestYear
    global CYear
    global TomYear
    global C5MinInc
    global C5MinIncL1
    global C5MinIncP1
    global Now
    Yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    Tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    # get current time and date
    Now = datetime.datetime.now()
    CMinute = Now.strftime('%M')
    CHour = Now.strftime('%H')
    if len(str(int(CHour) - 1)) == 1:
        CHourL1 = '0' + str(int(CHour) - 1)
    else:
        CHourL1 = str(int(CHour) - 1)
    if len(str(int(CHour) + 1)) == 1:
        CHourP1 = '0' + str(int(CHour) + 1)
    else:
        if str(int(CHour) + 1) == '24':
            CHourP1 = '00'
        else:
            CHourP1 = str(int(CHour) + 1)
    CDay = str(Now.strftime('%d'))
    if len(str(Yesterday.day)) == 1:
        CDayL1 = '0' + str(Yesterday.day)
    else:
        CDayL1 = str(Yesterday.day)
    if len(str(Tomorrow.day)) == 1:
        CDayP1 = '0' + str(Tomorrow.day)
    else:
        CDayP1 = str(Tomorrow.day)
    YestMonth = str(Yesterday.strftime('%m'))
    CMonth = str(Now.strftime('%m'))
    TomMonth = str(Tomorrow.strftime('%m'))
    YestYear = str(Yesterday.strftime('%Y'))
    CYear = str(Now.strftime('%Y'))
    TomYear = str(Tomorrow.strftime('%Y'))
    if (math.floor(int(CMinute) / 5) * 5) > 9:
        C5MinInc = str((math.floor(int(CMinute) / 5) * 5))
    else:
        C5MinInc = '0' + str((math.floor(int(CMinute) / 5) * 5))
    if len(str(int(C5MinInc) - 1)) == 1:
        C5MinIncL1 = '0' + str(int(C5MinInc) - 5)
    else:
        if str(int(C5MinInc) - 5) == "-5":
            C5MinIncL1 = '55'
        else:
            C5MinIncL1 = str(int(C5MinInc) - 5)
    if len(str(int(C5MinInc) + 1)) == 1:
        C5MinIncP1 = '0' + str(int(C5MinInc) + 5)
    else:
        if str(int(C5MinInc) + 5) == "60":
            C5MinIncP1 = '55'
        else:
            C5MinIncP1 = str(int(C5MinInc) + 5)
    TimeDict = {
        'Minute': CMinute,
        'Hour': CHour,
        'Last Hour': CHourL1,
        'Next Hour': CHourP1,
        'Day': CDay,
        'Last Day': CDayL1,
        'Next Day': CDayP1,
        'Month': CMonth,
        'Yesterday Month': YestMonth,
        'Tomorrow Month': TomMonth,
        'Year': CYear,
        'Yesterday Year': YestYear,
        'Tomorrow Year': TomYear,
        '5 Minute Interval': C5MinInc,
        'Last 5 Minute Interval': C5MinIncL1,
        'Next 5 Minute Interval': C5MinIncP1,
        'Now': Now
    }
    return TimeDict

def checksetupdirs():
    #check for SPP dir in documents
    try:
        os.listdir(SPPDocPath)
        print("Found SPP dir. Now checking sub dirs.")
    except WindowsError:
        print('Unable to find SPP dir. Creating dir in documents.')
        print('C:/Users/' + UserName + '/Onedrive/Documents/SPP')
        os.mkdir('C:/Users/' + UserName + '/Onedrive/Documents/SPP')

    #check for sub dirs in spp documents
    for i in SPPSubDirs:
        if i in os.listdir(SPPDocPath):
            pass
        else:
            print(f'Unable to find {i} folder. Creating {i} folder in SPP dir.')
            os.mkdir('C:/Users/' + UserName + f'/Onedrive/Documents/SPP/{i}')
    print('Finished checking sub dirs.')

def pulllatestcsv(x):
    #DAHRFR check/download
    if x == 'DAMC':
        SPPSubDirPath = SPPDocPath+'/'+x
    #check if most recent file is downloaded
        if int(CHour) >= 14 and TomMonth == CMonth:
            CDAMCFile = 'DA-MC-' + CYear + CMonth + CDayP1 + '0100.csv'
            LinkMonth = CMonth
        elif int(CHour) >= 14 and TomMonth != CMonth:
            CDAMCFile = 'DA-MC-' + CYear + TomMonth + CDayP1 + '0100.csv'
            LinkMonth = TomMonth
        else:
            CDAMCFile = 'DA-MC-' + CYear + CMonth + CDay + '0100.csv'
            LinkMonth = CMonth
        SPPCDAMCFilePath = SPPSubDirPath+'/'+CDAMCFile

        if CDAMCFile in os.listdir(SPPSubDirPath):
            print('Current DAMC file already downloaded.')
        else:
            print('Current DAMC file will be downloaded.')
            print(CDAMCFile)
            file = requests.get(f'https://portal.spp.org/file-browser-api/download/market-clearing?path=%2F{CYear}%2F{LinkMonth}%2F{CDAMCFile}')
            open(SPPCDAMCFilePath, 'wb').write(file.content)
            print("Current DAMC file finished downloading.")
            print(SPPCDAMCFilePath)
        return SPPCDAMCFilePath

    elif x == 'OPDATA':
        SPPSubDirPath = SPPDocPath + '/' + x
    # check if most recent files are downloaded
        if int(CMinute) > 6:
            CMTLFFile = 'OP-MTLF-' + f'{CYear}{CMonth}{CDay}{CHour}00.csv'
        else:
            CMTLFFile = 'OP-MTLF-' + f'{CYear}{CMonth}{CDay}{CHourL1}00.csv'
        if int(CMinute) > 6:
            CMTRFFile = 'OP-MTRF-' + f'{CYear}{CMonth}{CDay}{CHour}00.csv'
        else:
            CMTRFFile = 'OP-MTRF-' + f'{CYear}{CMonth}{CDay}{CHourL1}00.csv'
        if int(CMinute)-int(C5MinInc) > 1:
            CSTLFFile = 'OP-STLF-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinInc}.csv'
        else:
            CSTLFFile = 'OP-STLF-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinIncL1}.csv'
        if int(CMinute) - int(C5MinInc) > 1:
            CSTRFFile = 'OP-STRF-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinInc}.csv'
        else:
            CSTRFFile = 'OP-STRF-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinIncL1}.csv'
        OPFileArray = [CMTLFFile, CMTRFFile, CSTLFFile, CSTRFFile]

        for i in OPFileArray:
            if i in os.listdir(SPPSubDirPath):
                print(i + ' already downloaded.')
            else:
                if i == OPFileArray[0]:
                    file = requests.get(f'https://portal.spp.org/file-browser-api/download/mtlf-vs-actual?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{i}')
                    open(SPPSubDirPath + '/' + i, 'wb').write(file.content)
                    print(f"Current {i} file finished downloading.")
                elif i == OPFileArray[1]:
                    file = requests.get(f'https://portal.spp.org/file-browser-api/download/midterm-resource-forecast?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{i}')
                    open(SPPSubDirPath + '/' + i, 'wb').write(file.content)
                    print(f"Current {i} file finished downloading.")
                elif i == OPFileArray[2]:
                    file = requests.get(f'https://portal.spp.org/file-browser-api/download/stlf-vs-actual?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{CHourP1}%2F{i}')
                    open(SPPSubDirPath + '/' + i, 'wb').write(file.content)
                    print(f"Current {i} file finished downloading.")
                elif i == OPFileArray[3]:
                    file = requests.get(f'https://portal.spp.org/file-browser-api/download/shortterm-resource-forecast?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{CHourP1}%2F{i}')
                    open(SPPSubDirPath + '/' + i, 'wb').write(file.content)
                    print(f"Current {i} file finished downloading.")
        print("Check for latest OPDATA files finished.")
        return [SPPSubDirPath+'/'+CMTLFFile, SPPSubDirPath+'/'+CMTRFFile, SPPSubDirPath+'/'+CSTLFFile, SPPSubDirPath+'/'+CSTRFFile]

    elif x == 'RTBM':
        SPPSubDirPath = SPPDocPath + '/' + x
    # check if most recent files are downloaded
        if int(CMinute) - int(C5MinInc) > 1:
            CORFile = 'RTBM-OR-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinIncP1}.csv'
        else:
            CORFile = 'RTBM-OR-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinInc}.csv'
        CORFilePath = SPPSubDirPath + '/' + CORFile

        if CORFile in os.listdir(SPPSubDirPath):
            print('Current OR file already downloaded.')
        else:
            file = requests.get(f'https://portal.spp.org/file-browser-api/download/operating-reserves?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{CORFile}')
            open(CORFilePath, 'wb').write(file.content)
            print(f"Current {CORFile} file finished downloading.")
        return CORFilePath

    elif x == 'RTMD':
        SPPSubDirPath = SPPDocPath + '/' + x
        RTMDFileArray = ['summaryForecast.csv', 'TieFlows.csv']
    # No check can be completed due to file names
        for i in RTMDFileArray:
            if i == 'summaryForecast.csv':
                file = requests.get('https://portal.spp.org/chart-api/load-forecast/asFile')
            else:
                file = requests.get('https://portal.spp.org/chart-api/interchange-trend/asFile')
            open(SPPSubDirPath + '/' + i, 'wb').write(file.content)
            print(f"Current {i} file finished downloading.")
        return [SPPSubDirPath + '/' + RTMDFileArray[0], SPPSubDirPath + '/' + RTMDFileArray[1]]

    elif x == 'All':
        FolderArray= ['DAMC', 'OPDATA', 'RTBM', 'RTMD']
        for i in FolderArray:
            print(i)
            SPPSubDirPath = SPPDocPath + '/' + i
            if i == 'DAMC':
                # check if most recent file is downloaded
                if int(CHour) >= 14:
                    CDAMCFile = 'DA-MC-' + CYear + CMonth + CDayP1 + '0100.csv'
                else:
                    CDAMCFile = 'DA-MC-' + CYear + CMonth + CDay + '0100.csv'
                SPPCDAMCFilePath = SPPSubDirPath+'/'+CDAMCFile

                if CDAMCFile in os.listdir(SPPSubDirPath):
                    print('Current DAMC file already downloaded.')
                else:
                    print('Current DAMC file will be downloaded.')
                    file = requests.get(
                        f'https://portal.spp.org/file-browser-api/download/market-clearing?path=%2F{CYear}%2F{CMonth}%2F{CDAMCFile}')
                    open(SPPCDAMCFilePath, 'wb').write(file.content)
                    print("Current DAMC file finished downloading.")
                    print(SPPCDAMCFilePath)

            elif i == 'OPDATA':
            # check if most recent files are downloaded
                if int(CMinute) > 6:
                    CMTLFFile = 'OP-MTLF-' + f'{CYear}{CMonth}{CDay}{CHour}00.csv'
                else:
                    CMTLFFile = 'OP-MTLF-' + f'{CYear}{CMonth}{CDay}{CHourL1}00.csv'
                if int(CMinute) > 6:
                    CMTRFFile = 'OP-MTRF-' + f'{CYear}{CMonth}{CDay}{CHour}00.csv'
                else:
                    CMTRFFile = 'OP-MTRF-' + f'{CYear}{CMonth}{CDay}{CHourL1}00.csv'
                if int(CMinute)-int(C5MinInc) > 1:
                    CSTLFFile = 'OP-STLF-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinInc}.csv'
                else:
                    CSTLFFile = 'OP-STLF-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinIncL1}.csv'
                if int(CMinute) - int(C5MinInc) > 1:
                    CSTRFFile = 'OP-STRF-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinInc}.csv'
                else:
                    CSTRFFile = 'OP-STRF-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinIncL1}.csv'
                OPFileArray = [CMTLFFile, CMTRFFile, CSTLFFile, CSTRFFile]

                for y in OPFileArray:
                    if y in os.listdir(SPPSubDirPath):
                        print(y+ ' already downloaded.')
                    else:
                        if y == OPFileArray[0]:
                            file = requests.get(f'https://portal.spp.org/file-browser-api/download/mtlf-vs-actual?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{y}')
                            open(SPPSubDirPath + '/' + y, 'wb').write(file.content)
                            print(f"Current {y} file finished downloading.")
                        elif y == OPFileArray[1]:
                            file = requests.get(f'https://portal.spp.org/file-browser-api/download/midterm-resource-forecast?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{y}')
                            open(SPPSubDirPath + '/' + y, 'wb').write(file.content)
                            print(f"Current {y} file finished downloading.")
                        elif y == OPFileArray[2]:
                            file = requests.get(f'https://portal.spp.org/file-browser-api/download/stlf-vs-actual?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{CHourP1}%2F{y}')
                            open(SPPSubDirPath + '/' + y, 'wb').write(file.content)
                            print(f"Current {y} file finished downloading.")
                        elif y == OPFileArray[3]:
                            file = requests.get(f'https://portal.spp.org/file-browser-api/download/shortterm-resource-forecast?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{CHourP1}%2F{y}')
                            open(SPPSubDirPath + '/' + y, 'wb').write(file.content)
                            print(f"Current {y} file finished downloading.")
                print("Check for latest OPDATA files finished.")

            elif i == 'RTBM':
            # check if most recent files are downloaded
                if int(CMinute) - int(C5MinInc) > 1:
                    CORFile = 'RTBM-OR-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinIncP1}.csv'
                else:
                    CORFile = 'RTBM-OR-' + f'{CYear}{CMonth}{CDay}{CHour}{C5MinInc}.csv'
                CORFilePath = SPPSubDirPath + '/' + CORFile

                if CORFile in os.listdir(SPPSubDirPath):
                    print('Current OR file already downloaded.')
                else:
                    file = requests.get(f'https://portal.spp.org/file-browser-api/download/operating-reserves?path=%2F{CYear}%2F{CMonth}%2F{CDay}%2F{CORFile}')
                    open(CORFilePath, 'wb').write(file.content)
                    print(f"Current {CORFile} file finished downloading.")

            elif i == 'RTMD':
                RTMDFileArray = ['summaryForecast.csv', 'TieFlows.csv']
                SumFilePath = SPPSubDirPath + '/' + 'summaryForecast.csv'
                TieFilePath = SPPSubDirPath + '/' + 'TieFlows.csv'
            # No check can be completed due to file names
                for z in RTMDFileArray:
                    if z == 'summaryForecast.csv':
                        file = requests.get('https://portal.spp.org/chart-api/load-forecast/asFile')
                    else:
                        file = requests.get('https://portal.spp.org/chart-api/interchange-trend/asFile')
                    open(SPPSubDirPath + '/' + z, 'wb').write(file.content)
                    print(f"Current {z} file finished downloading.")
        SPPFileDict = {
            'Day Ahead Market Clearing': SPPCDAMCFilePath,
            'Mid Term Load Forcast': SPPSubDirPath + '/' + CMTLFFile,
            'Mid Term Resource Forecast': SPPSubDirPath + '/' + CMTRFFile,
            'Short Term Load Forecast': SPPSubDirPath + '/' + CSTLFFile,
            'Short Term Resource Forecast': SPPSubDirPath + '/' + CSTRFFile,
            'Operating Reserve': CORFilePath,
            'Summary Forecast': SumFilePath,
            'Tie Line Flows': TieFilePath
        }
        return SPPFileDict
getcurrtime()
pulllatestcsv('DAMC')
print(Now)