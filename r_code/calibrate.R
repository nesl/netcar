# This function calibrates the dataset
# It requires the name of the file and the size of dataset
calibrate = function(fileName, dataSize) {

  # Denote the initial calibration time
  START = 100
  # Used for corruption of packets
  MAX_TIME = 10000
  MAX_ACCEL = 1024
  # To convert from adc readings to gs
  H34C_CALIB = 0.00880646

  # Read the file
  l1 = read.table(fileName, head = T, nrows = dataSize)
  
  # remove bogus data based on packet corruption
  l1 = l1[l1$accel0 <= MAX_ACCEL & l1$accel1 <= MAX_ACCEL & l1$accel2 <= MAX_ACCEL,]
  l1 = l1[l1$time < MAX_TIME & l1$accel0 > 0 & l1$accel1 > 0 & l1$accel2 > 0,]
  
  # calculate the mean of the first samples for calibration
  l1calib = mean(l1[1:START,])
  
  # calibrate the data
  l1$accel0 = H34C_CALIB * (l1$accel0 - l1calib["accel0"])
  l1$accel1 = H34C_CALIB * (l1$accel1 - l1calib["accel1"])
  l1$accel2 = H34C_CALIB * (l1$accel2 - l1calib["accel2"])

  # Return the data set
  l1
}
