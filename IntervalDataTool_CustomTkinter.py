import customtkinter as tk
from tkinter import filedialog
import pandas as pd
from pandastable import Table
from PIL import Image
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from datetime import datetime, timedelta

# (All font types here = https://stackoverflow.com/questions/39614027/list-available-font-families-in-tkinter)

## Global Variables for function access
global df
global table
global desired_table
global Entry_StartRowNum
global Entry_EndRowNum
global Frame_UploadPage
global Frame_TitlePage
global counter
global columnSelectorButton
global CheckCombinedDateTime
global Entry_DateFormat_One
global Entry_DateFormat_Two
global Entry_DateFormat_Three


# Table used to calculate profiles and graphing
desired_table = pd.DataFrame()

# Counter used for number of columns selected (DONT DELETE)
counter = 1

## This function opens file explorer for the user to
## select the desired excel file to be opened.
def open_file(labels_row, end_row):
    global df
    global table
    global Frame_UploadPage
    global columnSelectorButton
    file_path = filedialog.askopenfilename(
        filetypes=[("XLSX Files", "*.xlsx"), ("CSV Files", "*.csv")]
    )

    if file_path.endswith(".csv"):
        # Convert CSV to Excel
        excel_file_path = os.path.splitext(file_path)[0] + ".xlsx"
        data_frame = pd.read_csv(file_path)
        data_frame.to_excel(excel_file_path, index=False)
        file_path = excel_file_path  # Update file_path with the Excel file path

    if file_path:
        # Remove last widget
        Frame_UploadPage.grid_remove()

        # Read the Excel file using pandas
        df = pd.read_excel(
            file_path,
            sheet_name=0,
            skiprows=lambda x: x < labels_row - 1,
            nrows=end_row - labels_row,
        )

        # Create GUI for Table column selection
        Frame_ColumnSelectorTitle = tk.CTkFrame(app)
        Frame_ColumnSelectorTitle.grid(row=0, column=2, padx=20, pady=(50, 0))

        # Frame for Title
        Label_Title = tk.CTkLabel(Frame_ColumnSelectorTitle, text="Column Selection")
        Label_Title.configure(
            font=("Eras Bold ITC", 40), anchor="center", padx=20, pady=20
        )
        Label_Title.grid(row=0, column=2)

        # Frame for the Table
        Frame_Table = tk.CTkFrame(app)
        Frame_Table.grid(row=1, column=2, padx=20, pady=(50, 0))

        # Create table
        table = Table(Frame_Table, dataframe=df)
        table.show()

        Frame_ColumnSelectorButtons = tk.CTkFrame(app)
        Frame_ColumnSelectorButtons.grid(row=2, column=2, padx=20, pady=(50, 0))

        # Check wether the checkbox was selected or not
        if CheckCombinedDateTime.get() == "off":
            ColumnSelectionButton = tk.CTkButton(
                Frame_ColumnSelectorButtons,
                text="Select Date Column",
                command=retrieve_3_columns,
            )
        else:
            ColumnSelectionButton = tk.CTkButton(
                Frame_ColumnSelectorButtons,
                text="Select Date/Time Column",
                command=retrieve_2_columns,
            )

        ColumnSelectionButton.configure(font=("Eras Medium ITC", 15))
        ColumnSelectionButton.grid(row=2, column=2)
        columnSelectorButton = ColumnSelectionButton

    else:
        raise Exception

def retrieve_2_columns():
    global df
    global table
    global desired_table
    global counter
    global columnSelectorButton

    # Change text on button depending on step
    if counter == 1:
        columnSelectorButton.configure(text="Select Power Column")

    #    # Get the selected column index
    selected_column_index = table.getSelectedColumn()

    #    # Check if a column is selected
    if selected_column_index is not None:
        # Get the column name from the dataframe
        column_name = df.columns[selected_column_index]

        # Retrieve the data from the selected column
        column_data = df[column_name]

        # Append the column data to the desired_table DataFrame
        desired_table[column_name] = column_data

        # Rename Date/Time Table
        if counter == 1:
            desired_table = desired_table.rename(columns={column_name: "Date/Time"})

        # Check if three columns have been added to desired_table
        if len(desired_table.columns) == 2:

            # Rename Power table
            desired_table = desired_table.rename(columns={column_name: "Power (kW)"})

            # Remove string from power table if any
            desired_table["Power (kW)"] = desired_table["Power (kW)"].astype(str)
            desired_table["Power (kW)"] = desired_table["Power (kW)"].str.replace("[a-zA-Z]", "", regex=True)
            desired_table["Power (kW)"] = desired_table["Power (kW)"].apply(FloatTryParse)
            
            # Cast as string
            desired_table["Date/Time"] = desired_table["Date/Time"].astype(str)

            # Format accordingly
            desired_table["Date/Time"] = desired_table["Date/Time"].apply(
                regexAndReturn_DateTime
            )

            # Show table
            analyzeAndGraph()

    # To make button text change
    counter = counter + 1

