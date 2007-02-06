staticPlot = function(fileName,dataSize)
{
  print(fileName)
  print(dataSize)

  fileData = scan(fileName,,(dataSize * 3))
  linuxTime = 0
  ac0 = 0
  ac1 = 0

  for(i in 1 : (dataSize * 3)) {
    if(i %% 3 == 1){
      linuxTime[i/3 + 1] = fileData[i]
    }
    if(i %% 3 == 2){
      ac0[i/3 + 1] = fileData[i]
    }
    if(i %% 3 == 0){
      ac1[i/3] = fileData[i]
    }
  }

  ## Plotting the graph
  plot(linuxTime, ac0)
}
