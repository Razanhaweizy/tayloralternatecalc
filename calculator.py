import sympy as sp
from tkinter import Tk, Label, Entry, Button, Scale, HORIZONTAL, Text, END, messagebox
from typing import List, Tuple, Dict

class TaylorSeriesCalculator:
    def __init__(self):
        self.root = Tk()
        self.root.title("Multivariate Taylor Series Calculator")
        self.setup_gui()
        
    def setup_gui(self):
        """Initialize all GUI elements"""
        # Main window configuration
        self.root.geometry("800x600")
        
        # Function input
        Label(self.root, text="Function (e.g., sin(x)*cos(y) + exp(t))").pack(pady=5)
        self.func_entry = Entry(self.root, width=50)
        self.func_entry.pack(pady=5)
        self.func_entry.insert(0, "sin(x)*cos(y)")  # Default example
        
        # Variables input
        Label(self.root, text="Variables (comma-separated, e.g., x,y,t)").pack(pady=5)
        self.vars_entry = Entry(self.root, width=50)
        self.vars_entry.pack(pady=5)
        self.vars_entry.insert(0, "x,y")  # Default example
        
        # Expansion points input
        Label(self.root, text="Expansion points (e.g., x=1.5;y=3;t=5)").pack(pady=5)
        self.expansions_entry = Entry(self.root, width=50)
        self.expansions_entry.pack(pady=5)
        self.expansions_entry.insert(0, "x=0;y=0")  # Default example
        
        # Order selection
        Label(self.root, text="Order of Taylor Series").pack(pady=5)
        self.taylor_order = Scale(self.root, from_=1, to=10, orient=HORIZONTAL, length=200)
        self.taylor_order.set(3)  # Default order
        self.taylor_order.pack(pady=5)
        
        # Calculate button
        Button(self.root, text="Calculate Taylor Series", 
               command=self.calculate_taylor_series).pack(pady=10)
        
        # Output display
        Label(self.root, text="Output").pack(pady=5)
        self.output_box = Text(self.root, height=15, width=80)
        self.output_box.pack(pady=5)

    def parse_inputs(self) -> Tuple[sp.Expr, List[sp.Symbol], List[Tuple[sp.Symbol, float]]]:
        """Parse and validate all user inputs"""
        try:
            # Parse function
            function_expr = self.func_entry.get().strip()
            if not function_expr:
                raise ValueError("Function expression cannot be empty")
            f = sp.sympify(function_expr)
            
            # Parse variables
            var_str = self.vars_entry.get().strip()
            if not var_str:
                raise ValueError("Variables cannot be empty")
            variables = [sp.symbols(var.strip()) for var in var_str.split(',')]
            
            # Parse expansion points
            exp_str = self.expansions_entry.get().strip()
            if not exp_str:
                raise ValueError("Expansion points cannot be empty")
            expansion_points = []
            for pt in exp_str.split(';'):
                var_name, value = pt.split('=')
                var = sp.symbols(var_name.strip())
                if var not in variables:
                    raise ValueError(f"Expansion point variable {var} not in declared variables")
                expansion_points.append((var, float(value)))
                
            # Validate that all variables have expansion points
            if len(expansion_points) != len(variables):
                raise ValueError("Number of expansion points must match number of variables")
                
            return f, variables, expansion_points
            
        except Exception as e:
            raise ValueError(f"Input parsing error: {str(e)}")

    def compute_taylor_expansion(self, f: sp.Expr, var: sp.Symbol, 
                               point: float, order: int) -> sp.Expr:
        """Compute Taylor expansion for a single variable"""
        expansion = 0
        term = f
        fact = 1
        
        for n in range(order + 1):
            if n > 0:
                term = sp.diff(term, var)
                fact *= n
            term_at_point = term.subs(var, point)
            expansion += term_at_point * (var - point)**n / fact
            
        return expansion

    def calculate_taylor_series(self):
        """Main calculation function"""
        try:
            self.output_box.delete(1.0, END)
            
            # Parse inputs
            f, variables, expansion_points = self.parse_inputs()
            order = self.taylor_order.get()
            
            # Calculate Taylor expansion for each variable
            result = f
            for var, point in expansion_points:
                result = self.compute_taylor_expansion(result, var, point, order)
                
                # Display intermediate result
                self.output_box.insert(END, 
                    f"\nExpansion around {var}={point} (order {order}):\n{result}\n")
                
            # Display final result
            self.output_box.insert(END, f"\nFinal approximation:\n{result.simplify()}\n")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.output_box.insert(END, f"Error occurred: {str(e)}\n")

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TaylorSeriesCalculator()
    app.run()