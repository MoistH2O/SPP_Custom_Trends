This repository contains code used to interact with the csv files contained in the SPP website. Specifically, it grabs .csv files from the marketplace and generates trending displays.
-
File Descriptions:
-
- [Utility.py](https://github.com/MoistH2O/SPP_Custom_Trends/blob/master/Utility.py)
  - This file performs the following actions:
  - Grabs user info to find the document directory in OneDrive
  - Checks for an SPP directory. If not found then creates an SPP dir. ***checksetupdirs()***
    - Checks for sub dir's in the SPP dir: Day Ahead Market Clearing, Operational Data, Real Time Balancing Market, Real Time Market Data. If any of these sub dir's are not found then it creates them.
  - Gets current date and time data. ***getcurrtime()***
  - Pulls files from SPP and stores them in the related sub dir folder. ***pulllatestcsv(x)***
    - A check is performed prior to pulling the file to ensure it doesn't already exist in a sub dir.

- [DataCalc.py](https://github.com/MoistH2O/SPP_Custom_Trends/blob/master/DataCalc.py)
  - Builds pandas data frames from downloaded .csv files.
  - Manipulates dataframes to create new trend lines.

_Required Modules_:
-
- [os](https://docs.python.org/3/library/os.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [requests](https://requests.readthedocs.io/en/latest/)
- [math](https://docs.python.org/3/library/math.html)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
