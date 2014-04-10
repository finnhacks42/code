Crime Waves, Hotspots and Hotdots : Spatio-temporal patterns in crime
========================================================

Existing predictive policing methods rely heavily on mapping crime levels to idenfify 'hot spots', geographical areas of high crime that persist over time. A common method is to use 2d kernal density estimation to generate a smooth map of the geographical distribution of crime. The kernal width and the time-window on which to aggreagte points may be optimized based on huristics or cross-validation. The time-windows used are typcially relatively long (6 months-1 year) so method essentially predicts that crime today at a given place will be the (spatially smoothed) long term average of crime at that location. 

Also prevelent in the liturature is the notion of repeat victimization. A few victims (or locations) account for a large percentage of the total number of crimes. The risk of a repeat event decays rapidly with time leading to the notion of high crime areas that are very localized in both time and space, sometimes refered to as 'hot dots'. Clusters of hot-dots may lead to a temporaly unstable hotspot. The extent and characteristics of repeat and near repeat victimisation may depend on neighbourhood features, including housing homogeneity, and socioeconomic metrics.

This implies there should be non-trivial spatial and temporal patterns in crime event data that could be captured by a machine learning algorithm.





Build features based on the reporting area as the geographical level of aggregation. 

The target variable will be the number of crimes in an area on each day. 

Crimes are categoriesed into types: agg_assult, assult, burglary, crim_misch, flid, found, other, robbery, theft, uumv

and into the type of premesis they were commited at: APARTMENT, APARTMENT_PARKING, BUSINESS_PARKING, CONVENIENCE_STORE, DEPARTMENT_STORE, DRIVEWAY, OTHER, PUBLIC_STREET, RESIDENCE, SCHOOL

The features will be the number of crimes of each type over the last day, 7 days and year, and the number of crimes targeting each premesis type over the last day, 7 days and year. There are 10 types of crime and 3 time periods we aggregate over giving 30 features, plus another 30 for the 10 types of premisis/days back combination. Then I also calculate the total crime over all types/premesis for each period back yeilding 63 features.

I built features for 2000,2001 & 2002




This gives a data set with 63 features and 830010 instances. Each instance corresponds to a given reporting area on a given day. Split it into a training and a test data set.



We build a baseline model with the total amount of crime over the past year as the only feature.

```
## 
## Call:
## lm(formula = target ~ A0ones_1_365, data = train)
## 
## Residuals:
##    Min     1Q Median     3Q    Max 
## -5.983 -0.355 -0.137  0.093 14.650 
## 
## Coefficients:
##              Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  4.68e-03   1.58e-03    2.96   0.0031 ** 
## A0ones_1_365 2.76e-03   6.27e-06  440.00   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 0.762 on 415003 degrees of freedom
## Multiple R-squared:  0.318,	Adjusted R-squared:  0.318 
## F-statistic: 1.94e+05 on 1 and 415003 DF,  p-value: <2e-16
```


And compare that the the results we get using all the features

