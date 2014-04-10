# note these instances are for the 10 reporting areas with the greatest level of crime, so are not representative of the whole city of Dalls.
set.seed(47) # lets not be too random...
features = read.table("/home/finn/phd/data/features_50_regr_target_08.txt", header=TRUE, sep="\t")
f <- features
f$row <- 1:nrow(f)

# separate into training and test sets
train = f[f$year < 2005,] 
test = f[f$year >= 2005,]

# first up, lets calulate our benchmark... which is for each reporting area, predict the mean value of crime over the training set for that reporting area

mean_crime <- aggregate(target~area,train, mean)
colnames(mean_crime) <- c("area","mean_this_area")
test_result <- merge(test[,c('row','area','target')],mean_crime,by="area")
test_result <- test_result[with(test_result, order(row)), ]
train <- merge(train,mean_crime,by="area")
test$mean_this_area = test_result$mean_this_area #explicitly make the benchmark result a feature for machine learning
b1_rsme <- sqrt(mean((test_result$target-test_result$mean_this_area)^2))

# plot benchmark prediction vs real
library(ggplot2)
test_result$instance <- 1:nrow(test_result)
ggplot(data=test_result, aes(instance)) + geom_line(aes(y=target, color="ground truth")) + geom_line(aes(y=mean_this_area, color="prediction")) + xlab("instance")+ylab("num thefts")+xlim(0,365)

# scale the features in the train and test set and drop area and year
train <- subset(train,select=-c(area,year))
test <- subset(test,select=-c(area,year))

train[,2:ncol(train)] <- scale(train[2:ncol(train)]) # scale all variables except target
test[,2:ncol(test)] <- scale(test[2:ncol(test)])

# now lets try a basic linear model - no regularization.
lm1 <- lm(train$target ~.,data=train)
lm_pred <- predict(lm1,test)
lm1_rsme <- sqrt(mean((test$target - lm_pred)^2))
test_result$lm_pred <- lm_pred
ggplot(data=test_result, aes(instance)) + geom_line(aes(y=target, color="ground truth")) + geom_line(aes(y=lm_pred, color="prediction")) + xlab("instance")+ylab("num thefts")


library(randomForest)

# lets try tuning...
#tuneRF(train[,-1], train[,1], 100, ntreeTry=50, stepFactor=10, improve=0.0001, trace=TRUE, plot=TRUE, doBest=FALSE)
# for estimating if we are over-fitting - I could see what the error rate is on the training set as compared to the test set - but that is just one measurment


rf1 <- randomForest(target ~ .,data=train,ntree=1000,do.trace=TRUE,maxnodes=256)         
rf1_pred <- predict(rf1, test)

test_result$rfpred <- rf1_pred
ggplot(data=test_result, aes(instance)) + geom_line(aes(y=target, color="ground truth")) + geom_line(aes(y=rfpred, color="prediction")) +geom_line(aes(y=mean_this_area, color="benchmark"))+  xlab("instance")+ylab("num thefts")

rf1_rsme <-sqrt(mean((test_result$target - test_result$rfpred)^2))
                    
# lets try again keeping only information from this area dist0period1category06
this_area_vars = c(1,2,3,grep("^dist0",names(train)),1193)
train2 = train[,this_area_vars]
test2 = test[,this_area_vars]
rf2 <- randomForest(target ~ mean_this_area+dow+month+dist0period1category06+dist1period1category6,data=train2,ntree=50,do.trace=TRUE)         
rf2_pred <- predict(rf2, test2, type="response")
test_result$rf2pred <- rf2_pred
ggplot(data=test_result, aes(instance)) + geom_line(aes(y=target, color="ground truth")) + geom_line(aes(y=rf2pred, color="prediction")) + xlab("instance")+ylab("num thefts")+xlim(0,365)
rf2_rsme <-sqrt(mean((test_result$target - test_result$rf2pred)^2))
#is it a problem for random forrest if we introduce variables that are strongly correlated with one-another - because that is certainly going to be the case here?

#lets do pca
# what we want to do is run PCA on the training data. Get the weight combinations for the top N components and construct the same combinations in the test data set.

train_data <- as.matrix(train[,-1])
train_label <- train[,1]
test_data <- as.matrix(test[,-1])
test_label <- test[,1]
pca <- prcomp(train_data, center = FALSE, scale = FALSE)
plot(cumsum(pca$sdev^2/sum(pca$sdev^2)))
train_pca <- as.data.frame(train_data %*% pca$rotation)


test_pca <- as.data.frame(test_data %*% pca$rotation)


# try random forest with first 100 pca components
n <- 20
train_n <- train_pca[,1:n]
test_n <- test_pca[,1:n]
train_n$target = train_label
test_n$target <- test_label


rf3 <- randomForest(target ~ .,data=train_n, ntree = 500, do.trace=TRUE)
rf3_pred <- predict(rf3, test_n, type="response")
test_result$rf3pred <- rf3_pred
ggplot(data=test_result, aes(instance)) + geom_line(aes(y=target, color="ground truth")) + geom_line(aes(y=rf3pred, color="prediction")) + xlab("instance")+ylab("num thefts")
rf3_rsme <-sqrt(mean((test_result$target - test_result$rf3pred)^2))

#messing around with svm
library(e1071)
svm_tune <- tune.svm(train[,-1],train[1],cost = c(1,10,100,100),gamma=c(0.01,0.001,0.0001,0.00001))

sub <- train[1:730,]

svm_model <- svm(target ~ ., data = train,type="eps-regression" ,cost = 10, gamma = 0.001)
svm_pred <- predict(svm_model, test)
test$pred_svm <- svm_pred

# think about how correlated are different types of crime. For for example, how correlated is light crime with violent crime over different time periods
#1 day, 1 week, 1 month, 1 year... measure on a sliding window? currently have a row for each time we get a crime.
