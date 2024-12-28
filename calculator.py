import sympy as sp
import tkinter as tk
from tkinter import scrolledtext

# Function to compute Taylor series approximation term by term
def taylor_series_approximation(f, a, n_terms=5):
    x = sp.symbols('x')
    taylor_expansion = 0
    steps = []
    
    # Compute the terms of the Taylor series
    for n in range(n_terms):
        # Compute the nth derivative of f
        nth_derivative = sp.diff(f, x, n)
        
        # Evaluate the nth derivative at the point a
        nth_derivative_at_a = nth_derivative.subs(x, a)
        
        # Compute the nth term
        term = nth_derivative_at_a * (x - a)**n / sp.factorial(n)
        
        # Add the term to the Taylor series
        taylor_expansion += term
        
        # Record the step for display
        steps.append(f"Term {n+1}: {term}")
    
    return taylor_expansion, steps

# Function to compute Taylor series for the sum of functions
def sum_functions_taylor_approximation(functions, points, n_terms=5):
    x = sp.symbols('x')
    sum_expansion = 0
    steps = []
    
    for f, a in zip(functions, points):
        term_expansion, term_steps = taylor_series_approximation(f, a, n_terms)
        sum_expansion += term_expansion
        steps.extend(term_steps)
    
    return sum_expansion, steps

# Function to compute Taylor series for the product of functions
def product_functions_taylor_approximation(functions, points, n_terms=5):
    x = sp.symbols('x')
    product_expansion = 1
    steps = []
    
    for f, a in zip(functions, points):
        term_expansion, term_steps = taylor_series_approximation(f, a, n_terms)
        product_expansion *= term_expansion
        steps.extend(term_steps)
    
    return product_expansion, steps

# UI setup
def show_steps():
    # Retrieve user inputs
    functions_input = entry_functions.get()
    points_input = entry_points.get()
    
    try:
        functions = [sp.sympify(f.strip()) for f in functions_input.split(',')]
        points = [float(p.strip()) for p in points_input.split(',')]
        
        # Calculate the Taylor Series
        sum_approx, sum_steps = sum_functions_taylor_approximation(functions, points)
        product_approx, product_steps = product_functions_taylor_approximation(functions, points)
        
        # Display the steps and results
        result_steps.delete(1.0, tk.END)  # Clear previous steps
        result_steps.insert(tk.END, "Sum Approximation Steps:\n")
        result_steps.insert(tk.END, "\n".join(sum_steps) + "\n\n")
        result_steps.insert(tk.END, "Product Approximation Steps:\n")
        result_steps.insert(tk.END, "\n".join(product_steps) + "\n\n")
        
        result_steps.insert(tk.END, f"Final Sum Approximation: {sum_approx}\n")
        result_steps.insert(tk.END, f"Final Product Approximation: {product_approx}\n")
    except Exception as e:
        result_steps.delete(1.0, tk.END)  # Clear previous results
        result_steps.insert(tk.END, f"Error: {e}")

# Set up the main window
window = tk.Tk()
window.title("Taylor Series Approximation")

# Create labels and input fields
label_functions = tk.Label(window, text="Enter Functions (comma-separated):")
label_functions.grid(row=0, column=0, padx=10, pady=5)

entry_functions = tk.Entry(window, width=50)
entry_functions.grid(row=0, column=1, padx=10, pady=5)

label_points = tk.Label(window, text="Enter Expansion Points (comma-separated):")
label_points.grid(row=1, column=0, padx=10, pady=5)

entry_points = tk.Entry(window, width=50)
entry_points.grid(row=1, column=1, padx=10, pady=5)

# Create a button to compute the Taylor series
compute_button = tk.Button(window, text="Compute Taylor Series", command=show_steps)
compute_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a scrollable text area to display the steps and results
result_steps = scrolledtext.ScrolledText(window, width=80, height=20)
result_steps.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Start the UI loop
window.mainloop()
