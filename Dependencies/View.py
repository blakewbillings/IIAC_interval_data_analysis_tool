import customtkinter as tk
from tkinter import filedialog
from pandastable import Table
import pandas as pd


class View:
    def __init__(self, controler):
        tk.set_appearance_mode("dark")
        app = tk.CTk()
        self.app = app
        self.controller = controler
        app.title("Data Analysis Tool")
        app.geometry("1000x1000")
        app.iconbitmap("ico.ico")
        app.grid_columnconfigure(2, weight=1)
    
    def createStartPage(self):
        titlePageFrame = tk.CTkFrame(self.app)
        self.titlePageFrame = titlePageFrame
        titlePageFrame.grid(row=0, column=2, padx=10, pady=(100, 0))
        titleOnlyFrame = tk.CTkFrame(titlePageFrame)
        titleOnlyFrame.grid(row=0, column=2, padx=100, pady=100)
        titleLabel = tk.CTkLabel(titleOnlyFrame, text="Data Analysis Tool")
        titleLabel.configure(font=("Eras Bold ITC", 50), anchor="center", pady=30, padx=30)
        titleLabel.grid(row=0, column=2, padx=10, pady=10)
        startButton = tk.CTkButton(titlePageFrame, text="Get Started", command=self.UploadPage)
        startButton.configure(font=("Eras Medium ITC", 15))
        startButton.grid(row=1, column=2, padx=200, pady=50)
        
    def UploadPage(self):
        # Frame Initialization
        uploadPageFrame = tk.CTkFrame(self.app)
        uploadPageFrame.grid(row=0, column=2, padx=20, pady=(50, 0))
        self.uploadPageFrame = uploadPageFrame
        rowRangeFrame = tk.CTkFrame(uploadPageFrame)
        rowRangeFrame.grid(row=3, column=2, padx=20, pady=(10, 0))

        # Remove TitlePage Frame
        self.titlePageFrame.grid_remove()

        # Title
        titleLabel = tk.CTkLabel(uploadPageFrame, text="Excel Format Setup")
        titleLabel.configure(font=("Eras Bold ITC", 40), anchor="center", pady=30, padx=210)
        titleLabel.grid(row=1, column=2, padx=10, pady=10)

        # Row Range Prompt.
        rowRangeLabel = tk.CTkLabel(uploadPageFrame, text="Indicate the range in which the data is located")
        rowRangeLabel.configure(font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30)
        rowRangeLabel.grid(row=2, column=2, padx=10, pady=0)

        # Starting Row Label
        startRowNumLabel = tk.CTkLabel(rowRangeFrame, text="Start (Labels' Row):")
        startRowNumLabel.configure(font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30)
        startRowNumLabel.grid(row=4, column=1, padx=10, pady=0)
        
        # Starting Row Entry
        startRowNumEntry = tk.CTkEntry(rowRangeFrame)
        startRowNumEntry.grid(row=4, column=2, padx=10, pady=0)
        self.startRowNumEntry = startRowNumEntry        

        # Ending Row Label
        endRowNumLabel = tk.CTkLabel(rowRangeFrame, text="End:")
        endRowNumLabel.configure(font=("Eras Medium ITC", 15), anchor="center", pady=20, padx=30)
        endRowNumLabel.grid(row=4, column=3, padx=10, pady=0)
        
        # Ending Row Entry
        endRowNumEntry = tk.CTkEntry(rowRangeFrame)
        endRowNumEntry.grid(row=4, column=4, padx=10, pady=0)
        self.endRowNumEntry = endRowNumEntry

        # Section where we check if the date and timestamps are combined or not
        check_var = tk.StringVar(value="on")
        CheckBox_DateTimeCheck = tk.CTkCheckBox(
            uploadPageFrame,
            text="Are Dates and Timestamps in the same column?",
            variable=check_var,
            onvalue="on",
            offvalue="off",
        )
        CheckBox_DateTimeCheck.configure(font=("Eras Medium ITC", 15))
        CheckBox_DateTimeCheck.grid(row=8, column=2, padx=10, pady=25)
        self.dateTimeCheckbox = CheckBox_DateTimeCheck

        # Button to upload the excel/csv file
        UploadButton_TitlePage = tk.CTkButton(uploadPageFrame, text="Upload Excel File", command=self.uploadButtonPressed)
        UploadButton_TitlePage.configure(font=("Eras Medium ITC", 15))
        UploadButton_TitlePage.grid(row=9, column=2, padx=10, pady=25)
    
    def uploadButtonPressed(self):
        if self.checkEntryFormat() == 1:
            filePath = filedialog.askopenfilename(filetypes=[("XLSX Files", "*.xlsx"), ("CSV Files", "*.csv")])
            self.controller.attemptFileOpening(filePath, int(self.startRowNumEntry.get()), int(self.endRowNumEntry.get()))
    
    def checkEntryFormat(self):
        FormatChecker = 1
        InvalidRowChecker = 1

        labels_row = self.Int32TryParse(self.startRowNumEntry.get())
        end_row = self.Int32TryParse(self.endRowNumEntry.get())
        Row_Entries = [self.startRowNumEntry, self.endRowNumEntry]

        for Row in Row_Entries:
            if self.Int32TryParse(Row.get()) == None:
                FormatChecker = self.FormatCheckingOnEntries(Row)
                InvalidRowChecker = -1

         # Check for the last row being lower than the first row
        if InvalidRowChecker == 1:
            if end_row <= labels_row:
                self.displayPopUpMessage(
                    f"Labels' Row '{end_row}' is smaller than or equal to Ending Row '{labels_row}'."
                )
                InvalidRowChecker = -1

         # Open file if everything looks like it follows the desired format
        if FormatChecker == 1 and InvalidRowChecker == 1:
            return 1
        return -1

    def FormatCheckingOnEntries(self, this):
        this.delete(0, len(this.get()))
        this.insert(0, "#ERROR")
        return -1

    def Int32TryParse(self, input):
        try:
            parsedInt = int(input)
            return parsedInt
        except ValueError:
            return None

    def displayPopUpMessage(self, message):
        ErrorPage = tk.CTkToplevel(self.app)
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

    def columnSelectionPage(self, df):
        # Clear GUI Frame
        self.uploadPageFrame.grid_remove()
        
        # Save values for future use
        self.fileDF = df
        self.counter = 1
        
        # Create GUI for Table column selection
        columnSelectorTitleFrame = tk.CTkFrame(self.app)
        columnSelectorTitleFrame.grid(row=0, column=2, padx=20, pady=(50, 0))

        # Frame for Title
        titleLabel = tk.CTkLabel(columnSelectorTitleFrame, text="Column Selection")
        titleLabel.configure(font=("Eras Bold ITC", 40), anchor="center", padx=20, pady=20)
        titleLabel.grid(row=0, column=2)

        # Frame for the Table
        frameTable = tk.CTkFrame(self.app)
        frameTable.grid(row=1, column=2, padx=20, pady=(50, 0))

        # Create table
        originalTable = Table(frameTable, dataframe=df)
        originalTable.show()
        self.originalTable = originalTable

        # Create new dataframe to hold formatted data
        self.filteredDF = pd.DataFrame(dtype=str)

        columnSelectorButtonsFrame = tk.CTkFrame(self.app)
        columnSelectorButtonsFrame.grid(row=2, column=2, padx=20, pady=(50, 0))

        # Check wether the checkbox was selected or not
        if (self.dateTimeCheckbox.get() == "off"):
            columnSelectionButton = tk.CTkButton(
                columnSelectorButtonsFrame,
                text="Select Date Column",
                command=self.retrieveThreeColumns,
            )
        else:
            columnSelectionButton = tk.CTkButton(
                columnSelectorButtonsFrame,
                text="Select Date/Time Column",
                command=self.retrieveTwoColumns,
            )

        columnSelectionButton.configure(font=("Eras Medium ITC", 15))
        columnSelectionButton.grid(row=2, column=2)
        self.columnSelectionButton = columnSelectionButton
    
    def FloatTryParse(self, input):
        try:
            parsedFloat = float(input)
            return parsedFloat
        except ValueError:
            return None

    def retrieveThreeColumns(self):
        # Change text on button depending on step
        if self.counter == 1:
            self.columnSelectionButton.configure(text="Select Time Column")
        if self.counter == 2:
            self.columnSelectionButton.configure(text="Select Power Column")

        # Get the selected column index
        selectedColumnIndex = self.originalTable.getSelectedColumn()
        
        # Check if a column is selected
        if selectedColumnIndex is not None:
        # Get the column name from the dataframe
            columnName = self.fileDF.columns[selectedColumnIndex]

        # Retrieve the data from the selected column
            columnData = self.fileDF[columnName]

        # Append the column data to the desired_table DataFrame
            self.filteredDF[columnName] = columnData

        # Rename Date/Time Table
            if self.counter == 1:
                self.filteredDF = self.filteredDF.rename(columns={columnName: "Date/Time"})
            if self.counter == 2:
                self.filteredDF = self.filteredDF.rename(columns={columnName: "temp"})

        # Check if three columns have been added to desired_table
            if len(self.filteredDF.columns) == 3:
                # Disable Button
                self.columnSelectionButton.configure(state="disabled")
                
                # Rename Power table
                self.filteredDF = self.filteredDF.rename(columns={columnName: "Power (kW)"})

                # Remove string from power table if any
                self.filteredDF["Power (kW)"] = self.filteredDF["Power (kW)"].astype(str)
                self.filteredDF["Power (kW)"] = self.filteredDF["Power (kW)"].str.replace("[a-zA-Z]", "", regex=True)
                self.filteredDF["Power (kW)"] = self.filteredDF["Power (kW)"].apply(self.FloatTryParse)
                    
                # Cast as string
                self.filteredDF["Date/Time"] = self.filteredDF["Date/Time"].astype(str)
                self.filteredDF["temp"] = self.filteredDF["temp"].astype(str)

                # Combine 'Date/Time' and 'temp' columns
                self.filteredDF["Date/Time"] = (self.filteredDF["Date/Time"] + " " + self.filteredDF["temp"])

                # Delete 'temp' column
                self.filteredDF = self.filteredDF.drop("temp", axis=1)
                # Normalize the data, and convert DateTime column elements into datetime objects
                self.filteredDF["Date/Time"] = self.filteredDF["Date/Time"].apply(lambda x: self.controller.normalizeDateTime(x))
                self.filteredDF["Date/Time"] = pd.to_datetime(self.filteredDF["Date/Time"])    
                
                # Get DailyProfile and DailyMaxMin
                self.dailyProfileDF = self.controller.getDailyProfile(self.filteredDF)
                self.dailyMaxMinDF  = self.controller.getDailyMaxMin(self.filteredDF)
                
                #Download Excel Files (Folder Creation TODO)
                self.filteredDF.to_excel('NormalizedIntervalData.xlsx')
                self.dailyProfileDF.to_excel('DailyProfile.xlsx')
                self.dailyMaxMinDF.to_excel('DailyMaxMin.xlsx')
                
                # Graph from Data and Download (Folder Creation TODO)
                self.controller.graphAndDownload(self.filteredDF, self.dailyProfileDF, self.dailyMaxMinDF)
                self.displayPopUpMessage("Done! Check the project folder to access the data generated!")

            # To make button text change
            self.counter = self.counter + 1
                
    def retrieveTwoColumns(self):
        if self.counter == 1:
            self.columnSelectionButton.configure(text="Select Power Column")
        
        # Get the selected column index
        selectedColumnIndex = self.originalTable.getSelectedColumn()
        
        # Check if a column is selected
        if selectedColumnIndex is not None:
        # Get the column name from the dataframe
            columnName = self.fileDF.columns[selectedColumnIndex]

        # Retrieve the data from the selected column
            columnData = self.fileDF[columnName]

        # Append the column data to the desired_table DataFrame
            self.filteredDF[columnName] = columnData

        # Rename Date/Time Table
            if self.counter == 1:
                self.filteredDF = self.filteredDF.rename(columns={columnName: "Date/Time"})
            if len(self.filteredDF.columns) == 2:
                # Disable Button
                self.columnSelectionButton.configure(state="disabled")                
                
                # Rename Power Column
                self.filteredDF = self.filteredDF.rename(columns={columnName: "Power (kW)"})
                
                # Remove string from power table if any
                self.filteredDF["Power (kW)"] = self.filteredDF["Power (kW)"].astype(str)
                self.filteredDF["Power (kW)"] = self.filteredDF["Power (kW)"].str.replace("[a-zA-Z]", "", regex=True)
                self.filteredDF["Power (kW)"] = self.filteredDF["Power (kW)"].apply(self.FloatTryParse)

                # Cast as string, normalize, and cast into a datetime object
                self.filteredDF["Date/Time"] = self.filteredDF["Date/Time"].astype(str)
                self.filteredDF["Date/Time"] = self.filteredDF["Date/Time"].apply(lambda x: self.controller.normalizeDateTime(x))
                self.filteredDF["Date/Time"] = pd.to_datetime(self.filteredDF["Date/Time"])
                
                # Get DailyProfile and DailyMaxMin
                self.dailyProfileDF = self.controller.getDailyProfile(self.filteredDF)
                self.dailyMaxMinDF  = self.controller.getDailyMaxMin(self.filteredDF)
                
                # Download Excel Files (Folder Creation TODO)
                self.filteredDF.to_excel('NormalizedIntervalData.xlsx')
                self.dailyProfileDF.to_excel('DailyProfile.xlsx')
                self.dailyMaxMinDF.to_excel('DailyMaxMin.xlsx')

                # Graph from Data and Download (Folder Creation TODO)
                self.controller.graphAndDownload(self.filteredDF, self.dailyProfileDF, self.dailyMaxMinDF)
                self.displayPopUpMessage("Done! Check the project folder to access the data generated!")
            self.counter = self.counter + 1
