Mapity maps

```{r}
library(sp)
library(rgdal)
latlong = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs"
data$beat <- as.integer(data$beat)

beat96_c <- data[data$beat==96 & !is.na(data$lat) & data$lat>0,]
beat96_c$descrip <- paste(c(data$block,data))
beat96_c$info <- do.call(paste, c(beat96_c[c("block", "street","description")], sep = " "))
beat96 <- beat96_c
coordinates(beat96) <- c("lon","lat")
proj4string(beat96) <- CRS("+proj=longlat +datum=WGS84")
beat96_ll <- spTransform(beat96, CRS("+proj=longlat +datum=WGS84"))
writeOGR(beat96["info"], "beat96.kml", layer="ucr1", driver="KML") 
```


```{r}
library(plotKML)
library(sp)
library(spacetime)

data(HRtemp08)
HRtemp08$ctime <- as.POSIXct(HRtemp08$DATE, format="%Y-%m-%dT%H:%M:%SZ")
sp <- SpatialPoints(HRtemp08[,c("Lon","Lat")])
proj4string(sp) <- CRS("+proj=longlat +datum=WGS84")
HRtemp08.st <- STIDF(sp, time = HRtemp08$ctime, data = HRtemp08[,c("NAME","TEMP")])
HRtemp08_jan <- HRtemp08.st[1:500]
plotKML(HRtemp08_jan[,,"TEMP"], dtime = 24*3600)


beat96df <- data[data$beat==332 & !is.na(data$lat) & data$lat>0,]
beat96 <-beat96df
beat96$ctime <-as.POSIXct(beat96$rep_date,format="%m/%d/%Y")
sp <- SpatialPoints(beat96[,c("lon","lat")])
proj4string(sp) <- CRS("+proj=longlat +datum=WGS84")
beat96.st <- STIDF(sp,time=beat96$ctime, data=beat96[,c("crime","geo_conf")])
plotKML(beat96.st)

proj4string(sp) <- CRS("+proj=longlat +datum=WGS84")


```




```{r}
library(maps)
library(mapdata)
map("worldHires","Canada",xlim=c(-141,-53),ylim=c(40,85),col="gray90",fill=TRUE)

library(RgoogleMaps)
bb <- qbbox(lat = data[data$geo_conf > .9,"lat"], lon = data[data$geo_conf>.9,"lon"])
MyMap <- GetMap.bbox(bb$lonR, bb$latR, destfile = "DALLAS.png", GRAYSCALE =TRUE)




data$beat <- as.integer(data$beat)
data$year <- as.integer(substr(data$rep_date,7,10))
ac = data[data$geo_conf >.8 & data$year < 2008 & !is.na(data$lat) ,c("lat","lon","beat","year")]
a <- ac[ac$beat==96,]
a$latd <- abs(a$lat-mean(a$lat))/sd(a$lat)
a$lond <-abs(a$lon-mean(a$lon))/sd(a$lon)
a <- a[a$latd < 2 & a$lond < 2,]

a$year <- as.factor(a$year)
b = a[sample(nrow(a),1000),]

qplot(lon,lat,color=year,size=I(3),data=a)





a$beat <- as.factor(a$beat)
plot(a$lon~a$lat,col=a$beat)

b = data[data$beat == 95 & data$geo_conf==1 &data$year < 2007,]
b$year <- as.factor(b$year)
plot(b$lon~b$lat,col=b$year)


library(ggplot2)
qplot(lon,lat,color=year,size=I(5),data=b)



#TODO look for beat structure changing over time ...
```