```
## 
## Call:
## lm(formula = target ~ ., data = train)
## 
## Residuals:
##    Min     1Q Median     3Q    Max 
## -5.763 -0.353 -0.139  0.091 14.634 
## 
## Coefficients: (6 not defined because of singularities)
##                               Estimate Std. Error t value Pr(>|t|)    
## (Intercept)                   1.04e-02   1.84e-03    5.66  1.5e-08 ***
## A0crime_trunk_theft_1        -5.73e-03   1.60e-02   -0.36  0.71980    
## A0crime_trunk_theft_7         2.53e-02   5.96e-03    4.24  2.2e-05 ***
## A0crime_trunk_theft_365       2.47e-03   3.20e-04    7.72  1.2e-14 ***
## A0crime_trunk_flid_1          1.16e-02   1.87e-02    0.62  0.53569    
## A0crime_trunk_flid_7          1.23e-02   6.98e-03    1.76  0.07853 .  
## A0crime_trunk_flid_365        3.09e-03   4.19e-04    7.38  1.6e-13 ***
## A0crime_trunk_robbery_1       2.71e-02   1.81e-02    1.49  0.13503    
## A0crime_trunk_robbery_7       1.14e-02   6.82e-03    1.68  0.09317 .  
## A0crime_trunk_robbery_365     3.74e-03   3.56e-04   10.53  < 2e-16 ***
## A0crime_trunk_other_1        -3.26e-03   1.64e-02   -0.20  0.84257    
## A0crime_trunk_other_7         1.38e-02   6.13e-03    2.25  0.02428 *  
## A0crime_trunk_other_365       2.42e-03   3.44e-04    7.02  2.2e-12 ***
## A0crime_trunk_burglary_1      2.38e-03   1.69e-02    0.14  0.88777    
## A0crime_trunk_burglary_7      3.00e-02   6.31e-03    4.76  1.9e-06 ***
## A0crime_trunk_burglary_365    1.23e-03   3.67e-04    3.34  0.00084 ***
## A0crime_trunk_assult_1       -1.39e-03   1.65e-02   -0.08  0.93289    
## A0crime_trunk_assult_7        1.65e-02   6.17e-03    2.67  0.00755 ** 
## A0crime_trunk_assult_365      2.27e-03   3.48e-04    6.51  7.4e-11 ***
## A0crime_trunk_uumv_1         -2.98e-03   1.71e-02   -0.17  0.86140    
## A0crime_trunk_uumv_7          2.11e-02   6.38e-03    3.30  0.00096 ***
## A0crime_trunk_uumv_365        2.57e-03   3.80e-04    6.77  1.3e-11 ***
## A0crime_trunk_agg_assult_1    2.42e-02   1.78e-02    1.36  0.17394    
## A0crime_trunk_agg_assult_7    8.02e-03   6.65e-03    1.21  0.22779    
## A0crime_trunk_agg_assult_365  2.36e-03   4.71e-04    5.00  5.7e-07 ***
## A0crime_trunk_crim_misch_1    3.64e-03   1.68e-02    0.22  0.82802    
## A0crime_trunk_crim_misch_7    1.36e-02   6.25e-03    2.18  0.02937 *  
## A0crime_trunk_crim_misch_365  3.03e-03   3.77e-04    8.04  9.1e-16 ***
## A0crime_trunk_found_1         1.61e-03   1.71e-02    0.09  0.92469    
## A0crime_trunk_found_7         2.55e-02   6.38e-03    4.00  6.3e-05 ***
## A0crime_trunk_found_365       2.11e-03   3.37e-04    6.26  3.9e-10 ***
## A0prem_PUBLIC_STREET_1        9.27e-03   1.65e-02    0.56  0.57447    
## A0prem_PUBLIC_STREET_7       -8.14e-03   6.17e-03   -1.32  0.18754    
## A0prem_PUBLIC_STREET_365     -1.98e-04   3.39e-04   -0.58  0.55868    
## A0prem_BUSINESS_PARKING_1     2.51e-02   1.78e-02    1.41  0.15709    
## A0prem_BUSINESS_PARKING_7    -4.52e-03   6.62e-03   -0.68  0.49423    
## A0prem_BUSINESS_PARKING_365   9.18e-05   3.65e-04    0.25  0.80141    
## A0prem_APARTMENT_1            8.06e-03   1.66e-02    0.48  0.62792    
## A0prem_APARTMENT_7           -1.80e-03   6.21e-03   -0.29  0.77205    
## A0prem_APARTMENT_365          4.31e-04   3.41e-04    1.26  0.20637    
## A0prem_RESIDENCE_1            9.90e-03   1.66e-02    0.60  0.55014    
## A0prem_RESIDENCE_7           -8.72e-03   6.19e-03   -1.41  0.15906    
## A0prem_RESIDENCE_365          2.45e-04   3.42e-04    0.72  0.47360    
## A0prem_OTHER_1                1.77e-02   1.62e-02    1.09  0.27359    
## A0prem_OTHER_7               -9.67e-03   6.04e-03   -1.60  0.10932    
## A0prem_OTHER_365             -9.30e-05   3.28e-04   -0.28  0.77654    
## A0prem_SCHOOL_1               2.72e-02   1.94e-02    1.40  0.16181    
## A0prem_SCHOOL_7               1.95e-02   7.08e-03    2.75  0.00590 ** 
## A0prem_SCHOOL_365            -3.57e-04   3.44e-04   -1.04  0.30019    
## A0prem_APARTMENT_PARKING_1    1.42e-02   1.65e-02    0.86  0.39174    
## A0prem_APARTMENT_PARKING_7   -3.19e-03   6.16e-03   -0.52  0.60471    
## A0prem_APARTMENT_PARKING_365 -3.83e-04   3.38e-04   -1.13  0.25709    
## A0prem_DRIVEWAY_1             2.12e-02   1.71e-02    1.24  0.21559    
## A0prem_DRIVEWAY_7            -7.08e-04   6.40e-03   -0.11  0.91196    
## A0prem_DRIVEWAY_365           1.45e-04   3.78e-04    0.38  0.70079    
## A0prem_DEPARTMENT_STORE_1     3.25e-02   2.02e-02    1.61  0.10728    
## A0prem_DEPARTMENT_STORE_7     1.14e-02   7.32e-03    1.56  0.11854    
## A0prem_DEPARTMENT_STORE_365  -4.95e-04   3.24e-04   -1.53  0.12680    
## A0prem_CONVENIENCE_STORE_1          NA         NA      NA       NA    
## A0prem_CONVENIENCE_STORE_7          NA         NA      NA       NA    
## A0prem_CONVENIENCE_STORE_365        NA         NA      NA       NA    
## A0ones_1_1                          NA         NA      NA       NA    
## A0ones_1_7                          NA         NA      NA       NA    
## A0ones_1_365                        NA         NA      NA       NA    
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 0.76 on 414947 degrees of freedom
## Multiple R-squared:  0.32,	Adjusted R-squared:  0.32 
## F-statistic: 3.43e+03 on 57 and 414947 DF,  p-value: <2e-16
```

