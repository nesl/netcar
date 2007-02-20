calibrate = function(fileName) {
	l1 = read.table(fileName,head=T)

	start = 100
	maxTime = 10000
	H34Ccalib = 0.00880646
	# remove bogus data
	l1 = l1[l1$accel0 <= 1024 & l1$accel1 <= 1024 & l1$accel2 <= 1024,]
	l1 = l1[l1$time < maxTime & l1$accel0 > 0 & l1$accel1 > 0 & l1$accel2 > 0,]

	# calculate the mean of the first samples for calibration
	l1calib = mean(l1[1:start,])
	
	# calibrate the data
	l1$accel0 = H34Ccalib*(l1$accel0 - l1calib["accel0"])
	l1$accel1 = H34Ccalib*(l1$accel1 - l1calib["accel1"])
	l1$accel2 = H34Ccalib*(l1$accel2 - l1calib["accel2"])

        l1
}
