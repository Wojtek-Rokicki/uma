import problem
import solver


dag_factory = problem.DagFactory(3, 5, 4, 6, 40)
dag = dag_factory.create_dag()
my_solver = solver.QlHeftSolver(1000, dag, 0, 0)
my_solver.solve()
