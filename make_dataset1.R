#Given a dataset xx made by clean_data.R, this script build one instance per day between year 2000 and 2007
#included with a feature space defined as follow.
#   X^d = (#crime_day_d_beat_1, #crime_day_d_beat_2, ..., #crime_day_d_beat_N )
#  instance_day_d = (X^d, X^d-X^(d-1), binary_indicator_day, binary_indicator_month, 1)

library(lubridate)

#Cut off date after from 2008 on
xxx <- xx[year(xx$rep_date) < 2008,]

n_beat <- max(xxx$beat)
date_list <- sort(unique(xxx$rep_date))
n_date <- length(date_list)

aggr1 <- aggregate(data=xxx, count ~ beat + rep_date, FUN=sum)

D <- matrix(0, nrow=length(date_list), ncol=(2*n_beat + 7 + 12 + 1))

yesterday_crime <- rep(0, n_beat)

for (index in 1:n_date) {  
  today_crime <- rep(0, n_beat)
  v <- aggr1[aggr1$rep_date == date_list[index], c("count", "beat")]
  today_crime[match(as.vector(v$beat), 1:n_beat)] <- v$count #Copy the number of crime only in the right beat positions
  
  day <- rep(0,7)
  day[wday(date_list[index])] = 1
  
  month <- rep(0,12)
  month[month(date_list[index])] = 1
  
  D[index,] <- c(today_crime, today_crime - yesterday_crime, day, month, 1)
  
  yesterday_crime <- today_crime
}

rm(xxx)

#Labels creation.
#Number of crimes tomorrow in beat 96 (tho most criminal)
#label <- D[2:n_date,96]
#Binary: -1 crime in beat 96 DO NOT DECREASE from yesterday, +1 crime INCREASE from yesterday
label <- sign(D[2:n_date,96] - D[1:(n_date-1),96])
label[label==0] <- -1

#Then get rid of the last row of D because we don't have a label for the following day
D <- D[1:(n_date-1),]

#Normalise numerical features (# = 2*n_beat)
D[,1:(2*n_beat)] <- scale(D[,1:(2*n_beat)])
#NaN <- 0
D <- apply(D,c(1,2),function(x){if (is.nan(x)) 0.0 else x})

save(D, label, file="/Users/giorgio/Desktop/crime prediction/Rdata/dataset1.R")
