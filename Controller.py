from Dependencies import View
from Dependencies.FileOpener import FileOpener
from Dependencies.dataNormalizer import DataNormalizer
from Dependencies.dataAnalyzer import DataAnalyzer
from Dependencies.Grapher import Grapher

class Controller:
    """
        Class/Method Template
    """
    def __init__(self):
        """
            Initialize the <Class Name> object.
        """
        self.GUI = View.View(self)

    def attemptFileOpening(self, filePath, startRow, endRow):
        """
            This method ... .
            
            Args:
                param1 (<type>): The first parameter.
            
            Returns:
                <type>: <what it returns>
        """
        try:
            fileDF = FileOpener.openFile(filePath, startRow, endRow)
            self.fileDF = fileDF
            self.GUI.columnSelectionPage(fileDF)
        except ValueError as e:
            print(f"Error: {e}")

    def normalizeDateTime(self, dateTime):
        return DataNormalizer.parseDateTime(dateTime)
    
    def onlyNumbersTimeFix(self, time):
        return DataNormalizer.onlyNumbersTimeFix(time)

    def getDailyMaxMin(self, intervalDataFrame):
        return DataAnalyzer.dailyMaxMin(intervalDataFrame)
        
    def getDailyProfile(self, intervalDataFrame):
        return DataAnalyzer.dailyProfile(intervalDataFrame)
    
    def graphAndDownload(self, formattedDF, dailyProfileDF, maxMinDF):
        Grapher(formattedDF, dailyProfileDF, maxMinDF).graphAll()

# Main
if __name__ == "__main__":
    controller = Controller()
    controller.GUI.createStartPage()
    controller.GUI.app.mainloop()
    
