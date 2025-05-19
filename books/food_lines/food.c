#include <stdio.h>
#include <stdlib.h>

// returns the index of the minimum value, -1 if not valid input
int find_min(int arr[], int len_arr) {
    if ( length(arr) == 0 ) {
        return -1;
    }
    int min_index = 0;
    int min_value = arr[0];
    // Start at 1 since index 0 is necessarily the min starting out
    for( int i = 1; i < len_arr; i++ ) {
        if ( arr[i] < min_value ) {
            min_index = i;
            min_value = arr[i];
        }
    }
    return min_index;
}

int* solve(int n, int m, int lines[]) {
    int joined_lines[m];
    int min_index = -1;
    for ( int i = 0; i < m; i++ ) {
        min_index = find_min(lines, n);
        if ( min_index != -1 ) {
            // Record the smallest line to join
            joined_lines[i] = lines[min_index];

            // Add the person that joined that line
            lines[min_index] += 1;
        }
        else {
            printf("Error");
        }
    }
}

int main() {
    solve(3, 4, [2, 3, 5]);
}