import numpy as np

def run_simulation(participants, equations, simulation_period):
    results = {name: [initial_value] for name, initial_value in participants.items()}
    names = list(participants.keys())

    for t in range(simulation_period):
        current_values = {name: results[name][-1] for name in names}

        for equation in equations:
            lhs, rhs = equation.split("=")
            name = lhs.replace("'", "").strip()

            if name not in current_values:
                raise KeyError(name)

            try:
                new_value = eval(rhs, {}, current_values)
            except ZeroDivisionError:
                raise ZeroDivisionError("Division by zero in equation: " + equation)

            results[name].append(new_value)

    return results
