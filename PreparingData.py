import pandas as pd
from OutliersProcessing import removeOutliers, getOutliers
from sklearn.preprocessing import StandardScaler

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


getOutliers(data, ['Rented Bike Count', 'Temperature', 'Humidity', 'Wind speed', 'Visibility', 'Solar Radiation', 'Rainfall', 'Snowfall'])

# It seems like every rainy or snowy days are counted as outliers because the weather is normal most of the time.
# Therefore, not going to remove outliers for Rainfall and Snowfall

# A lot of outliers for Solar Radiation. We can test this out with our models. For now, not removing outliers for this one

# Around 150 outliers for Rented Bike Count and Wind Speed. Remove outliers for now

data = removeOutliers(data, ['Rented Bike Count', 'Temperature', 'Humidity', 'Wind speed', 'Visibility'])
data = data.reset_index(drop=True)
print(data)


# Splitting data between categorical and numericals set for standardization
categoricalFeatures = ['Hour', 'Seasons_Autumn', 'Seasons_Spring', 'Seasons_Summer', 'Seasons_Winter', 'Holiday_No Holiday']
numericalFeatures = ['Rented Bike Count', 'Temperature', 'Humidity', 'Wind speed', 'Visibility', 'Solar Radiation', 'Rainfall', 'Snowfall']
categoricalValues = data[categoricalFeatures]
standardizedData = data.drop(columns=categoricalFeatures)

scaler = StandardScaler()
scaler.fit(standardizedData)
standardizedData = scaler.transform(standardizedData)
standardizedData = pd.DataFrame(standardizedData)
standardizedData.columns = numericalFeatures

standardizedData = pd.concat([standardizedData, categoricalValues], axis=1)
print(standardizedData)


