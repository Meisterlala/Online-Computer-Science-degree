#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    // Open file
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        return 1;
    }


    bool writingjpg = false;
    int imagenumb = 0;
    FILE *img;

    for (int i = 0; true; i++)
    {
        // Read first three bytes
        BYTE bytes[512];
        int blockcount = fread(&bytes, 1, 512, file);

        if (blockcount < 512)
        {
            return 0;
        }


        // If Jpeg
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            if (writingjpg)
            {
                fclose(img);
            }

            char *filename = malloc(sizeof(char) * 10);
            sprintf(filename, "%03i.jpg", imagenumb);
            imagenumb++;

            img = fopen(filename, "w");

            free(filename);


            fwrite(&bytes, 1, 512, img);

            writingjpg = true;

        }
        else if (writingjpg)
        {
            fwrite(&bytes, 1, 512, img);
        }




    }

    // Close file
    fclose(file);
}
