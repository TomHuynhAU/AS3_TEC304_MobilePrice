import tkinter as tk
from tkinter import messagebox
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


BASE_DIR = Path(__file__).resolve().parent
TRAIN_FILE = BASE_DIR / "train.csv"

FEATURE_COLUMNS = [
    "battery_power", "blue", "clock_speed", "dual_sim", "fc", "four_g",
    "int_memory", "m_dep", "mobile_wt", "n_cores", "pc", "px_height",
    "px_width", "ram", "sc_h", "sc_w", "talk_time", "three_g",
    "touch_screen", "wifi"
]

PRICE_LABELS = {
    0: "Price Range 0 - Low Cost",
    1: "Price Range 1 - Medium Cost",
    2: "Price Range 2 - High Cost",
    3: "Price Range 3 - Very High Cost",
}


def train_model():
    if not TRAIN_FILE.exists():
        raise FileNotFoundError(
            "train.csv was not found. Please keep train.csv in the same folder as gui_app.py"
        )

    train_data = pd.read_csv(TRAIN_FILE)

    X = train_data[FEATURE_COLUMNS]
    y = train_data["price_range"]

    x_train, x_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    trained_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    trained_model.fit(x_train, y_train)

    val_predictions = trained_model.predict(x_val)
    accuracy = accuracy_score(y_val, val_predictions)

    return trained_model, accuracy


def get_number(entry, field_name, number_type=float):
    value = entry.get().strip()

    if value == "":
        raise ValueError(f"{field_name} cannot be empty.")

    return number_type(value)


def predict_price():
    try:
        data = {
            "battery_power": get_number(entries["battery_power"], "Battery Power", int),
            "blue": get_number(entries["blue"], "Bluetooth", int),
            "clock_speed": get_number(entries["clock_speed"], "Clock Speed", float),
            "dual_sim": get_number(entries["dual_sim"], "Dual SIM", int),
            "fc": get_number(entries["fc"], "Front Camera", int),
            "four_g": get_number(entries["four_g"], "4G", int),
            "int_memory": get_number(entries["int_memory"], "Internal Memory", int),
            "m_dep": get_number(entries["m_dep"], "Mobile Depth", float),
            "mobile_wt": get_number(entries["mobile_wt"], "Mobile Weight", int),
            "n_cores": get_number(entries["n_cores"], "Number of Cores", int),
            "pc": get_number(entries["pc"], "Primary Camera", int),
            "px_height": get_number(entries["px_height"], "Pixel Height", int),
            "px_width": get_number(entries["px_width"], "Pixel Width", int),
            "ram": get_number(entries["ram"], "RAM", int),
            "sc_h": get_number(entries["sc_h"], "Screen Height", int),
            "sc_w": get_number(entries["sc_w"], "Screen Width", int),
            "talk_time": get_number(entries["talk_time"], "Talk Time", int),
            "three_g": get_number(entries["three_g"], "3G", int),
            "touch_screen": get_number(entries["touch_screen"], "Touch Screen", int),
            "wifi": get_number(entries["wifi"], "WiFi", int),
        }

        binary_fields = [
            "blue", "dual_sim", "four_g",
            "three_g", "touch_screen", "wifi"
        ]

        for field in binary_fields:
            if data[field] not in [0, 1]:
                raise ValueError(f"{field} must be 0 or 1.")

        input_df = pd.DataFrame([data], columns=FEATURE_COLUMNS)

        prediction = int(model.predict(input_df)[0])

        result_label.config(
            text=f"Prediction: {PRICE_LABELS[prediction]}"
        )

    except ValueError as error:
        messagebox.showerror("Input Error", str(error))

    except Exception as error:
        messagebox.showerror("Prediction Error", str(error))


try:
    model, model_accuracy = train_model()

except Exception as error:
    messagebox.showerror("Model Error", str(error))
    raise SystemExit


root = tk.Tk()
root.title("Mobile Price Predictor")
root.geometry("620x720")

frame = tk.Frame(root, padx=15, pady=15)
frame.pack(fill="both", expand=True)

title = tk.Label(
    frame,
    text="Mobile Price Predictor",
    font=("Arial", 18, "bold")
)
title.grid(row=0, column=0, columnspan=4, pady=10)

accuracy_label = tk.Label(
    frame,
    text=f"Model Accuracy: {model_accuracy:.2%}",
    font=("Arial", 10)
)
accuracy_label.grid(row=1, column=0, columnspan=4, pady=5)

fields = [
    ("battery_power", "Battery Power"),
    ("blue", "Bluetooth (0/1)"),
    ("clock_speed", "Clock Speed"),
    ("dual_sim", "Dual SIM (0/1)"),
    ("fc", "Front Camera MP"),
    ("four_g", "4G (0/1)"),
    ("int_memory", "Internal Memory"),
    ("m_dep", "Mobile Depth"),
    ("mobile_wt", "Mobile Weight"),
    ("n_cores", "Number of Cores"),
    ("pc", "Primary Camera MP"),
    ("px_height", "Pixel Height"),
    ("px_width", "Pixel Width"),
    ("ram", "RAM"),
    ("sc_h", "Screen Height"),
    ("sc_w", "Screen Width"),
    ("talk_time", "Talk Time"),
    ("three_g", "3G (0/1)"),
    ("touch_screen", "Touch Screen (0/1)"),
    ("wifi", "WiFi (0/1)"),
]

entries = {}

start_row = 2

for index, (key, label_text) in enumerate(fields):
    row = start_row + index // 2
    col = (index % 2) * 2

    tk.Label(frame, text=label_text).grid(
        row=row,
        column=col,
        sticky="w",
        padx=5,
        pady=5
    )

    entry = tk.Entry(frame, width=15)
    entry.grid(
        row=row,
        column=col + 1,
        padx=5,
        pady=5
    )

    entries[key] = entry


example_values = {
    "battery_power": 842,
    "blue": 0,
    "clock_speed": 2.2,
    "dual_sim": 0,
    "fc": 1,
    "four_g": 0,
    "int_memory": 7,
    "m_dep": 0.6,
    "mobile_wt": 188,
    "n_cores": 2,
    "pc": 2,
    "px_height": 20,
    "px_width": 756,
    "ram": 2549,
    "sc_h": 9,
    "sc_w": 7,
    "talk_time": 19,
    "three_g": 0,
    "touch_screen": 0,
    "wifi": 1,
}

for key, value in example_values.items():
    entries[key].insert(0, str(value))


predict_btn = tk.Button(
    frame,
    text="Predict Price Range",
    command=predict_price,
    font=("Arial", 12, "bold"),
    width=20
)
predict_btn.grid(row=13, column=0, columnspan=4, pady=20)

result_label = tk.Label(
    frame,
    text="Waiting for prediction...",
    font=("Arial", 12, "bold")
)
result_label.grid(row=14, column=0, columnspan=4, pady=10)

note_label = tk.Label(
    frame,
    text="Note: 0 = No, 1 = Yes for Bluetooth, Dual SIM, 3G, 4G, Touch Screen and WiFi.",
    font=("Arial", 9),
    wraplength=560
)
note_label.grid(row=15, column=0, columnspan=4, pady=10)

root.mainloop()