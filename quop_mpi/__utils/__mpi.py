import numpy as np
from mpi4py import MPI

def __scatter_1D_array(array, partition_table, MPI_COMM, dtype):

    rank = MPI_COMM.Get_rank()
    local_i = partition_table[rank + 1] - partition_table[rank]
    operator = np.empty(local_i, np.float64)

    counts = partition_table[1:] - partition_table[:-1]
    disps = partition_table[:-1] - 1

    if dtype == np.complex128:
        send_type = MPI.DOUBLE_COMPLEX
    elif dtype == np.float64:
        send_type = MPI.DOUBLE

    MPI_COMM.Scatterv([array, counts, disps, send_type], operator[:local_i], 0)

    return operator

def __scatter_sparse(row_starts, col_indexes, values, partition_table, MPI_COMM):

    rank = MPI_COMM.Get_rank()
    size = MPI_COMM.Get_size()

    lb = partition_table[rank] - 1
    ub = partition_table[rank + 1]

    if rank == 0:
        n_terms = MPI_COMM.bcast(len(row_starts[0]), 0)
    else:
        n_terms = MPI_COMM.bcast(None, 0)

    W_row_starts = []
    W_col_indexes = []
    W_values = []

    for i in n_terms:

        n_local_rows = partition_table[rank + 1] - partition_table[rank]
        W_row_starts.append(np.empty(n_local_rows + 1, np.int32))
        counts = partition_table[1:] - partition_table[0:-1] + 1
        disps = partition_table[0:-1] - 1

        if rank == 0:
            sends = [row_starts[i], counts, disps, MPI.DOUBLE_COMPLEX]
        else:
            sends = None

        MPI_COMM.Scatterv(sends, W_row_starts[-1], 0)

        n_local_nnz = W_row_starts[ub] - W_row_starts[lb]

        W_col_indexes.append(np.empty(n_local_nnz, np.int32))
        W_values.append(np.empty(n_local_nnz, np.complex128))

        counts = np.zeros(size, int)
        counts[rank] = n_local_nnz

        MPI_COMM.Reduce([counts, MPI.INTEGER], OP = MPI.SUM)

        disps = np.zeros(size, int)
        disps[1:] = np.cumsum(counts)

        if rank == 0:
            send_indexes = [col_indexes[i], counts, disps, MPI.INTEGER]
            send_values = [values[i], counts, disps, MPI.DOUBLE_COMPLEX]
        else:
            send_indexes = None
            send_values = None

        MPI_COMM.Scatterv(send_indexes, W_col_indexes[-1], 0)
        MPI_COMM.Scatterv(send_values, W_values[-1], 0)

    return W_row_starts, W_col_indexes, W_values

