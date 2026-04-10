#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char** argv) { // definição da estrutura de dados principal (muito importante o valor de rank, responsável pela distribuiçãp das threads por processo)
    int rank, size;
    int *array_local, *array;
    int soma_local, soma;
    int tamanho = 8;
    int tamanho_local;

    MPI_Init(&argc, &argv); //inicialização do MPI
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // definição da variavel responsável pelo rank
    MPI_Comm_size(MPI_COMM_WORLD, &size); // definição da variavel responsável pelo tamanho dos dados

    tamanho_local = tamanho / size;
    array_local = (int*)malloc(tamanho_local * sizeof(int)); //alocação do tamanho do array que será distribuído pelos processos

    if (rank == 0) { // alocação do primeiro processo
        array = (int*)malloc(tamanho * sizeof(int));
        printf("Array: ");
        for (int i = 0; i < tamanho; i++) { // distribui os arrays e calcula no rank 0
            array[i] = i + 1;
            printf("%d ", array[i]);
        }
        printf("\n");
    }

    MPI_Scatter(array, tamanho_local, MPI_INT, array_local, tamanho_local, MPI_INT, 0, MPI_COMM_WORLD); //distribui os outros ranks para serem processados

    soma_local = 0;
    printf("Array recebido pelo rank %2d: ", rank); // print do array processado pelo rank definido e calculado pelo rank 0
    for (int i = 0; i < tamanho_local; i++) {
        printf("%3d ", array_local[i]);
        soma_local += array_local[i];
    }
    printf("-- soma local: %4d\n", soma_local);

    MPI_Reduce(&soma_local, &soma, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD); // envia os valores para o rank 0 calcular no proximo ciclo

    if (rank == 0) {
        sleep(1);
        printf("Soma do array: %d\n", soma);
        printf("Valor esperado: %d\n", tamanho * (tamanho + 1) / 2);// o rank 0 calcula o array definido pelo rank anterior
        free(array);
    }

    free(array_local); // libera o ponteiro do array para evitar alocação infinita
    MPI_Finalize(); // finaliza o processo do mpi para não causar corrupções
}

