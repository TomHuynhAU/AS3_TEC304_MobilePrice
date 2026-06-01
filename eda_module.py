import pandas as pd
import matplotlib.pyplot as plt


# Load dataset
df = pd.read_csv("train.csv")

print("Dataset loaded successfully.")


# -------------------------------
# Basic Dataset Information
# -------------------------------

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Dataset Shape ---")
print(df.shape)


# -------------------------------
# Price Range Distribution
# -------------------------------

plt.figure(figsize=(6, 4))

df["price_range"].value_counts().sort_index().plot(
    kind="bar"
)

plt.title("Price Range Distribution")
plt.xlabel("Price Range")
plt.ylabel("Count")

plt.show()


# -------------------------------
# RAM vs Price Range
# -------------------------------

plt.figure(figsize=(6, 4))

plt.scatter(df["ram"], df["price_range"])

plt.title("RAM vs Price Range")
plt.xlabel("RAM")
plt.ylabel("Price Range")

plt.show()


# -------------------------------
# Battery Power vs Price Range
# -------------------------------

plt.figure(figsize=(6, 4))

plt.scatter(df["battery_power"], df["price_range"])

plt.title("Battery Power vs Price Range")
plt.xlabel("Battery Power")
plt.ylabel("Price Range")

plt.show()


# -------------------------------
# Correlation Analysis
# -------------------------------

correlation = df.corr()

print("\n--- Correlation with Price Range ---")
print(correlation["price_range"].sort_values(ascending=False))


# -------------------------------
# Important Features
# -------------------------------

important_features = correlation["price_range"].sort_values(
    ascending=False
)

print("\n--- Most Important Features ---")
print(important_features.head(6))