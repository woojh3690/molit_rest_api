import logging
import datetime

class LogManger : 
    def __init__(self, name) :
        self.log = logging.getLogger(name)
        self.log.propagate = True
        self.formatter = logging.Formatter("[%(asctime)-15s] (%(filename)s:%(lineno)d) [%(levelname)s] - %(message)s", "%Y-%m-%d %H:%M:%S")

        self.level = {
            "DEBUG" : logging.DEBUG,
            "INFO" : logging.INFO,
            "WARNING" : logging.WARNING,
            "ERROR" : logging.ERROR,
            "CRITICAL" : logging.CRITICAL
        }
        
    
    def stream_handler(self, level) :
        streamHandler = logging.StreamHandler()
        #streamHandler.setLevel(self.level[level])
        streamHandler.setFormatter(self.formatter)
        self.log.addHandler(streamHandler)
        self.log.setLevel(self.level[level])
        return self.log
    
    def file_handler(self, file_path, mode, level) :
        fileHandler = logging.FileHandler(file_path, mode=mode)
        #fileHandler.setLevel(self.level[level])
        fileHandler.setFormatter(self.formatter)
        self.log.addHandler(fileHandler)
        self.log.setLevel(self.level[level])
        return self.log
    
    def rotating_file_handler(self, file_path, mode, level, backupCouont, log_max_size) :
        fileHandler = logging.handlers.RotatingFileHandler(
            filename = file_path,
            maxBytes = log_max_size,
            backupCount = backupCount,
            mode = mode
        )
        #fileHandler.setLevel(self.level[level])
        fileHandler.setFormatter(self.formatter)
        self.log.addHandler(fileHandler)
        self.log.setLevel(self.level[level])
        return self.log        

#log = LogManger("test_log")
#log = log.stream_handler("INFO")
#log = log.file_handler(file_path="/root/rest_api/log/test.log", mode="a", level="INFO")

#log.debug("~DEBUG~")
#log.info("~INFO~")
#log.warning("~WARNING~")
#log.error("~ERROR~")
#log.critical("~CRITICAL~")


