import matplotlib.pyplot as plt

def plot_results(results):
    years = list(range(1, len(results) + 1))
    rabbits = [result[0] for result in results]
    foxes = [result[1] for result in results]

    plt.plot(years, rabbits, label="Rabbits")
    plt.plot(years, foxes, label="Foxes")
    plt.xlabel("Years")
    plt.ylabel("Population")
    plt.legend()
    plt.show()
