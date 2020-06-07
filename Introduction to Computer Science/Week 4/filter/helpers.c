#include "helpers.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int sum = image[h][w].rgbtRed + image[h][w].rgbtGreen + image[h][w].rgbtBlue;
            int avr = roundf(((float) sum) / 3.0);

            image[h][w].rgbtRed = avr;
            image[h][w].rgbtGreen = avr;
            image[h][w].rgbtBlue = avr;

        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            float originalRed = image[h][w].rgbtRed;
            float originalGreen = image[h][w].rgbtGreen;
            float originalBlue = image[h][w].rgbtBlue;

            float sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue;
            float sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue;
            float sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue;

            int r = roundf(sepiaRed);
            int g = roundf(sepiaGreen);
            int b = roundf(sepiaBlue);

            if (r > 255)
            {
                r = 255;
            }

            if (g > 255)
            {
                g = 255;
            }

            if (b > 255)
            {
                b = 255;
            }

            image[h][w].rgbtRed = r;
            image[h][w].rgbtGreen = g;
            image[h][w].rgbtBlue = b;

        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        RGBTRIPLE org[width];

        for (int w = 0; w < width; w++)
        {
            org[w].rgbtRed = image[h][w].rgbtRed;
            org[w].rgbtGreen = image[h][w].rgbtGreen;
            org[w].rgbtBlue = image[h][w].rgbtBlue;
        }

        for (int w = 0; w < width; w++)
        {
            int ref = width - w - 1;
            image[h][w].rgbtRed = org[ref].rgbtRed;
            image[h][w].rgbtGreen = org[ref].rgbtGreen;
            image[h][w].rgbtBlue = org[ref].rgbtBlue;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE res[height][width];


    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int sumr = 0;
            int sumg = 0;
            int sumb = 0;
            int count = 0;

            sumr = 0;
            sumg = 0;
            sumb = 0;
            count = 0;

            sumr += image[h][w].rgbtRed;
            sumg += image[h][w].rgbtGreen;
            sumb += image[h][w].rgbtBlue;
            count ++;

            if (w - 1 >= 0)
            {
                sumr += image[h][w - 1].rgbtRed;
                sumg += image[h][w - 1].rgbtGreen;
                sumb += image[h][w - 1].rgbtBlue;
                count ++;

                if (h - 1 >= 0)
                {
                    sumr += image[h - 1][w - 1].rgbtRed;
                    sumg += image[h - 1][w - 1].rgbtGreen;
                    sumb += image[h - 1][w - 1].rgbtBlue;
                    count ++;
                }

                if (h + 1 < height)
                {
                    sumr += image[h + 1][w - 1].rgbtRed;
                    sumg += image[h + 1][w - 1].rgbtGreen;
                    sumb += image[h + 1][w - 1].rgbtBlue;
                    count ++;
                }
            }

            if (h - 1 >= 0)
            {
                sumr += image[h - 1][w].rgbtRed;
                sumg += image[h - 1][w].rgbtGreen;
                sumb += image[h - 1][w].rgbtBlue;
                count ++;
            }

            if (h + 1 < height)
            {
                sumr += image[h + 1][w].rgbtRed;
                sumg += image[h + 1][w].rgbtGreen;
                sumb += image[h + 1][w].rgbtBlue;
                count ++;
            }

            if (w + 1 < width)
            {
                sumr += image[h][w + 1].rgbtRed;
                sumg += image[h][w + 1].rgbtGreen;
                sumb += image[h][w + 1].rgbtBlue;
                count ++;

                if (h - 1 >= 0)
                {
                    sumr += image[h - 1][w + 1].rgbtRed;
                    sumg += image[h - 1][w + 1].rgbtGreen;
                    sumb += image[h - 1][w + 1].rgbtBlue;
                    count ++;
                }

                if (h + 1 < height)
                {
                    sumr += image[h + 1][w + 1].rgbtRed;
                    sumg += image[h + 1][w + 1].rgbtGreen;
                    sumb += image[h + 1][w + 1].rgbtBlue;
                    count ++;
                }
            }


            int avgr = roundf((float)sumr / (float)count);
            int avgg = roundf((float)sumg / (float)count);
            int avgb = roundf((float)sumb / (float)count);

            res[h][w].rgbtRed = avgr;
            res[h][w].rgbtGreen = avgg;
            res[h][w].rgbtBlue = avgb;


        }


    }

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w] = res[h][w];
        }
    }
}
