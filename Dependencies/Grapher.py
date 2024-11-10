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


        """
        Note: When Thomas and I presented this, I received some feedback to fix the y axis bounds, 
        and to involve a rolling average line instead of a line of best fit. I updated my code in 
        Jupyter notebook, but not in here. I'm not sure what I need to do to transpose the code I wrote
        in Jupyter to make it work in Visual Studio. 
              
        I updated the section below with 'rolling average window'
        """
        # Miscellaneous parameters
        self.cutoffFactor = 0   #this number is the cutoff factor, 0.0 will give you all the data, 1.0 will give you only the values higher than the mean, 0.5 will only give you values higher than 50% of the mean
        self.window = 10        # sets how many points of data the rolling average is based off of
        self.magnitude = 10**np.floor(np.log10(np.mean(dailyProfileDF['kW'])))      #will decide the magnitude of the data based on the mean. Outputs 1, 10, 100, 1000, etc.
        self.ylow = np.floor(np.min(dailyProfileDF['kW'])/self.magnitude)*self.magnitude      #creates high and low bounds for the y axis based on the magnitude of the data
        self.yhigh = np.ceil(np.max(dailyProfileDF['kW'])/self.magnitude)*self.magnitude


        #all the month/day/time titles
        self.mdict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        self.monthTitles = [self.mdict[key] for key in self.whichMonths] + ['']
        self.dailyTitles = np.array(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', ''])
        self.setMonthTitles = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', '']

        #a list of hours of the day so we can label the x ticks
        self.Ip = ['12 am', '1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm', '12 am', '']

        #a way to add commas to axis values in the thousands 
        self.commas = ticker.StrMethodFormatter('{x:,.0f}')
        
        #choosing the colors for the graphs
        self.main_color1 = 'tab:blue'
        self.main_color2 = 'cornflowerblue'
        self.second_color1 = 'firebrick'
        self.second_color2 = 'lightcoral'

    def graphAll(self):
#        self.Graph_YearlyMaxMin()
        self.Graph_DayOfWeekMaxMin()
        self.Graph_MonthlyKwUsageByTimeOfDay()  
        self.Graph_MonthlyKwUsageByDayOfWeek()
        self.Graph_HistogramOfPeaksByTimeOfDay()
        self.Graph_HistogramOfPeaksByKwValues()
        self.Graph_MonthlyKwPeakProfile()
        

        #DUPLICATED CODE
    """      
      #THIS AREA OF CODE WAS DUPLICATED, NOT SURE WHY. KEEPING IT HERE JUST IN CASE
      
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

    #     plt.plot(time, upper, '.', color = self.main_color2, markersize = '3', label = 'upper value')   # Plotting markers for the upper and lower values
    #     plt.plot(time, lower, '.', color = self.second_color2, markersize = '3', label = 'lower value')


    #     # This plots the lines of best fit
    #     #----------------------------------------------------------------
    #     upcoefs = np.polyfit(time, upper, deg = 5)
    #     lowcoefs = np.polyfit(time, lower, deg = 5)

    #     upline = np.polyval(upcoefs, time)
    #     lowline = np.polyval(lowcoefs, time)

    #     plt.plot(time, upline, color = self.main_color1, linewidth = '2')
    #     plt.plot(time, lowline, color = 'firebrick', linewidth = '2')
    #     #-----------------------------------------------------------------

    #     plt.fill_between(time, upper, upline,color = self.main_color1, alpha = 0.2)
    #     plt.fill_between(time, lower, lowline, color = 'self.second_color1', alpha = 0.2)

    #     plt.xlabel('Month', size = 12)                                                                  # X Label
    #     plt.ylabel('Power (kW)', size = 12)                                                             # Y Label
    #     plt.xticks(ticks = tix, visible = False)                                                        # Hiding the x axis ticks
    #     plt.gca().set_xticks(ticks = tix + len(upper)/self.monthNum/2, minor=True)                           # Naming the x ticks and putting them in the middle
    #     plt.gca().set_xticklabels(self.monthTitles, minor=True)
    #     plt.tick_params(axis = 'x', which = 'minor', size = 0)
    #     plt.gca().yaxis.set_major_formatter(self.commas)                                                     # Adding commas to the y axis values
    #     plt.grid()                                                                                      # Grid
    #     plt.savefig('Max_Min_kW_For_The_Year.png')                                                      # Saves a figure into the same folder as this ipynb
    """
    
    def Graph_YearlyMaxMin(self):
        """
            This method creates a graph that shows the max/min throughout the year. The x axis has 
            each day throughout the course of a year, labeled by month. The y axis has the max and 
            min kW value for each day, and there is a rolling average line for both the max and the min
            
            Args:
                self (<Grapher>): itself
            
            Returns:
                png: returns the graph as a png image
        """
        

        """
        The area below will select which set (MaxValue or MinValue) has a higher 
        standard deviation. Then it will plot the data based on which one has the higher 
        std, this is because of the cutoff factor. If the cutoff factor is active, then 
        the upper/lower arrays will be created based on the one with more outliers
        """
        #---------------------------------------------
        #EXCLUDING OUTLIERS
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
        #PLOTTING ACTUAL VALUES

        time = np.linspace(0, len(upper), len(upper))   #an array for the x axis
        tix = np.linspace(0, len(upper), self.monthNum+1)   #an array for the tickmarks

        plt.figure(figsize=(8, 4))

        plt.plot(time, upper, '.', color = self.main_color2, markersize = '3', label = 'upper value') #plotting markers for the upper and lower values
        plt.plot(time, lower, '.', color = self.second_color2, markersize = '3', label = 'lower value')


        
        #----------------------------------------------------------------
        #ROLLING AVERAGE    

        upline = np.convolve(upper, np.ones(self.window)/self.window, mode = 'valid')            # this line creates the rolling average line, but it is missing the first 10 data points 
        upline = np.concatenate(( [np.mean(upper[:self.window-1])] * (self.window-1), upline))    # to fill the first 10 data points, just take the average of the first 10 points and concatenate it to the beginning of the rolling average line

        lowline = np.convolve(lower, np.ones(self.window)/self.window, mode = 'valid')             #same thing for the lower line
        lowline = np.concatenate(([np.mean(lower[:self.window-1])] * (self.window-1), lowline))

        plt.plot(time, upline, color = self.main_color1, linewidth = '2')                      # this plots the rolling average lines
        plt.plot(time, lowline, color = self.second_color1, linewidth = '2')

        #-----------------------------------------------------------------
        #MAKING GRAPH LOOK PRETTY

        plt.fill_between(time, upper, upline,color = self.main_color1, alpha = 0.2)       #coloring in the area between the rolling average line and datapoints
        plt.fill_between(time, lower, lowline, color = self.second_color1, alpha = 0.2)

        plt.xlabel('Month', size = 12)                                            #x label
        plt.ylabel('Power (kW)', size = 12)                                       #y label
        plt.xticks(ticks = tix, visible = False)                                  #hiding the x axis ticks
        plt.gca().set_xticks(ticks = tix + len(upper)/self.monthNum/2, minor=True)#, labels = month_titles)   #naming the x ticks and putting them in the middle
        plt.gca().set_xticklabels(self.monthTitles, minor=True)
        plt.tick_params(axis = 'x', which = 'minor', size = 0)
        plt.gca().yaxis.set_major_formatter(self.commas)                    #adding commas to the y axis values
        plt.grid()                                                     #grid

        plt.savefig('Max_Min_kW_For_The_Year.png')      #saves the figure into the same folder as this code

    def Graph_DayOfWeekMaxMin(self):
        """
            This method creates a graph that shows the max/min throughout a week. 
            Plots each max/min value that happened for each day. 
            For example: It will look at every tuesday in the year and plot the max/min kw for each of those Tuesdays.
            It does this for each day of the week. There is also a rolling average line.
            
            Args:
                self (<Grapher>): itself
            
            Returns:
                png: returns the graph as a png image
        """
        self.maxMinDF['dayofweek'] = pd.to_datetime(self.maxMinDF['Date']).dt.dayofweek  #creates a new column in the dataframe for what day of the week it is
        self.maxMinDF = self.maxMinDF.sort_values(['dayofweek', 'Date'])                 #sorts the dataframe by 1: day of week, and 2: date

        """
        The area below will select which set (MaxValue or MinValue) has a higher standard deviation. 
        Then it will plot the data based on which one has the higher std, this is because of the cutoff factor. 
        If the cutoff factor is active, then I want to create the upper/lower based on the one with more outliers
        """
        #--------------------------------------
        #EXCLUDING OUTLIERS
        upper = []
        lower = []

        if np.std(self.maxMinDF['MaxValue']) >= np.std(self.maxMinDF['MinValue']):             #the if and else will select which set (MaxValue or MinValue) has a higher standard deviation. Then it will plot the data based on which one has the higher std, this is because of the cutoff factor. If the cutoff factor is active, then I want to create the upper/lower based on the one with more outliers
            for u,l in zip(self.maxMinDF["MaxValue"],self.maxMinDF["MinValue"]):              #this goes through the data sets and find the min/max value and puts them in a new array named upper / lower
                if u >= np.mean(self.maxMinDF['MaxValue'])*self.cutoff_factor:
                    upper.append(u)
                    lower.append(l)
        else:
            for u,l in zip(self.maxMinDF["MaxValue"],self.maxMinDF["MinValue"]):
                if l >= np.mean(self.maxMinDF['MinValue'])*self.cutoff_factor:
                    upper.append(u)
                    lower.append(l)

        #--------------------------------------         
        #PLOTTING ACTUAL VALUES 

        plt.figure(figsize=(8, 4))
        time = np.linspace(0, len(upper), len(upper))          #creates the x axis
        tix = np.linspace(0, len(upper), 8)                    #creates spaces on the x axis to label it by days of the week

        plt.plot(time, upper, '.', color = self.main_color2, markersize = '3', label = 'upper value')               #plots the x and y values
        plt.plot(time, lower, '.', color = self.second_color2, markersize = '3', label = 'lower value', zorder = 0)

        #----------------------------------------------
        #ROLLING AVERAGE LINE

        upline = np.convolve(upper, np.ones(self.window)/self.window, mode = 'valid')            # this line creates the rolling average line data, but it is missing the first 20 data points
        upline = np.concatenate(( [np.mean(upper[:self.window-1])] * (self.window-1), upline))    # to fill the first 20 data points, I just take the average of the first points and concatenate it to the beginning of the rolling average data set

        lowline = np.convolve(lower, np.ones(self.window)/self.window, mode = 'valid')             #same thing for the lower line
        lowline = np.concatenate(([np.mean(lower[:self.window-1])] * (self.window-1), lowline))

        plt.plot(time, upline, color = self.main_color1, linewidth = '2')                      #plots the lines on the graph
        plt.plot(time, lowline, color = self.second_color1, linewidth = '2')
        #---------------------------------------
        #MAKING GRAPH LOOK PRETTY

        plt.fill_between(time, upper, upline, color = self.main_color1, alpha = 0.1)            #creats a transparent filler region between the rolling average line and actual data points
        plt.fill_between(time, lower, lowline, color = self.second_color1, alpha = 0.1)
        
        plt.xticks(ticks = tix, labels = self.dailyTitles, visible = False)             #says there are 8 tick marks on the x axis, and it hides the labels because their labels are numbers and we dont want that
        plt.gca().set_xticks(ticks = tix + len(upper)/14, minor = True)                 # creates minor tick marks in the middle of each major tick mark.
        plt.gca().set_xticklabels(self.dailyTitles, minor=True)                         # labels each minor tick mark by the day of the week
        plt.tick_params(axis = 'x', which = 'minor', size = 0)                          # makes the minor tick marks invisible by shrinking them to oblivion

        plt.ylabel('Power (kW)', size = 12)                                         # y axis title and font
        plt.xlabel('Day of Week', size = 12)                                        # x axis title and font
        plt.gca().yaxis.set_major_formatter(self.commas)                                 # creates commas for numbers in the y axis
        plt.grid()
        
        plt.savefig('Max_Min_kW_By_Day_of_Week.png')

    def Graph_MonthlyKwUsageByTimeOfDay(self):
        """
            This method creates a graph for each month that is in the data provided. 
            Each graph shows the kW profile for each day of the week in that month, blue is weekdays and red is weekends
            X axis is by time, 00:00 to 23:59
            
            Args:
                self (<Grapher>): itself
            
            Returns:
                png: returns the graph as a png image
        """

        #------------------------------------------------
        #CREATING DATAFRAMES FOR THE WEEKENDS AND WEEKDAYS
        
        day_of_week = []
        time = []
        kW = []
        month = []
        for d, t, k, m in zip(self.dailyProfileDF['Day of Week'], self.dailyProfileDF['Time'], self.dailyProfileDF['kW'], self.dailyProfileDF['Month']):  #creates dataframe for weekends
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
        for d, t, k, m in zip(self.dailyProfileDF['Day of Week'], self.dailyProfileDF['Time'], self.dailyProfileDF['kW'], self.dailyProfileDF['Month']):  #creates dataframe for weekdays
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

        wkdy = wkdy.sort_values(['month', 'time'])   #sorting the new dataframes by month, and then by time of day
        wknd = wknd.sort_values(['month', 'time'])
        #----------------------------------------------------------------------------
        #PLOTTING DATA

        fig, axes = plt.subplots(nrows = 3, ncols = 4, figsize = (10, 6))   #creating 12 subplots
        plt.subplots_adjust(wspace=0.5, hspace=1.0)                         #spacing out the subplots

        for i, ax in enumerate(axes.flatten()):
            subset_wkdy = wkdy[wkdy['month'] == i + 1]    #separating the data frames into months
            subset_wknd = wknd[wknd['month'] == i + 1]      

            ax.plot(np.linspace(0, 24, len(subset_wknd)), (subset_wknd['kW']), ',', color = self.second_color1, label = 'weekend')
            ax.plot(np.linspace(0, 24, len(subset_wkdy)), (subset_wkdy['kW']), ',', color = self.main_color1, label = 'weekday')     #plotting data


            ax.set_xticks(ticks = np.linspace(0, 24, 5))  #x axis goes from 0 to 24, with 5 tickmarks
            ax.set_xticklabels(self.Ip[::6],  rotation = 45)
            ax.set_yticks(ticks = np.linspace(self.ylow, self.yhigh, 5)) # sets the bounds of the y axis, ylow & yhigh were determined earlier in "miscellaneous parameters"         
            ax.set_title(self.setMonthTitles[i])          #naming the subplots 
            ax.tick_params(labelsize = 8)          #making the font size for the axis smaller
            if i % 4 == 0:                         #check if it's the leftmost subplot in each row
                ax.set_ylabel('Power (kW)', size = 10)                #y-axis label for the leftmost subplot
            ax.grid()                              #grid
            ax.yaxis.set_major_formatter(self.commas)   #add commas to the y axis
    
    
        legend_handles = [plt.Line2D([], [], marker='s', markersize=4, linestyle='None', label='Weekday', color = self.main_color1),
                          plt.Line2D([], [], marker='s', markersize=4, linestyle='None', label='Weekend', color = self.second_color1)]     #this part lets you modify the legend, it is set to having squares as the markers.

        fig.legend(handles=legend_handles)

        plt.savefig('Monthly_kW_by_Time_of_Day.png')     #saves a figure into the same folder as this code

    def Graph_MonthlyKwUsageByDayOfWeek(self):
         
        """
            This method creates a 12 graphs that shows the kW usage throughout the month, sorted by the days of the week.
            X axis is each day of the week. Example: it takes all of the 15-min kW values from each Tuesday for the whole month and plots it,
            And it does that for each day of the week, for each month.
            
            Args:
                self (<Grapher>): itself
            
            Returns:
                png: returns the graph as a png image
       """
        self.dailyProfileDF = self.dailyProfileDF.sort_values(['Month', 'Day of Week'])   #sorting the entire dataframe by month and then day of the week
        self.dailyProfileDF['x'] = np.arange(len(self.dailyProfileDF))                    #creating a new column that assigns a number to each row in this new order

        fig, axes = plt.subplots(nrows = 6, ncols = 2, figsize=(10, 12))  #creating 12 subplots
        plt.subplots_adjust(top = .925, wspace=0.25, hspace=1)            #spacing out the subplots



        for i, ax, in enumerate(axes.flatten()):
            subset = self.dailyProfileDF[self.dailyProfileDF['Month'] == i + 1]        #splitting the data into 12 subsets
            ax.plot(subset['x'], subset['kW'], '-', color = self.main_color1)   #plotting each subset into it's respective subplot


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
        """
            This method creates a histogram that shows at what time of day the kW peaks are happening.
            
            Args:
                self (<Grapher>): itself
            
            Returns:
                png: returns the graph as a png image
        """
        #-----------------------------------------------
        #EXCLUDING OUTLIERS
        MaxTime = []
        for u,t in zip(self.maxMinDF["MaxValue"],self.maxMinDF["MaxTime"]):     #if you want to exclude days that have an upper kW output less than the mean * cutoff_factor, then run this section of code
            if u >= np.mean(self.maxMinDF['MaxValue'])*self.cutoffFactor:
                MaxTime.append(t)
        #-----------------------------------------------
        #PLOTTING THE DATA
        hours = [time.hour for time in MaxTime]     #creating a list of what times the max kW peak for each day is happening
        
        plt.figure(figsize=(8, 4))
        plt.hist(hours, bins = 24, range = (0, 23), rwidth = 0.8, color = self.main_color1)  #plotting the data
        
        #----------------------------------------------
        #MAKING IT LOOK PRETTY

        plt.gca().set_axisbelow(True)                                        #required to run below formatting code
        plt.grid(axis = 'y')                                                 #setting only horizontal grid lines
        tix = np.linspace(0, 23, 13)                                              #setting up tickmarks on the x axis
        plt.xticks(ticks = tix, labels = self.Ip[::2], rotation = 40, size = 10)  #formatting the time values on the x axis
        plt.xlabel('Time of Day', size = 12)                                      #labeling x and y axis
        plt.ylabel('Frequency of Peaks', size = 12)

        plt.savefig('Peak_Frequency_by_Time_of_Day.png')

    def Graph_HistogramOfPeaksByKwValues(self):
        """
            This method creates a histogram that how frequent certain peak values are.
            Example: 100 days of the year the peak kW was between 0-10, 150 days of the year the peak kW was between 40-50, etc.
            
            Args:
                self (<Grapher>): itself
            
            Returns:
                png: returns the graph as a png image
        """
        #if you want to exclude days that have an upper kW output less than the mean * cutoff_factor, then run this section of code
        #-----------------------------------------------
        #EXCLUDING OUTLIERS
        MaxValue = []
        for u in self.maxMinDF["MaxValue"]:
            if u >= np.mean(self.maxMinDF['MaxValue'])*self.cutoffFactor:
                MaxValue.append(u)
        # -----------------------------------------------
        #PLOTTING THE DATA

        mag = 10**np.floor(np.log10(np.mean(MaxValue) )) #finds the magnitude of the peak values

        high_peak = np.ceil(np.max(MaxValue)/mag)*mag   #finds what the upper bound will be depending on the highest peak value
        low_peak = np.floor(np.min(MaxValue)/mag)*mag   #finds what the lower bound will be depending on the lowest peak value

        plt.figure(figsize=(8, 4))
        plt.hist(MaxValue, bins = int(high_peak/mag), rwidth = 0.8, range = (low_peak, high_peak), color = self.second_color1)
        #-------------------------------------------------
        #MAKING IT PRETTY

        plt.gca().xaxis.set_major_formatter(self.commas)
        plt.gca().set_axisbelow(True)
        plt.grid(axis = 'y')
        plt.tick_params(axis = 'both', direction = 'inout')
        plt.ylabel('Frequency of Peak Value', size = 12)
        plt.xlabel('Peak kW', size = 12)

        plt.savefig('Peak_Frequency_by_Peak_Value.png')

    def Graph_MonthlyKwPeakProfile(self):
        """
            This method creates a graph that shows the demand profile 3 hours before and after the peak value for each month.
            This allows us to see if the facility has a constant process, of if it was a fluke if there was a random spike.
            
            Args:
                self (<Grapher>): itself
            
            Returns:
                png: returns the graph as a png image
        """
        rng = 60/self.timeInterval*3 #amount of datapoints for 3 hours before/after the max

        fig, axes = plt.subplots(nrows = 4, ncols = 3, figsize=(10, 8))  #creating 12 subplots
        plt.subplots_adjust(wspace=0.6, hspace=1.0)                      #spacing the subplots

        lower = []                #empty list, and creating a counter 'n'
        n = 0
        for i, ax in zip(self.whichMonths, axes.flatten()):                                                       #this runs through each month
            idxmax = self.desiredTable.loc[self.desiredTable['Date/Time'].dt.month == i,  'Power (kW)'].idxmax()  #idxmax is looking at all the data points in the month, and finding the location of max kW
            subset = self.desiredTable.loc[idxmax-rng:idxmax+rng]                                                 #subset is the actual set of datapoints before/after the max
            high = subset['Power (kW)'].max()                                  #the value of the max
            low = subset['Power (kW)'].min()                                   #the value of the min, within 3 hours before/after the max
            lower.append(low)                                                  #saving the low values for each month into a list

            tix = subset['Date/Time'].dt.strftime('%I:%M %p')            #formats the time on the x axis
            title = subset['Date/Time'].dt.strftime('%b %d')             #formats the title of each subplot
    
    
            ax.plot(tix, subset['Power (kW)'])                       #actually plots the subplot
            ax.plot(rng, high, '.', color = self.second_color1)       #creates a point where the peak happened
            ax.annotate(f'{int(high):,}', xy=(rng, high), xytext=(74, -2.5), textcoords='offset points', arrowprops=dict(arrowstyle='-', color = self.second_color1), color = self.second_color1, size = 8)   #creates an arrow pointing to the peak point and labels it with the peak value

            ax.set_xticks(tix[::int(60/self.timeInterval)])
            ax.set_yticks(ticks = np.linspace(self.ylow, self.yhigh, 3))   # sets the bounds of the y axis, ylow & yhigh were determined earlier based on the magnitude of the dataset
            ax.set_title(title.max())                                       #naming the subplots 
            ax.tick_params(axis = 'x', labelsize = 6, rotation = 55)          #making the font size for the axis smaller

            if (n) % 3 == 0:                                          #check if it's the leftmost subplot in each row
                ax.set_ylabel('Power (kW)', size = 10)                #y-axis label for the leftmost subplot
            ax.grid()                                                 #grid
            ax.yaxis.set_major_formatter(self.commas)                 #add commas to the y axis
            n += 1
    
        plt.savefig('Monthly_Peak_Profile.png')
