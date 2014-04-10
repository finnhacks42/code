#Log loss function and gradient
f <- function(w) {
  xw <- X %*% w
  ai <- log(exp(xw) + exp(-xw))
  #ai <- ai * is.finite(ai) + xw*is.infinite(ai)
  lterm <- sum(ai)
  
  meanop <- colSums(X*y)
  rterm <- w %*% meanop
  reg <- lambda * (w %*% w)
  ret <- lterm - rterm + reg
  
  if (is.infinite(ret)) {print (ret); quit()}
  
  ret
}

g <- function(w) {
  xw <- as.vector(X %*% w)
  lterm <- colSums(X*tanh(xw))
  rterm <- colSums(X*y)
  reg <- 2 * lambda * w
  
  lterm - rterm + reg
}

#Sigmoid function
conditional <- function(XX,ww){
  xw <- XX %*% ww
  #exp(xw) / (exp(xw) + exp(-xw))
  1 / (1 + exp(-2 * xw))
}

#This trains a logistic regression on the dataset produced by make_dataset
n_instances <- nrow(D)
n_features <- ncol(D)

cut1 <- floor(n_instances/8*6)
cut2 <- floor(n_instances/8*7) 
  
train <- as.matrix(D[1:cut1,])
train_label <- label[1:cut1]

validation <- as.matrix(D[(cut1+1):cut2,])
validation_label <- label[(cut1+1):cut2]

test <- as.matrix(D[-(1:cut2),])
test_label <- label[-(1:cut2)]

#Cross-validation
#lambdas <- 0
lambdas <- c(50000,10000,5000,2500,1000,500,100,10,1,0.1,0.01, 0)

len <- length(lambdas)
areas <- rep(0,len)
pred <- matrix(0,ncol=len,nrow=nrow(validation))
w_matrix <- matrix(0,ncol=len,nrow=n_features)

X <- train
y <- train_label
w0 <- 0.01*rnorm(ncol(X))

for (l in 1:len){
  
  lambda <- lambdas[l]
  temp <- optim(w0, fn=f, gr=g, method="L-BFGS-B", control=list(trace=3, maxit=300))
  w_matrix[,l] <- temp$par
 
  pred[,l] <- conditional(validation, w_matrix[,l])
  areas[l] <- auc((validation_label+1)/2, pred[,l])
}
opt <- which(areas==max(areas))
w_opt <- w_matrix[,opt]
print(sum((round(pred[,opt])) == (validation_label+1)/2) / length(pred[,opt]))


#Test
pred_test <- conditional(test, w_opt)
print(auc((test_label+1)/2, pred_test))

print(sum((round(pred_test)) == (test_label+1)/2) / length(pred_test))

####
# Now train the same model but only with features 96 an 471, and the 1-column
# the most correlated as for 
# aggr10 <- data.frame(x=apply(D,2,function(x){cov(x,label)}))
# ggplot(data=aggr10,aes(x=1:nrow(aggr10), y=x)) + geom_point() + xlab("features") + ylab("correlation with label")

# E <- D[,c(96,471,ncol(D))]
# n_features <- ncol(D)
# 
# cut1 <- floor(n_instances/8*6)
# cut2 <- floor(n_instances/8*7) 
# 
# train <- as.matrix(D[1:cut1,])
# train_label <- label[1:cut1]
# 
# validation <- as.matrix(D[(cut1+1):cut2,])
# validation_label <- label[(cut1+1):cut2]
# 
# test <- as.matrix(D[-(1:cut2),])
# test_label <- label[-(1:cut2)]
# 
# #Cross-validation
# #lambdas <- 0
# lambdas <- c(50000,10000,5000,2500,1000,500,100,10,1,0.1, 0)
# 
# len <- length(lambdas)
# areas <- rep(0,len)
# pred <- matrix(0,ncol=len,nrow=nrow(validation))
# w_matrix <- matrix(0,ncol=len,nrow=n_features)
# 
# X <- train
# y <- train_label
# w0 <- 0.01*rnorm(ncol(X))
# 
# for (l in 1:len){
#   
#   lambda <- lambdas[l]
#   temp <- optim(w0, fn=f, gr=g, method="L-BFGS-B", control=list(trace=3, maxit=300))
#   w_matrix[,l] <- temp$par
#   
#   pred[,l] <- conditional(validation, w_matrix[,l])
#   areas[l] <- auc((validation_label+1)/2, pred[,l])
# }
# opt <- which(areas==max(areas))
# w_opt <- w_matrix[,opt]
# print(sum((round(pred[,opt])) == (validation_label+1)/2) / length(pred[,opt]))
# 
# 
# #Test
# pred_test <- conditional(test, w_opt)
# print(auc((test_label+1)/2, pred_test))
# 
# print(sum((round(pred_test)) == (test_label+1)/2) / length(pred_test))
