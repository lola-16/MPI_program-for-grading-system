from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = {'55'}
else:
    data = None

data = comm.bcast(data, root=0)
print(f"Process {rank} received data: {data}")