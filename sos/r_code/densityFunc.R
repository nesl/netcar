densityFunc = function(dataFile, eventFile) {

  source("numatch.R")
  DATASIZE = 10000
  
  data = calibrate(dataFile)
  event = read.table(eventFile, sep = "\t", header = TRUE, nrows = DATASIZE)

  data$event = 0
  
  for(i in 1:nrow(event)){
     cc = numatch(data[,1],event[i,1])
      data$event[cc] = event[i,2]
   }

  plot(density(data$accel0[data$event==4]),type="l",col=6)
  lines(density(data$accel0[data$event==3]),type="l",col=5)  
}
