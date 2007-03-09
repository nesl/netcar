calibrate = function(fileName, dataSize) {
# This function calibrates the dataset
# It requires the name of the file and the size of dataset

  # Denote the initial calibration time
  START = 10
  STARTEND = 500
  # Used for corruption of data packets
  MAX_ACCEL = 1024
  # Used for corruption of time stamp
  # This is a heuristic value, time values increasing this number are considered to be incorrect
  THRESHOLD = 50
  # To convert from adc readings to gs
  H34C_CALIB = 0.00880646

  # Read the data file
  data = read.table(fileName, head = T, nrows = dataSize)

  # remove bogus data based on corruption of acceleration data
  # Any acceleration value greater than MAX_ACCEL is removed
  data = data[data$accel0 <= MAX_ACCEL & data$accel1 <= MAX_ACCEL & data$accel2 <= MAX_ACCEL,]
  data = data[data$accel0 > 0 & data$accel1 > 0 & data$accel2 > 0,]

  # remove bogus data based on corruption of time stamp
  # compute a matrix of TRUE and FALSE which is typically TRUE
  # and false if the subsequent sample is smaller or bigger than
  # the threshold

  # Generate a matrix of same length as data
  data_set = 0
  length(data_set) = length(data$time)
  # The initial values are kept as unchanged
  data_set[1:START] = TRUE

  valid = START
  for(i in START:(length(data$time) - 1)) {
    # assume that the data point at START is a valid data point
    # remove the next data point if it is smaller than this data point
    if(data$time[valid] > data$time[i + 1]) {
      data_set[i + 1] = FALSE
    }
    # remove the next data point if it is bigger than the allowed THRESHOLD
    # The THRESHOLD is used to account for packet lossese 
    else if((data$time[i + 1] - data$time[valid]) > THRESHOLD) {
      data_set[i + 1] = FALSE
    }
    # else this is a good data sample
    else {
      valid = i + 1
      data_set[i + 1] = TRUE
    }
  }

  # assign to data only those values which are marked TRUE
  data = data[data_set == TRUE,]

  # calculate the mean of the first samples for calibration
  datacalib = mean(data[START:STARTEND,])

  # calibrate the data
  data$accel0 = H34C_CALIB * (data$accel0 - datacalib["accel0"])
  data$accel1 = H34C_CALIB * (data$accel1 - datacalib["accel1"])
  data$accel2 = H34C_CALIB * (data$accel2 - datacalib["accel2"])
  
  # Return the data set
  data
}
