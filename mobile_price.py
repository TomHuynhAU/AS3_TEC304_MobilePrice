# Mobile Price Prediction App
# Part 1 - Susan: Load and check data
# Part 2 - Ashinka: Data analysis
# Part 3 - Alan: Machine learning model
# Part 4 - Tom: GUI application

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# --------------------------------------------------
# Part 1 - Susan
# Load and check data
# --------------------------------------------------

def load_data():
    data = pd.read_csv("train.csv")

    print("Data loaded successfully")
    print("\nFirst 5 rows:")
    print(data.head())

    print("\nData information:")
    print(data.info())

    print("\nMissing values:")
    print(data.isnull().sum())

    return data


# --------------------------------------------------
# Part 2 - Ashinka
# Data analysis
# --------------------------------------------------

def show_charts(data):
    data["price_range"].value_counts().sort_index().plot(kind="bar")
    plt.title("Price Range Count")
    plt.xlabel("Price Range")
    plt.ylabel("Number of Phones")
    plt.show()

    plt.scatter(data["ram"], data["price_range"])
    plt.title("RAM vs Price Range")
    plt.xlabel("RAM")
    plt.ylabel("Price Range")
    plt.show()


# --------------------------------------------------
# Part 3 - Alan
# Machine learning model
# --------------------------------------------------

def train_model(data):
    X = data.drop("price_range", axis=1)
    y = data["price_range"]

    x_train, x_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(x_train, y_train)

    predicted = model.predict(x_test)
    accuracy = accuracy_score(y_test, predicted)

    print("\nModel Accuracy:", accuracy)

    return model, accuracy


# --------------------------------------------------
# Part 4 - Tom
# GUI application
# --------------------------------------------------

def predict_price():
    try:
        values = []

        for entry in entries:
            value = entry.get()

            if value == "":
                messagebox.showerror("Error", "Please fill in all fields")
                return

            values.append(float(value))

        result = model.predict([values])[0]

        if result == 0:
            text = "Low Cost Phone"
        elif result == 1:
            text = "Medium Cost Phone"
        elif result == 2:
            text = "High Cost Phone"
        else:
            text = "Very High Cost Phone"

        result_label.config(
            text="Prediction: Price Range " + str(result) + " - " + text
        )

    except:
        messagebox.showerror("Error", "Please enter numbers only")


def clear_data():
    for entry in entries:
        entry.delete(0, tk.END)

    result_label.config(text="Prediction:")


# Main program
data = load_data()

# Uncomment this line if you want to show charts
# show_charts(data)

model, accuracy = train_model(data)


features = [
    "battery_power",
    "blue",
    "clock_speed",
    "dual_sim",
    "fc",
    "four_g",
    "int_memory",
    "m_dep",
    "mobile_wt",
    "n_cores",
    "pc",
    "px_height",
    "px_width",
    "ram",
    "sc_h",
    "sc_w",
    "talk_time",
    "three_g",
    "touch_screen",
    "wifi"
]


display_names = [
    "Battery Power",
    "Bluetooth",
    "Clock Speed",
    "Dual SIM",
    "Front Camera",
    "4G",
    "Internal Memory",
    "Mobile Depth",
    "Mobile Weight",
    "Number of Cores",
    "Primary Camera",
    "Pixel Height",
    "Pixel Width",
    "RAM",
    "Screen Height",
    "Screen Width",
    "Talk Time",
    "3G",
    "Touch Screen",
    "WiFi"
]


sample = [
    842, 0, 2.2, 0, 1, 0, 7, 0.6, 188, 2,
    2, 20, 756, 2549, 9, 7, 19, 0, 0, 1
]


root = tk.Tk()
root.title("Mobile Price Predictor")
root.geometry("900x720")
root.configure(bg="#2f2f2f")


title = tk.Label(
    root,
    text="Mobile Price Predictor",
    font=("Arial", 20, "bold"),
    bg="#2f2f2f",
    fg="white"
)
title.pack(pady=15)


accuracy_label = tk.Label(
    root,
    text="Model Accuracy: " + str(round(accuracy * 100, 2)) + "%",
    font=("Arial", 13, "bold"),
    bg="#2f2f2f",
    fg="white"
)
accuracy_label.pack(pady=5)


frame = tk.Frame(root, bg="#2f2f2f")
frame.pack(pady=20)


entries = []

for i in range(len(features)):
    row = i // 2
    col = (i % 2) * 2

    label = tk.Label(
        frame,
        text=display_names[i],
        width=18,
        anchor="w",
        font=("Arial", 12, "bold"),
        bg="#2f2f2f",
        fg="white"
    )
    label.grid(row=row, column=col, padx=15, pady=8)

    entry = tk.Entry(
        frame,
        width=22,
        font=("Arial", 12),
        bg="#1f1f1f",
        fg="white",
        insertbackground="white"
    )
    entry.grid(row=row, column=col + 1, padx=15, pady=8)

    entry.insert(0, sample[i])
    entries.append(entry)


button_frame = tk.Frame(root, bg="#2f2f2f")
button_frame.pack(pady=15)


predict_button = tk.Button(
    button_frame,
    text="Predict",
    command=predict_price,
    width=18,
    font=("Arial", 12, "bold")
)
predict_button.grid(row=0, column=0, padx=15)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_data,
    width=18,
    font=("Arial", 12, "bold")
)
clear_button.grid(row=0, column=1, padx=15)


result_label = tk.Label(
    root,
    text="Prediction:",
    font=("Arial", 16, "bold"),
    bg="#2f2f2f",
    fg="white"
)
result_label.pack(pady=20)


note = tk.Label(
    root,
    text="Note: For yes/no fields, use 1 for Yes and 0 for No.",
    font=("Arial", 12),
    bg="#2f2f2f",
    fg="white"
)
note.pack(pady=5)


root.mainloop()