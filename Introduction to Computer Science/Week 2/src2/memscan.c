// Stores names using an array

#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Names
    int names[1];

    for (int i = 0; true; i++){
        printf("%x",names[i]);
        if(i % 10 == 0){
            printf("\n");
        }
    }
}
