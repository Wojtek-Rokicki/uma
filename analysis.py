import matplotlib.pyplot as plt
from problem import DagFactory


def plot_stats(makespans: list, speedups: list, arts: list, efficiencies: list, dag_factory: DagFactory, step, folder,
               filename):
    steps = range(0, len(makespans) * step, step)

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(steps, makespans)
    axs[0, 0].set_title("Makespan")
    axs[0, 0].set(xlabel="Liczba iteracji nauczania", ylabel="Makespan")

    axs[0, 1].plot(steps, speedups)
    axs[0, 1].set_title("Speedup")
    axs[0, 1].set(xlabel="Liczba iteracji nauczania", ylabel="Speedup")

    axs[1, 0].plot(steps, arts)
    axs[1, 0].set_title("ART")
    axs[1, 0].set(xlabel="Liczba iteracji nauczania", ylabel="ART")

    axs[1, 1].plot(steps, efficiencies)
    axs[1, 1].set_title("Efficiency")
    axs[1, 1].set(xlabel="Liczba iteracji nauczania", ylabel="Efficiency")

    plt.tight_layout()
    plt.savefig(f"results/{folder}/{filename}.png")
    #plt.show()
