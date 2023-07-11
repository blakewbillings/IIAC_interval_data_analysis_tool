import string
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
from datetime import datetime as dt
##%matplotlib inline
##%config InlineBackend.figure_format = 'svg'

# Some nice things
# (All font types here = https://stackoverflow.com/questions/39614027/list-available-font-families-in-tkinter)

## Global Variables for function access
global df
global table
global desired_table
global Entry_StartRowNum
global Frame_UploadPage
global Frame_TitlePage
global counter
global columnSelectorButton

# temps
desired_table = pd.DataFrame()
counter = 1

## This function opens file explorer for the user to
## select the desired excel file to be opened.
def open_file(labels_row):
    global df
    global table
    global Frame_UploadPage
    global columnSelectorButton
    file_path = filedialog.askopenfilename(filetypes=[("XLSX Files", "*.xlsx"), ("CSV Files", "*.csv")])
    
    if file_path.endswith(".csv"):
        # Convert CSV to Excel
        excel_file_path = os.path.splitext(file_path)[0] + ".xlsx"
        data_frame = pd.read_csv(file_path)
        data_frame.to_excel(excel_file_path, index=False)
        file_path = excel_file_path  # Update file_path with the Excel file path

    if file_path:
        #Remove last widget
        Frame_UploadPage.grid_remove()

        # Read the Excel file using pandas
        df = pd.read_excel(file_path, sheet_name=0, skiprows = lambda x: x < labels_row - 1)

        # Create GUI for Table column selection
        Frame_ColumnSelectorTitle = tk.CTkFrame(app)
        Frame_ColumnSelectorTitle.grid(row=0, column=2, padx=20, pady=(50, 0))
        
        # Frame for Title
        Label_Title = tk.CTkLabel(Frame_ColumnSelectorTitle, text="Column Selection")
        Label_Title.configure(font=('Eras Bold ITC', 40), anchor='center', padx=20, pady=20)
        Label_Title.grid(row=0, column=2)
        
        # Frame for the Table
        Frame_Table = tk.CTkFrame(app)
        Frame_Table.grid(row = 1, column =2 , padx=20, pady=(50,0))

        # Create table
        table = Table(Frame_Table, dataframe=df)
        table.show()
     
        Frame_ColumnSelectorButtons = tk.CTkFrame(app)
        Frame_ColumnSelectorButtons.grid(row = 2, column = 2, padx = 20, pady=(50,0))

        ColumnSelectionButton = tk.CTkButton(Frame_ColumnSelectorButtons, text="Select Date Column", command = retrieve_column)
        ColumnSelectionButton.configure(font=('Eras Medium ITC',15))
        ColumnSelectionButton.grid(row = 2, column = 2)
        columnSelectorButton = ColumnSelectionButton

    else:
        print("Could not open the file")

def retrieve_column():
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
        
        if counter == 1:
            desired_table = desired_table.rename(columns={column_name: 'Date/Time'})
        if counter == 2:
            desired_table = desired_table.rename(columns={column_name: 'temp'})

        # Check if three columns have been added to desired_table
        if len(desired_table.columns) == 3:
            # 
            desired_table = desired_table.rename(columns={column_name: 'Power (kW)'})

            # Combine Date/Time content and temp
            # Use separate method
            
            # Cast as string
            desired_table['Date/Time'] = desired_table['Date/Time'].astype(str)
            desired_table['temp'] = desired_table['temp'].astype(str)

            # Format accordingly
            desired_table['Date/Time'] = desired_table['Date/Time'].apply(regexAndReturn_Date)
            desired_table['temp'] = desired_table['temp'].apply(regexAndReturn_TimeStamp)

            # Combine 'Date/Time' and 'temp' columns
            desired_table['Date/Time'] = desired_table['Date/Time'] + ' ' + desired_table['temp']

            # Delete 'temp' column
            desired_table = desired_table.drop('temp', axis=1)        
            
            analyzeAndGraph()


    # To make button text change
    counter = counter + 1


def regexAndReturn_Date(current_date):
    pattern = r"^(\d{4})([-/])(\d{2})\2(\d{2})"

    match = re.match(pattern, current_date[:10])
    if match:
        day = match.group(1)
        month = match.group(3)
        year = match.group(4)
        return f"{day}-{month}-{year}"
    
    return "ERROR"

def regexAndReturn_TimeStamp(time):
    time_length = len(time)
    
    if time_length == 1:
        time = f"00:0{time}"
    elif time_length == 2:
        time = f"00:{time}"
    elif time_length == 3:
        time = f"0{time[0]}:{time[1:]}"
    elif time_length == 4:
        time = f"{time[0]}{time[1]}:{time[2]}{time[3]}"
    
    pattern = r"^(\d{1,4})([:/-])(\d{2})$"
    
    match = re.match(pattern, time)
    
    if match:
        hour = match.group(1)
        separator = match.group(2)
        minute = match.group(3)
        return f"{hour}:{minute}"
    
    return "ERROR"

def analyzeAndGraph():
    # Create a new window to display the desired_table
    toplevel = tk.CTkToplevel(app)

    # Create the table from desired_table
    table = Table(toplevel, dataframe = desired_table)
    table.show()

    dailyProfile
    dailyMaxMin


