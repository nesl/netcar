eventTimings = function(dataFile, eventFile, dataSize) {
# This function plots the density of the different events
# It requires the file with the data, file with the events and the size of data

  BIN_SIZE = 0.05
  MAX_TIME = 600
  THRESHOLD = 0.04
  
  source("numatch.R")
  source("calibrate.R")
  source("binData.R")

  # Calibrate the data and read in the events file
  data = calibrate(dataFile, dataSize)
  event = read.table(eventFile, sep = "\t", header = TRUE)

  # Calling mark's function on all the valid events 
  data$event = 0  
  for(i in 1:nrow(event)){
    # If we have run out of data, quit
    if (event[i,1] > data[length(data$time),1])
      break
    # Call the function
     cc = numatch(data[,1],event[i,1])
      data$event[cc] = event[i,2]
   }

  # Get the avg for when the car started
  start = data[data$event == 1,]
  start_avg = mean(start$accel0)

  bin_data = binData(data, MAX_TIME)

  for (i in 1:length(binData$time)) {
    if(abs(binData$accel0[i] - start_avg) > THRESHOLD) {
      print("found something")
    }
  }
}
