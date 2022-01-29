import matplotlib.pyplot as plt
from problem import DagFactory


def plot_stats(makespans: list, speedups: list, arts: list, efficiencies: list, dag_factory: DagFactory, step,
               iterations, ccr):
    plt.figure(0)
    steps = range(0, len(makespans) * step, step)
    plt.plot(steps, makespans)
    plt.title(f'Iterations={iterations}, CCR={ccr}', pad=30)
    plt.xlabel("Liczba iteracji nauczania")
    plt.ylabel("Makespan")
    plt.savefig(f"results/makespan/makespan-{dag_factory.min_ranks}-{dag_factory.max_ranks}-{dag_factory.min_per_rank}"
                f"-{dag_factory.max_per_rank}-{dag_factory.seed}.pdf")
    plt.close(0)

    plt.figure(0)
    plt.plot(steps, speedups)
    plt.xlabel("Liczba iteracji nauczania")
    plt.ylabel("Speedup")
    plt.savefig(f"results/speedup/speedup-{dag_factory.min_ranks}-{dag_factory.max_ranks}-{dag_factory.min_per_rank}"
                f"-{dag_factory.max_per_rank}-{dag_factory.seed}.pdf")
    plt.close(0)

    plt.figure(0)
    plt.plot(steps, arts)
    plt.xlabel("Liczba iteracji nauczania")
    plt.ylabel("ART")
    plt.savefig(f"results/art/art-{dag_factory.min_ranks}-{dag_factory.max_ranks}-{dag_factory.min_per_rank}"
                f"-{dag_factory.max_per_rank}-{dag_factory.seed}.pdf")
    plt.close(0)

    plt.figure(0)
    plt.plot(steps, efficiencies)
    plt.xlabel("Liczba iteracji nauczania")
    plt.ylabel("Efficiency")
    plt.savefig(f"results/efficiency/efficiency-{dag_factory.min_ranks}-{dag_factory.max_ranks}-{dag_factory.min_per_rank}"
                f"-{dag_factory.max_per_rank}-{dag_factory.seed}.pdf")
    plt.close(0)
