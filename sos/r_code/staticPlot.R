staticPlot = function(fileName,dataSize){
  print(dataSize)
  print(fileName)

  # Read the data from the file
  file_data = read.table(fileName,sep = "\t",header = TRUE,nrows = dataSize)

  print("done reading data")

  # List of variables used in this function
  linux_time = 0
  ac0 = 0
  ac1 = 0
  ac2 = 0
  data_min = 0
  data_max = 0
  plot_data = 0

  linux_time = file_data[,1]
  ac0 = file_data[,2]
  ac1 = file_data[,3]
  ac2 = file_data[,4]

  # Compute the coordinate system
  # It is the min of the dataset and the max of the dataset
  data_min = min(ac0, ac1, ac2)
  data_max = max(ac0, ac1, ac2)
    
  ## Plotting the graph
  plot_data = range(linux_time)
  ylimit = range(ac0,ac1,ac2)
  # This plot sets up the coordinate system
  #plot(linux_time,ac0, type = "n", xlim = plot_data, ylim = ylimit)
  # Plot ac0
  #points(linux_time, ac0, col = "blue",type = "l")
  pairs(cbind(ac0,ac1,ac2))
  # Plot ac1
  #points(linux_time, ac1, col = "red", type = "l")
  # Plot ac2
  #points(linux_time, ac2, col = "black", type = "l")
}
