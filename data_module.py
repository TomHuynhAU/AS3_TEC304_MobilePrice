
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(train_file="train.csv", test_file="test.csv"):
    train_data = pd.read_csv(train_file)
    test_data = pd.read_csv(test_file)

    print("Training data loaded successfully.")
    print("Testing data loaded successfully.")
    print("Train shape:", train_data.shape)
    print("Test shape:", test_data.shape)

    return train_data, test_data


def explore_data(train_data):
    print("\n--- First 5 Rows ---")
    print(train_data.head())

    print("\n--- Dataset Information ---")
    print(train_data.info())

    print("\n--- Statistical Summary ---")
    print(train_data.describe())

    print("\n--- Missing Values ---")
    print(train_data.isnull().sum())

    print("\n--- Price Range Count ---")
    print(train_data["price_range"].value_counts())


def preprocess_data(train_data, test_data):
    # Separate input features and target output
    X = train_data.drop("price_range", axis=1)
    y = train_data["price_range"]

    # Remove id column from test dataset because it is not useful for prediction
    if "id" in test_data.columns:
        test_data = test_data.drop("id", axis=1)

    # Split training data into training and validation sets
    X_train, X_valid, y_train, y_valid = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Scale the data so all features are on a similar range
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_valid_scaled = scaler.transform(X_valid)
    test_scaled = scaler.transform(test_data)

    print("\nData preprocessing completed successfully.")
    print("X_train:", X_train_scaled.shape)
    print("X_valid:", X_valid_scaled.shape)
    print("Test:", test_scaled.shape)

    return X_train_scaled, X_valid_scaled, y_train, y_valid, test_scaled, scaler


# This part runs only when this file is executed directly
if __name__ == "__main__":
    train_data, test_data = load_data()
    explore_data(train_data)

    X_train, X_valid, y_train, y_valid, test_data_scaled, scaler = preprocess_data(
        train_data,
        test_data
    )