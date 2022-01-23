import problem
import solver

if __name__ == "__main__":
    dag_factory = problem.DagFactory(10, 15, 10, 15, 70, seed=4)
    dag = dag_factory.create_dag()
    CCR = problem.calc_ccr(dag)
    print("CCR = " + str(CCR))
    processors = [solver.Processor(1), solver.Processor(1)]
    my_solver = solver.QlHeftSolver(400, dag, 0.1, 0.001, processors)
    my_solver.solve()
    print("OK")
