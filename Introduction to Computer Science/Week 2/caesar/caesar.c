// Uppercases string using ctype library (and an unnecessary condition)

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(int argc, string argv[])
{

    if (argc != 2)
    {
        printf("missing command-line argument\n");
        return 1;
    }

    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Read Cypher Key
    int key = atoi(argv[1]);

    // Get user input
    string s = get_string("plaintext:  ");
    printf("ciphertext: ");

    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // If Uppercase
        if (isupper(s[i]))
        {
            int c = s[i] + key % 26;
            if (c > 90)
            {
                c -= 26;
            }
            printf("%c", c);
        }
        // If Lowercase
        else if (islower(s[i]))
        {
            int c = s[i] + key % 26;
            if (c > 122)
            {
                c -= 26;
            }
            printf("%c", c);
        }
        // Else just Print
        else
        {
            printf("%c", s[i]);
        }

    }

    printf("\n");

}