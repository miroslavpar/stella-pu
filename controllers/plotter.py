import matplotlib.pyplot as plt
import random

def plot_results(results):
    plt.figure()
    for name, data in results.items():
        color = "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
        plt.plot(data, label=name, color=color)

    plt.xlabel("Years")
    plt.ylabel("Population")
    plt.title("Simulation Results")
    plt.legend()
    plt.grid(True)
    plt.show()
