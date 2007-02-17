tag = function(dataFile, eventFile) {

  DATASIZE = 10000
  
  data = read.table(dataFile, sep = "\t", header = TRUE, nrows = DATASIZE)
  event = read.table(eventFile, sep = "\t", header = TRUE, nrows = DATASIZE)

  # Remove bogus data when the accel value is too big
  data = data[data$accel0 <= 1024 & data$accel1 <= 1024 & data$accel2 <= 1024,]
  # Remove bogus data when the time is too large
  data = data[data[,1] <= 10000,]
  event = event[event[,1] <= 10000,]

  data$event = 0
  
  for(i in 1:nrow(event)){
     cc = numatch(data[,1],event[i,1])
      data$event[cc] = event[i,2]
   }

  plot(data$accel0, data$accel1, col = data$event)

}
