import customtkinter as tk
from tkinter import FALSE, TRUE, filedialog
import pandas as pd
from pandastable import Table

# Some nice things
# (All font types here = https://stackoverflow.com/questions/39614027/list-available-font-families-in-tkinter)

## Global Variables for function access
global df
global table
global desired_table
global IsDateTime;
desired_table = pd.DataFrame()
global Frame_TablePage

## This function opens file explorer for the user to
## select the desired excel file to be opened.
def open_file():
    global df
    global table
    global Frame_TablePage
    file_path = filedialog.askopenfilename(filetypes=[("XLSX Files", "*.xlsx")])

    if file_path:
        # Get the row number for labels
        #labels_row = int(label_labelsRowEntry.get())
        labels_row = int(5)
        
        # Read the Excel file using pandas
        #df = pd.read_excel(file_path, sheet_name=0, skiprows=lambda x: x < labels_row - 1)
        df = pd.read_excel(file_path, sheet_name=0, skiprows=lambda x: x < labels_row - 1)

        # Create dummy table
        #table = Table(frame_table, dataframe=df)
        table = Table(Frame_TablePage, dataframe=df)
        table.show()

#def retrieve_column():
#    global df
#    global table
#    global desired_table

#    # Get the selected column index
#    selected_column_index = table.getSelectedColumn()

#    # Check if a column is selected
#    if selected_column_index is not None:
#        # Get the column name from the dataframe
#        column_name = df.columns[selected_column_index]

#        # Retrieve the data from the selected column
#        column_data = df[column_name]

#        # Append the column data to the desired_table DataFrame
#        desired_table[column_name] = column_data

#        # Print the updated desired_table
#        print(desired_table)

#        # Check if three columns have been added to desired_table
#        if len(desired_table.columns) == 3:
#            # Create a new window to display the desired_table
#            window = tk.Toplevel()
#            window.title("Desired Table")

#            # Create the table from desired_table
#            table = Table(window, dataframe=desired_table)
#            table.show()

def DateTimeBool():
    global IsDateTime
    if IsDateTime is FALSE:
        IsDateTime = TRUE
    else:
        IsDateTime = FALSE

def uploadbutton_pressed():

    ### Still working on this method, as well as next steps after this ###
    global Frame_TablePage
    Frame_TablePage = tk.CTkFrame(app)
    Frame_TablePage.grid(row = 0, column = 2, padx=20, pady=(50,0))
    try: 
        open_file()
    except:
        startbutton_pressed

def startbutton_pressed():
    global IsDateTime
    IsDateTime = TRUE
    # Frame Initialization
    Frame_UploadPage = tk.CTkFrame(app)
    Frame_UploadPage.grid(row = 0, column=2, padx=20, pady=(50,0))

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
    #TODO: Use try-except for when the entry given is not an integer
    Label_Important = tk.CTkLabel(Frame_UploadPage, text = "IMPORTANT: Everything under the Labels will be considered data")
    Label_Important.configure(font=('Eras Medium ITC',10), anchor = 'center', pady=0, padx=30)
    Label_Important.grid(row = 5, column=2, padx=10, pady=2)
    
    # Section where we check if the date and timestamps are combined or not
    Label_DateTimeCheck = tk.CTkLabel(Frame_UploadPage, text = "Are Dates and Timestamps in the same column?")
    Label_DateTimeCheck.configure(font=('Eras Medium ITC',15), anchor = 'center', pady=30, padx=30)
    Label_DateTimeCheck.grid(row = 6, column = 2, padx=10, pady=0)
    check_var = tk.StringVar(value="on")
    CheckBox_DateTimeCheck = tk.CTkCheckBox(Frame_UploadPage, command=DateTimeBool, text = "Are Dates and Timestamps in the same column?", variable=check_var, onvalue = "on", offvalue = "off")
    CheckBox_DateTimeCheck.configure(font=('Eras Medium ITC',15))
    CheckBox_DateTimeCheck.grid(row = 7, column = 2, padx=10, pady=0)

    # Button to upload the excel file
    UploadButton_TitlePage = tk.CTkButton(Frame_UploadPage,text="Upload Excel File", command = uploadbutton_pressed)
    UploadButton_TitlePage.configure(font=('Eras Medium ITC',15))
    UploadButton_TitlePage.grid(row=8,column=2, padx=10, pady=80)


def CreateStartingPage():
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
#app.iconbitmap("ico.ico")
# configure grid system
#app.grid_rowconfigure(2, weight=1)  
app.grid_columnconfigure(2, weight=1)

CreateStartingPage()


## Starting Row for Table
#label_dataLabels = tk.Label(window, text="Insert Row Number in which Labels for the data are")
#label_dataLabels.pack()
#label_dataLabels_2 = tk.Label(window, text="(Everything under the label will be considered data):")
#label_dataLabels_2.pack()

## Entry Box for Starting Row for Table
#label_labelsRowEntry = tk.Entry(window)
#label_labelsRowEntry.pack()

## Add button to select the file from file explorer
#button = tk.Button(window, text="Open Excel File", command=open_file)
#button.pack()

## Create a frame to hold the table
#frame_table = tk.Frame(window)
#frame_table.pack()

## Add button to retrieve selected column data
#retrieve_button = tk.Button(window, text="Retrieve Column Data", command=retrieve_column)
#retrieve_button.pack()

## Start the GUI
app.mainloop()

#""" End of MAIN """