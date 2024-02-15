import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# read processed_dataset.csv
processed_dataset = pd.read_csv('processed_dataset.csv')

# Data preprocessing
# Perform feature selection
selected_features = processed_dataset.iloc[:, :-1] # remove target column

# Scale the features
scaler = StandardScaler()
selected_features = scaler.fit_transform(selected_features)

# Perform imputation
imputer = SimpleImputer(strategy='median')
selected_features = imputer.fit_transform(selected_features)

# Save the preprocessed dataset
preprocessed_dataset = pd.DataFrame(selected_features, columns=selected_features.columns)
preprocessed_dataset.to_csv('preprocessed_dataset.csv', index=False)

# Feature engineering
# Perform feature transformation
engineered_features = selected_features ** 2

# Save the engineered dataset
engineered_dataset = pd.DataFrame(engineered_features, columns=selected_features.columns)
engineered_dataset.to_csv('engineered_dataset.csv', index=False)