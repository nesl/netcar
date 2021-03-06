binData = function(data, maxTime) {
        # size of the bins over which we average
        binsize = 0.05

        # create the full number of bins
        times = seq(1, maxTime, binsize)
        intervals = cut(data$time, times)
        numintervals = as.numeric(intervals)
        binaccel0 = sapply(split(data$accel0, numintervals), mean)
        binaccel1 = sapply(split(data$accel1, numintervals), mean)
        binaccel2 = sapply(split(data$accel2, numintervals), mean)
        datatimes = as.numeric(names(binaccel0))
        
        y = data.frame(time=times, accel0 = rep(NA, length(times)), accel1 = rep(NA, length(times)), accel2 = rep(NA, length(times)))
        y$accel0[datatimes] = binaccel0
        y$accel1[datatimes] = binaccel1
        y$accel2[datatimes] = binaccel2
        y
}
