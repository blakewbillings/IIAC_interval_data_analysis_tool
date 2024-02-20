from datetime import timedelta
from dateutil import parser

class DataNormalizer:
    def parseDateTime(dateTime):
        try:
            splitted = dateTime.split()
            if (len(splitted) == 2): 
                time = splitted[1]
                if (time == "2400"):
                    time = "0000"
                    newDateTime = splitted[0] + ' ' + time
                    parsedDateTime = parser.parse(newDateTime)
                    parsedDateTime += timedelta(days=1)
                    return parsedDateTime.strftime("%Y-%m-%d %H:%M:%S")
            parsedDateTime = parser.parse(dateTime)
            return parsedDateTime.strftime("%Y-%m-%d %H:%M:%S")
  
        except parser.ParserError:
            splitted = dateTime.split()
            if (len(splitted) > 2):
                return DataNormalizer.parseDateTime(splitted[0] + ' ' + splitted[2])
        return dateTime

    def onlyNumbersTimeFix(time):
        time_length = len(time)
        match(time_length):
            case 1:
                time = f"00:0{time}:00"
            case 2:
                time = f"00:{time}:00"
            case 3:
                time = f"0{time[0]}:{time[1]}{time[2]}:00"
            case 4:
                time = f"{time[0]}{time[1]}:{time[2]}{time[3]}:00"
            case 5:
                time = f"0{time[0]}:{time[1]}{time[2]}:{time[3]}{time[4]}"
            case 6:
                time = f"{time[0]}{time[1]}:{time[2]}{time[3]}:{time[4]}{time[5]}"
        return time