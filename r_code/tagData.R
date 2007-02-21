tag = function(data, events) {

  data$event = 0
  
  for(i in 1:nrow(events)){
    # break if ran out of data
    #if (events[i,1] > data[nrow(data),1])
    #  break
    # Calling Mark's function
    cc = numatch(data[,1],events[i,1])
    data$event[cc] = events[i,2]
  }

  # Plotting the x acceleration against y and making it color coded
  plot(data$accel0, data$accel1, col = data$event)
}
