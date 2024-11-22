import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Helper function
def findMinMax(data):
  q1 = data.quantile(0.25)
  q3 = data.quantile(0.75)
  min = q1 - 1.5 * (q3 - q1)
  max = q3 + 1.5 * (q3 - q1)
  return min, max

# Function to help us visualize the outliers. Produce boxplot and print out outliers
def getOutliers(data, features):
  for i, feature in enumerate(features, 1):
    plt.subplot(1,len(features),i)
    data[[feature]].boxplot()
    
    min, max = findMinMax(data[feature])
    outliers_lower = data[feature] < min
    outliers_upper = data[feature] > max
    
    if outliers_lower.any():
      print(feature, "- Lower outliers:\n", data.loc[outliers_lower, feature])
    if outliers_upper.any():
      print(feature, "- Upper outliers:\n", data.loc[outliers_upper, feature])
      
  plt.show()
  
# Return a new set of data with outliers removed
def removeOutliers(data, features):
  removeIdx = pd.Series([False] * len(data))
  for feature in features:
    min, max = findMinMax(data[feature])
    outliers_lower = data[feature] < min
    outliers_upper = data[feature] > max
    
    removeIdx = removeIdx | outliers_lower | outliers_upper

  return data.loc[~removeIdx]


# Main

data = pd.DataFrame(pd.read_csv('./SeoulBikeData.csv'))

# Remove rows with non-functioning day / no bike rented
functioningDay = data['Functioning Day'] == 'Yes'
data = data.loc[functioningDay]

# Dropping some features:
# Date: can't process and we already have the holiday feature
# Dew temp: not relevant
# Functioning day: already process
data = data.drop(columns=['Date', 'Dew point temperature', 'Functioning Day'])


# One Hot Encode categorical features
# Hour should be categorical too. Not sure how to handle it yet
data = pd.get_dummies(data, columns=['Seasons'], dtype=int)
data = pd.get_dummies(data, columns=['Holiday'], dtype=int, drop_first=True)


# getOutliers(data, ['Rented Bike Count', 'Temperature', 'Humidity', 'Wind speed', 'Visibility', 'Solar Radiation', 'Rainfall', 'Snowfall'])

# It seems like every rainy or snowy days are counted as outliers because the weather is normal most of the time.
# Therefore, not going to remove outliers for Rainfall and Snowfall

# A lot of outliers for Solar Radiation. We can test this out with our models. For now, not removing outliers for this one

# Around 150 outliers for Rented Bike Count and Wind Speed. Remove outliers for now

data = removeOutliers(data, ['Rented Bike Count', 'Temperature', 'Humidity', 'Wind speed', 'Visibility'])
data = data.reset_index(drop=True)

# Splitting data between categorical and numericals set for standardization
categorical_features = ['Hour', 'Seasons_Autumn', 'Seasons_Spring', 'Seasons_Summer', 'Seasons_Winter', 'Holiday_No Holiday']
numerical_features = ['Rented Bike Count', 'Temperature', 'Humidity', 'Wind speed', 'Visibility', 'Solar Radiation', 'Rainfall', 'Snowfall']
categorical_values = data[categorical_features]
numerical_values = data[numerical_features]

scaler = StandardScaler()
numerical_values = scaler.fit_transform(numerical_values)
numerical_values = pd.DataFrame(numerical_values)
numerical_values.columns = numerical_features

processed_data = pd.concat([numerical_values, categorical_values], axis=1)
print(processed_data)

# Save to a new CSV file
processed_data.to_csv('ProcessedData.csv', index=False)


