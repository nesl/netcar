staticPlot = function(fileName,dataSize){
  source("calibrate.R")

  # List of variables used in this function
  linux_time = 0
  ac0 = 0
  ac1 = 0
  ac2 = 0
  data_min = 0
  data_max = 0
  plot_data = 0

  cali_data = calibrate(fileName)
  linux_time = cali_data[1:dataSize,1]
  ac0 = cali_data[1:dataSize,2]
  ac1 = cali_data[1:dataSize,3]
  ac2 = cali_data[1:dataSize,4]

  ## Plotting the graph
  xlimit = range(linux_time)
  ylimit = range(ac0,ac1,ac2)
  # This plot sets up the coordinate system
  plot(linux_time, ac0, type = "n", xlim = xlimit, ylim = ylimit)
  # Plot ac0
  points(linux_time, ac0, col = "blue",type = "l")
  # Plot ac1
  points(linux_time, ac1, col = "red", type = "l")
  # Plot ac2
  points(linux_time, ac2, col = "black", type = "l")
  #pairs(cbind(ac0,ac1,ac2))
}
