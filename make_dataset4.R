#Given a dataset xx made by clean_data.R, this script build one instance per day between year 2000 and 2006 per date
#included with a feature space defined as follow.
#  

#This function selects only "soft crimes" in the dataset
soft_crime <- function(data) {
  data[grep("VICE|FOUND PROPERTY|MISCHIEF|DISORDERLY CONDUCT|DRUNK|FENCE", data$description, ignore.case=T),]
}

library(lubridate)

#Cut off date after from 2007
xxx <- xx[year(xx$rep_date) < 2007,]
n_beat <- max(xxx$beat)

date_min <- min(xxx$rep_date)
date_max <- max(xxx$rep_date)
date_list <- seq(date_min,date_max,"days") #produces a sequence of dates, one for every day between date_min and date_max
n_date <- length(date_list)

#Features extraction

# produces a data frame with columns: beat,rep_date,count, where count is the sum of the number of burglaries in that beat on that date.
aggr_burglary <- aggregate(data=xxx[xxx$description == "BURGLARY",], count ~ beat + rep_date, FUN=sum)

# simple features ...
library(sqldf)
tmp <- sqldf('select beat, rep_date, sum(description="BURGLARY") as burglaries from xx group by beat,rep_date') # this is a sparce df - days where the result is 0 are not represented

D <- matrix(0, nrow=length(date_list-1)*n_beat, ncol=4)



index = 1
for (date in 2:n_date) { # we are iterating through all the days and beats and building a feature for each day, beat combination
  for (beat in 1:n_beat) {
   
    # feature of length d + 1 representing burglaries in this beat today and on the previous d days.
    burglary <- rep(0,2)
    for (d in 0:1){
      temp <- aggr_burglary[aggr_burglary$rep_date == date_list[index-d] & aggr_burglary$beat == beat,c("count")]
      if (length(temp) != 0){
        burglary[d+1] <- temp
      }
    }
    
    D[index,] <- c(burglary)
   
    index <- index + 1
  }
}



#Labels creation.
#Number of crimes tomorrow in beat 96
label <- D[2:n_date,96]

#Then get rid of the last row of D because we don't have a label for the following day
D <- D[1:(n_date-1),]

#Get rid of the first 14 instances because the way we compute the features
D <- D[-c(1:14),]
label <- label[-c(1:14)]

#Normalise numerical features
D[,1:(ncol(D)-20)] <- scale(D[,1:(ncol(D)-20)])
#NaN <- 0
D <- apply(D,c(1,2),function(x){if (is.nan(x)) 0.0 else x})

save(D, label, file="/Users/giorgio/Desktop/crime prediction/Rdata/dataset3.R")



#TEST: USE AVERAGED LABEL OF THE NEXT WEEK
library(gtools)
label <- running(label, width=7)
D <- D[1:(nrow(D)-6),]