def retrieve_3_columns():
    global df
    global table
    global desired_table
    global counter
    global columnSelectorButton

    # Change text on button depending on step
    if counter == 1:
        columnSelectorButton.configure(text="Select Time Column")
    if counter == 2:
        columnSelectorButton.configure(text="Select Power Column")

    #    # Get the selected column index
    selected_column_index = table.getSelectedColumn()

    #    # Check if a column is selected
    if selected_column_index is not None:
        # Get the column name from the dataframe
        column_name = df.columns[selected_column_index]

        # Retrieve the data from the selected column
        column_data = df[column_name]

        # Append the column data to the desired_table DataFrame
        desired_table[column_name] = column_data

        # Rename Date/Time Table
        if counter == 1:
            desired_table = desired_table.rename(columns={column_name: "Date/Time"})
            print(desired_table["Date/Time"])
        if counter == 2:
            desired_table = desired_table.rename(columns={column_name: "temp"})

        # Check if three columns have been added to desired_table
        if len(desired_table.columns) == 3:
            # Rename Power table
            desired_table = desired_table.rename(columns={column_name: "Power (kW)"})

            # Remove string from power table if any
            desired_table["Power (kW)"] = desired_table["Power (kW)"].astype(str)
            desired_table["Power (kW)"] = desired_table["Power (kW)"].str.replace("[a-zA-Z]", "", regex=True)
            desired_table["Power (kW)"] = desired_table["Power (kW)"].astype(float)

            # Cast as string
            desired_table["Date/Time"] = desired_table["Date/Time"].astype(str)
            desired_table["temp"] = desired_table["temp"].astype(str)
            

            # Format accordingly
            desired_table["Date/Time"] = desired_table["Date/Time"].apply(special_regexAndReturn_Date)
            desired_table["temp"] = desired_table["temp"].apply(regexAndReturn_TimeStamp)

            # Combine 'Date/Time' and 'temp' columns
            desired_table["Date/Time"] = (desired_table["Date/Time"] + " " + desired_table["temp"])

            # Delete 'temp' column
            desired_table = desired_table.drop("temp", axis=1)

            analyzeAndGraph()

    # To make button text change
    counter = counter + 1

def remove_words_from_time(time):
    # Regular expression pattern to match valid substrings
    pattern = r"(AM|am|PM|pm|\d+|:|-|/|\s+)"

    # Find all valid substrings in the string
    valid_substrings = re.findall(pattern, time)

    # Join the valid substrings to form the modified string
    modified_string = "".join(valid_substrings).strip()

    return modified_string

def regexAndReturn_Date(current_date):    
   DayGroupIndex = 1
   MonthGroupIndex = 1
   YearGroupIndex = 1

   if 'D' in Entry_DateFormat_One.get().upper():
        DayGroupIndex = 1
   elif 'D' in Entry_DateFormat_Two.get().upper():
        DayGroupIndex = 2
   else:
        DayGroupIndex = 3

   if 'M' in Entry_DateFormat_One.get().upper():
        MonthGroupIndex = 1
   elif 'M' in Entry_DateFormat_Two.get().upper():
        MonthGroupIndex = 2
   else:
        MonthGroupIndex = 3

   if 'Y' in Entry_DateFormat_One.get().upper():
        YearGroupIndex = 1
   elif 'Y' in Entry_DateFormat_Two.get().upper():
        YearGroupIndex = 2
   else:
        YearGroupIndex = 3


   patterns = [ r"^(\d{2})[-/](\d{2})[-/](\d{4})",  # pattern_MM_DD_YYYY
                r"^(\d{2})[-/](\d{1})[-/](\d{4})",  # pattern_MM_D_YYYY
                r"^(\d{1})[-/](\d{2})[-/](\d{4})",  # pattern_M_DD_YYYY
                r"^(\d{1})[-/](\d{1})[-/](\d{4})",  # pattern_M_D_YYYY

                r"^(\d{4})[-/](\d{2})[-/](\d{2})",  # pattern_YYYY_MM_DD
                r"^(\d{4})[-/](\d{2})[-/](\d{1})",  # pattern_YYYY_MM_D
                r"^(\d{4})[-/](\d{1})[-/](\d{2})",  # pattern_YYYY_M_DD
                r"^(\d{4})[-/](\d{1})[-/](\d{1})",  # pattern_YYYY_M_D
            ]
   for pattern in patterns:
        match = re.match(pattern, current_date)

        if match:
            day = match.group(DayGroupIndex).zfill(2)
            month = match.group(MonthGroupIndex).zfill(2)
            year = match.group(YearGroupIndex)
            return f"{day}-{month}-{year}"
        
   return "ERROR"

