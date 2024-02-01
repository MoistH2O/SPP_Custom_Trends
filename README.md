This repository contains code used to interact with the SPP website. Specifically, it grabs .csv files from the marketplace and generates trending displays.

File Descriptions:

Utility.py
This file performs the following actions:
  - Grabs user info to find the document directory in OneDrive
  - Checks for an SPP direcotry. If not found then creates a SPP dir
  -   Checks for sub dir's in the SPP dir: Day Ahead Market Clearing, Operational Data, Real Time Balancing Market, Real Time Market Data. If any of these sub dir's are not found then it creates them.
  - Gets current date and time data.
  - Pulls files from SPP and stores them in the related sub dir folder.
  -   A check is performed prior to pulling the file to ensure it doesn't already exist in a sub dir.

DataCalc.py
  - Currenty a WIP
