#Import Dataset
library(readr)
library(ggplot2)
library(dplyr)
library(hablar)
library(car)
library(caret)
data <- read_csv("cleaned.csv", col_types = cols(Genre = col_factor(levels = c("Dance", "Beats", "Rap"))))

#Examine Data
qqplot(data$Plays,data$Reposts)
qqplot(log(data$Plays),log(data$Reposts))

qqplot(data$Plays,data$Likes)
qqplot(log(data$Plays),log(data$Likes))

qqplot(data$Plays,data$Comments)
qqplot(log(data$Plays),log(data$Comments))

#Log transform variables
data_log <- data
data_log[,3:7] <- log(data_log[,3:7])

#Remove -inf values as log(0) = -inf
data_log <- rationalize(data_log)
data_log <- na.exclude(data_log)

#Build Linear Models

#Reposts
summary(lm(Reposts ~ Plays + Genre + Followers, data=data_log))
summary(lm(Reposts ~ Plays + Followers, data=data_log))
summary(lm(Reposts ~ Plays + Genre, data=data_log))
summary(lm(Reposts ~ Plays, data=data_log))
##Model with Genre, Followers added has highest Adj. R^2, and lowest Residual Std. Error
#Could've used AIC or selection algorithims, but I only had to choose 3 variables so I did it manually

#Summarise and Plot Model
model_rp <- lm(Reposts ~ Plays + Genre + Followers, data=data_log)
summary(model_rp)
plot(model_rp)

#Likes
summary(lm(Likes ~ Plays + Genre + Followers, data=data_log))
summary(lm(Likes ~ Plays + Followers, data=data_log))
summary(lm(Likes ~ Plays + Genre, data=data_log))
summary(lm(Likes ~ Plays, data=data_log))
##Model with Genre, Followers added has highest Adj. R^2 and lowest RSE

model_lp <- lm(Likes ~ Plays + Genre + Followers, data=data_log)
summary(model_lp)
plot(model_lp)


#Comments
summary(lm(Comments ~ Plays + Genre + Followers, data=data_log))
summary(lm(Comments ~ Plays + Followers, data=data_log))
summary(lm(Comments ~ Plays + Genre, data=data_log))
summary(lm(Comments ~ Plays, data=data_log))
##Model with Genre, Followers added has highest Adj. R^2, and lowest RSE

model_cp <- lm(Comments ~ Plays + Genre + Followers, data=data_log)
summary(model_cp)
plot(model_cp)


#Followers
model_fp <- lm(Plays ~ Followers + Genre, data=data_log)
summary(model_fp)
plot(model_fp)

#Outlier Test
outlierTest(model_cp)
outlierTest(model_fp)
outlierTest(model_rp)
outlierTest(model_lp)

#Cook's Distance for LP Model
cooksd_lp <- cooks.distance(model_lp)
plot(cooksd_lp, cex=2, main="Influential Obs by Cooks distance")  # plot cook's distance
abline(h = 4*mean(cooksd, na.rm=T), col="red")  # add cutoff line
text(x=1:length(cooksd_lp)+1, y=cooksd_lp, labels=ifelse(cooksd_lp>4*mean(cooksd_lp, na.rm=T),names(cooksd_lp),""), col="red")  # add labels

#Cook's Distance for CP Model
cooksd_cp <- cooks.distance(model_cp)
plot(cooksd_cp, cex=2, main="Influential Obs by Cooks distance")  # plot cook's distance
abline(h = 4*mean(cooksd_cp, na.rm=T), col="red")  # add cutoff line
text(x=1:length(cooksd_cp)+1, y=cooksd_cp, labels=ifelse(cooksd_cp>4*mean(cooksd_cp, na.rm=T),names(cooksd_cp),""), col="red")  # add labels

#Cook's Distance for FP Model
cooksd_fp <- cooks.distance(model_fp)
plot(cooksd_fp, cex=2, main="Influential Obs by Cooks distance")  # plot cook's distance
abline(h = 4*mean(cooksd_fp, na.rm=T), col="red")  # add cutoff line
text(x=1:length(cooksd_fp)+1, y=cooksd_fp, labels=ifelse(cooksd_fp>4*mean(cooksd_fp, na.rm=T),names(cooksd_fp),""), col="red")  # add labels

#Model Validation

#K-fold cross validation k = 10
train(Comments ~ Plays + Genre + Followers, data=na.exclude(data_log),trControl=trainControl(method="cv", number=10),method='bayesglm')
train(Reposts ~ Plays + Genre + Followers, data=na.exclude(data_log),trControl=trainControl(method="cv", number=10),method='bayesglm')
train(Likes ~ Plays + Genre + Followers, data=na.exclude(data_log),trControl=trainControl(method="cv", number=10),method='bayesglm')
train(Plays ~ Followers + Genre, data=na.exclude(data_log),trControl=trainControl(method="cv", number=10),method='bayesglm')

#Random forest
library(randomForest)

#Seperate Our Training and Test Sets
train <- sample(1:nrow(data_log),300)

l_for <- randomForest(Likes ~ Plays + Genre + Followers, data=data_log,subset =train);l_for
r_for <- randomForest(Reposts ~ Plays + Genre + Followers, data=data_log,subset=train);r_for
c_for <- randomForest(Comments ~ Plays + Genre + Followers, data=data_log,subset=train);c_for
p_for <- randomForest(Plays ~ Followers + Genre, data=data_log,subset=train);p_for

#Inference / predict new values
new_dat <- data.frame(Genre='Dance',Followers=log(2000),Plays=log(17000))
exp(predict(model_lp,new_dat,interval='confidence'))
exp(predict(model_rp,new_dat,interval='confidence'))
exp(predict(model_cp,new_dat,interval='confidence'))

#Shiny App

