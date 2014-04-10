Crime and Punishment
====================================================================================

Initial exploratory analysis
------------------------------------------------------------------------------------

```r
# load the data
data = read.table("/home/finn/phd/data/rawwithgeo.txt", header = TRUE, sep = "\t")
```


I have categorized the crimes based on the first two digits of the *ucr1* column and maped the resulting factor levels to descriptive strings based on the information provided at http://policereports.dallaspolice.net/ucr.htm. The meaning of a couple of two digit codes, that occured in our data but were not listed on the above website, were inferred from viewing a summary of the descriptions provided for these cases in the data. I then constructed 4 groupings of these categories. Currently they are:

- Light: criminal mischief, disorderly, vice, fence and found property
- Violent: assult, agg assult, murder, rape and robbery
- Property: theft, burglary, un-authorized use of a motor vehicle
- Other: all other crime categories 

```r
# categorize the crime
data$crime <- as.factor(substr(data$ucr1, 1, 2))
library(plyr)
data$crime <- revalue(data$crime, c(`01` = "murder", `02` = "rape", `03` = "robbery", 
    `04` = "agg_assult", `05` = "burglary", `06` = "theft", `07` = "uumv", `08` = "assult", 
    `09` = "arson", `10` = "forge", `11` = "fraud", `12` = "embezzlement", `13` = "fence", 
    `14` = "crim_misch", `16` = "vice", `17` = "sex off", `18` = "drugs", `20` = "child", 
    `24` = "disorderly", `26` = "other", `29` = "runnawy", `32` = "flid", `33` = "injured", 
    `34` = "injured2", `39` = "att_suicide", `40` = "death", `41` = "missing_person", 
    `42` = "lost", `43` = "found"))

light <- c("crim_misch", "disorderly", "vice", "fence", "found")  #matches the broken windows paper by Gregorio?
violent <- c("assult", "agg_assult", "murder", "rape", "robbery")
property <- c("theft", "burglary", "uumv")


data$crime_category <- "other"
data$crime_category[data$crime %in% light] <- "light"
data$crime_category[data$crime %in% violent] <- "violent"
data$crime_category[data$crime %in% property] <- "property"
data$crime_category <- as.factor(data$crime_category)
```

How many crimes do we have in each category

```r
crime_by_category <- as.data.frame(prop.table(table(data$crime_category)))
crime_by_category <- crime_by_category[with(crime_by_category, order(-Freq)), 
    ]  # sort to order by frequency
barplot(crime_by_category$Freq, names.arg = crime_by_category$Var1, ylab = "proportion of crime", 
    main = "proportion of crime by category")
```

![plot of chunk unnamed-chunk-1](figure/unnamed-chunk-11.png) 

```r

crime_by_type <- as.data.frame(prop.table(table(data$crime)))
crime_by_type <- crime_by_type[with(crime_by_type, order(-Freq)), ]
crime_by_type <- crime_by_type[1:20, ]
barplot(crime_by_type$Freq, names.arg = crime_by_type$Var1, ylab = "proportion of crime", 
    main = "proportion of crime by ucr code (top 20)", las = 2)
```

![plot of chunk unnamed-chunk-1](figure/unnamed-chunk-12.png) 


Correlation between light and violent crime accross reportingareas. 
![plot of chunk visualize-relationship-between-crime-types](figure/visualize-relationship-between-crime-types.png) 


I calculated a number of temporal variables from the *rep_date*, *starttime*, *endtime* and *dispatchtime* variables. They are:
- year the year in which the event took place
- month: the month of year in which the event took place
- dow: the day of week in which the event took place
- hourofday: the hour of day - based on dispatchtime
- responcetime: the difference between starttime and dispatchtime. Where negative, 24 hours was added to deal with cases on either side of the midnight boundary
- onscenetime: the difference between endtime and starttime. Where negative, 24 hours was added to deal with cases on either side of the midnight boundary


