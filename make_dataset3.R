#Given a dataset xx made by clean_data.R, this script build one instance per day between year 2000 and 2006
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
date_list <- seq(date_min,date_max,"days")
n_date <- length(date_list)

#Features extraction
aggr_burglary <- aggregate(data=xxx[xxx$description == "BURGLARY",], count ~ beat + rep_date, FUN=sum)

### NOTE: HERE WE CHANGE THE n_beat to save space. Beat between 263 and 374 never reported burglaries.
n_beat <- max(aggr_burglary$beat)


xxx_96 <- xxx[xxx$beat == 96,]
aggr_soft_crime <- aggregate(data=soft_crime(xxx_96), count ~ rep_date, FUN=sum)
xxx_burglary <- xxx_96[xxx_96$description == "BURGLARY",]
aggr_burglary_residence <- aggregate(data=xxx_burglary[grep("^RESIDENCE", xxx_burglary$premises, ignore.case=T),], count ~ rep_date, FUN=sum)
aggr_burglary_watch <- aggregate(data=xxx_burglary, count ~ watch + rep_date, FUN=sum)

aggr_bmv <- aggregate(data=xxx[xxx$description == "BMV" & xxx$beat == 96,], count ~ rep_date, FUN=sum)
aggr_robbery <- aggregate(data=xxx[xxx$description == "ROBBERY" & xxx$beat == 96,], count ~ rep_date, FUN=sum)

D <- matrix(0, nrow=length(date_list-14), ncol=(7*n_beat + 14*2 + 14*4*2 + 14*2 + 14*2 + 14*2 + 7 + 12 + 1))

yday_soft_crime <- rep(0,14)
yday_residence_burglary <- rep(0,14)
yday_watch_burglary <- rep(0,14)
yday_bmv <- rep(0,14)
yday_robbery <- rep(0,14)

for (index in 14:n_date) {
  
  #Day and month vectors
  day <- rep(0,7)
  day[wday(date_list[index])] = 1
  month <- rep(0,12)
  month[month(date_list[index])] = 1
  
  #Soft crime in beat=96 in the last 2 weeks
  soft_crime <- rep(0, 14)
  for (d in 0:13){
    temp <- aggr_soft_crime[aggr_soft_crime$rep_date == date_list[index] - d, c("count")]
    if (length(temp)!= 0)
      soft_crime[d+1] <- temp
  }
  
  #Burglaries "not in residence" in beat=96 in the last 2 weeks
  residence_burglary <- rep(0, 14)
  for (d in 0:13){
    temp <- aggr_burglary_residence[aggr_burglary_residence$rep_date == date_list[index] - d, c("count")]
    if (length(temp)!= 0)
      residence_burglary[d+1] <- temp
  }
  
  #Burglaries by watch in beat=96 in the last 2 weeks
  watch_burglary <- rep(0,0)
  for (d in 0:13) {
    temp1 <- rep(0, 4)
    for (w in 1:4){
      if (w == 4) w <- "U"
      temp <- aggr_burglary_watch[aggr_burglary_watch$rep_date == date_list[index] - d & aggr_burglary_watch$watch == w, c("count")]
      if (length(temp)!= 0){
        if (w != "U")
          temp1[w] <- temp
        else
          temp1[4] <- temp
      }
    }
    watch_burglary <- c(watch_burglary, temp1)
  }
  
  #BMV in beat=96 in the last 2 weeks
  bmv <- rep(0, 14)
  for (d in 0:13){
    temp <- aggr_bmv[aggr_bmv$rep_date == date_list[index] - d, c("count")]
    if (length(temp)!= 0)
      bmv[d+1] <- temp
  }
  
  #Robbery in beat=96 in the last 2 weeks
  robbery <- rep(0, 14)
  for (d in 0:13){
    temp <- aggr_robbery[aggr_robbery$rep_date == date_list[index] - d, c("count")]
    if (length(temp)!= 0)
      robbery[d+1] <- temp
  }

  
  city_burglary <- rep(0, 0)
  for (d in 0:6){
    temp <- rep(0,n_beat)
    v <- aggr_burglary[aggr_burglary$rep_date == date_list[index] - d, c("count", "beat")]
    temp[match(as.vector(v$beat), 1:n_beat)] <- v$count #Copy the number of crime only in the right beat positions    
    city_burglary <- c(city_burglary, temp)
  }
  
  D[index,] <- c(city_burglary, soft_crime, (soft_crime - yday_soft_crime), watch_burglary, (watch_burglary - yday_watch_burglary), residence_burglary, (residence_burglary - yday_residence_burglary), bmv, (bmv - yday_bmv), robbery, (robbery - yday_robbery), day, month, 1)
  
  #Update yesterday crimes
  yday_soft_crime <- soft_crime
  yday_residence_burglary <- residence_burglary
  yday_watch_burglary <- watch_burglary
  yday_bmv <- bmv
  yday_robbery <- robbery
}

rm(xxx)

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
