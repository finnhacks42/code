Multi-task learning
========================================================
Playing around with what this means, and a test for VW


```r
set.seed(29)
num_tasks = 10
num_features = 1
# lets first assume that for each task, the true relationship is a linear in
# one variable where the intercept and slope term are drawn from a normal
# distribution.  so for each task y = a + bx + noise
tasks = 1:num_tasks
a_list = runif(num_tasks, -100, 100)  #rnorm(num_tasks,mean=-1,sd=.2)
b_list = runif(num_tasks, -100, 100)  #rnorm(num_tasks,mean=3,sd=.5)
c_list = runif(num_tasks, -100, 100)  #rnorm(num_tasks,mean=2,sd=.7)
noise_sd = rnorm(num_tasks, mean = 20, sd = 10)
nrows_list = sample(1:100, num_tasks)

N = sum(nrows_list)
tmp <- matrix(nrow = N, ncol = 2 + (num_tasks + 1) * num_features)

row = 0
for (i in 1:num_tasks) {
    rows = nrows_list[i]
    a = a_list[i]
    b = b_list[i]
    c = c_list[i]
    sd = noise_sd[i]
    cat_features = as.integer(tasks == i)
    for (j in 1:rows) {
        # generate a row
        row = row + 1
        x = runif(1)
        # x2 = runif(1)
        y = a + b * x + rnorm(1, 0, sd)
        features = c(x)
        cross_terms = apply(expand.grid(features, cat_features), 1, FUN = function(x) {
            x[1] * x[2]
        })
        tmp[row, ] <- c(features, y, i, cross_terms)
    }
}

df <- data.frame(tmp)
names(df)[1:3] <- c("x", "y", "cat")
df$cat <- as.factor(df$cat)

s <- sample(1:nrow(df), nrow(df)/2)
train = df[s, ]
test = df[-s, ]
```



```r
lm1 <- lm(y ~ x, data = train)
test$l1 <- predict(lm1, newdata = test)
rmse1 <- sqrt(mean((test$y - test$l1)^2))
test <- test[with(test, order(cat, x)), ]
# lets do some plots
plot(train$x, train$y, col = train$cat)
lines(test$x, test$l1)
```

![plot of chunk A single model](figure/A_single_model.png) 



```r
lm2 <- lm(y ~ x + cat, data = train)
test$l2 <- predict(lm2, newdata = test)
rmse2 <- sqrt(mean((test$y - test$l2)^2))

# learns 3 lines with different intercepts but they are constrained to have
# the same slope
plot(train$x, train$y, col = train$cat)
for (t in 1:num_tasks) {
    tmp <- test[test$cat == t, ]
    lines(tmp$x, tmp$l2)
}
```

![plot of chunk r categorical regression](figure/r_categorical_regression.png) 




```r
# take the cross product of the feature space with the categories # note if
# you take cat of of this then it does different slopes but fixed
# intercept...
lm3 <- lm(y ~ x + cat + X4 + X5 + X6 + X7 + X8 + X9 + X10 + X11 + X12 + X13, 
    data = train)
test$l3 <- predict(lm3, newdata = test)
```

```
## Warning: prediction from a rank-deficient fit may be misleading
```

```r
rmse3 <- sqrt(mean((test$y - test$l3)^2))

# learns 3 lines with different intercept and slope
plot(df$x, df$y, col = df$cat)
for (t in 1:num_tasks) {
    tmp <- test[test$cat == t, ]
    lines(tmp$x, tmp$l3)
}
```

![plot of chunk personalized model](figure/personalized_model.png) 







To simply compare the rates, for simple linear regression rmse = 64.2693, for regression with the inclusion of categorical variables rmse = 32.754 and with the inclusion of the cross terms between the category and the feature set rmse = 29.8526



