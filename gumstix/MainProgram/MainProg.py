import GPSmodule
import Accel
import SlogModule
import time

if(__name__ == "__main__"):
    GPS = GPSmodule
    ACC = Accel
    ##GPSSLOG = SlogModule
    ##ACCSLOG = SlogModule
    SLOG = SlogModule
    GPS.GPSmodule()
    Accel.AccXMLPut()
    time.sleep(5)
    while True:
        SLOG.DataSlog().ChangeDB('kimyh@ucla.edu','password','85','Accel')
        SLOG.DataSlog().ChangeXML(GPS.GPSXMLqueue.get())
        SLOG.DataSlog().Slog()
        SLOG.DataSlog().ChangeDB('kimyh@ucla.edu','password','85','GPS')
        SLOG.DataSlog().ChangeXML(ACC.AccXMLQueue.get())
        SLOG.DataSlog().Slog()
        
        
