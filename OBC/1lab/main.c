#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
    
#define ITERATIONS      1000    
#define WARMUP          20      
#define MIN_SIZE        1       
#define MAX_SIZE_MB     16      

int main(int argc, char** argv) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size != 2) {
        if (rank == 0) {
            fprintf(stderr, "Ошибка: требуется процесса (mpirun -np 2)\n");
        }
        MPI_Finalize();
        return 1;
    }

    int sizes[25];
    int num_sizes = 0;
    for (int exp = 0; exp <= 24; exp++) {
        int sz = 1 << exp;  
        if (sz <= MAX_SIZE_MB * 1024 * 1024) {
            sizes[num_sizes++] = sz;
        }
    }

    if (rank == 0) {
        printf("# Size(bytes)\tTime(sec)\tBandwidth(MB/s)\tLatency(us)\n");
        printf("# -----------------------------------------------------------\n");
        fflush(stdout);
    }

    for (int s = 0; s < num_sizes; s++) {
        int msg_size = sizes[s];
        char *sendbuf = (char*)malloc(msg_size);
        char *recvbuf = (char*)malloc(msg_size);
        
        if (!sendbuf || !recvbuf) {
            fprintf(stderr, "rank %d: ошибка выделения памяти для %d байт\n", rank, msg_size);
            MPI_Abort(MPI_COMM_WORLD, 1);
        }

        memset(sendbuf, (rank == 0) ? 0xAA : 0x55, msg_size);

        for (int i = 0; i < WARMUP; i++) {
            MPI_Request req[2];
            if (rank == 0) {
                MPI_Isend(sendbuf, msg_size, MPI_BYTE, 1, 0, MPI_COMM_WORLD, &req[0]);
                MPI_Irecv(recvbuf, msg_size, MPI_BYTE, 1, 0, MPI_COMM_WORLD, &req[1]);
            } else {
                MPI_Irecv(recvbuf, msg_size, MPI_BYTE, 0, 0, MPI_COMM_WORLD, &req[0]);
                MPI_Isend(sendbuf, msg_size, MPI_BYTE, 0, 0, MPI_COMM_WORLD, &req[1]);
            }
            MPI_Waitall(2, req, MPI_STATUSES_IGNORE);
        }

        MPI_Barrier(MPI_COMM_WORLD);
        double start = MPI_Wtime();

        for (int i = 0; i < ITERATIONS; i++) {
            MPI_Request req[2];
            if (rank == 0) {
                MPI_Isend(sendbuf, msg_size, MPI_BYTE, 1, 0, MPI_COMM_WORLD, &req[0]);
                MPI_Irecv(recvbuf, msg_size, MPI_BYTE, 1, 0, MPI_COMM_WORLD, &req[1]);
            } else {
                MPI_Irecv(recvbuf, msg_size, MPI_BYTE, 0, 0, MPI_COMM_WORLD, &req[0]);
                MPI_Isend(sendbuf, msg_size, MPI_BYTE, 0, 0, MPI_COMM_WORLD, &req[1]);
            }
            MPI_Waitall(2, req, MPI_STATUSES_IGNORE);
        }

        MPI_Barrier(MPI_COMM_WORLD);
        double end = MPI_Wtime();
        double total_time = end - start;
        double avg_time = total_time / ITERATIONS;

        if (rank == 0) {
            double bandwidth_mbs = (msg_size * 1.0) / (avg_time * 1024 * 1024); 
            double latency_us = avg_time * 1e6;                                
            
            printf("%d\t\t%.9f\t%.3f\t\t%.3f\n", 
                   msg_size, avg_time, bandwidth_mbs, latency_us);
            fflush(stdout);
        }

        free(sendbuf);
        free(recvbuf);
    }

    MPI_Finalize();
    return 0;
}