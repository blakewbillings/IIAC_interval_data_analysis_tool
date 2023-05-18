import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pandastable import Table

# Global Variables for function access
global df
global table
global desired_table
desired_table = pd.DataFrame()

# This function opens file explorer for the user to
# select the desired excel file to be opened.
def open_file():
    global df
    global table
    file_path = filedialog.askopenfilename(filetypes=[("XLSX Files", "*.xlsx")])

    if file_path:
        # Get the row number for labels
        labels_row = int(label_labelsRowEntry.get())

        # Read the Excel file using pandas
        df = pd.read_excel(file_path, sheet_name=0, skiprows=lambda x: x < labels_row - 1)

        # Create dummy table
        table = Table(frame_table, dataframe=df)
        table.show()

def retrieve_column():
    global df
    global table
    global desired_table

    # Get the selected column index
    selected_column_index = table.getSelectedColumn()

    # Check if a column is selected
    if selected_column_index is not None:
        # Get the column name from the dataframe
        column_name = df.columns[selected_column_index]

        # Retrieve the data from the selected column
        column_data = df[column_name]

        # Append the column data to the desired_table DataFrame
        desired_table[column_name] = column_data

        # Print the updated desired_table
        print(desired_table)

        # Check if three columns have been added to desired_table
        if len(desired_table.columns) == 3:
            # Create a new window to display the desired_table
            window = tk.Toplevel()
            window.title("Desired Table")

            # Create the table from desired_table
            table = Table(window, dataframe=desired_table)
            table.show()

""" Start of MAIN """

# Create GUI
window = tk.Tk()
window.title("Excel File Choosing")

# Title
label_title = tk.Label(window, text="Excel Format Setup")
label_title.pack(pady=10)

# Starting Row for Table
label_dataLabels = tk.Label(window, text="Insert Row Number in which Labels for the data are")
label_dataLabels.pack()
label_dataLabels_2 = tk.Label(window, text="(Everything under the label will be considered data):")
label_dataLabels_2.pack()

# Entry Box for Starting Row for Table
label_labelsRowEntry = tk.Entry(window)
label_labelsRowEntry.pack()

# Add button to select the file from file explorer
button = tk.Button(window, text="Open Excel File", command=open_file)
button.pack()

# Create a frame to hold the table
frame_table = tk.Frame(window)
frame_table.pack()

# Add button to retrieve selected column data
retrieve_button = tk.Button(window, text="Retrieve Column Data", command=retrieve_column)
retrieve_button.pack()

# Start the GUI
window.mainloop()

""" End of MAIN """
