#This trains a linear regression on the dataset produced by make_dataset3

n_instances <- nrow(D)
n_features <- ncol(D)

cut1 <- floor(n_instances/7*5)
cut2 <- floor(n_instances/7*6)
  
train <- as.matrix(D[1:cut1,])
train_label <- label[1:cut1]

validation <- as.matrix(D[(cut1+1):cut2,])
validation_label <- label[(cut1+1):cut2]

test <- as.matrix(D[-(1:cut2),])
test_label <- label[-(1:cut2)]

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

#plot validation
library(ggplot2)
df <- data.frame(x=1:length(validation_label),y1=validation_label,y2=pred[,opt])
ggplot(data=df, aes(x)) + geom_line(aes(y=y1, color="ground truth")) + geom_line(aes(y=y2, color="prediction"))


#Test
pred_test <- test %*% w_opt
print(sqrt(mean((pred_test - test_label) ** 2)))

#plot
library(ggplot2)
df <- data.frame(x=1:length(test_label),y1=test_label,y2=pred_test)
ggplot(data=df, aes(x)) + geom_line(aes(y=y1, color="ground truth")) + geom_point(aes(y=y1, color="ground truth")) + geom_line(aes(y=y2, color="prediction")) + geom_line(aes(y=-abs(y2-y1), color="abs error")) + xlab("time") + ylab("number of burglaries") + guides(color=guide_legend(title=NULL))

