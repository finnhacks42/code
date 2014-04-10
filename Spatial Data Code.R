# The following code runs some examples from R meetup talk of 14/09/2011
# It only runs those examples for which the data is included in an R package 
# Several are from the excellent book "Applied Spatial Data Analysis with R"
# See http://www.asdar-book.org/ for full code from that book

# For best results please use R 2.13.1 Patched - not R 2.13.1
# In windows you can run the code using [File / Source R Code] from the menus 
# Note that this will install several R packages. If those packages are
# already installed you can remove the 'install.packages' line of code.

## Install/Load Software And Datasets 

pkgs <- c("sp","rgdal","maptools","gpclib","gstat","spdep","spatstat",
  "splancs","DCluster","geoR")
install.packages(pkgs, dependencies="Depends") # installs many packages
for(i in seq(along=pkgs)) library(pkgs[i], character.only=TRUE)
gpclibPermit()
datas <- c("lansing", "japanesepines", "redwoodfull", "cells","copper",
  "humberside", "meuse", "meuse.grid", "meuse.riv")
do.call(data, as.list(datas))
pal <- colorRampPalette(c("wheat1", "red3"))(20)
devAskNewPage(ask = TRUE)

## Maple Point Pattern Example

lmaple <- lansing[lansing$marks=="maple",]; marks(lmaple) <- NULL
plot(lmaple, pch=19, cex=1, main = "Maple Trees")
lmapleint <- ppm(lmaple, trend = ~polynom(x,y,2))
grd <- GridTopology(cellcentre.offset=c(0.005,0.005), cellsize=c(0.01, 0.01),
  cells.dim=c(100, 100))
locs <- as.data.frame(coordinates(grd)); names(locs) <- c("x","y")
lmapleint <- data.frame(intensity=predict(lmapleint,locations=locs))
parintm <- SpatialGridDataFrame(grd, data=lmapleint)
lyt <- list("sp.points", SpatialPoints(as.points(lmaple)), pch=19, col="black", cex=0.7)
print(spplot(parintm, at=seq(0,1400,length.out=8), col.regions=pal, sp.layout=list(lyt)))

lmapleint2 <- as(density(lmaple, sigma=.15), "SpatialGridDataFrame")
print(spplot(lmapleint2, at=seq(0,1400,length.out=8), col.regions=pal, sp.layout=list(lyt)))

## Clustering In Point Patterns Example 

spred <- as(redwoodfull, "SpatialPoints")
spcells <- as(cells, "SpatialPoints")
spjpines <- as(japanesepines, "SpatialPoints")
spjpines1 <- elide(spjpines, scale=TRUE, unitsq=TRUE)
dpp<-data.frame(rbind(coordinates(spjpines1), coordinates(spred), 
   coordinates(spcells)))
njap<-nrow(coordinates(spjpines1))
nred<-nrow(coordinates(spred))
ncells<-nrow(coordinates(spcells))
dpp<-cbind(dpp,c(rep("JAPANESE",njap), rep("REDWOOD", nred), rep("CELLS", ncells))) 
names(dpp)<-c("x", "y", "DATASET")
print(xyplot(y~x|DATASET, data=dpp, pch=19, aspect=1))
plot(allstats(cells), lwd=3)
plot(allstats(japanesepines), lwd=3)
plot(allstats(redwoodfull), lwd=3)

r <- seq(0, sqrt(2)/6, by = 0.005)
envjap <- envelope(as(spjpines1, "ppp"), fun=Gest, r=r, nrank=2, nsim=99)
envred <- envelope(as(spred, "ppp"), fun=Gest, r=r, nrank=2, nsim=99)
envcells <- envelope(as(spcells, "ppp"), fun=Gest, r=r, nrank=2, nsim=99)
Gresults <- rbind(envjap, envred, envcells) 
Gresults <- cbind(Gresults, rep(c("JAPANESE", "REDWOOD", "CELLS"), each=length(r)))

Fenvjap<-envelope(as(spjpines1, "ppp"), fun=Fest, r=r, nrank=2, nsim=99)
Fenvred<-envelope(as(spred, "ppp"), fun=Fest, r=r, nrank=2, nsim=99)
Fenvcells<-envelope(as(spcells, "ppp"), fun=Fest, r=r, nrank=2, nsim=99)
Fresults<-rbind(Fenvjap, Fenvred, Fenvcells)
Fresults<-cbind(Fresults, rep(c("JAPANESE", "REDWOOD", "CELLS"), each=length(r)))

Kenvjap<-envelope(as(spjpines1, "ppp"), fun=Kest, r=r, nrank=2, nsim=99)
Kenvred<-envelope(as(spred, "ppp"), fun=Kest, r=r, nrank=2, nsim=99)
Kenvcells<-envelope(as(spcells, "ppp"), fun=Kest, r=r, nrank=2, nsim=99)
Kresults<-rbind(Kenvjap, Kenvred, Kenvcells)
Kresults<-cbind(Kresults, rep(c("JAPANESE", "REDWOOD", "CELLS"), each=length(r)))

