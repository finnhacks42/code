#Random forest
library(randomForest)

pred_rf <- randomForest(x=rbind(train,validation), y=c(train_label,validation_label), xtest=test, ytest=test_label, ntree=50, do.trace = TRUE)

df <- data.frame(x=1:length(test_label), y1=test_label, y2=as.numeric(pred_rf$test$predicted))
ggplot(data=df, aes(x)) + geom_line(aes(y=y1, color="ground truth")) + geom_point(aes(y=y1, color="ground truth")) + geom_line(aes(y=y2, color="prediction")) + geom_line(aes(y=-abs(y2-y1), color="error")) + xlab("time") + ylab("number of burglaries")

print(sqrt(mean((as.numeric(pred_rf$test$predicted) - test_label) ** 2)))