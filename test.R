library(mlbench)
library(caret)
library(lattice)
library(ggplot2)
library(pROC)
data(Sonar)
str(Sonar[,1:10])
inTraining <- createDataPartition(Sonar$Class, p =0.75, list = FALSE)
training <- Sonar[inTraining,]
testing <- Sonar[-inTraining,]

# fitControl<- trainControl(method = "repeatedcv", number=10,repeats =10)
# set.seed(825)
# gbmFit1 <- train(Class ~., data = training,
#                  method = "gbm",
#                  trControl = fitControl,
#                  verbose = FALSE)
# gbmFit1
# 
# gbmGrid1 <- expand.grid(interaction.depth = c(1,5,9),
#                         n.trees = (1:30)*50,
#                         shrinkage = 0.1,
#                         n.minobsinnode = 20)
# nrow(gbmGrid1)
# set.seed(825)
# gbmFit2 <- train(Class ~ ., data = training,
#                  method = "gbm",
#                  trControl = fitControl,
#                  verbose = FALSE,
#                  tuneGrid = gbmGrid1)
# gbmFit2
# trellis.par.set(caretTheme())
# plot(gbmFit2)
# 
# 
# fitControl <- trainControl(method = "repeatedcv",
#                            number = 10,
#                            repeats = 10,
#                            ## Estimate class probabilities
#                            classProbs = TRUE,
#                            ## Evaluate performance using 
#                            ## the following function
#                            summaryFunction = twoClassSummary)
# 
# set.seed(825)
# gbmFit3 <- train(Class ~ ., data = training,
#                  method = "gbm",
#                  trControl = fitControl,
#                  verbose = FALSE,
#                  tuneGrid = gbmGrid,
#                  ## Specify which metric to optimize
#                  metric = "ROC")
# gbmFit3
# 
# 
# 
# 
# library(caret)
# set.seed(998)
# inTraining <- createDataPartition(Sonar$Class, p = .75, list = FALSE)
# training <- Sonar[ inTraining,]
# testing  <- Sonar[-inTraining,]
# 
fitControl <- trainControl(method = "repeatedcv",
                           number = 2,
                           repeats = 1,
                           classProbs = TRUE,
                           summaryFunction = twoClassSummary,
                          search = "random")

set.seed(825)
# browser()
som_fit <- train(Class ~ ., data = training,
                 method = "xyf",
                 preProc = c("center", "scale"),
                 metric = "ROC",
                 tuneLength = 30,
                 trControl = fitControl)

ss<-predict(som_fit, newdata = testing[1:20,], type = "raw")

write.csv(ss, file = "test.csv", sep = ",")

