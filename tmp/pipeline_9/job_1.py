import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Read the dataset
df = pd.read_csv('dataset.csv')

# Perform data preprocessing
scaler = StandardScaler()
df['features'] = scaler.fit_transform(df[['feature1', 'feature2', 'feature3']])
df['label'] = scaler.transform(df['label'])

# Save the processed dataset
df.to_csv('processed_dataset.csv', index=False)