import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class Grapher:
    def __init__(self, desiredTable, dailyProfileDF, maxMinDF):
        self.desiredTable = desiredTable
        self.dailyProfileDF = dailyProfileDF
        self.maxMinDF = maxMinDF
        
        self.whichMonths = desiredTable['Date/Time'].dt.month.unique() #This will find out which months are present
        self.monthNum = len(self.whichMonths) #How many different months there are
        self.timeInterval = (desiredTable['Date/Time'][1] - desiredTable['Date/Time'][0]).total_seconds()/60 # difference between timestamps in minutes

        # Graph Formatting
        self.cutoffFactor = 0   #this number is the cutoff factor, 0.0 will give you all the data, 1.0 will give you only the values higher than the mean, 0.5 will only give you values higher than 50% of the mean

        #all the month/day/time titles
        self.mdict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        self.monthTitles = [self.mdict[key] for key in self.whichMonths] + ['']
        self.dailyTitles = np.array(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', ''])
        self.setMonthTitles = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', '']

        #a list of hours of the day so we can label the x ticks
        self.Ip = ['12 am', '1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm', '12 am', '']

        #a way to add commas to axis values in the thousands 
        self.commas = ticker.StrMethodFormatter('{x:,.0f}')

    def graphAll(self):
#        self.Graph_YearlyMaxMin()
        self.Graph_DayOfWeekMaxMin()
        self.Graph_MonthlyKwUsageByTimeOfDay()  
        self.Graph_MonthlyKwUsageByDayOfWeek()
        self.Graph_HistogramOfPeaksByTimeOfDay()
        self.Graph_HistogramOfPeaksByKwValues()
        self.Graph_MonthlyKwPeakProfile()
            
    # def graphYearlyMaxMin(self):
    #     upper = []
    #     lower = []
    #     if np.std(self.maxMinDF['MaxValue']) >= np.std(self.maxMinDF['MinValue']):
    #         for u,l in zip(self.maxMinDF["MaxValue"],self.maxMinDF["MinValue"]):
    #             if u >= np.mean(self.maxMinDF['MaxValue'])*self.cutoffFactor:
    #                 upper.append(u)
    #                 lower.append(l)
    #     else:
    #         for u,l in zip(self.maxMinDF["MaxValue"],self.maxMinDF["MinValue"]):
    #             if l >= np.mean(self.maxMinDF['MinValue'])*self.cutoffFactor:
    #                 upper.append(u)
    #                 lower.append(l)
    #     # -----------------------------------------------
    #     time = np.linspace(0, len(upper), len(upper))                                                   # An array for the x axis
    #     tix = np.linspace(0, len(upper), self.monthNum+1)                                                    # An array for the tickmarks
    #     plt.figure(figsize=(8, 4))

    #     plt.plot(time, upper, '.', color = 'cornflowerblue', markersize = '3', label = 'upper value')   # Plotting markers for the upper and lower values
    #     plt.plot(time, lower, '.', color = 'lightcoral', markersize = '3', label = 'lower value')


    #     # This plots the lines of best fit
    #     #----------------------------------------------------------------
    #     upcoefs = np.polyfit(time, upper, deg = 5)
    #     lowcoefs = np.polyfit(time, lower, deg = 5)

    #     upline = np.polyval(upcoefs, time)
    #     lowline = np.polyval(lowcoefs, time)

    #     plt.plot(time, upline, color = 'tab:blue', linewidth = '2')
    #     plt.plot(time, lowline, color = 'firebrick', linewidth = '2')
    #     #-----------------------------------------------------------------

    #     plt.fill_between(time, upper, upline,color = 'tab:blue', alpha = 0.2)
    #     plt.fill_between(time, lower, lowline, color = 'firebrick', alpha = 0.2)

    #     plt.xlabel('Month', size = 12)                                                                  # X Label
    #     plt.ylabel('Power (kW)', size = 12)                                                             # Y Label
    #     plt.xticks(ticks = tix, visible = False)                                                        # Hiding the x axis ticks
    #     plt.gca().set_xticks(ticks = tix + len(upper)/self.monthNum/2, minor=True)                           # Naming the x ticks and putting them in the middle
    #     plt.gca().set_xticklabels(self.monthTitles, minor=True)
    #     plt.tick_params(axis = 'x', which = 'minor', size = 0)
    #     plt.gca().yaxis.set_major_formatter(self.commas)                                                     # Adding commas to the y axis values
    #     plt.grid()                                                                                      # Grid
    #     plt.savefig('Max_Min_kW_For_The_Year.png')                                                      # Saves a figure into the same folder as this ipynb

    def Graph_YearlyMaxMin(self):
        """
            This method ... .
            
            Args:
                param1 (<type>): The first parameter.
            
            Returns:
                png: <what it returns>
        """
        upper = []
        lower = []
        if np.std(self.maxMinDF['MaxValue']) >= np.std(self.maxMinDF['MinValue']):
            for u,l in zip(self.maxMinDF["MaxValue"],self.maxMinDF["MinValue"]):
                if u >= np.mean(self.maxMinDF['MaxValue'])*self.cutoffFactor:
                    upper.append(u)
                    lower.append(l)
        else:
            for u,l in zip(self.maxMinDF["MaxValue"],self.maxMinDF["MinValue"]):
                if l >= np.mean(self.maxMinDF['MinValue'])*self.cutoffFactor:
                    upper.append(u)
                    lower.append(l)
        # -----------------------------------------------
        

        time = np.linspace(0, len(upper), len(upper))   #an array for the x axis
        tix = np.linspace(0, len(upper), self.monthNum+1)   #an array for the tickmarks

        plt.figure(figsize=(8, 4))

        plt.plot(time, upper, '.', color = 'cornflowerblue', markersize = '3', label = 'upper value') #plotting markers for the upper and lower values
        plt.plot(time, lower, '.', color = 'lightcoral', markersize = '3', label = 'lower value')


        #this plots the lines of best fit
        #----------------------------------------------------------------
        upcoefs = np.polyfit(time, upper, deg = 5)
        lowcoefs = np.polyfit(time, lower, deg = 5)

        upline = np.polyval(upcoefs, time)
        lowline = np.polyval(lowcoefs, time)

        plt.plot(time, upline, color = 'tab:blue', linewidth = '2')
        plt.plot(time, lowline, color = 'firebrick', linewidth = '2')
        #-----------------------------------------------------------------


        plt.fill_between(time, upper, upline,color = 'tab:blue', alpha = 0.2)
        plt.fill_between(time, lower, lowline, color = 'firebrick', alpha = 0.2)

        plt.xlabel('Month', size = 12)                                            #x label
        plt.ylabel('Power (kW)', size = 12)                                       #y label
        plt.xticks(ticks = tix, visible = False)                                  #hiding the x axis ticks
        plt.gca().set_xticks(ticks = tix + len(upper)/self.monthNum/2, minor=True)#, labels = month_titles)   #naming the x ticks and putting them in the middle
        plt.gca().set_xticklabels(self.monthTitles, minor=True)
        plt.tick_params(axis = 'x', which = 'minor', size = 0)
        plt.gca().yaxis.set_major_formatter(self.commas)                    #adding commas to the y axis values
        plt.grid()                                                     #grid

        plt.savefig('Max_Min_kW_For_The_Year.png')     #saves a figure into the same folder as this ipynb

    def Graph_DayOfWeekMaxMin(self):
        self.maxMinDF['dayofweek'] = pd.to_datetime(self.maxMinDF['Date']).dt.dayofweek
        self.maxMinDF = self.maxMinDF.sort_values(['dayofweek', 'Date'])

        #---------------------------------------
        upper = []
        lower = []
        wknd = []
        wkdy = []
        if np.std(self.maxMinDF['MaxValue']) >= np.std(self.maxMinDF['MinValue']):
            for u, l, d in zip(self.maxMinDF['MaxValue'], self.maxMinDF['MinValue'], self.maxMinDF['dayofweek']):
                if d >= 5 or u >= np.mean(self.maxMinDF['MaxValue'])*self.cutoffFactor:
                    upper.append(u)
                    lower.append(l)
                    if d >= 5:
                        wknd.append(u)
                    else:
                        wkdy.append(u)
        else:
            for u, l, d in zip(self.maxMinDF['MaxValue'], self.maxMinDF['MinValue'], self.maxMinDF['dayofweek']):
                if l >= np.mean(self.maxMinDF['MinValue'])*self.cutoffFactor:
                    upper.append(u)
                    lower.append(l)
                    if d >= 5:
                        wknd.append(u)
                    else:
                        wkdy.append(u)
        #---------------------------------------

        time = np.linspace(0, len(upper), len(upper))
        wkdy_time = np.linspace(0, len(wkdy), len(wkdy))
        wknd_time = np.linspace(0, len(wknd), len(wknd))

        tix = np.linspace(0, len(upper), 8)

        wknd_coefs = np.polyfit(wknd_time, wknd, deg = 3)
        wkdy_coefs = np.polyfit(wkdy_time, wkdy, deg = 4)
        lowcoefs = np.polyfit(time, lower, deg = 5)

        wknd_mean = np.polyval(wknd_coefs, wknd_time)
        wkdy_mean = np.polyval(wkdy_coefs, wkdy_time)
        lmean = np.polyval(lowcoefs, time)

        wknd_time = wknd_time + np.max(wkdy_time)

        plt.figure(figsize=(8, 4))

        plt.plot(wknd_time, wknd_mean, color = 'tab:blue', linewidth = '2')
        plt.plot(wkdy_time, wkdy_mean, color = 'tab:blue', linewidth = '2')
        plt.plot(time, lmean, color = 'firebrick', linewidth = '2')

        plt.plot([wkdy_time[-1], wknd_time[0]], [wkdy_mean[-1], wknd_mean[0]], '--', color='tab:blue')

        plt.fill_between(wkdy_time, upper[:len(wkdy)], wkdy_mean, color = 'tab:blue', alpha = 0.2)
        plt.fill_between(wknd_time, upper[len(wkdy):], wknd_mean, color = 'tab:blue', alpha = 0.2)
        plt.fill_between(time, lower, lmean, color = 'firebrick', alpha = 0.2)

        plt.plot(time, upper, '.', color = 'cornflowerblue', markersize = '3', label = 'upper value') 
        plt.plot(time, lower, '.', color = 'lightcoral', markersize = '3', label = 'lower value', zorder = 0)

        plt.xticks(ticks = tix, labels = self.dailyTitles, visible = False)
        plt.gca().set_xticks(ticks = tix + len(upper)/14, minor = True)
        plt.gca().set_xticklabels(self.dailyTitles, minor=True)
        plt.tick_params(axis = 'x', which = 'minor', size = 0) #test comment

        plt.ylabel('Power (kW)', size = 12)
        plt.xlabel('Day of Week', size = 12)
        plt.gca().yaxis.set_major_formatter(self.commas)
        plt.grid()

        plt.savefig('Max_Min_kW_By_Day_of_Week.png')

    def Graph_MonthlyKwUsageByTimeOfDay(self):
        day_of_week = []
        time = []
        kW = []
        month = []
        for d, t, k, m in zip(self.dailyProfileDF['Day of Week'], self.dailyProfileDF['Time'], self.dailyProfileDF['kW'], self.dailyProfileDF['Month']):
            if d == 6 or d == 7:
                day_of_week.append(d)
                time.append(t)
                kW.append(k)
                month.append(m)

        wknd = pd.DataFrame()
        wknd['day_of_week'] = day_of_week
        wknd['time'] = time
        wknd['kW'] = kW
        wknd['month'] = month


        day_of_week = []
        time = []
        kW = []
        month = []
        for d, t, k, m in zip(self.dailyProfileDF['Day of Week'], self.dailyProfileDF['Time'], self.dailyProfileDF['kW'], self.dailyProfileDF['Month']):
            if d != 6 and d != 7:
                day_of_week.append(d)
                time.append(t)
                kW.append(k)
                month.append(m)

        wkdy = pd.DataFrame()
        wkdy['day_of_week'] = day_of_week
        wkdy['time'] = time
        wkdy['kW'] = kW
        wkdy['month'] = month

        wkdy = wkdy.sort_values(['month', 'time'])
        wknd = wknd.sort_values(['month', 'time'])
        #----------------------------------------------------------------------------

        fig, axes = plt.subplots(nrows = 3, ncols = 4, figsize = (10, 6))   #creating 12 subplots
        plt.subplots_adjust(wspace=0.5, hspace=1.0)                         #spacing out the subplots

        for i, ax in enumerate(axes.flatten()):
            subset_wkdy = wkdy[wkdy['month'] == i + 1]    #separating the data frames into months
            subset_wknd = wknd[wknd['month'] == i + 1]      

            ax.plot(np.linspace(0, 24, len(subset_wknd)), (subset_wknd['kW']), ',', color = 'firebrick', label = 'weekend')
            ax.plot(np.linspace(0, 24, len(subset_wkdy)), (subset_wkdy['kW']), ',', color = 'tab:blue', label = 'weekday')     #plotting data


            ax.set_xticks(ticks = np.linspace(0, 24, 5))  #x axis goes from 0 to 24, with 5 tickmarks
            ax.set_xticklabels(self.Ip[::6],  rotation = 45)
            ax.set_yticks(ticks = np.linspace(0, np.ceil(np.max(self.dailyProfileDF['kW'])/100)*100 + 100, 5))   #y axis goes from 0 to the max(rounded up to the next hundred) with 5 tickmarks
            ax.set_title(self.setMonthTitles[i])          #naming the subplots 
            ax.tick_params(labelsize = 8)          #making the font size for the axis smaller
            if i % 4 == 0:                         #check if it's the leftmost subplot in each row
                ax.set_ylabel('Power (kW)', size = 10)                #y-axis label for the leftmost subplot
            ax.grid()                              #grid
            ax.yaxis.set_major_formatter(self.commas)   #add commas to the y axis
    
    
        legend_handles = [plt.Line2D([], [], marker='s', markersize=4, linestyle='None', label='Weekday', color = 'tab:blue'),
                          plt.Line2D([], [], marker='s', markersize=4, linestyle='None', label='Weekend', color = 'firebrick')]

        fig.legend(handles=legend_handles)

        plt.savefig('Monthly_kW_by_Time_of_Day.png')     #saves a figure into the same folder as this ipynb

    def Graph_MonthlyKwUsageByDayOfWeek(self):
        self.dailyProfileDF = self.dailyProfileDF.sort_values(['Month', 'Day of Week'])   #sorting the entire dataframe by month and then day of the week
        self.dailyProfileDF['x'] = np.arange(len(self.dailyProfileDF))                    #creating a new column that assigns a number to each row in this new order

        fig, axes = plt.subplots(nrows = 6, ncols = 2, figsize=(10, 12))  #creating 12 subplots
        plt.subplots_adjust(top = .925, wspace=0.25, hspace=1)            #spacing out the subplots



        for i, ax, in enumerate(axes.flatten()):
            subset = self.dailyProfileDF[self.dailyProfileDF['Month'] == i + 1]        #splitting the data into 12 subsets
            ax.plot(subset['x'], subset['kW'], '-', color = 'tab:blue')   #plotting each subset into it's respective subplot


            tix = np.linspace(np.min(subset['x']), np.max(subset['x']), 8)
            middle_tix = tix + len(subset['x'])/14

            ax.set_yticks(ticks = np.linspace(0, np.ceil(np.max(self.dailyProfileDF['kW'])/100)*100+100, 5))  #y axis goes from 0 to the max(rounded up to the next hundred) with 5 tickmarks
            ax.set_xticks(ticks = tix)
            ax.set_xticklabels(self.dailyTitles, visible = False)
            ax.set_xticks(ticks = middle_tix, minor = True)
            ax.set_xticklabels(self.dailyTitles, size = 8, minor=True)
            ax.tick_params(axis = 'x', which = 'minor', size = 0)
            ax.tick_params(labelsize = 8)

            ax.set_title(self.setMonthTitles[i])             #naming subplots
            if i % 2 == 0:                            #Check if it's the leftmost subplot in each row
                ax.set_ylabel('Power (kW)', size = 10)                   #y-axis label for the leftmost subplot
            ax.yaxis.set_major_formatter(self.commas)      #add commas to the y axis
            ax.grid() 
    
        plt.savefig('Monthly_kW_by_Day_of_Week.png')   #saves a figure into the same folder as this ipynb

    def Graph_HistogramOfPeaksByTimeOfDay(self):
        #-----------------------------------------------
        MaxTime = []
        for u,t in zip(self.maxMinDF["MaxValue"],self.maxMinDF["MaxTime"]):
            if u >= np.mean(self.maxMinDF['MaxValue'])*self.cutoffFactor:
                MaxTime.append(t)
        #-----------------------------------------------

        hours = [time.hour for time in MaxTime]
        tix = np.linspace(0, 23, 13)

        plt.figure(figsize=(8, 4))
        plt.hist(hours, bins = 24, range = (0, 23), rwidth = 0.8, color = 'tab:blue')
        plt.gca().set_axisbelow(True)
        plt.grid(axis = 'y')

        plt.xticks(ticks = tix, labels = self.Ip[::2], rotation = 40, size = 10)
        plt.xlabel('Time of Day', size = 12)
        plt.ylabel('Frequency of Peaks', size = 12)

        plt.savefig('Peak_Frequency_by_Time_of_Day.png')

    def Graph_HistogramOfPeaksByKwValues(self):
        #if you want to exclude days that have an upper kW output less than the mean * cutoff_factor, then run this section of code
        #-----------------------------------------------
        MaxValue = []
        for u in self.maxMinDF["MaxValue"]:
            if u >= np.mean(self.maxMinDF['MaxValue'])*self.cutoffFactor:
                MaxValue.append(u)
        # -----------------------------------------------

        high = np.ceil(np.max(MaxValue)/1000)*1000

        plt.figure(figsize=(8, 4))
        plt.hist(MaxValue, bins = int(high/100), rwidth = 0.8, range = (0, high), color = 'firebrick')

        plt.gca().xaxis.set_major_formatter(self.commas)
        plt.gca().set_axisbelow(True)
        plt.grid(axis = 'y')
        plt.tick_params(axis = 'both', direction = 'inout')
        plt.ylabel('Frequency of Peak Value', size = 12)
        plt.xlabel('Peak kW', size = 12)

        plt.savefig('Peak_Frequency_by_Peak_Value.png')

    def Graph_MonthlyKwPeakProfile(self):
        rng = 60/self.timeInterval*3 #amount of datapoints for 3 hours before/after the max

        fig, axes = plt.subplots(nrows = 4, ncols = 3, figsize=(10, 8))  #creating 12 subplots
        plt.subplots_adjust(wspace=0.6, hspace=1.0) 

        lower = []
        n = 0
        for i, ax in zip(self.whichMonths, axes.flatten()):
            idxmax = self.desiredTable.loc[self.desiredTable['Date/Time'].dt.month == i,  'Power (kW)'].idxmax()
            subset = self.desiredTable.loc[idxmax-rng:idxmax+rng]
            high = subset['Power (kW)'].max()
            low = subset['Power (kW)'].min()
            lower.append(low) 

            tix = subset['Date/Time'].dt.strftime('%I:%M %p')
            title = subset['Date/Time'].dt.strftime('%b %d')
    
            ax.plot(tix, subset['Power (kW)'])
            ax.plot(rng, high, '.', color = 'firebrick')
            ax.annotate(f'{int(high):,}', xy=(rng, high), xytext=(74, -2.5), textcoords='offset points', arrowprops=dict(arrowstyle='-', color = 'firebrick'), color = 'firebrick', size = 8)

            ax.set_xticks(tix[::int(60/self.timeInterval)])
            ax.set_yticks(ticks = np.linspace(np.floor(np.min(lower)/100-1)*100, np.ceil(np.max(self.desiredTable['Power (kW)'])/100+1)*100, 3))   #y axis goes from 0 to the max(rounded up to the next hundred) with 5 tickmarks
            ax.set_title(title.max())          #naming the subplots 
            ax.tick_params(axis = 'x', labelsize = 6, rotation = 55)          #making the font size for the axis smaller

            if (n) % 3 == 0:                         #check if it's the leftmost subplot in each row
                ax.set_ylabel('Power (kW)', size = 10)                #y-axis label for the leftmost subplot
            ax.grid()                              #grid
            ax.yaxis.set_major_formatter(self.commas)   #add commas to the y axis
            n += 1
    
        plt.savefig('Monthly_Peak_Profile.png')
