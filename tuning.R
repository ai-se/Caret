library(caret)
library(randomForest)


## prepare data
set.seed(1)
rm(list = ls())
mydata <- read.csv("data/JM1.csv", head = TRUE, sep = ",")
testdata <-read.csv("data/JM1_test.csv", head = TRUE, sep = ",")
# inTraining <-createDataPartition(mydata$X..label, p = 0.75, list = FALSE)
training <-mydata
testing <- testdata

### tuning
fitControl <- trainControl(method = "cv",number = 5, repeats = 1)
rfGrid <- expand.grid(mtry = seq(50,150,by=2))
rfFit <-train(X..label ~ ., data = training, method = "rf", trControl = fitControl,
              verbose = FALSE, tuneGrid = rfGrid)


### testing?a
pred <-predict(rfFit, newdata=testing)
perf_AUC = performance(pred,"auc")
perf_AUC@y.values[[1]]