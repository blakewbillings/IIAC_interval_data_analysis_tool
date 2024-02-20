import pandas as pd
import os

class FileOpener:
    
    @staticmethod
    def openFile(filePath, startRow, endRow):
        if filePath.endswith(".csv"):
            # Convert CSV to Excel
            excelFilePath = os.path.splitext(filePath)[0] + ".xlsx"
            dataFrame = pd.read_csv(filePath, dtype=str)
            dataFrame.to_excel(excelFilePath, index=False)
            filePath = excelFilePath  # Update filePath with the Excel file path

        if filePath:
            # Disable the natural datetime formatting
            pd.set_option('display.date_dayfirst', False)
            pd.set_option('display.date_yearfirst', False)

            # Read the Excel file using pandas
            df = pd.read_excel(filePath, sheet_name=0, dtype=str, skiprows=lambda x: x < startRow - 1, nrows=endRow - startRow)
            return df

        raise ValueError("File path is empty or invalid")