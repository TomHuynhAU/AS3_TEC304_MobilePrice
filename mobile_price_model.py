# Mobile Price Range Prediction Model
# Alan_Verro

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

X = train.drop("price_range", axis=1)
y = train["price_range"]

x_train, x_val, y_train, y_val = train_test_split(
    X, 
    y, 
    test_size=0.2, 
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100, 
    random_state=42
)


model.fit(x_train, y_train)

val_predictions = model.predict(x_val)
accuracy_score(y_val, val_predictions)

print("Model Accuracy:", accuracy_score(y_val, val_predictions))

test_features = test.drop(columns=["id"], errors='ignore')
test_predictions = model.predict(test_features)
print(test_predictions)

output = pd.DataFrame({'id': test['id'], 'price_range': test_predictions})
output.to_csv('model_price_predictions.csv', index=False)