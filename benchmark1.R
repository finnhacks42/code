#Those are benchmark predictors for the classification of {increase, DO NOT increase} tomorrow.
#The script assumes the data is in the format returned by make_dataaset1, in data.frame D and label
#Frequencies are calculated only up to the second last year (2006), leaving 2007 for testing

n_beat <- 375
n_instances <- nrow(D)
cut <- floor(n_instances/8*7)

#Estimate the naive frequence of increasing crime in a unknown day
naive_freq <- sum(label[1:cut]==+1) / cut
#Print model accuracy
print(max(naive_freq,1-naive_freq))

#Estimates the frequences of increasing crime the day after a fixed day i
day_index <- (2 * n_beat) 
day_freq <- rep(0,7)
for (i in 1:7){
  days <- which(D[1:cut,day_index+i] == 1, arr.ind=TRUE)
  day_freq[i] <- sum(label[days]==1) / length(days)
}
#Print model accuracies
print(pmax(day_freq,1-day_freq))

#Estimates the frequences of increasing crime the day after a fixed day i, in a month j
month_index <- (2 * n_beat + 7) 
month_freq <- matrix(0,nrow=7,ncol=12)
for (i in 1:7){
  for (j in 1:12){
    days <- which(D[1:cut,day_index+i] == 1 & D[1:cut,month_index+j] == 1, arr.ind=TRUE)
    month_freq[i,j] <- sum(label[days]==1) / length(days)
  }
}
#Print model accuracies
print(pmax(month_freq,1-month_freq))
