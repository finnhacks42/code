Title
========================================================

This is an R Markdown document. Markdown is a simple formatting syntax for authoring web pages (click the **MD** toolbar button for help on Markdown).

When you click the **Knit HTML** button a web page will be generated that includes both content as well as the output of any embedded R code chunks within the document. You can embed an R code chunk like this:


```r
library(lubridate)
data$responcetime <- as.duration(data$starttime2 - data$dispatchtime2)
```

```
## Error: error in evaluating the argument 'x' in selecting a method for
## function 'as.duration': Error in data$starttime2 : object of type
## 'closure' is not subsettable
```



