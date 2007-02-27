# This function calibrates the dataset
# It requires the name of the file and the size of dataset
calibrate = function(fileName, dataSize) {

  # Denote the initial calibration time
  START = 100
  # Used for corruption of data packets
  MAX_ACCEL = 1024
  # Used for corruption of time stamp
  PERIOD = 1/50
  THRESHOLD = 50
  # To convert from adc readings to gs
  H34C_CALIB = 0.00880646

  # Read the data file
  data = read.table(fileName, head = T, nrows = dataSize)

  # remove bogus data based on corruption of acceleration data
  data = data[data$accel0 <= MAX_ACCEL & data$accel1 <= MAX_ACCEL & data$accel2 <= MAX_ACCEL,]

  data_set = 0
  length(data_set) = length(data$time)
  data_set[1:START] = TRUE

  # remove bogus data based on corruption of time stamp
  for(i in START:(length(data$time) - 1)) {
    # assume that the data point at START is a valid data point
    # remove the next data point if it is smaller than this data point
    if(data$time[i] > data$time[i + 1]) {
      print("deleted data less than time")
      data_set[i + 1] = FALSE
    }
    # remove the next data point if it is bigger than the allowed THRESHOLD
    # The THRESHOLD is used to account for packet lossese 
    else if((data$time[i] - data$time[i + 1]) > THRESHOLD) {
      data_set[i + 1] = FALSE
      print("deleted data more than time")
    }
    else {
      data_set[i + 1] = TRUE
    }
  }

  print("done")
  
  data = data[data_set == TRUE,]

  data
  
  # calculate the mean of the first samples for calibration
#  datacalib = mean(data[1:START,])
  
  # calibrate the data
#  data$accel0 = H34C_CALIB * (data$accel0 - datacalib["accel0"])
#  data$accel1 = H34C_CALIB * (data$accel1 - datacalib["accel1"])
#  data$accel2 = H34C_CALIB * (data$accel2 - datacalib["accel2"])

  # Return the data set
#  data
}
