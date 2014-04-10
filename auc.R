#Calculate AUC for a vector of label in {0,1} and a vector of prediction of the same lenght

library(ggplot2)

auc <- function(outcome, pred){
  N <- length(pred) 
  N_pos <- sum(outcome) #Number of P
  dfauc <- data.frame(out = outcome, prob = pred)
  dfauc <- dfauc[order(-dfauc$prob),] #Order by descending score
  
  dfauc$above <- (1:N) - cumsum(dfauc$out)
  return( 1- sum( dfauc$above * dfauc$out ) / (N_pos * (N-N_pos) ) )
}

ggplot_roc_curve <- function(outcome, prediction){
  
  Npos <- sum(outcome == 1)
  Nneg <- length(outcome) - Npos
  
  df <- data.frame(out = outcome, prob = prediction)
  df <- df[order(-df$prob),] #Order by descending score
  #data frame for TPR and FPR
  dfplot <- data.frame(tpr=c(0,cumsum(df$out) / Npos), fpr=c(0,(cumsum(df$out == 0)) / Nneg))
  ggplot(data=dfplot, aes(dfplot$fpr,dfplot$tpr)) + geom_line() + xlab("FPR") + ylab("TPR")
}