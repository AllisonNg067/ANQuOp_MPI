import mpi4py.MPI
import h5py
from quop_mpi.algorithm import qaoa
from quop_mpi import observable
from quop_mpi.toolkit import I, Z
import networkx as nx
import numpy as np
import numpy.random as rand

Graph = nx.circular_ladder_graph(4)

vertices = len(Graph.nodes)
system_size = 2 ** vertices

G = nx.to_scipy_sparse_matrix(Graph)

#Change to use a normal distribution - quality values come from the normal distribution. Experiment on mean n sd
def maxcut_qualities(G):
    C = 0
    for i in range(G.shape[0]):
        for j in range(G.shape[0]):
            if G[i, j] != 0:
                C += 0.5 * (I(vertices) - (Z(i, vertices) @ Z(j, vertices)))
    return -C.diagonal()


alg = qaoa(system_size)

alg.set_qualities(observable.serial, {"function": maxcut_qualities, "args": [G]})
#R value
alg.set_depth(2)
#Carries out simulation
alg.execute()
alg.print_optimiser_result()
alg.save("maxcut", "depth 2", "w")
