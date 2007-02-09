staticPlot = function(fileName,dataSize){
  print(dataSize)
  print(fileName)

  # Read the data from the file
  file_data = scan(fileName,,(dataSize * 4))
  # List of variables used in this function
  linux_time = 0
  ac0 = 0
  ac1 = 0
  ac2 = 0
  data_min = 0
  data_max = 0
  plot_data = 0

  # Divide the data up into its respective category
  for(i in 1 : (dataSize * 4)) {
    if(i %% 4 == 1){
      linux_time[i/4 + 1] = file_data[i]
    }
    if(i %% 4 == 2){
      ac0[i/4 + 1] = file_data[i]
    }
    if(i %% 4 == 3){
      ac1[i/4 + 1] = file_data[i]
    }
    if(i %% 4 == 0){
      ac2[i/4] = file_data[i]
    }
  }

  # Compute the coordinate system
  # It is the min of the dataset and the max of the dataset
  data_min = min(ac0, ac1, ac2)
  data_max = max(ac0, ac1, ac2)
  # Construct a dataset with atleast one min and one max
  # so approximately half and half
  for(i in 1 : (dataSize %/% 2)) {
    plot_data[i] = data_min
  }
  for(i in ((dataSize %/% 2) + 1) : dataSize) {
    plot_data[i] = data_max
  }

  ## Plotting the graph
  # This plot sets up the coordinate system
  plot(linux_time, plot_data, type = "n")
  # Plot ac0
  points(linux_time, ac0, col = "blue")
  # Plot ac1
  points(linux_time, ac1, col = "red")
  # Plot ac2
  points(linux_time, ac2, col = "black")
}
