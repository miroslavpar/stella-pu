from config.settings import (
    INITIAL_RABBITS, INITIAL_FOXES, SIMULATION_PERIOD, RABBIT_BIRTH_RATE, RABBIT_DEATH_RATE,
    FOX_BIRTH_RATE, FOX_DEATH_RATE, FOX_CONSUMPTION_RATE
)

def simulate_population():
    rabbits = INITIAL_RABBITS
    foxes = INITIAL_FOXES
    results = []

    for _ in range(SIMULATION_PERIOD):
        rabbit_growth = rabbits * RABBIT_BIRTH_RATE
        rabbit_death = rabbits * RABBIT_DEATH_RATE + foxes * FOX_CONSUMPTION_RATE
        fox_growth = foxes * FOX_BIRTH_RATE
        fox_death = foxes * FOX_DEATH_RATE

        rabbits = rabbits + rabbit_growth - rabbit_death
        foxes = foxes + fox_growth - fox_death
        results.append((rabbits, foxes))

    return results
