numatch = function(x,a){
  r = ((1:length(x))[abs(x-a)==min(abs(x-a))])[1]
  r = ((r-100):(r+100))
  r[r> 0 & r <= length(x)]
}
