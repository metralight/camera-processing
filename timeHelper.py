import datetime

# univerzalni timestmap co se da pouzit i do nazvu slozky a souboru
def getTimestamp(millis=True):
    currentTime = datetime.datetime.now()
    return currentTime.strftime("%Y-%m-%d_%H-%M-%S" + (".%f" if millis == True else ""))

# pekny timestamp dovnitr souboru napr reports, bez milisekund
def getTimestampNiceVersion():
    currentTime = datetime.datetime.now()
    return currentTime.strftime("%Y-%m-%d %H:%M:%S")