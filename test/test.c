#include <stdio.h>
#include <stdlib.h>

int main(void) {
    // int x = 40;
    // printf("|%d|%5d|%-5d|%5.3d|%-5.3d|\n", x, x, x, x, x);

    float f = 839.21f;
    printf("|%10.3f|%10.3e|%-10g|\n", f, f, f);
    for (int i = 0; i < 10; i++) {
        printf("\a");
    }
}