def special_regexAndReturn_Date(current_date):
    patterns = [ r"^(\d{2})[-/](\d{2})[-/](\d{4})",  # pattern_MM_DD_YYYY
				r"^(\d{2})[-/](\d{1})[-/](\d{4})",  # pattern_MM_D_YYYY
				r"^(\d{1})[-/](\d{2})[-/](\d{4})",  # pattern_M_DD_YYYY
				r"^(\d{1})[-/](\d{1})[-/](\d{4})",  # pattern_M_D_YYYY

				r"^(\d{4})[-/](\d{2})[-/](\d{2})",  # pattern_YYYY_MM_DD
				r"^(\d{4})[-/](\d{2})[-/](\d{1})",  # pattern_YYYY_MM_D
				r"^(\d{4})[-/](\d{1})[-/](\d{2})",  # pattern_YYYY_M_DD
				r"^(\d{4})[-/](\d{1})[-/](\d{1})",  # pattern_YYYY_M_D
			]
    for pattern in patterns:
        match = re.match(pattern, current_date)
        
        if match:
            day = match.group(3).zfill(2)
            month = match.group(2).zfill(2)
            year = match.group(1)
            return f"{day}-{month}-{year}"
        
def regexAndReturn_TimeStamp(time):
    # Remove unwanted spaces/words
    time = remove_words_from_time(time)
    time = time.replace(" ", "")
    hasPM = "no"
    if "AM" in time:
        time = time.replace("AM", "")
    elif "PM" in time:
        time = time.replace("PM" "")
        hasPM = "yes"
    time = re.sub(r"[:\-/]", "", time)
    time_length = len(time)

    if time_length == 1:
        time = f"00:0{time}:00"
    elif time_length == 2:
        time = f"00:{time}:00"
    elif time_length == 3:
        time = f"0{time[0]}:{time[1]}{time[2]}:00"
    elif time_length == 4:
        hour = f"{time[0]}{time[1]}"
        minute = f"{time[2]}{time[3]}"
        second = f"00"

        if hasPM == "yes" and hour != "12":
            hour = int(hour) + 12
            hour = str(hour)
            time = f"{hour}:{minute}:{second}"
        else:
            time = f"{hour}:{minute}:{second}"
    elif time_length == 6:
        hour = f"{time[0]}{time[1]}"
        minute = f"{time[2]}{time[3]}"
        second = f"{time[4]}{time[5]}"

        if hasPM == "yes":
            hour = int(hour) + 12
            hour = str(hour)

        time = f"{hour}:{minute}:{second}"

    pattern = r"^(\d{2}):(\d{2}):(\d{2})$"
    match = re.match(pattern, time)

    if match:
        hour = match.group(1)
        minute = match.group(2)
        second = match.group(3)
        return f"{hour}:{minute}:{second}"
    return f"ERROR"

def regexAndReturn_DateTime(DateTime):
    DateTime = remove_words_from_time(DateTime)
    date, time = DateTime.split()
    date = regexAndReturn_Date(date)
    time = regexAndReturn_TimeStamp(time)

    return f"{date} {time}"

