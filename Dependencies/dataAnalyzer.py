import numpy as np
import pandas as pd


class DataAnalyzer:
    def dailyProfile(desiredTable):
        powerTitle = "Power (kW)"
        dateTimeTitle = "Date/Time"
   
        # This section creates the dp dataframe used for the graphs.
        whichMonths = desiredTable[dateTimeTitle].dt.month.unique() #This will find out which months are present
        # number_of_months = len(which_months) #How many different months there are

        timeInterval = (desiredTable[dateTimeTitle][1] - desiredTable[dateTimeTitle][0]).total_seconds()/60 # difference between timestamps in minutes
        intervalsPerWeek = int(24*7*(60/timeInterval)) # how many time intervals there are in one week. Used for creating the dp dataframe

        data = []

        for i in whichMonths:
            md = desiredTable[desiredTable[dateTimeTitle].dt.month == i]
            mdt = md[dateTimeTitle]
    
            for t in np.arange(0, intervalsPerWeek):
                time = mdt.iloc[t].time()    
                month = mdt.iloc[t].month
                dyofwk = mdt.iloc[t].weekday() + 1
                kW = np.mean(md[powerTitle].iloc[t::intervalsPerWeek])

                data.append([time, month, dyofwk, kW])
        
        dp = pd.DataFrame(data, columns=['Time', 'Month', 'Day of Week', 'kW'])
        # dp takes the average of the 4 or 5 values of a specific time and day throughout each week.
        # Example: the kW value for 2:15am on a tuesday in January, is the average of all the tuesdays at 2:15am in January
        return dp


    def dailyMaxMin(desiredTable):
        powerTitle = "Power (kW)"
        dateTimeTitle = "Date/Time"
        res = []
        for d in pd.date_range(desiredTable[dateTimeTitle].min().date(), desiredTable[dateTimeTitle].max().date()):
            dd = desiredTable[desiredTable[dateTimeTitle].dt.date == d.date()]
    
            if not dd.empty:
                max_value = dd[powerTitle].max()
                max_time = dd.loc[dd[powerTitle].idxmax(), dateTimeTitle].time()
                min_value = dd[powerTitle].min()
                min_time = dd.loc[dd[powerTitle].idxmin(), dateTimeTitle].time()
                res.append([d, max_value, max_time, min_value, min_time])

        mm = pd.DataFrame(res, columns=['Date', 'MaxValue', 'MaxTime', 'MinValue', 'MinTime'])
        return mm
