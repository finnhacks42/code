#Generate a plot of event-pair occurence for burglaries
#Same as figure1-right of "Self-exciting point process modelling of crime"

plot_event_pairs <- function(event_vector){

  len <- length(event_vector[event_vector != 0] - 1)
  result_vector <- list()
  
  i <- 1
  while (i < length(event_vector)){
    if (event_vector[i] != 0){
      k <- i + 1
      
      while (k <= length(event_vector) & event_vector[k] == 0) {
        k <- k + 1
      }
      if (k > length(event_vector)) break
      
      result_vector[length(result_vector)+1] <- list(k-i)
      i <- k - 1
    }
    i <- i + 1
  }
                     
  plot(table(as.numeric(result_vector))/length(result_vector), xlab="burglary pairs", ylab="frequency")
}