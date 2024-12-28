import numpy as np
import math

# Define the factorial function
def factorial(n):
    return np.math.factorial(n)

# Define the Taylor Series approximation for a function f around a point a
def taylor_series_approx(f, a, n_terms=5):
    """
    Approximates the Taylor series of function f around a point a up to n_terms terms.
    
    Parameters:
    f: function - The function to approximate.
    a: float - The point around which to approximate the function.
    n_terms: int - The number of terms in the Taylor series approximation.
    
    Returns:
    A function that approximates f(x) around a using n_terms terms.
    """
    def approx(x):
        result = 0
        for n in range(n_terms):
            # nth derivative evaluated at a
            derivative = (f(a + 0.0001) - f(a - 0.0001)) / (2 * 0.0001) if n == 0 else (f(a + 0.0001) - f(a - 0.0001)) / (2 * 0.0001)
            result += (derivative / factorial(n)) * ((x - a) ** n)
        return result
    return approx

# Case 1: Sum of functions (g(x, y, z, ...))
def case_1_approximation(functions, points, n_terms=5):
    """
    Case 1 approximation where the function is a sum of individual functions.
    
    Parameters:
    functions: list of functions - The functions to approximate.
    points: list of floats - The points around which to approximate each function.
    n_terms: int - The number of terms in the Taylor series approximation.
    
    Returns:
    A function that approximates the sum of functions at the given points.
    """
    approximations = []
    
    # For each function, compute the Taylor series approximation around the corresponding point
    for f, point in zip(functions, points):
        approximations.append(taylor_series_approx(f, point, n_terms))
    
    # Return the sum of these approximations
    def approx(x):
        return sum(approx(x) for approx in approximations)
    
    return approx

# Case 2: Product of functions (g(x, y, z, ...))
def case_2_approximation(functions, points, n_terms=5):
    """
    Case 2 approximation where the function is a product of individual functions.
    
    Parameters:
    functions: list of functions - The functions to approximate.
    points: list of floats - The points around which to approximate each function.
    n_terms: int - The number of terms in the Taylor series approximation.
    
    Returns:
    A function that approximates the product of functions at the given points.
    """
    approximations = []
    
    # For each function, compute the Taylor series approximation around the corresponding point
    for f, point in zip(functions, points):
        approximations.append(taylor_series_approx(f, point, n_terms))
    
    # Return the product of these approximations
    def approx(x):
        result = 1
        for approximation in approximations:
            result *= approximation(x)
        return result
    
    return approx

# Case 3: Sum of different functions (d(x) + f(y) + g(z) + ...)
def case_3_approximation(functions, points, n_terms=5):
    """
    Case 3 approximation for functions like d(x) + f(y) + g(z).
    
    Parameters:
    functions: list of functions - The functions to approximate.
    points: list of floats - The points around which to approximate each function.
    n_terms: int - The number of terms in the Taylor series approximation.
    
    Returns:
    A function that approximates the sum of these functions at the given points.
    """
    return case_1_approximation(functions, points, n_terms)

# Case 4: Combination of sum and product of functions
def case_4_approximation(functions, points, n_terms=5):
    """
    Case 4 approximation where some functions are added and some multiplied.
    
    Parameters:
    functions: list of functions - The functions to approximate.
    points: list of floats - The points around which to approximate each function.
    n_terms: int - The number of terms in the Taylor series approximation.
    
    Returns:
    A function that approximates the combined sum and product at the given points.
    """
    # For simplicity, let's assume the first few functions are summed and the rest are multiplied
    sum_functions = functions[:len(functions) // 2]
    product_functions = functions[len(functions) // 2:]
    
    sum_approx = case_1_approximation(sum_functions, points[:len(sum_functions)], n_terms)
    product_approx = case_2_approximation(product_functions, points[len(sum_functions):], n_terms)
    
    # Return the combined sum and product approximation
    def approx(x):
        return sum_approx(x) * product_approx(x)
    
    return approx

# Case 5: Composite functions with sums and products
def case_5_approximation(functions, points, n_terms=5):
    """
    Case 5 approximation where the function is a composite of sums and products.
    
    Parameters:
    functions: list of functions - The functions to approximate.
    points: list of floats - The points around which to approximate each function.
    n_terms: int - The number of terms in the Taylor series approximation.
    
    Returns:
    A function that approximates the composite function at the given points.
    """
    sum_functions = functions[:len(functions) // 2]
    product_functions = functions[len(functions) // 2:]
    
    sum_approx = case_1_approximation(sum_functions, points[:len(sum_functions)], n_terms)
    product_approx = case_2_approximation(product_functions, points[len(sum_functions):], n_terms)
    
    # Return the combination of sum and product approximations
    def approx(x):
        return sum_approx(x) + product_approx(x)
    
    return approx

# Example functions and points for testing
functions = [np.sin, np.cos]
points = [2, 3]
approx = case_1_approximation(functions, points, n_terms=5)

# Test the approximation
x = 2.5
print(f"Approximated value at x={x}: {approx(x)}")
