import logging
import logging.handlers

def ConfigureLogging(logLevel, name="full"):
    # nastavit logovani
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logLevel)

    # fileHandler = logging.handlers.TimedRotatingFileHandler(logFile, when="midnight", backupCount=30)
    fileHandler = logging.handlers.RotatingFileHandler(f"logs/{name}.log", maxBytes=100000000, backupCount=3)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler) 

    fileHandlerExceptions = logging.handlers.RotatingFileHandler("logs/exceptions.log", maxBytes=100000000, backupCount=3)
    fileHandlerExceptions.setFormatter(logFormatter)
    fileHandlerExceptions.setLevel(logging.ERROR)
    rootLogger.addHandler(fileHandlerExceptions) 
    
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)