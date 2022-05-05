#include <stdio.h>
#include <stdlib.h>

int main(){
    srand(0);
    for (int i = 0; i < 32; i++)
        printf("%d, ", rand());
    printf("\n");
    srand(1);
    for (int i = 0; i < 32; i++)
        printf("%d, ", rand());
    printf("\n");
    srand(2);
    for (int i = 0; i < 32; i++)
        printf("%d, ", rand());
    printf("\n");
}