function(file-name,data-size)
{
  ## Size of the Dataset
  DATA_SIZE = 9
  ## Name of the file
  FILE_NAME = "test.log"

  file_data = scan(FILE_NAME,,DATA_SIZE)
  linux_time = 0
  ac0 = 0
  ac1 = 0

  for(i in 1 : DATA_SIZE) {
    if(i %% 3 == 1){
      linux_time[i/3 + 1] = file_data[i]
    }
    if(i %% 3 == 2){
      ac0[i/3 + 1] = file_data[i]
    }
    if(i %% 3 == 0){
      ac1[i/3] = file_data[i]
    }
  }

  ## Plotting the graph
  plot(linux_time, ac0)
}
