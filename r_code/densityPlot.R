densityPlot = function(dataFile, eventFile, dataSize) {
# This function plots the density of the different events
# It requires the file with the data, file with the events and the size of data

  # define which events this should do the plotting for
  EVENT1 = 3
  EVENT2 = 4
  
  source("numatch.R")
  source("calibrate.R")

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

  # Generate the plots
  plot(density(data$accel0[data$event==EVENT2]),type="l",col=6)
  lines(density(data$accel0[data$event==EVENT1]),type="l",col=5)  
}
