calibrate = function() {
	l1 = read.table("1.log",head=T)
	l2 = read.table("2.log",head=T)
	l3 = read.table("3.log",head=T)

	start = 100
	maxTime = 10000
	H34Ccalib = 0.00880646
	# remove bogus data
	l1 = l1[l1$accel0 <= 1024 & l1$accel1 <= 1024 & l1$accel2 <= 1024,]
	l1 = l1[l1$time < maxTime & l1$accel0 > 0 & l1$accel1 > 0 & l1$accel2 > 0,]
	l2 = l2[l2$accel0 <= 1024 & l2$accel1 <= 1024 & l2$accel2 <= 1024,]
	l2 = l2[l2$time < maxTime & l2$accel0 > 0 & l2$accel1 > 0 & l2$accel2 > 0,]
	l3 = l3[l3$accel0 <= 1024 & l3$accel1 <= 1024 & l3$accel2 <= 1024,]
	l3 = l3[l3$time < maxTime & l3$accel0 > 0 & l3$accel1 > 0 & l3$accel2 > 0,]

	# calculate the mean of the first samples for calibration
	l1calib = mean(l1[1:start,])
	l2calib = mean(l2[1:start,])
	l3calib = mean(l3[1:start,])
	
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
}
