import tkinter as tk
from tkinter import messagebox

# Temporary prediction function
def predict_price():
    try:
        ram = int(ram_entry.get())
        battery = int(battery_entry.get())
        memory = int(memory_entry.get())

        # Dummy logic for testing only
        if ram < 1000:
            result = "Price Range 0 (Low Cost)"
        elif ram < 2000:
            result = "Price Range 1 (Medium Cost)"
        elif ram < 3000:
            result = "Price Range 2 (High Cost)"
        else:
            result = "Price Range 3 (Very High Cost)"

        result_label.config(text=result)

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numbers."
        )


# Main Window
root = tk.Tk()
root.title("Mobile Price Predictor")
root.geometry("400x350")

# Title
title = tk.Label(
    root,
    text="Mobile Price Predictor",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

# RAM
tk.Label(root, text="RAM").pack()
ram_entry = tk.Entry(root)
ram_entry.pack()

# Battery
tk.Label(root, text="Battery Power").pack()
battery_entry = tk.Entry(root)
battery_entry.pack()

# Memory
tk.Label(root, text="Internal Memory").pack()
memory_entry = tk.Entry(root)
memory_entry.pack()

# Predict Button
predict_btn = tk.Button(
    root,
    text="Predict",
    command=predict_price
)
predict_btn.pack(pady=20)

# Result
result_label = tk.Label(
    root,
    text="Waiting for prediction...",
    font=("Arial", 12, "bold")
)
result_label.pack()

root.mainloop()