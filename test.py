import numpy as np
from scipy.optimize import minimize

def residuals(x, r):
    x1, x2, x3, x4 = x[:3], x[3:6], x[6:9], x[9:]
    r12, r13, r14, r23, r24, r34 = r
    eqs = [
        2 * (x2 - x1).T - 2 * r12,
        2 * (x3 - x1).T - 2 * r13,
        2 * (x4 - x1).T - 2 * r14,
        2 * (x3 - x2).T - 2 * r23,
        2 * (x4 - x2).T - 2 * r24,
        2 * (x4 - x3).T - 2 * r34
    ]
    return np.sum([(eq - (r**2 - np.linalg.norm(xi)**2 + np.linalg.norm(xj)**2))**2 for eq, xi, xj, r in zip(eqs, [x1, x1, x1, x2, x2, x3], [x2, x3, x4, x3, x4, x4], r)])

# Example input values for r12, r13, r14, r23, r24, r34
r = np.array([1.0, 2.0, 3.0, 2.5, 3.5, 1.5])

# Initial guess for x1, x2, x3, x4 (12 variables)
x0 = np.zeros(12)

# Minimize the residual sum of squares
result = minimize(residuals, x0, args=(r,), method='BFGS')

x_solution = result.x.reshape(4, 3)
print(x_solution)