def analyzeAndGraph():
    # Create a new window to display the desired_table
    toplevel = tk.CTkToplevel(app)

    # Create the table from desired_table
    table = Table(toplevel, dataframe=desired_table)
    table.show()

    desired_table["Date/Time"] = desired_table["Date/Time"].apply(transform_datetime)     
    # Change if midnight its 24hrs

    DailyProfile_DF = dailyProfile()
    DailyMaxMin_DF = dailyMaxMin()
    
    which_months = desired_table['Date/Time'].dt.month.unique() #This will find out which months are present
    number_of_months = len(which_months) #How many different months there are
    time_interval = (desired_table['Date/Time'][1] - desired_table['Date/Time'][0]).total_seconds()/60 # difference between timestamps in minutes

    # Graph Formatting
    cutoff_factor = 0   #this number is the cutoff factor, 0.0 will give you all the data, 1.0 will give you only the values higher than the mean, 0.5 will only give you values higher than 50% of the mean

    #all the month/day/time titles
    mdict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    month_titles = [mdict[key] for key in which_months] + ['']
    day_titles = np.array(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', ''])
    set_month_titles = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', '']

    #a list of hours of the day so we can label the x ticks
    Ip = ['12 am', '1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', '8 am', '9 am', '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm', '12 am', '']

    #a way to add commas to axis values in the thousands
    commas = ticker.StrMethodFormatter('{x:,.0f}')

    Graph_YearlyMaxMin(DailyMaxMin_DF, number_of_months, cutoff_factor, month_titles, commas)
    Graph_DayOfWeekMaxMin(DailyMaxMin_DF, cutoff_factor, day_titles, commas)
    Graph_MonthlyKwUsageByTimeOfDay(DailyProfile_DF, set_month_titles, Ip, commas)
    Graph_MonthlyKwUsageByDayOfWeek(DailyProfile_DF, day_titles, set_month_titles, commas)
    Graph_HistogramOfPeaksByTimeOfDay(DailyMaxMin_DF, cutoff_factor, Ip)
    Graph_HistogramOfPeaksByKwValues(DailyMaxMin_DF, cutoff_factor, commas)
    Graph_MonthlyKwPeakProfile(which_months, time_interval, commas)

def Graph_YearlyMaxMin(mm, number_of_months, cutoff_factor, month_titles, commas):
    upper = []
    lower = []
    if np.std(mm['MaxValue']) >= np.std(mm['MinValue']):
        for u,l in zip(mm["MaxValue"],mm["MinValue"]):
            if u >= np.mean(mm['MaxValue'])*cutoff_factor:
                upper.append(u)
                lower.append(l)
    else:
        for u,l in zip(mm["MaxValue"],mm["MinValue"]):
            if l >= np.mean(mm['MinValue'])*cutoff_factor:
                upper.append(u)
                lower.append(l)
    # -----------------------------------------------


    time = np.linspace(0, len(upper), len(upper))   #an array for the x axis
    tix = np.linspace(0, len(upper), number_of_months+1)   #an array for the tickmarks

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
    plt.gca().set_xticks(ticks = tix + len(upper)/number_of_months/2, minor=True)#, labels = month_titles)   #naming the x ticks and putting them in the middle
    plt.gca().set_xticklabels(month_titles, minor=True)
    plt.tick_params(axis = 'x', which = 'minor', size = 0)
    plt.gca().yaxis.set_major_formatter(commas)                    #adding commas to the y axis values
    plt.grid()                                                     #grid

    plt.savefig('Max_Min_kW_For_The_Year.png')     #saves a figure into the same folder as this ipynb

def Graph_DayOfWeekMaxMin(mm, cutoff_factor, day_titles, commas):
    mm['dayofweek'] = pd.to_datetime(mm['Date']).dt.dayofweek
    mm = mm.sort_values(['dayofweek', 'Date'])

    #---------------------------------------
    upper = []
    lower = []
    wknd = []
    wkdy = []
    if np.std(mm['MaxValue']) >= np.std(mm['MinValue']):
        for u, l, d in zip(mm['MaxValue'], mm['MinValue'], mm['dayofweek']):
            if d >= 5 or u >= np.mean(mm['MaxValue'])*cutoff_factor:
                upper.append(u)
                lower.append(l)
                if d >= 5:
                    wknd.append(u)
                else:
                    wkdy.append(u)
    else:
        for u, l, d in zip(mm['MaxValue'], mm['MinValue'], mm['dayofweek']):
            if l >= np.mean(mm['MinValue'])*cutoff_factor:
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

    plt.xticks(ticks = tix, labels = day_titles, visible = False)
    plt.gca().set_xticks(ticks = tix + len(upper)/14, minor = True)
    plt.gca().set_xticklabels(day_titles, minor=True)
    plt.tick_params(axis = 'x', which = 'minor', size = 0)

    plt.ylabel('Power (kW)', size = 12)
    plt.xlabel('Day of Week', size = 12)
    plt.gca().yaxis.set_major_formatter(commas)
    plt.grid()

    plt.savefig('Max_Min_kW_By_Day_of_Week.png')

def Graph_MonthlyKwUsageByTimeOfDay(dp, set_month_titles, Ip, commas):
    day_of_week = []
    time = []
    kW = []
    month = []
    for d, t, k, m in zip(dp['Day of Week'], dp['Time'], dp['kW'], dp['Month']):
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
    for d, t, k, m in zip(dp['Day of Week'], dp['Time'], dp['kW'], dp['Month']):
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
        ax.set_xticklabels(Ip[::6],  rotation = 45)
        ax.set_yticks(ticks = np.linspace(0, np.ceil(np.max(dp['kW'])/100)*100 + 100, 5))   #y axis goes from 0 to the max(rounded up to the next hundred) with 5 tickmarks
        ax.set_title(set_month_titles[i])          #naming the subplots 
        ax.tick_params(labelsize = 8)          #making the font size for the axis smaller
        if i % 4 == 0:                         #check if it's the leftmost subplot in each row
            ax.set_ylabel('Power (kW)', size = 10)                #y-axis label for the leftmost subplot
        ax.grid()                              #grid
        ax.yaxis.set_major_formatter(commas)   #add commas to the y axis
    
    
    legend_handles = [plt.Line2D([], [], marker='s', markersize=4, linestyle='None', label='Weekday', color = 'tab:blue'),
                      plt.Line2D([], [], marker='s', markersize=4, linestyle='None', label='Weekend', color = 'firebrick')]

    fig.legend(handles=legend_handles)

    plt.savefig('Monthly_kW_by_Time_of_Day.png')     #saves a figure into the same folder as this ipynb

def Graph_MonthlyKwUsageByDayOfWeek(dp, day_titles, set_month_titles, commas):
    dp = dp.sort_values(['Month', 'Day of Week'])   #sorting the entire dataframe by month and then day of the week
    dp['x'] = np.arange(len(dp))                    #creating a new column that assigns a number to each row in this new order

    fig, axes = plt.subplots(nrows = 6, ncols = 2, figsize=(10, 12))  #creating 12 subplots
    plt.subplots_adjust(top = .925, wspace=0.25, hspace=1)            #spacing out the subplots



    for i, ax, in enumerate(axes.flatten()):
        subset = dp[dp['Month'] == i + 1]        #splitting the data into 12 subsets
        ax.plot(subset['x'], subset['kW'], '-', color = 'tab:blue')   #plotting each subset into it's respective subplot


        tix = np.linspace(np.min(subset['x']), np.max(subset['x']), 8)
        middle_tix = tix + len(subset['x'])/14

        ax.set_yticks(ticks = np.linspace(0, np.ceil(np.max(dp['kW'])/100)*100+100, 5))  #y axis goes from 0 to the max(rounded up to the next hundred) with 5 tickmarks
        ax.set_xticks(ticks = tix)
        ax.set_xticklabels(day_titles, visible = False)
        ax.set_xticks(ticks = middle_tix, minor = True)
        ax.set_xticklabels(day_titles, size = 8, minor=True)
        ax.tick_params(axis = 'x', which = 'minor', size = 0)
        ax.tick_params(labelsize = 8)

        ax.set_title(set_month_titles[i])             #naming subplots
        if i % 2 == 0:                            #Check if it's the leftmost subplot in each row
            ax.set_ylabel('Power (kW)', size = 10)                   #y-axis label for the leftmost subplot
        ax.yaxis.set_major_formatter(commas)      #add commas to the y axis
        ax.grid() 
    
    plt.savefig('Monthly_kW_by_Day_of_Week.png')   #saves a figure into the same folder as this ipynb

def Graph_HistogramOfPeaksByTimeOfDay(mm, cutoff_factor, Ip):
    #-----------------------------------------------
    MaxTime = []
    for u,t in zip(mm["MaxValue"],mm["MaxTime"]):
        if u >= np.mean(mm['MaxValue'])*cutoff_factor:
            MaxTime.append(t)
    #-----------------------------------------------

    hours = [time.hour for time in MaxTime]
    tix = np.linspace(0, 23, 13)

    plt.figure(figsize=(8, 4))
    plt.hist(hours, bins = 24, range = (0, 23), rwidth = 0.8, color = 'tab:blue')
    plt.gca().set_axisbelow(True)
    plt.grid(axis = 'y')

    plt.xticks(ticks = tix, labels = Ip[::2], rotation = 40, size = 10)
    plt.xlabel('Time of Day', size = 12)
    plt.ylabel('Frequency of Peaks', size = 12)

    plt.savefig('Peak_Frequency_by_Time_of_Day.png')

def Graph_HistogramOfPeaksByKwValues(mm, cutoff_factor, commas):
    #if you want to exclude days that have an upper kW output less than the mean * cutoff_factor, then run this section of code
    #-----------------------------------------------
    MaxValue = []
    for u in mm["MaxValue"]:
        if u >= np.mean(mm['MaxValue'])*cutoff_factor:
            MaxValue.append(u)
    # -----------------------------------------------

    high = np.ceil(np.max(MaxValue)/1000)*1000

    plt.figure(figsize=(8, 4))
    plt.hist(MaxValue, bins = int(high/100), rwidth = 0.8, range = (0, high), color = 'firebrick')

    plt.gca().xaxis.set_major_formatter(commas)
    plt.gca().set_axisbelow(True)
    plt.grid(axis = 'y')
    plt.tick_params(axis = 'both', direction = 'inout')
    plt.ylabel('Frequency of Peak Value', size = 12)
    plt.xlabel('Peak kW', size = 12)

    plt.savefig('Peak_Frequency_by_Peak_Value.png')

def Graph_MonthlyKwPeakProfile(which_months, time_interval, commas):
    rng = 60/time_interval*3 #amount of datapoints for 3 hours before/after the max

    fig, axes = plt.subplots(nrows = 4, ncols = 3, figsize=(10, 8))  #creating 12 subplots
    plt.subplots_adjust(wspace=0.6, hspace=1.0) 

    lower = []
    n = 0
    for i, ax in zip(which_months, axes.flatten()):
    
        idxmax = desired_table.loc[desired_table['Date/Time'].dt.month == i,  'Power (kW)'].idxmax()
        subset = desired_table.loc[idxmax-rng:idxmax+rng]
        high = subset['Power (kW)'].max()
        low = subset['Power (kW)'].min()
        lower.append(low) 

        tix = subset['Date/Time'].dt.strftime('%I:%M %p')
        title = subset['Date/Time'].dt.strftime('%b %d')
    
        ax.plot(tix, subset['Power (kW)'])
        ax.plot(rng, high, '.', color = 'firebrick')
        ax.annotate(f'{int(high):,}', xy=(rng, high), xytext=(74, -2.5), textcoords='offset points', arrowprops=dict(arrowstyle='-', color = 'firebrick'), color = 'firebrick', size = 8)

        ax.set_xticks(tix[::int(60/time_interval)])
        ax.set_yticks(ticks = np.linspace(np.floor(np.min(lower)/100-1)*100, np.ceil(np.max(desired_table['Power (kW)'])/100+1)*100, 3))   #y axis goes from 0 to the max(rounded up to the next hundred) with 5 tickmarks
        ax.set_title(title.max())          #naming the subplots 
        ax.tick_params(axis = 'x', labelsize = 6, rotation = 55)          #making the font size for the axis smaller

        if (n) % 3 == 0:                         #check if it's the leftmost subplot in each row
            ax.set_ylabel('Power (kW)', size = 10)                #y-axis label for the leftmost subplot
        ax.grid()                              #grid
        ax.yaxis.set_major_formatter(commas)   #add commas to the y axis
        n += 1
    
    plt.savefig('Monthly_Peak_Profile.png')

def transform_datetime(input_date_str):
    date_format = "%d-%m-%Y %H:%M:%S"
    try:
        date_obj = datetime.strptime(input_date_str, date_format)
    except ValueError:
        # Handle the case of "24:00:00" by replacing it with "00:00:00" and adding one day
        input_date_str = input_date_str.replace("24:00:00", "00:00:00")
        date_obj = datetime.strptime(input_date_str, date_format)
        date_obj += timedelta(days=1)

    return date_obj

def dailyProfile():
    power_title = "Power (kW)"
    DateTime_Title = "Date/Time"
   
    # This section creates the dp dataframe used for the graphs.
    which_months = desired_table[DateTime_Title].dt.month.unique() #This will find out which months are present
    # number_of_months = len(which_months) #How many different months there are

    time_interval = (desired_table[DateTime_Title][1] - desired_table[DateTime_Title][0]).total_seconds()/60 # difference between timestamps in minutes
    intvls_a_week = int(24*7*(60/time_interval)) # how many time intervals there are in one week. Used for creating the dp dataframe

    data = []

    for i in which_months:
        md = desired_table[desired_table[DateTime_Title].dt.month == i]
        mdt = md[DateTime_Title]
    
        for t in np.arange(0, intvls_a_week):
            time = mdt.iloc[t].time()    
            month = mdt.iloc[t].month
            dyofwk = mdt.iloc[t].weekday() + 1
            kW = np.mean(md[power_title].iloc[t::intvls_a_week])

            data.append([time, month, dyofwk, kW])
        
    dp = pd.DataFrame(data, columns=['Time', 'Month', 'Day of Week', 'kW'])
    # dp takes the average of the 4 or 5 values of a specific time and day throughout each week.
    # Example: the kW value for 2:15am on a tuesday in January, is the average of all the tuesdays at 2:15am in January

    # Show things
    toplevel = tk.CTkToplevel(app)

    # Create the table from desired_table
    table = Table(toplevel, dataframe = dp)
    table.show()

    return dp

def dailyMaxMin():
    power_title = "Power (kW)"
    DateTime_Title = "Date/Time"

    res = []
    for d in pd.date_range(desired_table[DateTime_Title].min().date(), desired_table[DateTime_Title].max().date()):
        dd = desired_table[desired_table[DateTime_Title].dt.date == d.date()]
    
        if not dd.empty:
            max_value = dd[power_title].max()
            max_time = dd.loc[dd[power_title].idxmax(), DateTime_Title].time()
            min_value = dd[power_title].min()
            min_time = dd.loc[dd[power_title].idxmin(), DateTime_Title].time()
            res.append([d, max_value, max_time, min_value, min_time])

    mm = pd.DataFrame(res, columns=['Date', 'MaxValue', 'MaxTime', 'MinValue', 'MinTime'])
    
    toplevel = tk.CTkToplevel(app)

    # Create the table from mm DataFrame
    table = Table(toplevel, dataframe=mm)
    table.show()
    
    return mm

def displayErrorPopUp(message):
    ErrorPage = tk.CTkToplevel(app)
    ErrorMessage = tk.CTkLabel(ErrorPage, text=message)
    ErrorMessage.configure(
        font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30
    )
    ErrorMessage.grid(row=1, column=2, padx=10, pady=10)
    CloseButton = tk.CTkButton(
        ErrorPage, text="I Understand", command=lambda: ErrorPage.destroy()
    )
    CloseButton.configure(font=("Eras Medium ITC", 15))
    CloseButton.grid(row=2, column=2, padx=10, pady=10)

def uploadbutton_pressed():
    try:
        FormatChecker = 1
        InvalidRowChecker = 1
        DuplicateChecker = 1

        ValidFormats = ["M", "D", "DD", "MM", "YYYY"]
        Date_Entries = [Entry_DateFormat_One,Entry_DateFormat_Two, Entry_DateFormat_Three]
        labels_row = Int32TryParse(Entry_StartRowNum.get())
        end_row = Int32TryParse(Entry_EndRowNum.get())
        Row_Entries = [Entry_StartRowNum, Entry_EndRowNum]


        # Invalid Entry Checking
        for Entry in Date_Entries:
            if Entry.get().upper() not in ValidFormats:
                FormatChecker = FormatCheckingOnEntries(Entry)

        for Row in Row_Entries:
            if Int32TryParse(Row.get()) == None:
                FormatChecker = FormatCheckingOnEntries(Row)
                InvalidRowChecker = -1

        # Check for the last row being lower than the first row
        if InvalidRowChecker == 1:
            if end_row <= labels_row:
                displayErrorPopUp(
                    f"Labels' Row '{end_row}' is smaller than or equal to Ending Row '{labels_row}'."
                )
                InvalidRowChecker = -1
        
        # Check for duplicates in Date_Entries
        DuplicateChecker = CheckForDuplicateEntries()

        # Open file if everything looks like it follows the desired format
        if FormatChecker == 1 and InvalidRowChecker == 1 and DuplicateChecker == 1:
            open_file(labels_row, end_row)

    except:
        displayErrorPopUp(f"Something went wrong when attempting to open the file")
        startbutton_pressed()

def CheckForDuplicateEntries():
    Date_Entries = [Entry_DateFormat_One, Entry_DateFormat_Two, Entry_DateFormat_Three]
    for i in range(len(Date_Entries)):
        for j in range(i + 1, len(Date_Entries)):
            if Date_Entries[i].get().upper().__contains__(Date_Entries[j].get().upper()):
                displayErrorPopUp(f"Duplicates have been found at Entry {i + 1} and {j + 1}")
                return -1
    return 1

def FormatCheckingOnEntries(this):
    this.delete(0, len(this.get()))
    this.insert(0, "#ERROR")
    return -1

def Int32TryParse(input):
    try:
        parsed_int = int(input)
        return parsed_int
    except ValueError:
        return None

def FloatTryParse(input):
    try:
        parsed_float = float(input)
        return parsed_float
    except ValueError:
        return

def startbutton_pressed():
    global Entry_StartRowNum
    global Entry_EndRowNum
    global Frame_UploadPage
    global Frame_TitlePage
    global CheckCombinedDateTime
    global Entry_DateFormat_One
    global Entry_DateFormat_Two
    global Entry_DateFormat_Three

    # Frame Initialization
    Frame_UploadPage = tk.CTkFrame(app)
    Frame_UploadPage.grid(row=0, column=2, padx=20, pady=(50, 0))
    Frame_RowsRange = tk.CTkFrame(Frame_UploadPage)
    Frame_RowsRange.grid(row=3, column=2, padx=20, pady=(10, 0))
    Frame_DateFormat = tk.CTkFrame(Frame_UploadPage)
    Frame_DateFormat.grid(row=7, column=2, padx=20, pady=(2, 0))

    # Remove TitlePage Frame
    Frame_TitlePage.grid_remove()

    # Title
    Label_Title = tk.CTkLabel(Frame_UploadPage, text="Excel Format Setup")
    Label_Title.configure(
        font=("Eras Bold ITC", 40), anchor="center", pady=30, padx=210
    )
    Label_Title.grid(row=1, column=2, padx=10, pady=10)

    # Section where we prompt the user what its range of data is, starting from the labels and finishing on the last point of data.
    Label_RowsRange = tk.CTkLabel(
        Frame_UploadPage, text="Indicate the range in which the data is located"
    )
    Label_RowsRange.configure(
        font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30
    )
    Label_RowsRange.grid(row=2, column=2, padx=10, pady=0)

    Label_StartRowNum = tk.CTkLabel(Frame_RowsRange, text="Start (Labels' Row):")
    Label_StartRowNum.configure(
        font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30
    )
    Label_StartRowNum.grid(row=4, column=1, padx=10, pady=0)
    Entry_StartRowNum = tk.CTkEntry(Frame_RowsRange)
    Entry_StartRowNum.grid(row=4, column=2, padx=10, pady=0)

    Label_StartRowNum = tk.CTkLabel(Frame_RowsRange, text="End:")
    Label_StartRowNum.configure(
        font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30
    )
    Label_StartRowNum.grid(row=4, column=3, padx=10, pady=0)
    Entry_EndRowNum = tk.CTkEntry(Frame_RowsRange)
    Entry_EndRowNum.grid(row=4, column=4, padx=10, pady=0)

    # Section where we prompt the user the format of how the date is recorded (Ex: MM/DD/YYYY)
    Label_DateFormat = tk.CTkLabel(
        Frame_UploadPage,
        text=f"Indicate the format at which the Dates are shown in the data sheet using (Ex: MM/DD/YYYY)",
    )
    Label_DateFormat.configure(
        font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30
    )
    Label_DateFormat.grid(row=6, column=2, padx=10, pady=8)

    Entry_DateFormat_One = tk.CTkEntry(Frame_DateFormat)
    Entry_DateFormat_One.grid(row=7, column=1, padx=10, pady=0)

    Label_Dash_One = tk.CTkLabel(Frame_DateFormat, text="/")
    Label_Dash_One.configure(
        font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30
    )
    Label_Dash_One.grid(row=7, column=2, padx=6, pady=0)

    Entry_DateFormat_Two = tk.CTkEntry(Frame_DateFormat)
    Entry_DateFormat_Two.grid(row=7, column=3, padx=10, pady=0)

    Label_Dash_Two = tk.CTkLabel(Frame_DateFormat, text="/")
    Label_Dash_Two.configure(
        font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30
    )
    Label_Dash_Two.grid(row=7, column=4, padx=6, pady=0)

    Entry_DateFormat_Three = tk.CTkEntry(Frame_DateFormat)
    Entry_DateFormat_Three.grid(row=7, column=5, padx=10, pady=0)

    # Section where we check if the date and timestamps are combined or not
    check_var = tk.StringVar(value="on")
    CheckBox_DateTimeCheck = tk.CTkCheckBox(
        Frame_UploadPage,
        text="Are Dates and Timestamps in the same column?",
        variable=check_var,
        onvalue="on",
        offvalue="off",
    )
    CheckBox_DateTimeCheck.configure(font=("Eras Medium ITC", 15))
    CheckBox_DateTimeCheck.grid(row=8, column=2, padx=10, pady=25)
    CheckCombinedDateTime = CheckBox_DateTimeCheck

    # Button to upload the excel file
    UploadButton_TitlePage = tk.CTkButton(
        Frame_UploadPage, text="Upload Excel File", command=uploadbutton_pressed
    )
    UploadButton_TitlePage.configure(font=("Eras Medium ITC", 15))
    UploadButton_TitlePage.grid(row=9, column=2, padx=10, pady=25)

def CreateStartingPage():
    global Frame_TitlePage
    Frame_TitlePage = tk.CTkFrame(app)
    Frame_TitlePage.grid(row=0, column=2, padx=10, pady=(100, 0))
    Frame_TitleOnlyFrame = tk.CTkFrame(Frame_TitlePage)
    Frame_TitleOnlyFrame.grid(row=0, column=2, padx=100, pady=100)
    Label_Title = tk.CTkLabel(Frame_TitleOnlyFrame, text="Data Analysis Tool")
    Label_Title.configure(font=("Eras Bold ITC", 50), anchor="center", pady=30, padx=30)
    Label_Title.grid(row=0, column=2, padx=10, pady=10)
    StartButton = tk.CTkButton(
        Frame_TitlePage, text="Get Started", command=startbutton_pressed
    )
    StartButton.configure(font=("Eras Medium ITC", 15))
    StartButton.grid(row=1, column=2, padx=200, pady=50)


# """ Start of MAIN """

## Create GUI

tk.set_appearance_mode("dark")
app = tk.CTk()
app.title("Data Analysis Tool")
app.geometry("1000x1000")


# configure grid system
app.grid_columnconfigure(2, weight=1)

# Start GUI program
CreateStartingPage()

## Start the GUI
app.mainloop()

# """ End of MAIN """