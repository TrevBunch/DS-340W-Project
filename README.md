Modeling Fantasy Football Player Performance With An Emphasis on Rookie Players
=========================================================
by Kush Lalwani and Trevor Bunch

Why We Chose This Topic
------------

Problem: Fantasy football is continuously increasing in popularity and newer/casual users need more insight into their roster formation

Solution: Using data and machine learning can help improve decisions and we learned which models and features can give the best projections and insight

Problem: Issue of poor performance projecting rookies in our research and rookies are a valuable part of fantasy – can be top performers but initially undervalued

Solution: We want to improve upon past research and be able to predict rookies more accurately

Data
----

Data sourced from profootballreference.com, Sleeper, ESPN

Use 5 seasons of historical data (2019–2023) to predict NFL player’s 2024 fantasy points

Train/Test/Validation split = 70/20/10

Processing
-----------------

Clean data to include relevant attributes for fantasy football point calculations

Innovation
-----------------

Include college statistics and NFL draft information of players

Gives historical data to rookies which helps identify trends among successful rookie players

Add strength of schedule feature and preseason rankings

Models
------

Use 5 ML models to project points: Random Forest, Lasso Regression, XGBoost, Neural Network, Support Vector Regression

Create different models for different positions, weight relevant features higher for each position

Validation
-------

Use Grid Search Cross Validation to test multiple hyperparameter combinations for the models

Test on validation data: RMSE, MAE, R2

Evaluation
--------------------------

Compare our model’s projections to preseason media projections

Compare our projections and media projections to real 2024 results

Work
--------------------------

Collect all relevant data for player stats, draft order, and other non-quantitative stats

Implement using pandas and scikit-learn libraries in Python

Use a random split to train, test, and validate the various models' findings

Hypothesis: Using historical player and team statistics, we can accurately predict a player's season-long fantasy football score with a Root Mean Squared Error (RMSE) of ≤10 for non-rookie players and ≤15 for rookies.

Compare our model's findings to point projections from fantasy companies: Sleeper, FanDuel, DraftKings, etc.


