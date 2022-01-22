import problem
import solver


dag_factory = problem.DagFactory(3, 5, 4, 6, 40)
dag = dag_factory.create_dag()
processors = [solver.Processor(5), solver.Processor(1), solver.Processor(3)]
my_solver = solver.QlHeftSolver(10000, dag, 0, 0, processors)
my_solver.solve()