print(xyplot(obs~theo|y, data=Gresults, type="l", xlab="", ylab="", main="G Function",
	panel=function(x, y, subscripts)
	{
		lpolygon(c(x, rev(x)), 
		   c(Gresults$lo[subscripts], rev(Gresults$hi[subscripts])),
		   border="gray", col="gray")
		llines(x, y, col="black", lwd=2)
	}
))

print(xyplot(obs~theo|y, data=Fresults, type="l", xlab="", ylab="", main="F Function",
	panel=function(x, y, subscripts)
	{
		lpolygon(c(x, rev(x)), 
		   c(Fresults$lo[subscripts], rev(Fresults$hi[subscripts])),
		   border="gray", col="gray")
		llines(x, y, col="black", lwd=2)
	}
))

print(xyplot(obs~theo|y, data=Kresults, type="l", xlab="", ylab="", main="K Function",
	panel=function(x, y, subscripts)
	{
		lpolygon(c(x, rev(x)), 
		   c(Kresults$lo[subscripts], rev(Kresults$hi[subscripts])),
		   border="gray", col="gray")
		llines(x, y, col="black", lwd=2)
	}
))

## Copper Point Pattern Example 

X <- rotate(copper$SouthPoints, pi/2)
L <- rotate(copper$SouthLines, pi/2)
par(mfrow=c(2,1))
plot(X, pch=16, main="Copper Data")
plot(L, add=TRUE)
Z <- distmap(L)
plot(Z, col=pal, main = "Covariate", ribbon=FALSE)
par(mfrow=c(1,1))
plot(rhohat(X, Z), xlab="Distance To Fault", lwd=3, cex=1.5)
cop1 <- ppm(X, trend = ~x+y)
cop2 <- ppm(X, trend = ~x+y+V1, covariates=list(V1=Z))

grd <- GridTopology(cellcentre.offset=c(-158.233,-0.355), cellsize=c(1.58, 0.35),
  cells.dim=c(100, 100))
locs <- as.data.frame(coordinates(grd)); names(locs) <- c("x","y")
lcop1 <- data.frame(intensity=predict(cop1,locations=locs))
lcop2 <- data.frame(intensity=predict(cop2,locations=locs))
lcop <- cbind(lcop1,lcop2); names(lcop) <- c("Without_Covariate","With_Covariate")
parint <- SpatialGridDataFrame(grd, data=lcop)
lyt <- list("sp.points", SpatialPoints(as.points(X)), pch=19, col="black", cex=1)
print(spplot(parint, at=seq(.005,.025,length.out=8), col.regions=pal, sp.layout=list(lyt),
  main="Covariate Comparison", cex = 1.5))

## Humberside Childhood Leukaemia Example 
  
marks(humberside) <- factor(marks(humberside),c("control","case"))
plot(humberside,chars=c(15,16),cols=c(1,3),cex=1.2,main="Humberside Leukaemia")
plot(density(split(humberside)),ribbon=FALSE,col=pal,main="Humberside Leukaemia")
plot(relrisk(humberside,sigma=100),zlim=c(0,1),col=pal,ribbon=FALSE,main="Relative Risk")
plot(humberside$window,add=TRUE)
plot(humberside,chars=c(15,16),cols=c(1,3),cex=1.2,add=TRUE)

## Geostatistcal Meuse Example

coordinates(meuse) <- c("x", "y")
coordinates(meuse.grid) <- c("x", "y")
gridded(meuse.grid) <- TRUE
meuse.lst <- list(Polygons(list(Polygon(meuse.riv)), "meuse.riv")) 
meuse.sr <- SpatialPolygons(meuse.lst)
zn.idw <- krige(log(zinc) ~ 1, meuse, meuse.grid)

image(zn.idw, col = grey.colors(4, 1, 1))
plot(meuse.sr, add=TRUE, col="grey")
plot(meuse, pch = 1, cex = sqrt(meuse$zinc)/20, add = TRUE)
legVals <- c(100, 200, 500, 1000, 2000)
legend("left", legend=legVals, pch = 1, pt.cex = sqrt(legVals)/20, bty = "n",
  title="measured, ppm", cex=1, y.inter=0.9)
title("Zinc Measurements")

image(zn.idw, col = pal)
plot(meuse.sr, add=TRUE, col="grey")
plot(meuse, pch = 1, cex = sqrt(meuse$zinc)/20, add = TRUE)
legend("left", legend=legVals, pch = 1, pt.cex = sqrt(legVals)/20, bty = "n",
  title="measured, ppm", cex=1, y.inter=0.9)
