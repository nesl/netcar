correlationPlot = function() {
        source("calibrate.R")
        source("binData.R")
        
        maxTime = 600

        d1 = calibrate("1.log", -1)
        d2 = calibrate("2.log", -1)
        d3 = calibrate("3.log", -1)

        # create the same bins for all the data
        bd1 = binData(d1, maxTime)
        bd2 = binData(d2, maxTime)
        bd3 = binData(d3, maxTime)

        pairs(cbind(bd1$accel0, bd2$accel0, bd3$accel0), c("node1", "node2", "node3"), xlim=range(-1,1), ylim=range(-1,1), title="Accel0")
      }
