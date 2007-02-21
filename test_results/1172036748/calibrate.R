calibrate = function() {
	l1 = read.table("1.log",head=T)
	l2 = read.table("2.log",head=T)
	l3 = read.table("3.log",head=T)

	start = 5
        startend = 500
	maxTime = 600 
	H34Ccalib = 0.00880646
        binsize = 0.05
	# remove bogus data
	l1 = l1[l1$accel0 <= 1024 & l1$accel1 <= 1024 & l1$accel2 <= 1024,]
	l1 = l1[l1$time < maxTime & l1$accel0 > 0 & l1$accel1 > 0 & l1$accel2 > 0,]
	l2 = l2[l2$accel0 <= 1024 & l2$accel1 <= 1024 & l2$accel2 <= 1024,]
	l2 = l2[l2$time < maxTime & l2$accel0 > 0 & l2$accel1 > 0 & l2$accel2 > 0,]
        l3 = l3[l3$accel0 <= 1024 & l3$accel1 <= 1024 & l3$accel2 <= 
	l3 = l3[l3$time < maxTime & l3$accel0 > 0 & l3$accel1 > 0 & l3$accel2 > 0,]

	# calculate the mean of the first samples for calibration
	l1calib = mean(l1[start:startend,])
	l2calib = mean(l2[start:startend,])
	l3calib = mean(l3[start:startend,])
	
	# calibrate the data
	l1$accel0 = H34Ccalib*(l1$accel0 - l1calib["accel0"])
	l1$accel1 = H34Ccalib*(l1$accel1 - l1calib["accel1"])
	l1$accel2 = H34Ccalib*(l1$accel2 - l1calib["accel2"])
	l2$accel0 = H34Ccalib*(l2$accel0 - l2calib["accel0"])
	l2$accel1 = H34Ccalib*(l2$accel1 - l2calib["accel1"])
	l2$accel2 = H34Ccalib*(l2$accel2 - l2calib["accel2"])
	l3$accel0 = H34Ccalib*(l3$accel0 - l3calib["accel0"])
	l3$accel1 = H34Ccalib*(l3$accel1 - l3calib["accel1"])
	l3$accel2 = H34Ccalib*(l3$accel2 - l3calib["accel2"])


	# bin the results
        

        times = seq(1, maxTime, binsize)
        intervals = cut(l1$time, times)
        numintervals = as.numeric(intervals)
        l1binaccel0 = sapply(split(l1$accel0, numintervals), mean)
        l1binaccel1 = sapply(split(l1$accel1, numintervals), mean)
        l1binaccel2 = sapply(split(l1$accel2, numintervals), mean)
        l1times = as.numeric(names(l1binaccel0))*0.05 
        intervals = cut(l2$time, times)
        numintervals = as.numeric(intervals)
        l2binaccel0 = sapply(split(l2$accel0, numintervals), mean)
        l2binaccel1 = sapply(split(l2$accel1, numintervals), mean)
        l2binaccel2 = sapply(split(l2$accel2, numintervals), mean)
        l2times = as.numeric(names(l2binaccel0))*0.05
        intervals = cut(l3$time, times)
        numintervals = as.numeric(intervals)
        l3binaccel0 = sapply(split(l3$accel0, numintervals), mean)
        l3binaccel1 = sapply(split(l3$accel1, numintervals), mean)
        l3binaccel2 = sapply(split(l3$accel2, numintervals), mean)
        l3times = as.numeric(names(l3binaccel0))*0.05

y = data.frame(time=times, n1accel0=rep(NA, length(times)), n2accel0=rep(NA, length(times)), n3accel0=rep(NA, length(times)), n1accel1=rep(NA, length(times)), n2accel1=rep(NA, length(times)), n3accel1=rep(NA, length(times)), n1accel2=rep(NA, length(times)), n2accel2=rep(NA, length(times)), n3accel2=rep(NA, length(times)))

y$n1accel0[l1times] = l1binaccel0
y$n2accel0[l2times] = l2binaccel0
y$n3accel0[l3times] = l3binaccel0
y$n1accel1[l1times] = l1binaccel1
y$n2accel1[l2times] = l2binaccel1
y$n3accel1[l3times] = l3binaccel1
y$n1accel2[l1times] = l1binaccel2
y$n2accel2[l2times] = l2binaccel2
y$n3accel2[l3times] = l3binaccel2

#plot(y$n1accel0, y$n2accel0)
#lines(y$n1accel1, y$n2accel1, type='p', col='blue')
#lines(y$n1accel2, y$n2accel2, type='p', col='magenta')
END=length(times)
pairs(cbind(y$n1accel0[1:END], y$n2accel0[1:END], y$n1accel1[1:END], y$n2accel1[1:END], y$n1accel2[1:END], y$n2accel2[1:END]), names(y)[2:7], xlim=range(-1:1), ylim=range(-1:1))
pairs(cbind(y$n1accel0[1:END], y$n3accel0[1:END], y$n1accel1[1:END], y$n3accel1[1:END], y$n1accel2[1:END], y$n3accel2[1:END]), c(names(y)[2:4],names(y)[8:10]), xlim=range(-1:1), ylim=range(-1:1))
pairs(cbind(y$n3accel0[1:END], y$n2accel0[1:END], y$n3accel1[1:END], y$n2accel1[1:END], y$n3accel2[1:END], y$n2accel2[1:END]), names(y)[5:10], xlim=range(-1:1), ylim=range(-1:1))

