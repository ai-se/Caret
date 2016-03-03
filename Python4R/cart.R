
#######

library(caret)
library("pROC")
library(C50)
library("ada")
difference <- function(x.1,x.2,...){
  x.1p <- do.call("paste", x.1)
  x.2p <- do.call("paste", x.2)
  x.1[! x.1p %in% x.2p, ]
}
randomSample = function(df,n) { 
  return (df[sample(nrow(df), n, replace=TRUE),])
}


SB<-function(datasets,nums){
  datasets$bug[datasets$bug >0] <-1
  datasets$bug[datasets$bug == 0] <-0
  datasets$bug <- factor(datasets$bug, labels = c("N","Y"))
  train_data<-randomSample(datasets,nrow(datasets))
  trainX <-train_data[,1:length(train_data)-1]
  trainY <-train_data$bug
  test_data<-difference(datasets, train_data)
  colnames(test_data)<-names(train_data)
  
  ########## Tuning Process #################
#   fitControl <- trainControl(method = "boot",classProbs = TRUE, summaryFunction = twoClassSummary)
#   Grid <-  expand.grid(.cp = c(0.0001,0.001,0.01,0.1,0.5))
#   Fit2 <- train(train_data$bug ~., data = train_data,
#                 method = "rpart",
#                 trControl = fitControl,
#                 tuneGrid = Grid,
#                 metric = "ROC")
  
  
  ########## repeats 100 times #################
  keep <-c()
  for( i in 1:10){
    train_data<-randomSample(datasets,nrow(datasets))
    trainX <-train_data[,1:length(train_data)-1]
    trainY <-train_data$bug
    test_data<-difference(datasets, train_data)
    colnames(test_data)<-names(train_data)

    ########## Default MODEl #################
    control2 <- rpart.control(cp=nums)
    Default_model<- rpart(train_data$bug ~ ., data = train_data, control=control2)
    Default_predicted <- predict(Default_model, test_data)
    frame_default_predicted <- data.frame(Default_predicted)
    names(frame_default_predicted)<-c('N','Y')
    Default_roc <-roc(predictor = frame_default_predicted$Y, response = test_data$bug, levels = rev(levels(test_data$bug)))
    Default_auc <-auc(Default_roc)
    keep[i] <- Default_auc
  }
#   cat(keep)
   return (median(keep))  ### return median values
  
}



set.seed(1)
setwd("/Users/WeiFu/Github/Caret/dataR")
# Fetch command line arguments
myArgs <- commandArgs(trailingOnly = TRUE)
data_src = myArgs[1]
param = as.numeric(myArgs[2])
results_data <-c()
data_src <-"./NASA/JM1.csv"
data_set <- read.csv(data_src, sep= ",")
results_data[1] <- SB(data_set, param)
cat(results_data)