title("Zinc Measurements")

zn.idw2 <- krige(log(zinc) ~ 1, meuse, meuse.grid, degree = 2)
image(zn.idw2, col = pal)
plot(meuse.sr, add=TRUE, col="grey")
plot(meuse, pch = 1, cex = sqrt(meuse$zinc)/20, add = TRUE)
legend("left", legend=legVals, pch = 1, pt.cex = sqrt(legVals)/20, bty = "n",
  title="measured, ppm", cex=1, y.inter=0.9)
title("Zinc Measurements")

zn.idw3 <- krige(log(zinc) ~ sqrt(dist), meuse, meuse.grid)
image(zn.idw3, col = pal)
plot(meuse.sr, add=TRUE, col="grey")
plot(meuse, pch = 1, cex = sqrt(meuse$zinc)/20, add = TRUE)
legend("left", legend=legVals, pch = 1, pt.cex = sqrt(legVals)/20, bty = "n",
  title="measured, ppm", cex=1, y.inter=0.9)
title("Zinc Measurements")

zn.idw4 <- krige(log(zinc) ~ sqrt(dist) + x + y + I(x*y) + I(x^2) + I(y^2), meuse, meuse.grid)
image(zn.idw4, col = pal)
plot(meuse.sr, add=TRUE, col="grey")
plot(meuse, pch = 1, cex = sqrt(meuse$zinc)/20, add = TRUE)
legend("left", legend=legVals, pch = 1, pt.cex = sqrt(legVals)/20, bty = "n",
  title="measured, ppm", cex=1, y.inter=0.9)
title("Zinc Measurements")

zn.lm <- lm(log(zinc) ~ sqrt(dist) + x + y + I(x*y) + I(x^2) + I(y^2), meuse)
meuse$fitted.lmz <- predict(zn.lm, meuse) - mean(predict(zn.lm, meuse))
meuse$residuals.lmz <- residuals(zn.lm)
print(spplot(meuse, c("fitted.lmz","residuals.lmz"), col.regions = rev(heat.colors(5)), cex=1.2))

cld <- gstat::variogram(log(zinc) ~ sqrt(dist)+x+y+I(x*y)+I(x^2)+I(y^2), meuse, cloud = TRUE)
svgm <- gstat::variogram(log(zinc) ~ sqrt(dist)+x+y+I(x*y)+I(x^2)+I(y^2), meuse)
d <- data.frame(gamma = c(cld$gamma, svgm$gamma),
	distance = c(cld$dist, svgm$dist),
	id = c(rep("cloud", nrow(cld)), rep("sample variogram", nrow(svgm))))
print(xyplot(gamma ~ distance | id, d,
	scales = list(y = list(relation = "free")),
	layout = c(1, 2), as.table = TRUE, ylab = "Squared Difference",
	panel = function(x,y, ...) {
		if (panel.number() == 2)
			panel.loess(x, y) 
		panel.xyplot(x,y,...)
	}, 
	xlim = c(0, 1590),
	cex = .5, pch = 3
))

v.fit <- fit.variogram(svgm, vgm(1, "Sph", 800, 1))
print(plot(svgm, v.fit, pch = 16, cex=1.4))

zn.idw5 <- krige(log(zinc) ~ sqrt(dist) + x + y + I(x*y) + I(x^2) + I(y^2), meuse, meuse.grid, v.fit)
image(zn.idw5, col = pal)
plot(meuse.sr, add=TRUE, col="grey")
plot(meuse, pch = 1, cex = sqrt(meuse$zinc)/20, add = TRUE)
legend("left", legend=legVals, pch = 1, pt.cex = sqrt(legVals)/20, bty = "n",
  title="measured, ppm", cex=1, y.inter=0.9)
title("Zinc Measurements")

zn.sim <- krige(log(zinc) ~ sqrt(dist) + x + y, 
  meuse, meuse.grid, v.fit, nsim=6, nmax=40)
print(spplot(zn.sim, col.regions=pal))

plot(1:10,1:10,type="n",axes=FALSE,xlab="",ylab="")
cat("\nFinished!\nThanks for attending the talk.\n")
text(5,8,"Finished! Thanks for attending the talk.",cex=1.5)
cat("Please continue to support The Melbourne R Meetup Group.\n")
text(5,7,"Please continue to support",cex=1.5)
text(5,6,"The Melbourne R Meetup Group.",cex=1.5)
cat("Have a great day.\n\n")
text(5,5,"Have a great day.",cex=1.5)
cat("Alec Stephenson\n")
text(5,4,"Alec Stephenson",cex=1)
cat("astephenson@swin.edu.au\n")
text(5,3.5,"astephenson@swin.edu.au",cex=1)


  
  
