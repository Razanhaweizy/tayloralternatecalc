import sympy as sp
from tkinter import Tk, Label, Entry, Button, Scale, HORIZONTAL, StringVar, Text, END

def calculate_taylor_series():
    try:
        # User inputs
        function_expr = func_entry.get()
        variables = vars_entry.get().split(',')
        expansions = expansions_entry.get().split(';')
        order = taylor_order.get()

        # Parse the function
        f = sp.sympify(function_expr)
        var_symbols = [sp.symbols(var.strip()) for var in variables]
        
        # Parse expansion points
        expansion_points = [
            (sp.symbols(pt.split('=')[0].strip()), float(pt.split('=')[1].strip()))
            for pt in expansions
        ]
        
        # Compute Taylor series for each variable
        taylor_series = f
        for var, point in expansion_points:
            taylor_series = sp.series(taylor_series, var, point, n=order).removeO()
        
        # Update output box
        output_box.delete(1.0, END)
        output_box.insert(END, f"Original Function: {f}\n")
        output_box.insert(END, f"Taylor Series Approximation: {taylor_series}\n")
    except Exception as e:
        output_box.delete(1.0, END)
        output_box.insert(END, f"Error: {e}")

# GUI setup
root = Tk()
root.title("Taylor Series Calculator")

# Input fields
Label(root, text="Function (e.g., sin(x)*exp(y))").pack()
func_entry = Entry(root, width=50)
func_entry.pack()

Label(root, text="Variables (comma-separated, e.g., x,y)").pack()
vars_entry = Entry(root, width=50)
vars_entry.pack()

Label(root, text="Expansion points (e.g., x=1.5;y=3)").pack()
expansions_entry = Entry(root, width=50)
expansions_entry.pack()

Label(root, text="Order of Taylor Series").pack()
taylor_order = Scale(root, from_=1, to=10, orient=HORIZONTAL)
taylor_order.pack()

Button(root, text="Calculate Taylor Series", command=calculate_taylor_series).pack()

# Output display
Label(root, text="Output").pack()
output_box = Text(root, height=10, width=70)
output_box.pack()

# Run the GUI
root.mainloop()
