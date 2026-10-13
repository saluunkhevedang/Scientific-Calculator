import tkinter as tk
import math
import re

# Main Window
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("500x700")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

degree_mode = True

# Display
display = tk.Entry(
    root,
    font=("Arial", 24),
    bg="#313244",
    fg="white",
    insertbackground="white",
    bd=0,
    justify="right"
)
display.pack(fill="both", padx=15, pady=20, ipady=20)


# Calculator Functions
def press(value):
    display.insert(tk.END, value)


def clear():
    display.delete(0, tk.END)


def delete():
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])


def toggle_mode():
    global degree_mode
    degree_mode = not degree_mode
    mode_button.config(text="DEG" if degree_mode else "RAD")


def factorial(x):
    if x < 0 or not float(x).is_integer():
        raise ValueError("Invalid factorial")
    return math.factorial(int(x))


def calculate():
    try:
        expression = display.get()

        # Replace mathematical constants
        expression = expression.replace("π", "pi")
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")

        # Mathematical functions
        functions = {
            "sin": lambda x: math.sin(math.radians(x) if degree_mode else x),
            "cos": lambda x: math.cos(math.radians(x) if degree_mode else x),
            "tan": lambda x: math.tan(math.radians(x) if degree_mode else x),
            "asin": lambda x: math.degrees(math.asin(x)) if degree_mode else math.asin(x),
            "acos": lambda x: math.degrees(math.acos(x)) if degree_mode else math.acos(x),
            "atan": lambda x: math.degrees(math.atan(x)) if degree_mode else math.atan(x),
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "factorial": factorial,
            "abs": abs
        }

        allowed_names = {
            **functions,
            "pi": math.pi,
            "e": math.e
        }

        # Validate expression characters
        if not re.fullmatch(r"[0-9a-zA-Z_+\-*/().,% ]+", expression):
            raise ValueError("Invalid expression")

        result = eval(
            expression,
            {"__builtins__": {}},
            allowed_names
        )

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")


# Button Layout
buttons = [
    ["sin(", "cos(", "tan(", "log("],
    ["asin(", "acos(", "atan(", "ln("],
    ["sqrt(", "factorial(", "x²", "x³"],
    ["(", ")", "π", "e"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "%", "+"],
    ["AC", "DEL", "DEG/RAD", "="]
]


def button_click(value):

    if value == "AC":
        clear()

    elif value == "DEL":
        delete()

    elif value == "=":
        calculate()

    elif value == "DEG/RAD":
        toggle_mode()

    elif value == "x²":
        press("**2")

    elif value == "x³":
        press("**3")

    elif value == "%":
        press("/100")

    elif value == "factorial(":
        press("factorial(")

    else:
        press(value)


# Create Calculator Buttons
for row in buttons:

    frame = tk.Frame(root, bg="#1e1e2e")
    frame.pack(expand=True, fill="both", padx=10)

    for value in row:

        if value == "DEG/RAD":

            mode_button = tk.Button(
                frame,
                text="DEG",
                font=("Arial", 12, "bold"),
                bg="#fab387",
                fg="black",
                bd=0,
                command=toggle_mode
            )

            mode_button.pack(
                side="left",
                expand=True,
                fill="both",
                padx=4,
                pady=4
            )

        else:

            color = "#89b4fa" if value == "=" else "#45475a"

            if value in ["AC", "DEL"]:
                color = "#f38ba8"

            button = tk.Button(
                frame,
                text=value,
                font=("Arial", 14, "bold"),
                bg=color,
                fg="white",
                activebackground="#585b70",
                activeforeground="white",
                bd=0,
                command=lambda v=value: button_click(v)
            )

            button.pack(
                side="left",
                expand=True,
                fill="both",
                padx=4,
                pady=4
            )


# Keyboard Support
def keyboard_input(event):
    if event.keysym == "Return":
        calculate()
    elif event.keysym == "Escape":
        clear()


root.bind("<Return>", keyboard_input)
root.bind("<Escape>", keyboard_input)

# Run Calculator
root.mainloop()