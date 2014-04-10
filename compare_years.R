#The script compare the diversity of distribution A on years [2000-2005] with distribution B
# on year 2006, and C on year [2007].
#That is done training a logistic regression on instances from A labeled +1, and from B (C) labeled -1 and then computing the Gini
#The bigger the gini, the more separable -and therefore different- are the distributions

#Log loss function and gradient, no regulariser
f <- function(w) {
  xw <- X %*% w
  ai <- log(exp(xw) + exp(-xw))
  #ai <- ai * is.finite(ai) + xw*is.infinite(ai)
  lterm <- sum(ai)
  
  meanop <- colSums(X*y)
  rterm <- w %*% meanop
  ret <- lterm - rterm
  
  if (is.infinite(ret)) {print (ret); quit()}
  
  ret
}

g <- function(w) {
  xw <- as.vector(X %*% w)
  lterm <- colSums(X*tanh(xw))
  rterm <- colSums(X*y)
  
  lterm - rterm
}

#Sigmoid function
conditional <- function(XX,ww){
  xw <- XX %*% ww
  #exp(xw) / (exp(xw) + exp(-xw))
  1 / (1 + exp(-2 * xw))
}

n_instances <- nrow(D)
n_features <- ncol(D)

cut1 <- floor(n_instances/8*6)
cut2 <- floor(n_instances/8*7) 


## TEST A AGAINST B

X <- D[1:cut2,]
y <- c(rep(1,cut1),rep(-1,cut2-cut1))
shuffle <- sample(nrow(X))
X <- X[shuffle, ]
y <- y[shuffle]

newcut <- floor(nrow(X)/5)
test <- X[1:newcut,] #hold out 1/5 of the dataset
test_label <- y[1:newcut]
X <- X[-(1:newcut),] #training set
y <- y[-(1:newcut)]

w0 <- 0.01*rnorm(ncol(X))

temp <- optim(w0, fn=f, gr=g, method="L-BFGS-B", control=list(trace=3, maxit=300))
w <- temp$par

pred <- conditional(test, w)
area <- auc((test_label+1)/2, pred)
gini = 2 * area - 1
print(gini)


## TEST A AGAINST C

X <- D[c(1:cut1,(cut2+1):nrow(D)),]
y <- c(rep(1,cut1),rep(-1,n_instances - cut2))
shuffle <- sample(nrow(X))
X <- X[shuffle, ]
y <- y[shuffle]

newcut <- floor(nrow(X)/5)
test <- X[1:newcut,] #hold out 1/5 of the dataset
test_label <- y[1:newcut]
X <- X[-(1:newcut),] #training set
y <- y[-(1:newcut)]

w0 <- 0.01*rnorm(ncol(X))

temp <- optim(w0, fn=f, gr=g, method="L-BFGS-B", control=list(trace=3, maxit=300))
w <- temp$par

pred <- conditional(test, w)
area <- auc((test_label+1)/2, pred)
gini = 2 * area - 1
print(gini)

#A / B gini = 0.79
#A / C gini = 0.92


