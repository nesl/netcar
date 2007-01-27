import GPSmodule
import Accel
import SlogModule
import time

if(__name__ == "__main__"):
    GPS = GPSmodule
    ACC = Accel
    ##GPSSLOG = SlogModule
    ##ACCSLOG = SlogModule
    SLOG = SlogModule.DataSlog()
    GPS.GPSmodule()
    Accel.AccXMLPut()
    time.sleep(5)
    while True:
        SLOG.ChangeDB('kimyh@ucla.edu','password','85','GPS')
        XML = GPS.GPSXMLqueue.get()
	SLOG.ChangeXML(XML)
        SLOG.Slog()
        SLOG.ChangeDB('kimyh@ucla.edu','password','85','Accel')
	XML =  ACC.AccXMLQueue.get()
        SLOG.ChangeXML(XML)
        SLOG.Slog()
        
        
