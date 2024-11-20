/*
docker compose exec main gcc -fopenmp -o ./src/3_cffi/test ./src/3_cffi/test.c
docker compose exec main ./src/3_cffi/test
rm -rf ./src/3_cffi/test
*/

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

static int omp_odd_counter(int *a, int n) {
    int count_odd = 0;

    #pragma omp parallel for reduction(+:count_odd)
    for (int i = 0; i < n; i++) {
        if (a[i] % 2 == 1) {
            count_odd++;
        }
    }
    
    return count_odd;
}

int main() {
    int a[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int n = sizeof(a) / sizeof(a[0]);
    int out = omp_odd_counter(a, n);

    printf("expected: 5\n");
    printf("got: %d\n", out);
    return EXIT_SUCCESS;
}
