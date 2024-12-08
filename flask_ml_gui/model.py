import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
# Random Tree Forest Approach
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

# Load data
standardizedData = pd.read_csv('../ProcessedData.csv')

X = standardizedData.drop('Rented Bike Count', axis=1) #X = feature matrix
y = standardizedData['Rented Bike Count'] #y = target variable

poly = PolynomialFeatures(degree=1) 
X_poly = poly.fit_transform(X) 

def random_forest(X, y, folds, learning_rate=0.1, n_estimators=30):
    kf = KFold(n_splits=folds, shuffle=True, random_state=42) #split into folds for cross validation
    fold_mses = [] #just for documentation for the index of the best one
    fold_rs = []
    models = []

    for train_index, val_index in kf.split(X): #loop through the folds
        X_train, X_val = X[train_index], X[val_index]
        y_train, y_val = y[train_index], y[val_index]

        gbr = RandomForestRegressor(random_state=42)
        gbr.fit(X_train, y_train)

        # Predict and evaluate on the validation set
        y_pred = gbr.predict(X_val)
        mse = mean_squared_error(y_val, y_pred)
        fold_mses.append(mse)
        fold_rs.append(r2_score(y_val, y_pred))
        models.append(gbr)

    print(f"Finished Training")
    return models[np.argmin(fold_mses)]  # Return the best model

# Train and get the best model
best_model = random_forest(X_poly, y, folds=3)

class HourTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass  # No hyperparameters for this transformer
    
    def fit(self, X, y=None):
        # No fitting required for this transformation
        return self
    
    def transform(self, X):
        # Transform Hour data
        hour = X['Hour']
        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        hour = pd.concat([hour_sin, hour_cos], axis=1)
        hour = pd.DataFrame(hour)
        hour.columns = ['hour_sin', 'hour_cos']
        X.drop(columns=['Hour'])
        X = pd.concat([X, hour], axis=1)
        return X

# Perform Data Standardization
numerical_features = ['hour_sin', 'hour_cos', 'Temperature', 'Humidity', 'Wind speed', 'Visibility', 'Solar Radiation', 'Rainfall', 'Snowfall']
ct = ColumnTransformer([
        ('Standardize', StandardScaler(), numerical_features)
    ], remainder='passthrough')

# Train standardizer on correct data
ct.fit(pd.DataFrame(pd.read_csv('../NoOutlierData.csv')).drop('Rented Bike Count', axis=1))

hr_transform = HourTransformer()

# Form pipeline for usage in Web Development Application
pipeline = Pipeline([
    ('hour_transform', hr_transform),
    ('scaler', ct),  # Step 1: Standardize the data
    ('poly', poly),
    ('rf', best_model)  # Step 2: Random Forest model
])