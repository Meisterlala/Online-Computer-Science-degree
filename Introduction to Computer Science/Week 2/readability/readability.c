// Uppercases string using ctype library (and an unnecessary condition)

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string s = get_string("Text: ");
    string inp = s;
    int letterc = 0;
    int wordc = 1;
    int sentencec = 0;

    for (int i = 0, n = strlen(inp); i < n; i++)
    {
        char curr = s[i];

        // Check if a letter
        if (isalpha(curr))
        {
            letterc++;
        }

        if (curr == 32)
        {
            wordc++;
        }

        if (curr == 46 || curr == 33 || curr == 63)
        {
            sentencec++;
        }
    }

    float ln = (float) letterc / (float) wordc * 100.0;
    float sn = (float) sentencec / (float) wordc * 100.0;

    float index = 0.0588 * ln - 0.296 * sn - 15.8;
    int grade = round(index);

    // printf("%i letter(s)\n", letterc);
    // printf("%i word(s)\n", wordc);
    // printf("%i sentence(s)\n", sentencec);

    if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}
