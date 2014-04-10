```{r}
# create a data frame with a row for each reporting area for each day and the number of crimes of type x that occured on that day.
df <- data[data$crime_category=='light',c('date','reportingarea')]
date_seq <- seq(min(df$date),max(df$date),'days')

```


```{r average-crime}
# for each reporting area, calculate the average number of crimes of type x / day. Then the average number of type x on day d given crime y on d-1,d-2,...
data$ones <- rep(1,nrow(data)) # create a vector of all 1s 
x_condition <-data$crime_category=="violent"
crime_sub <- data[x_condition,]
n_days = as.numeric(max(crime_sub$date)-min(crime_sub$date)) # the number of days in the data set
background <- aggregate(ones~reportingarea,data=crime_sub,sum) # count the number of number of crimes in each reporting area 
colnames(background) <- c('reportingarea','p0')
background$p0 <- background$p0/n_days

# now how to calulate the frequency that an event occured on day d given one occured on day d-1 - what do we do if one occured on d-1 and d-2?

# for each area, find all days on which an event occured. 
y_condition <- x_condition # look at the temporal correlation between light crime and light crime
days_forward = 56
last_day <- max(data$date) - days(days_forward)
event_days <- data[y_condition & data$date < last_day ,c('date','reportingarea')]#all the days on which crime of type y occured. 
event_days$crime_date <- event_days$date 
data_events <- data[,c('date','reportingarea','ones')]
result <- background

for (day in 1:days_forward) {
  print(day)
  event_days$date <- event_days$crime_date+days(day)
  # left merge event_days with data_events on next-day = date and reporting area
  joined <- merge(x = event_days, y = data_events, by = c('date','reportingarea'), all.x=TRUE)
  joined["ones"][is.na(joined["ones"])] <- 0
  a <- aggregate(ones ~ reportingarea,data = joined,FUN=function(x) p=sum(x)/length(x))
  a <- as.data.frame(as.list(a)) #this funny list to data frame conversion required due to a bug in R that otherwise does not fully recognize the calulated columns
  names(a) <- c('reportingarea',paste("p",day,sep=""))
  result <- merge(result,a,by='reportingarea')
}

mean_per <- apply(result[,-1],2,mean)
plot(mean_per,xlab="day forward",ylab="average number of crimes")

```

```{r}
for (day in 1:days_forward) {
  print(day)
}
```


f_diff <- function(vect) {
  d <- diff(vect)
  d <- c(NA,d)
  return(d)
}


library(foreign)
greg <- read.dta("/home/finn/phd/data/fulldata_latlong.dta")
finn <- read.table("/home/finn/phd/data/rawwithgeo.txt", header=TRUE, sep="\t")
georgio <- read.table("/home/finn/phd/data/fixrawdata.txt",header=TRUE,sep="\t")

finn$year <- as.integer(substr(finn$rep_date,7,10))
greg$year <- as.integer(substr(greg$rep_date,7,10))
greg$lat <- greg$y
greg$lon <- greg$x

sub <- finn[finn$geo_conf > .8,]
#sub <- greg


# for each beat lets calculate the median latitude and the median longitude.
median_lat <- aggregate(lat~reportingarea+year,sub, median)
median_lon <- aggregate(lon~reportingarea+year,sub,median)
colnames(median_lat) <- c("beat","year","lat") #call the geographic region we are working with beat in this code so as to not have to change is as we switch region we look at.
colnames(median_lon) <- c("beat","year","lon")

meads <- merge(median_lat,median_lon,by=c("year","beat"))
meads <- meads[meads$year <=2011,]


# lets calculate the difference in lat and the difference in lon for each year for each beat.
# order by beat, then year. 
meads <- meads[with(meads, order(beat,year)),]
# we want a count of how many years a beat has data for
count_by_year <- aggregate(lat~beat,meads,length)
colnames(count_by_year) <- c("beat","year_count")
meads <- merge(meads,count_by_year,by="beat")
rm(count_by_year)
meads <- meads[meads$year_count == 11,]
# cacluate a column lat_diff and a column lon_diff by applying f_diff 
meads$lat_diff <- f_diff(meads$lat) # the value for the year 2000 will always be NA or from a different beat but we will throw it out later ...
meads$lon_diff <- f_diff(meads$lon)
meads$dist_diff <- sqrt(meads$lat_diff^2+meads$lon_diff^2)*100*110 #to get in meters one degree of lat or lon assumed equal to 110km
meads <- meads[meads$year > 2000,]
by_year <- aggregate(dist_diff~year,meads,mean)
plot(by_year$year,by_year$dist_diff,xlab="year",ylab="~mean difference in median lat-lon from previous year (meters)",main="reporting area centroid variation by year",pch=19)


library(plyr)
ddply(iris, "Species", function(x){
  y <- subset(x, select= -Species)
  apply(y, 2, mean)
})
d2 <- ddply(meads,~beat,transform,lat_diff= f_diff(meads$lat))

blat <- by(meads[,"lat"],meads$bfact,f_diff)

by(iris[, 1:4], Species, mean)

dd[with(dd, order(-z, b)), ]

beat, year, lat-diff, lon-diff


f_geo <- finn[,c("lat","lon","off_num","geo_conf","beat")]
y_geo <- y[,c("x","y","off_num","beat")]

m <- merge(f_geo,y_geo,by="off_num")
m$diff <- sqrt((m$x-m$lon)^2+(m$y-m$lat)^2)

y_sample <- y[sample(nrow(y),1000),]

data_y <- merge(y_sample,data,by="off_num")
finn_y <- merge(y_sample,finn,by="off_num")




library(ggplot2)
y$beat <- as.integer(y$beat)
y$year <- as.integer(substr(y$rep_date,7,10))
ac = y[y$year < 2007,c("x","y","year","beat")]

a <- ac[ac$beat==190,]

#remove outliers to see core area of plot
a$latd <- abs(a$y-mean(a$y))/sd(a$y) 
a$lond <-abs(a$x-mean(a$x))/sd(a$x)
a <- a[a$latd < 2 & a$lond < 2,]

a$year <- as.factor(a$year) # tranform year back to a factor so points can be coloured by it
b = a[sample(nrow(a),1000),] #optionally sample a to ensure that points not just plotting on top of one-another

qplot(x,y,color=year,size=I(3),data=a)