```r
library(lubridate)
data$year <- as.integer(substr(data$rep_date, 7, 10))
data$starttime2 <- hms(data$starttime)
data$endtime2 <- hms(data$endtime)
data$dispatchtime2 <- hm(data$dispatchtime)
data$responcetime <- as.duration(data$starttime2 - data$dispatchtime2)
data$onscenetime <- as.duration(data$endtime2 - data$starttime2)
data$onscenetime[!is.na(data$onscenetime) & data$onscenetime < 0] <- data$onscenetime[!is.na(data$onscenetime) & 
    data$onscenetime < 0] + as.duration(hours(24))
data$responcetime[!is.na(data$responcetime) & data$responcetime < 0] <- data$responcetime[!is.na(data$responcetime) & 
    data$responcetime < 0] + as.duration(hours(24))
data$date <- mdy(as.character(data$rep_date))
data$dow <- wday(data$date)
data$month <- month(data$date)
data$hourofday <- hour(data$dispatchtime2)
```


Basic histograms of temporal variables

```r
barplot(table(data$hourofday), las = 3, xlab = "hour of day", ylab = "number of crimes", 
    main = "crime counts by hour of day")
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-21.png) 

```r
barplot(table(data$dow), las = 3, xlab = "day of week", ylab = "number of crimes", 
    main = "crime counts by day of week")
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-22.png) 

```r
barplot(table(data$month), las = 3, xlab = "month of year", ylab = "number of crimes", 
    main = "crime counts by month of year")
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-23.png) 

```r
barplot(table(data$year), las = 3, xlab = "year", ylab = "number of crimes", 
    main = "crime counts by year")
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-24.png) 

```r

tmp <- data[data$responcetime < 720 * 60, "responcetime"]  #ignore times longer than 12 hours
hist(tmp/60, xlab = "responce time (minutes)", main = "distribution of responce times")
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-25.png) 

```r
tmp <- data[data$onscenetime < 180 * 60, "onscenetime"]  #ignore times longer than 3 hours
hist(tmp/60, xlab = "minutes spent on scene", main = "distribution of time spent on scene")
```

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-26.png) 

```r
rm(tmp)
```



These plots summarize the relationship between responce-time, on-scene-time and a number of other variables. There was less correlation with other variables than I would have anticipated.

```r
plot(responcetime/(60) ~ crime_category, data = data, varwidth = TRUE, outline = FALSE, 
    xlab = "crime type", ylab = "responce time (minutes)", main = "responce time vs crime type")
```

![plot of chunk visualize-temporal-variables](figure/visualize-temporal-variables1.png) 

```r
plot(onscenetime/60 ~ crime_category, data = data, varwidth = TRUE, outline = FALSE, 
    xlab = "crime type", ylab = "time spent on scene (minutes)", main = "on scene time vs crime type")
```

![plot of chunk visualize-temporal-variables](figure/visualize-temporal-variables2.png) 

```r

# responce time by time of day and day of week
boxplot(responcetime/60 ~ dow, data = data, outline = FALSE, main = "responce time by day of week")
```

![plot of chunk visualize-temporal-variables](figure/visualize-temporal-variables3.png) 

```r
boxplot(responcetime/60 ~ hourofday, data = data, outline = FALSE, main = "responce time by hour of day")
```

![plot of chunk visualize-temporal-variables](figure/visualize-temporal-variables4.png) 

```r

data$division <- as.integer(substr(data$beat, 1, 1))
data$sector <- as.integer(substr(data$beat, 1, 2))

# by geographical area
boxplot(responcetime/60 ~ division, data = data, varwfenceidth = TRUE, outline = FALSE, 
    main = "responce time by division")
```

![plot of chunk visualize-temporal-variables](figure/visualize-temporal-variables5.png) 

```r
boxplot(responcetime/60 ~ sector, data = data, varwidth = TRUE, outline = FALSE, 
    main = "responce time by sector")
```

![plot of chunk visualize-temporal-variables](figure/visualize-temporal-variables6.png) 





Testing for variation in beat and reporting area lables
-----------------------------------------------------------------------------------------------------------
I have calculated the geographical centroid of each beat, for each year as the median lat and longitude of the points in that beat that year. Then, for each year, we can look at the mean difference in the centroids, accross all the beats, from the previous year. This gives an indication of how much change there has been overall in how the lables map to geographical areas. The process for reporting area is the same. I'd say we can conclude from this that something definately happend, at least with the beat labels we have, in 2003 and 2008/2009, but the reporting area appears relatively constant, all the way up to 2010.


```r
sub <- data[data$geo_conf > 0.8, ]  # restrict to data with confident geo

f_diff <- function(vect) {
    d <- diff(vect)
    d <- c(NA, d)
    return(d)
}

