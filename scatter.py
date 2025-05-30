from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print("Total number of processes:", size)
print("Rank of current process:", rank)

if rank == 0:
    data = [(i+1)**2 for i in range(size)]
    print("Data generated by root process:", data)
else:
    data = None

data = comm.scatter(data, root=0)

print("Process", rank, "received data:", data)
assert data == (rank+1)**2
print("Data verification successful for process", rank)