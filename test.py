# Returns the Jacobian matrix of the residuals function. The matrix
# has size [i x 3], where 'i' is the number of observations.
def residualsJacobian(observations, current_guess):
    j_r = np.zeros((len(observations), 3))
    for i, observation in enumerate(observations):
        # Cache the distance from the station to the current
        # guess since it's a common denominator.
        distance = Distance(observation.Station, current_guess)

        j_r[i, 0] = (current_guess.X - observation.Station.X) / distance
        j_r[i, 1] = (current_guess.Y - observation.Station.Y) / distance
        j_r[i, 2] = (current_guess.Z - observation.Station.Z) / distance

    return j_r

# Returns the column vector with the residuals. It has size [i x 1].
def residuals(observations, current_guess):
    r = np.zeros((len(observations), 1))
    for i, observation in enumerate(observations):
        distance = Distance(observation.Station, current_guess)
        r[i] = observation.Distance - distance

    return r

# Returns the sum of the squares of the residuals.
def SumOfResidualSquares(observations, current_guess):
    sum_of_squares = 0.0
    for observation in observations:
        distance = Distance(observation.Station, current_guess)
        sum_of_squares += (observation.Distance - distance) ** 2

    return sum_of_squares

# Implements one iteration of the Gauss-Newton algorithm
# (https://en.wikipedia.org/wiki/Gauss%E2%80%93Newton_algorithm), as
# applied to true range multilateration. Returns the new guess.
def GaussNetwonIteration(observations, current_guess):
    # The variable names in this function mirror those from the Wikipedia article.

    # Current guess of the algorithm
    beta_s = np.array([current_guess.X, current_guess.Y, current_guess.Z])

    # Jacobian matrix of the residuals, and its transpose.
    j_r = residualsJacobian(observations, current_guess)
    j_r_t = np.transpose(j_r)

    # Left pseudoinverse of j_r.
    left_pseudoinverse = np.linalg.solve(np.matmul(j_r_t, j_r), j_r_t)

    # Matrix of residuals.
    r = residuals(observations, current_guess)

    # Compute and return the new guess.
    addend = np.matmul(left_pseudoinverse, r)
    beta_s += addend.flatten()

    return Point(beta_s[0], beta_s[1], beta_s[2])

def Trilaterate(observations, initial_guess, max_iterations, min_sum_of_residual_squares):
    guess = initial_guess
    iteration = 1
    while True:
        guess = GaussNetwonIteration(observations, guess)
        if max_iterations > 0 and iteration == max_iterations:
            # Maximum number of iterations reached.
            # Return partial guess and error condition.
            raise Exception(f"Trilaterate: reached maximum number of iterations {max_iterations}")

        if SumOfResidualSquares(observations, guess) < min_sum_of_residual_squares:
            # The minimum threshold for the sum of the squares of the residuals has been reached.
            return guess

        iteration += 1