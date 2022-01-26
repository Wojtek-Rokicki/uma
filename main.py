import problem
import solver

if __name__ == "__main__":
    dag_factory = problem.DagFactory(2, 2, 3, 3, 70, 50, 100, 200, 300, seed=4)
    dag = dag_factory.create_dag()
    CCR = problem.calc_ccr(dag)
    print("CCR = " + str(CCR))
    processors = [solver.Processor(21), solver.Processor(18), solver.Processor(16)]
    my_solver = solver.QlHeftSolver(500, dag, 1.0, 0.8, processors)
    processors = my_solver.solve()
