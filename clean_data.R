#This is all the data preparation phase
library("lubridate")
load("/home/finn/phd/data/fixrawdata.R")

#Add count row
xx <- cbind(x, rep(1, nrow(x)))
colnames(xx)[length(colnames(xx))] <- "count"

#Drop agency, off_num and record_date, and signal1, signal2
xx <- subset(xx,select=-c(1,2,40))

#Cast date and time of the day fields
xx$off_date <- as.Date(xx$off_date, format="%m/%d/%Y")
xx$rep_date <- as.Date(xx$rep_date, format="%m/%d/%Y")
xx$starttime <- as.numeric(seconds(xx$starttime)) - 1
xx$endtime <- as.numeric(seconds(xx$endtime)) - 1
xx$dispatchtime <- (as.numeric(seconds(xx$dispatchtime)) - 1) * 60
xx$date_occurence1 <- as.Date(xx$date_occurence1, format="%m/%d/%Y")
xx$time_occurence1 <- (as.numeric(seconds(xx$time_occurence1)) - 1) * 60
xx$date_occurence2 <- as.Date(xx$date_occurence2, format="%m/%d/%Y")
xx$time_occurence2 <- (as.numeric(seconds(xx$time_occurence2)) - 1) * 60

#Select only instances with date <=2010, the other are typos
xx <- xx[year(xx$off_date) <= 2010,]

#some factor as numerical
xx$beat <- as.numeric(xx$beat)
xx$reportingarea <- as.numeric(xx$reportingarea)

#Put "null" categorical value where needed
levels(xx$name) <- c(levels(xx$name), "null")
xx$name[xx$name == ""] <- "null"
xx$name[xx$name == " "] <- "null"
xx$name <- factor(xx$name, exclude="")
xx$name <- factor(xx$name, exclude=" ")
levels(xx$race) <- c(levels(xx$race), "null")
xx$race[xx$race == " "] <- "null"
xx$race <- factor(xx$race, exclude=" ")
levels(xx$age) <- c(levels(xx$age), "null")
xx$age[xx$age == " "] <- "null"
xx$age <- factor(xx$age, exclude=" ")
levels(xx$gender) <- c(levels(xx$gender), "null")
xx$gender[xx$gender== " "] <- "null"
xx$gender <- factor(xx$gender, exclude=" ")
levels(xx$direction) <- c(levels(xx$direction), "null")
xx$direction[xx$direction== " "] <- "null"
xx$direction <- factor(xx$direction, exclude=" ")
levels(xx$apt) <- c(levels(xx$apt), "null")
xx$apt[xx$apt== " "] <- "null"
xx$apt <- factor(xx$apt, exclude=" ")
levels(xx$city) <- c(levels(xx$city), "null")
xx$city[xx$city== " "] <- "null"
xx$city[is.na(xx$city)] <- "null"
xx$city <- factor(xx$city, exclude=" ")
xx$city <- factor(xx$city, exclude=NA)
levels(xx$state) <- c(levels(xx$state), "null")
xx$state[xx$state== " "] <- "null"
xx$state[is.na(xx$state)] <- "null"
xx$state <- factor(xx$state, exclude=" ")
xx$state <- factor(xx$state, exclude=NA)
xx$zip <- factor(xx$zip)
levels(xx$zip) <- c(levels(xx$zip), "null")
xx$zip[is.na(xx$zip)] <- "null"
xx$zip <- factor(xx$zip, exclude=NA)
levels(xx$bus_direction) <- c(levels(xx$bus_direction), "null")
xx$bus_direction[xx$bus_direction == " "] <- "null"
xx$bus_direction <- factor(xx$bus_direction, exclude=" ")
levels(xx$bus_street) <- c(levels(xx$bus_street), "null")
xx$bus_street[xx$bus_street== " "] <- "null"
xx$bus_street[is.na(xx$bus_street)] <- "null"
xx$bus_street <- factor(xx$bus_street, exclude=" ")
xx$bus_street <- factor(xx$bus_street, exclude=NA)
levels(xx$bus_city) <- c(levels(xx$bus_city), "null")
xx$bus_city[xx$bus_city== " "] <- "null"
xx$bus_city[is.na(xx$bus_city)] <- "null"
xx$bus_city <- factor(xx$bus_city, exclude=" ")
xx$bus_city <- factor(xx$bus_city, exclude=NA)
xx$property_attack_code <- factor(xx$property_attack_code)
levels(xx$property_attack_code) <- c(levels(xx$property_attack_code), "null")
xx$property_attack_code[is.na(xx$property_attack_code)] <- "null"
xx$property_attack_code <- factor(xx$property_attack_code, exclude=NA)
levels(xx$ucr2) <- c(levels(xx$ucr2), "null")
xx$ucr2[xx$ucr2== " "] <- "null"
xx$ucr2 <- factor(xx$ucr2, exclude=" ")
levels(xx$weather) <- c(levels(xx$weather), "null")
xx$weather[xx$weather == " "] <- "null"
xx$weather <- factor(xx$weather, exclude=" ")
levels(xx$reporting_officer_badge2) <- c(levels(xx$reporting_officer_badge2), "null")
xx$reporting_officer_badge2[xx$reporting_officer_badge2 == " "] <- "null"
xx$reporting_officer_badge2 <- factor(xx$reporting_officer_badge2, exclude=" ")
levels(xx$status) <- c(levels(xx$status), "null")
xx$status[xx$status == ""] <- "null"
xx$status <- factor(xx$status, exclude="")

#Handle null values of the data_occurence and time_occurrence fields
xx <- cbind(xx, is.na(xx$date_occurence2))
colnames(xx)[length(colnames(xx))] <- "is_na_date_occurence2"
xx$date_occurence2[is.na(xx$date_occurence2)] <- mean(na.omit(xx$date_occurence2))
xx <- cbind(xx, (xx$time_occurence2 == ""))
colnames(xx)[length(colnames(xx))] <- "is_na_time_occurence2"
xx$time_occurence2[xx$is_na_time_occurence2 == TRUE] <- mean(xx$time_occurence2[xx$is_na_time_occurence2 == FALSE])

#Drop record_data
xx <- subset(xx,select=-c(38))

save(xx,file="/home/finn/phd/data/cleaned.R")
