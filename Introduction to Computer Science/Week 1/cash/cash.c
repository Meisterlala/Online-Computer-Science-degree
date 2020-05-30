#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int counter = 0;
    float f;
    do
    {
        f = get_float("Change owed: ");
    }

    while (f < 0);

    int cents = round(f * 100);

    while(cents >= 25){
        cents -= 25;
        counter++;
    }

     while(cents >= 10){
        cents -= 10;
        counter++;
    }

     while(cents >= 5){
        cents -= 5;
        counter++;
    }

     while(cents >= 1){
        cents -= 1;
        counter++;
    }

    printf("%i\n", counter);
}
