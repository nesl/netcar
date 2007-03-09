correlationPlot = function(validEvents) {
        source("calibrate.R")
        source("binData.R")
        source("markData.R")
        
        maxTime = 600
        eventFile = "event.log"

        d1 = calibrate("1.log", -1)
        d2 = calibrate("2.log", -1)
        d3 = calibrate("3.log", -1)

        # create the same bins for all the data
        bd1 = binData(d1, maxTime)
        bd2 = binData(d2, maxTime)
        bd3 = binData(d3, maxTime)

        #mark the data with events
        bd1 = markData(bd1, eventFile)
        bd2 = markData(bd2, eventFile)
        bd3 = markData(bd3, eventFile)
        
        bd1 = bd1[bd1$event == 3 & bd1$event == 4]
        bd2 = bd2[bd2$event == 3 & bd2$event == 4]
        bd3 = bd3[bd3$event == 3 & bd3$event == 4]

        pairs(cbind(bd1$accel0, bd2$accel0, bd3$accel0), c("node1", "node2", "node3"), xlim=range(-1,1), ylim=range(-1,1), title="Accel0", col=bd1$event)
        event = read.table(eventFile, sep = "\t", header = TRUE)
        legend("bottomright", legend=unique(event$event), fill=as.numeric(unique(event$event)), inset=c(0.15, 0.05), text.width=20)

}
