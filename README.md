# Stock-Prediction-Project

# Blog Link- https://medium.com/analytics-vidhya/stocks-market-prediction-multi-class-classification-f23fc3286136 

# Business Objective

There have been surge in people investing in stock from last few years and specially when people can invest from our their own smartphone, they have started understanding the importance of investment whether its stocks, real estate or metals.

Lots of people who do not know much about how stocks behave or at what time they should buy/sell a particular stock keeping the risk involved in mind, a Recommendation model can help them to choose the right stock.

A Model which can recommend users what to buy or what to sell in real time is our Business Objective.

# Constraints

1.Low Latency(In Real time within in few nano seconds the model should be able to classify the stocks according to the market )

2.Errors can be very costly, people can loose their money by one wrong prediction though the model can't be 100% accurate.

3.Interpretablity is important.

4.Probablity of a particular stock belonging to each class is needed.

# Machine Learning Formulation

This Recommendation model should classify a particular stock, whether its a "STRONG_BUY" "STRONG_SELL" "BUY" "SELL" "HOLD".

The major challenge of this classification problem is imabalance natures of class labels, most of times user has to HOLD the stocks and very few times STRONG BUY and STRONG SELL Signal is there.

# DATA

Scraped data for 64 US Companies from Yahoo Finance website, initially data has 41k rows and 67 features, Recommendation column has been added to data as the target class, This Recommendation column was calculated using domain knowledge of stock market(from some rule based system) and also from manual observation.

# PERFORMANCE METRIC

It is a simple multiclass classification problem, we can just use Multi-Class log loss for checking the performance.

Other than that we will use accuracy(after checking if data is balanced or not), here the important thing is we care equally about Precision and Recall because we care equall about False Positives and False Negatives.

Example1

Let's say we have a case when actually stock is "NOT A STRONG SELL" at that moment and model predicted it to be "STRONG SELL", here user will sell the stocks and after some time price of that stock rises and user won't be happy with the model and he/she might not use it afterwards. This is a case of False Positive.

Example2

let's say we have a case when actually stock is a "STRONG SELL" at the moment and model predicted it to be "NOT A STRONG SELL", Now in this case user can loose money because trend may change after some time and stocks price will decrease, User will definitely won't use the model. This is the case of False Negative.

So the best perfomance metric would be F1 score because F1 score is the harmonic mean between precision and recall and it will be high when both precision and recall will be high.

This Project was a part of my internship at Dimensions & Fact Solutions Private Limited(UK), The company is currently working on the stock market entry exit predictions, we have also deployed this project on a web app, where we used StreamLit as a Front end and Google Cloud Platform as a Backend.

I am not sharing the link of app here because i dont want people to use the app for real time trading, This web app is still in a very early stage and it may lead to wrong decisions.

Still if somebody wants to see this for educational or recruitment purpose, please drop a mail on "iamnishesh21@gmail.com".
