from mpi4py import MPI
import networkx as nx
import numpy as np
import quop_mpi as qu

comm = MPI.COMM_WORLD

p = 3
n_qubits = 7

np.random.seed(2)

def x0(p):
    return np.random.uniform(low = 0, high = 1, size = 2 * p)

qwao = qu.MPI.qwao(n_qubits, comm)
qwao.log_success("log", "qwao", action = "w")
qwao.set_graph(qu.graph_array.complete(qwao.size))
qwao.set_initial_state(name="equal")
qwao.set_qualities(qu.qualities.random_floats)
qwao.plan()
qwao.execute(x0(p))
qwao.save("qwao", "example_config", action = "w")
qwao.destroy_plan()
qwao.print_result()

hyper_cube = nx.to_scipy_sparse_matrix(nx.hypercube_graph(n_qubits))
qaoa = qu.MPI.qaoa(hyper_cube,comm)
qaoa.log_success("log", "qaoa", action = "a")
qaoa.set_initial_state(name = "equal")
qaoa.set_qualities(qu.qualities.random_floats)
qaoa.execute(x0(p))
qaoa.save("qaoa", "example_config", action = "w")
qaoa.print_result()