centroid_change <- function(median_lat, median_lon) {
    colnames(median_lat) <- c("beat", "year", "lat")  #call the geographic region beat in this code so as to not have to change is as we switch region we look at.
    colnames(median_lon) <- c("beat", "year", "lon")
    meads <- merge(median_lat, median_lon, by = c("year", "beat"))
    meads <- meads[meads$year <= 2011, ]
    
    # order by beat, then year.
    meads <- meads[with(meads, order(beat, year)), ]
    # we want a count of how many years a beat has data for
    count_by_year <- aggregate(lat ~ beat, meads, length)
    colnames(count_by_year) <- c("beat", "year_count")
    meads <- merge(meads, count_by_year, by = "beat")
    rm(count_by_year)
    meads <- meads[meads$year_count == 11, ]  #only consider regions that have at least 1 data point for all the years
    # cacluate a column lat_diff and a column lon_diff by applying f_diff
    meads$lat_diff <- f_diff(meads$lat)  # the value for the year 2000 will always be NA or from a different beat but we will throw it out later ...
    meads$lon_diff <- f_diff(meads$lon)
    meads$dist_diff <- sqrt(meads$lat_diff^2 + meads$lon_diff^2) * 100 * 110  #to get in meters one degree of lat or lon assumed equal to 110km
    meads <- meads[meads$year > 2000, ]
    return(meads)
}

beat_median_lat <- aggregate(lat ~ beat + year, sub, median)
beat_median_lon <- aggregate(lon ~ beat + year, sub, median)
beat_change_detail <- centroid_change(beat_median_lat, beat_median_lon)
beat_change <- aggregate(dist_diff ~ year, beat_change_detail, mean)
plot(beat_change$year, beat_change$dist_diff, ylim = c(0, 330), xlab = "year", 
    ylab = "~mean difference in median lat-lon from previous year (meters)", 
    main = "beat centroid variation by year", pch = 19)
```

![plot of chunk testing-centroid-variation](figure/testing-centroid-variation.png) 

```r
diff_2003 <- beat_change_detail[beat_change_detail$year == 2003, ]
diff_2005 <- beat_change_detail[beat_change_detail$year == 2005, ]
diff_2008 <- beat_change_detail[beat_change_detail$year == 2008, ]
```

We can look in more detail at what happened in 2003 and 2008 by looking at the distribution of changes in beat centroid. The following plots show these distributions for 2003, 2005 (as a control when nothing seemed to be happening) and 2008.

```r
hist(diff_2003$dist_diff, xlab = "change in beat centroid (meters)", main = "distribution of changes in beat centroid, 2002-2003", 
    breaks = 20)
```

![plot of chunk testing-centroid-variation-plots](figure/testing-centroid-variation-plots1.png) 

```r
hist(diff_2005$dist_diff, xlab = "change in beat centroid (meters)", main = "distribution of changes in beat centroid, 2004-2005", 
    breaks = 20)
```

![plot of chunk testing-centroid-variation-plots](figure/testing-centroid-variation-plots2.png) 

```r
hist(diff_2008$dist_diff, xlab = "change in beat centroid (meters)", main = "distribution of changes in beat centroid, 2007-2008", 
    breaks = 20)
```

![plot of chunk testing-centroid-variation-plots](figure/testing-centroid-variation-plots3.png) 

And doing the same for reporting area

```r
ra_median_lat <- aggregate(lat ~ reportingarea + year, sub, median)
ra_median_lon <- aggregate(lon ~ reportingarea + year, sub, median)
ra_change_detail <- centroid_change(ra_median_lat, ra_median_lon)
ra_change <- aggregate(dist_diff ~ year, ra_change_detail, mean)
plot(ra_change$year, ra_change$dist_diff, ylim = c(0, 330), xlab = "year", ylab = "~mean difference in median lat-lon from previous year (meters)", 
    main = "reporting area centroid variation by year", pch = 19)
```

![plot of chunk testing-ra-centroid-variation](figure/testing-ra-centroid-variation1.png) 

```r
plot(ra_change$year, ra_change$dist_diff, xlab = "year", ylab = "~mean difference in median lat-lon from previous year (meters)", 
    main = "reporting area centroid variation by year (closeup)", pch = 19)
```

![plot of chunk testing-ra-centroid-variation](figure/testing-ra-centroid-variation2.png) 