def dailyProfile():
    time_diff = desired_table.index[1].minute-desired_table.index[0].minute

    interval = 24*7*(60/time_diff)

    months = desired_table.index.month.max()

    data = []

    for i in range(months):
        md = desired_table[desired_table.index.month == i+1]
        mdi = md.index

        for j in range(int(interval)):
            time = mdi[j].time()
            month = mdi[j].month
            day_of_week = mdi[j].weekday() + 1
            kW = np.mean(md['Power (kW)'].iloc[j::int(interval)])

            #uncomment to print values        
            print(f"Time: {time}, Month: {month}, Day of Week: {day_of_week}, kW: {kW}")

            data.append([time, month, day_of_week, kW])

    daily_profile = pd.DataFrame(data, columns=['Time', 'Month', 'Day of Week', 'kW'])
    dp = daily_profile



def dailyMaxMin():
    results = []

    for day in pd.date_range(start=desired_table.index.min().date(), end=desired_table.index.max().date(), freq='D'):
        daily_data = desired_table[desired_table.index.date == day.date()]

        if len(daily_data) > 0:
            max_value = daily_data['Power (kW)'].max()
            max_time = daily_data.loc[daily_data['Power (kW)'].idxmax()].name.time()
            min_value = daily_data['Power (kW)'].min()
            min_time = daily_data.loc[daily_data['Power (kW)'].idxmin()].name.time()
            results.append({'Date': day.date(), 'MaxValue': max_value, 'MaxTime': max_time, 'MinValue': min_value, 'MinTime': min_time})

    daily_max_min = pd.concat([pd.DataFrame(result, index=[0]) for result in results], ignore_index=True)
    mm = daily_max_min

    #uncomment to print values
    print(daily_max_min)


def analyzeDF(toplevel):
    TimeColumn = desired_table.iloc[:,0]
    TimeStampColumn = desired_table.iloc[:, 1];
    print(TimeColumn)
    print(TimeStampColumn)
    
    TimeStampColumn = pd.to_datetime(TimeStampColumn)
    TimeColumn = pd.to_datetime(TimeColumn).dt.tz_localize(None)
    desired_table.set_index(TimeStampColumn,inplace = True)

def uploadbutton_pressed():
    try: 
        labels_row = int(Entry_StartRowNum.get())
        open_file(labels_row)

    except:
        ## Window pop-up saying that the entry item is not valid
        Entry_StartRowNum.delete(0, len(Entry_StartRowNum.get()))
        Entry_StartRowNum.insert(0, "#ERROR")

def startbutton_pressed():
    global Entry_StartRowNum
    global Frame_UploadPage
    global Frame_TitlePage

    # Frame Initialization
    Frame_UploadPage = tk.CTkFrame(app)
    Frame_UploadPage.grid(row = 0, column=2, padx=20, pady=(50,0))

    #Remove TitlePage Frame
    Frame_TitlePage.grid_remove()

    # Title
    Label_Title = tk.CTkLabel(Frame_UploadPage, text = "Excel Format Setup")
    Label_Title.configure(font=('Eras Bold ITC', 40), anchor = 'center', pady=30, padx=210)
    Label_Title.grid(row = 2, column = 2, padx=10,pady=10)
    
    # Section where we prompt the user where the labels of the excel sheet are
    Label_StartRowNum = tk.CTkLabel(Frame_UploadPage, text = "Indicate the Row Number where the Data Labels are located")
    Label_StartRowNum.configure(font=('Eras Medium ITC',15), anchor = 'center', pady=20, padx=30)
    Label_StartRowNum.grid(row = 3, column = 2, padx=10, pady=0)
    Entry_StartRowNum = tk.CTkEntry(Frame_UploadPage)
    Entry_StartRowNum.grid(row = 4, column=2, padx=10, pady=0)
    Label_Important = tk.CTkLabel(Frame_UploadPage, text = "IMPORTANT: Everything under the Labels will be considered data")
    Label_Important.configure(font=('Eras Medium ITC',10), anchor = 'center', pady=0, padx=30)
    Label_Important.grid(row = 5, column=2, padx=10, pady=2)
    
    # Section where we check if the date and timestamps are combined or not
    check_var = tk.StringVar(value="on")
    CheckBox_DateTimeCheck = tk.CTkCheckBox(Frame_UploadPage, text = "Are Dates and Timestamps in the same column?", variable=check_var, onvalue = "on", offvalue = "off")
    CheckBox_DateTimeCheck.configure(font=('Eras Medium ITC',15))
    CheckBox_DateTimeCheck.grid(row = 6, column = 2, padx=10, pady=30)

    # Button to upload the excel file
    UploadButton_TitlePage = tk.CTkButton(Frame_UploadPage,text="Upload Excel File", command = uploadbutton_pressed)
    UploadButton_TitlePage.configure(font=('Eras Medium ITC',15))
    UploadButton_TitlePage.grid(row=7,column=2, padx=10, pady=30)


def CreateStartingPage():
    global Frame_TitlePage
    Frame_TitlePage = tk.CTkFrame(app)
    Frame_TitlePage.grid(row = 0, column = 2, padx=10, pady=(100,0))
    Frame_TitleOnlyFrame = tk.CTkFrame(Frame_TitlePage)
    Frame_TitleOnlyFrame.grid(row = 0, column = 2, padx=100, pady=100)
    Label_Title = tk.CTkLabel(Frame_TitleOnlyFrame, text = "Data Analysis Tool")
    Label_Title.configure(font=('Eras Bold ITC', 50), anchor = 'center', pady=30, padx=30)
    Label_Title.grid(row = 0, column = 2, padx=10,pady=10)
    StartButton = tk.CTkButton(Frame_TitlePage,text="Get Started", command = startbutton_pressed)
    StartButton.configure(font=('Eras Medium ITC',15))
    StartButton.grid(row=1,column=2, padx=200, pady=50)
#""" Start of MAIN """

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

#""" End of MAIN """