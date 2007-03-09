staticPlot = function(fileName, dataSize){
# This code simply plots a graph of the all three acceleration components
# Specify the file name and the data size to analysis
  
  # List of variables used in this function
  data_min = 0
  data_max = 0
  plot_data = 0

  # Get calibrated data
  source("calibrate.R")
  data = calibrate(fileName, dataSize)

  ## Plotting the graph
  xlimit = range(data$time)
  ylimit = range(data$accel0, data$accel1, data$accel2)
  # This plot sets up the coordinate system
  plot(data$time, data$accel0, type = "n", xlim = xlimit, ylim = ylimit)
  # Plot ac0
  points(data$time, data$accel0, col = "blue",type = "l")
  # Plot ac1
  points(data$time, data$accel1, col = "red", type = "l")
  # Plot ac2
  points(data$time, data$accel2, col = "black", type = "l")
  #pairs(cbind(ac0,ac1,ac2))
}
