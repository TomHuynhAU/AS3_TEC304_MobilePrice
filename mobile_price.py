# Mobile Price Prediction App

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def load_data():
    data = pd.read_csv("train.csv")
    print("Data loaded successfully")
    print(data.head())
    print(data.info())
    print("Missing values:")
    print(data.isnull().sum())
    return data


def train_model(data):
    X = data.drop("price_range", axis=1)
    y = data["price_range"]

    x_train, x_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=500,
        random_state=42
    )

    model.fit(x_train, y_train)

    val_predictions = model.predict(x_val)
    accuracy = accuracy_score(y_val, val_predictions)

    print("\nModel Accuracy:", accuracy)

    importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    })

    print("\nTop 5 Important Features:")
    print(importance.sort_values(by="Importance", ascending=False).head(5))

    validation_data = x_val.copy()
    validation_data["Actual Price Range"] = y_val.values
    validation_data["Predicted Price Range"] = val_predictions
    validation_data["Correct"] = validation_data["Actual Price Range"] == validation_data["Predicted Price Range"]

    return model, accuracy, validation_data


def price_text(value):
    if value == 0:
        return "Low Cost Phone"
    elif value == 1:
        return "Medium Cost Phone"
    elif value == 2:
        return "High Cost Phone"
    else:
        return "Very High Cost Phone"


def predict_price():
    try:
        values = []

        for entry in entries:
            value = entry.get()

            if value == "":
                messagebox.showerror("Error", "Please fill in all fields")
                return

            values.append(float(value))

        input_data = pd.DataFrame([values], columns=features)
        result = model.predict(input_data)[0]

        result_label.config(
            text="Manual Prediction: Price Range " + str(result) + " - " + price_text(result)
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_data():
    for entry in entries:
        entry.delete(0, tk.END)

    result_label.config(text="Prediction:")


def predict_from_csv():
    try:
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv")]
        )

        if file_path == "":
            return

        new_data = pd.read_csv(file_path)
        ids = new_data["id"] if "id" in new_data.columns else range(len(new_data))
        features_data = new_data.drop(columns=["id"], errors="ignore")

        predictions = model.predict(features_data)

        output = pd.DataFrame({
            "id": ids,
            "price_range": predictions
        })

        output.to_csv("mobile_price_predictions.csv", index=False)

        messagebox.showinfo(
            "Success",
            "Predictions saved to mobile_price_predictions.csv"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_validation_record():
    global current_index

    row = validation_data.iloc[current_index]

    for i, feature in enumerate(features):
        entries[i].delete(0, tk.END)
        entries[i].insert(0, row[feature])

    actual = int(row["Actual Price Range"])
    predicted = int(row["Predicted Price Range"])
    correct = row["Correct"]

    if correct:
        status = "Correct"
    else:
        status = "Wrong"

    validation_label.config(
        text=
        "Validation Record: " + str(current_index + 1) + " / " + str(len(validation_data)) +
        "\nActual: " + str(actual) + " - " + price_text(actual) +
        "\nPredicted: " + str(predicted) + " - " + price_text(predicted) +
        "\nResult: " + status
    )


def next_record():
    global current_index

    if current_index < len(validation_data) - 1:
        current_index += 1
        show_validation_record()


def previous_record():
    global current_index

    if current_index > 0:
        current_index -= 1
        show_validation_record()


# Main program
data = load_data()
model, accuracy, validation_data = train_model(data)

current_index = 0


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
root.geometry("1000x820")
root.configure(bg="#2f2f2f")


title = tk.Label(
    root,
    text="Mobile Price Predictor",
    font=("Arial", 20, "bold"),
    bg="#2f2f2f",
    fg="white"
)
title.pack(pady=10)


accuracy_label = tk.Label(
    root,
    text="Model Accuracy: " + str(round(accuracy * 100, 2)) + "%",
    font=("Arial", 13, "bold"),
    bg="#2f2f2f",
    fg="white"
)
accuracy_label.pack(pady=5)


frame = tk.Frame(root, bg="#2f2f2f")
frame.pack(pady=10)


entries = []

for i in range(len(features)):
    row = i // 2
    col = (i % 2) * 2

    label = tk.Label(
        frame,
        text=display_names[i],
        width=18,
        anchor="w",
        font=("Arial", 11, "bold"),
        bg="#2f2f2f",
        fg="white"
    )
    label.grid(row=row, column=col, padx=15, pady=5)

    entry = tk.Entry(
        frame,
        width=22,
        font=("Arial", 11),
        bg="#1f1f1f",
        fg="white",
        insertbackground="white"
    )
    entry.grid(row=row, column=col + 1, padx=15, pady=5)

    entry.insert(0, sample[i])
    entries.append(entry)


button_frame = tk.Frame(root, bg="#2f2f2f")
button_frame.pack(pady=10)


predict_button = tk.Button(
    button_frame,
    text="Predict Manual Input",
    command=predict_price,
    width=20,
    font=("Arial", 11, "bold")
)
predict_button.grid(row=0, column=0, padx=8)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_data,
    width=12,
    font=("Arial", 11, "bold")
)
clear_button.grid(row=0, column=1, padx=8)


csv_button = tk.Button(
    button_frame,
    text="Load CSV and Predict",
    command=predict_from_csv,
    width=22,
    font=("Arial", 11, "bold")
)
csv_button.grid(row=0, column=2, padx=8)


nav_frame = tk.Frame(root, bg="#2f2f2f")
nav_frame.pack(pady=10)


previous_button = tk.Button(
    nav_frame,
    text="Previous Test",
    command=previous_record,
    width=18,
    font=("Arial", 11, "bold")
)
previous_button.grid(row=0, column=0, padx=10)


next_button = tk.Button(
    nav_frame,
    text="Next Test",
    command=next_record,
    width=18,
    font=("Arial", 11, "bold")
)
next_button.grid(row=0, column=1, padx=10)


result_label = tk.Label(
    root,
    text="Prediction:",
    font=("Arial", 14, "bold"),
    bg="#2f2f2f",
    fg="white"
)
result_label.pack(pady=10)


validation_label = tk.Label(
    root,
    text="Validation Record:",
    font=("Arial", 13, "bold"),
    bg="#2f2f2f",
    fg="white",
    justify="left"
)
validation_label.pack(pady=10)


note = tk.Label(
    root,
    text="Use Previous Test / Next Test to browse validation data and compare actual vs predicted price range.",
    font=("Arial", 11),
    bg="#2f2f2f",
    fg="white"
)
note.pack(pady=5)


show_validation_record()

root.mainloop()