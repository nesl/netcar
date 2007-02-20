tag = function(data, events) {

  data$event = 0
  
  for(i in 1:nrow(event)){
    # break if ran out of data
    if (event[i,1] > data(length(data%time), 1))
      break
    # Calling Mark's function
    cc = numatch(data[,1],event[i,1])
    data$event[cc] = event[i,2]
   }

  # Plotting the x acceleration against y and making it color coded
  plot(data$accel0, data$accel1, col = data$event)
}
