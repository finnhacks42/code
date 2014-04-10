
features = read.table("/home/finn/phd/data/features4.txt", header=TRUE, sep="\t")
features$year <- as.integer(substr(features$day,1,4)) #extract the year as an integer for easy subsetting


# benchmarks, calculate the average for each beat per day only use events during the training set and then simply predict this value on the validation set.
mean_crime <- aggregate(target~beat,features[features$year <= 2004,], mean)
colnames(mean_crime) <- c("beat","mean_this_beat")
bench1 <- merge(features[features$year == 2005,c(2,3)],mean_crime,by="beat")
bench1$errorsq <- (bench1$target-bench1$mean_this_beat)^2
b1_rsme <- sqrt(mean(bench1$errorsq))
# plot benchmark prediction vs real
library(ggplot2)
bench1$instance <- 1:nrow(bench1)
ggplot(data=bench1, aes(instance)) + geom_line(aes(y=target, color="ground truth")) + geom_line(aes(y=mean_this_beat, color="prediction")) + xlab("instance")+ylab("num burglaries")

# ok lets try a linear model where the only input parameter is the avearge previous number of burglaries

features <- merge(features,mean_crime,by="beat")
features[,6:(ncol(features))] <- scale(features[,6:(ncol(features))])
features$const <- rep(1,nrow(features))


train = features[features$year <= 2004,]
train_label <- train[,train$target]
train <- as.matrix(train[,-train$target])

validation <- features[features$year == 2005,]
validation_label <- validation[,validation$target]
validation <- as.matrix(validation[,-validation$target])

test <- features[features$year==2006,]
test_label <- test[,test$target]
test <- as.matrix(test[,-test$tearget])

# lets try a linear model with the build in R functionality
df <- features[features$year <= 2004,]
df_test <- features[features$year == 2005,]
lm1 <- lm(df$target ~.,data=df)
lm_pred <- predict(lm1,df_test)
lm1_rsme <- sqrt(mean((df_test$target - lm_pred)^2))

df2 <- features[features$year <= 2004,c("target","mean_this_beat","target1")] 
df2_test <- features[features$year == 2005,c("target","mean_this_beat","target1")]
lm2 = lm(df2$target ~.,data=df2)
lm2_pred <- predict(lm2,df2_test)
lm2_rsme <- sqrt(mean((df2_test$target-lm2_pred)^2))


#Random forest
library(randomForest)

pred_ref <- randomForest(x=train,y=train_label,xtest=validation,ytest=validation_label,ntree=50,do.trace=TRUE)
#pred_rf <- randomForest(x=rbind(train,validation), y=c(train_label,validation_label), xtest=test, ytest=test_label, ntree=50, do.trace = TRUE)

df <- data.frame(x=1:length(validation_label), y1=validation_label, y2=as.numeric(pred_rf$test$predicted))
ggplot(data=df, aes(x)) + geom_line(aes(y=y1, color="ground truth")) + geom_point(aes(y=y1, color="ground truth")) + geom_line(aes(y=y2, color="prediction")) + geom_line(aes(y=-abs(y2-y1), color="error")) + xlab("time") + ylab("number of burglaries")

print(sqrt(mean((as.numeric(pred_rf$test$predicted) - validation_label) ** 2)))

#SVM





# consider dropping date,beat,day_of_week and month as they are not propper numerical variables?

#This trains a linear regression on the dataset produced by make_features
#n_instances <- nrow(D)
n_features <- ncol(train)

#Cross-validation
#lambdas <- 0
lambdas <- c(10000000, 5000000, 1000000, 500000, 100000,50000,10000,5000) #,2500,1000,500,100,1,0.01)
lambdas <- c(2500,1000,500,100,1,0.01)

len <- length(lambdas)
pred <- matrix(0,ncol=len,nrow=nrow(validation))
rmse <- rep(0, len)
w_matrix <- matrix(0,ncol=len,nrow=n_features)

for (l in 1:len){
  lambda <- lambdas[l]
  w_matrix[,l] <- solve(t(train) %*% train + lambdas[l] * diag(1, n_features), t(train) %*% train_label)
  pred[,l] <- validation %*% w_matrix[,l]
  rmse[l] <- sqrt(mean((pred[,l] - validation_label) ** 2))
  cat(sprintf("lambda %f - rmse %f\n", lambdas[l], rmse[l]))
}

opt <- which.min(rmse)
w_opt <- w_matrix[,opt]
print(rmse)

# plot validation
df <- data.frame(x=1:length(validation_label),y1=validation_label,y2=pred[,opt])
ggplot(data=df, aes(x)) + geom_line(aes(y=y1, color="ground truth")) + geom_line(aes(y=y2, color="prediction")) + xlab("instance")+ylab("num burglaries")

# plot the cor of the target variable against all other variables
c = cor(features)
plot(c[3,-3],xlab="features",ylab="cor",pch=15)
