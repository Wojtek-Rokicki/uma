import problem
import solver

if __name__ == "__main__":
    dag_factory = problem.DagFactory(20, 20, 3, 7, 70, 1, 15, 1, 15, seed=4)
    dag = dag_factory.create_dag()
    CCR = problem.calc_ccr(dag)
    print("CCR = " + str(CCR))
    processors = [solver.Processor(3), solver.Processor(2), solver.Processor(2), solver.Processor(2)]
    my_solver = solver.QlHeftSolver(300, dag, 1.0, 0.8, processors)
    my_solver.solve()
    print("OK")