```
## Warning: prediction from a rank-deficient fit may be misleading
```


The ratio of the root-mean-squared-errors is 0.9988 ... not a lot of improvment.

What happens if we model at the sector level




```
## 
## Call:
## lm(formula = target ~ A0ones_1_365, data = train)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -21.066  -3.319  -0.367   2.954  28.669 
## 
## Coefficients:
##               Estimate Std. Error t value Pr(>|t|)    
## (Intercept)  -2.05e-02   1.32e-01   -0.15     0.88    
## A0ones_1_365  2.79e-03   2.09e-05  133.80   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 4.9 on 11678 degrees of freedom
## Multiple R-squared:  0.605,	Adjusted R-squared:  0.605 
## F-statistic: 1.79e+04 on 1 and 11678 DF,  p-value: <2e-16
```

```
## 
## Call:
## lm(formula = target ~ ., data = train)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -18.573  -3.272  -0.351   2.930  28.487 
## 
## Coefficients: (6 not defined because of singularities)
##                              Estimate Std. Error t value Pr(>|t|)    
## (Intercept)                   0.39129    0.22613    1.73  0.08359 .  
## A0crime_trunk_theft_1         0.24026    0.09934    2.42  0.01559 *  
## A0crime_trunk_theft_7        -0.00945    0.03650   -0.26  0.79566    
## A0crime_trunk_theft_365       0.00940    0.00250    3.76  0.00017 ***
## A0crime_trunk_flid_1          0.28067    0.11623    2.41  0.01576 *  
## A0crime_trunk_flid_7         -0.03727    0.04321   -0.86  0.38845    
## A0crime_trunk_flid_365        0.00845    0.00258    3.27  0.00107 ** 
## A0crime_trunk_robbery_1       0.20836    0.11293    1.85  0.06506 .  
## A0crime_trunk_robbery_7      -0.04078    0.04205   -0.97  0.33221    
## A0crime_trunk_robbery_365     0.01524    0.00275    5.54  3.1e-08 ***
## A0crime_trunk_other_1         0.16514    0.10207    1.62  0.10571    
## A0crime_trunk_other_7        -0.01180    0.03756   -0.31  0.75329    
## A0crime_trunk_other_365       0.01162    0.00302    3.84  0.00012 ***
## A0crime_trunk_burglary_1      0.24106    0.10481    2.30  0.02147 *  
## A0crime_trunk_burglary_7      0.01218    0.03862    0.32  0.75242    
## A0crime_trunk_burglary_365    0.00682    0.00294    2.32  0.02031 *  
## A0crime_trunk_assult_1        0.26143    0.10294    2.54  0.01111 *  
## A0crime_trunk_assult_7        0.01401    0.03782    0.37  0.71099    
## A0crime_trunk_assult_365      0.00952    0.00279    3.41  0.00066 ***
## A0crime_trunk_uumv_1          0.36264    0.10673    3.40  0.00068 ***
## A0crime_trunk_uumv_7         -0.03448    0.03893   -0.89  0.37589    
## A0crime_trunk_uumv_365        0.01026    0.00297    3.45  0.00055 ***
## A0crime_trunk_agg_assult_1    0.23530    0.11084    2.12  0.03378 *  
## A0crime_trunk_agg_assult_7   -0.00119    0.04039   -0.03  0.97647    
## A0crime_trunk_agg_assult_365  0.00566    0.00325    1.74  0.08178 .  
## A0crime_trunk_crim_misch_1    0.28477    0.10394    2.74  0.00616 ** 
## A0crime_trunk_crim_misch_7   -0.01215    0.03788   -0.32  0.74849    
## A0crime_trunk_crim_misch_365  0.00911    0.00289    3.15  0.00164 ** 
## A0crime_trunk_found_1         0.18313    0.10591    1.73  0.08380 .  
## A0crime_trunk_found_7        -0.01434    0.03891   -0.37  0.71247    
## A0crime_trunk_found_365       0.00981    0.00272    3.60  0.00032 ***
## A0prem_PUBLIC_STREET_1       -0.13324    0.10244   -1.30  0.19337    
## A0prem_PUBLIC_STREET_7        0.03689    0.03781    0.98  0.32934    
## A0prem_PUBLIC_STREET_365     -0.00822    0.00260   -3.16  0.00159 ** 
## A0prem_BUSINESS_PARKING_1    -0.24672    0.11112   -2.22  0.02642 *  
## A0prem_BUSINESS_PARKING_7     0.07698    0.04063    1.89  0.05816 .  
## A0prem_BUSINESS_PARKING_365  -0.00839    0.00290   -2.90  0.00375 ** 
## A0prem_APARTMENT_1           -0.17969    0.10338   -1.74  0.08223 .  
## A0prem_APARTMENT_7            0.00694    0.03870    0.18  0.85761    
## A0prem_APARTMENT_365         -0.00636    0.00279   -2.28  0.02275 *  
## A0prem_RESIDENCE_1           -0.14925    0.10257   -1.46  0.14567    
## A0prem_RESIDENCE_7            0.02620    0.03771    0.69  0.48729    
## A0prem_RESIDENCE_365         -0.00810    0.00298   -2.72  0.00661 ** 
## A0prem_OTHER_1               -0.22474    0.10078   -2.23  0.02576 *  
## A0prem_OTHER_7                0.03280    0.03735    0.88  0.37989    
## A0prem_OTHER_365             -0.00758    0.00271   -2.80  0.00519 ** 
## A0prem_SCHOOL_1              -0.17306    0.11873   -1.46  0.14500    
## A0prem_SCHOOL_7               0.03953    0.04172    0.95  0.34339    
## A0prem_SCHOOL_365            -0.00774    0.00274   -2.83  0.00473 ** 
## A0prem_APARTMENT_PARKING_1   -0.21594    0.10285   -2.10  0.03578 *  
## A0prem_APARTMENT_PARKING_7    0.05084    0.03738    1.36  0.17385    
## A0prem_APARTMENT_PARKING_365 -0.00917    0.00284   -3.23  0.00123 ** 
## A0prem_DRIVEWAY_1            -0.27676    0.10646   -2.60  0.00935 ** 
## A0prem_DRIVEWAY_7             0.08945    0.03863    2.32  0.02061 *  
## A0prem_DRIVEWAY_365          -0.00580    0.00274   -2.12  0.03441 *  
## A0prem_DEPARTMENT_STORE_1    -0.38606    0.12737   -3.03  0.00244 ** 
## A0prem_DEPARTMENT_STORE_7     0.12176    0.04566    2.67  0.00768 ** 
## A0prem_DEPARTMENT_STORE_365  -0.00834    0.00255   -3.28  0.00106 ** 
## A0prem_CONVENIENCE_STORE_1         NA         NA      NA       NA    
## A0prem_CONVENIENCE_STORE_7         NA         NA      NA       NA    
## A0prem_CONVENIENCE_STORE_365       NA         NA      NA       NA    
## A0ones_1_1                         NA         NA      NA       NA    
## A0ones_1_7                         NA         NA      NA       NA    
## A0ones_1_365                       NA         NA      NA       NA    
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 4.83 on 11622 degrees of freedom
## Multiple R-squared:  0.618,	Adjusted R-squared:  0.616 
## F-statistic:  330 on 57 and 11622 DF,  p-value: <2e-16
```

```
## Warning: prediction from a rank-deficient fit may be misleading
```

The ratio of the all feature rmse to the baseline rmse is now 0.9892













