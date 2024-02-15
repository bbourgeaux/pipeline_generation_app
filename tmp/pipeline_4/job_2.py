import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('data.csv')

# Remove duplicates and inconsistencies
clean_data = data.drop_duplicates()
clean_data = clean_data.dropna()
clean_data = clean_data.reset_index(drop=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(clean_data.drop('target', axis=1), clean_data['target'], test_size=0.2)

# Train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model's accuracy
accuracy = accuracy_score(y_test, model.predict(X_test))

# Generate the analysis report
report = f"Accuracy: {accuracy:.2f}"
with open('analysis_report.txt', 'w') as f:
    f.write(report)