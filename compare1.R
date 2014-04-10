#Compare logistic regression and benchmark1 on a ROC curve
#TO RUN AFTER logistic_regression.R

n_beat <- 375
Npos <- sum(test_label == 1)
Nneg <- length(pred_test) - Npos

df <- data.frame(out = (test_label+1)/2, prob = pred_test)
df <- df[order(-df$prob),] #Order by descending score
#data frame for TPR and FPR
dfplot <- data.frame(tpr=c(0,cumsum(df$out) / Npos), fpr=c(0,(cumsum(df$out == 0)) / Nneg))
plot <- ggplot(data=dfplot, aes(dfplot$fpr,dfplot$tpr)) + geom_line() + xlab("FPR") + ylab("TPR")

#Naive benchmark 1
b1_pred <- rep(round(naive_freq),length(test_label))
b1 <- data.frame(tpr=sum(b1_pred[which(test_label==1,arr.ind=TRUE)] == 1) / Npos, fpr=sum(b1_pred[which(test_label==-1,arr.ind=TRUE)] == 1) / Nneg)
plot <- plot + geom_point(data=b1, aes(b1$fpr, b1$tpr),colour = "red", size = I(2.5), shape = 15)

#Day prediction based on day of the week, benchmark 1
day_index <- (2 * n_beat)
b2_pred <- rep(0,length(test_label))
for (i in 1:7){
  days <- which(test[,day_index+i] == 1, arr.ind=TRUE)
  
  b2_pred[days] <- round(day_freq[i])
}
b2 <- data.frame(tpr=sum(b2_pred[which(test_label==1,arr.ind=TRUE)] == 1) / Npos, fpr=sum(b2_pred[which(test_label==-1,arr.ind=TRUE)] == 1) / Nneg)
plot <- plot + geom_point(data=b2, aes(b2$fpr, b2$tpr), colour="blue", size = I(2.5), shape = 16)

#Day prediction based on day of the week and month, benchmark 1
month_index <- (2 * n_beat + 7) 
b3_pred <- rep(0,length(test_label))
for (i in 1:7){
  for (j in 1:12){
    days <- which(test[,day_index+i] == 1 & test[,month_index+j] == 1, arr.ind=TRUE)
    b3_pred[days] <- round(month_freq[i,j])
  }
}
b3 <- data.frame(tpr=sum(b3_pred[which(test_label==1,arr.ind=TRUE)] == 1) / Npos, fpr=sum(b3_pred[which(test_label==-1,arr.ind=TRUE)] == 1) / Nneg)
plot <- plot + geom_point(data=b3, aes(b3$fpr, b3$tpr), colour="yellow", size = I(2.5), shape = 17)

#Plot also line of random choice
df0 <- data.frame(x=c(0,1),y=c(0,1))
plot <- plot + geom_line(data=df0, aes(df0$x,df0$y))

plot