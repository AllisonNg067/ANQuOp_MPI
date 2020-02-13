import qwao_mpi as qw
import numpy as np
import networkx as nx
from mpi4py import MPI

comm = MPI.COMM_WORLD

def x0(p,seed):
    return np.random.uniform(low = 0, high = 1, size = 2*p)

for qubits in range(2,3):
    qwao = qw.MPI.qwao(qubits,comm)
    qwao.set_initial_state(name="split")
    qwao.log_success("qwao_complete_split","split",action="a")
    qwao.set_graph(qw.graph_array.complete(qwao.size))
    qwao.plan()
    qwao.benchmark(range(1,2), 5, param_func = x0, qual_func = qw.qualities.random_floats, filename = "qwao_complete_split",label = "qwao_" + str(qubits))
    qwao.destroy_plan()
