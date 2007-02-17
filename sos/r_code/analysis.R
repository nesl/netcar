analysis = function(logFile,eventFile,logDataSize,eventDataSize){

  # reading log_file and event_file data
  log_file_data = scan(logFile, ,logDataSize * 4)
  event_file_data = scan(eventFile, ,eventDataSize * 2)

  print("log_file_data")
  print(log_file_data)
  print("event_file_data")
  print(event_file_data)
  
  # List of variables used in this function
  linux_time = 0
  ac0 = 0
  ac1 = 0
  ac2 = 0

  # Divide the log_file data up into its respective category
  for(i in 1 : (logDataSize * 4)) {
    if(i %% 4 == 1){
      linux_time[i/4 + 1] = log_file_data[i]
    }
    if(i %% 4 == 2){
      ac0[i/4 + 1] = log_file_data[i]
    }
    if(i %% 4 == 3){
      ac1[i/4 + 1] = log_file_data[i]
    }
    if(i %% 4 == 0){
      ac2[i/4] = log_file_data[i]
    }
  }
  print("linux_time")
  print(linux_time)
  print("ac0")
  print(ac0)
  print("ac1")
  print(ac1)
  print("ac2")
  print(ac2)

}
