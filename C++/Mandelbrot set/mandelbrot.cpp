#include <iostream>
#include <cmath>
#include <SFML/Window.hpp>
#include <SFML/Graphics.hpp>

//May have displaying issues for display res. != 1920x1080

/*
Controls:
    Zoom-in = scroll up
    Zoom-out = scroll down
    Navigation = Arrow keys
    Increase num. of iterations = shift + up
    Decrease num. of iterations = shift + down
    Re-initialise window = Enter
*/

const int width = 900, height = 600;
//const double zoomScale = 1.1, moveScale = 10.0; //To be used later

int maxIter = 32; //Program uses maximum escape time of 'maxIter' terms
//double zoom = 1.0; //Will zoom into centre by default
double minRe = -2, maxRe = 1, minIm = -1, maxIm = 1; //Range of values for the window
double reInc = (maxRe - minRe)/width; //Multiply by x-coord of pixel to get the increment to add to minRe
double imInc = (maxIm - minIm)/height; //Multiply by y-coord of pixel to get the increment to add to minRe

struct complexNumber
{
    long double re;
    long double im;
};

//Image is loaded into texture, which is drawn onto a sprite, which is drawn onto a window

sf::Color HSVtoRGB(int H, double S, double V) {
	int output[3];
    double C = S * V;
	double X = C * (1 - abs(fmod(H / 60.0, 2) - 1));
	double m = V - C;
	double Rs, Gs, Bs;

	if(H >= 0 && H < 60) {
		Rs = C;
		Gs = X;
		Bs = 0;	
	}
	else if(H >= 60 && H < 120) {	
		Rs = X;
		Gs = C;
		Bs = 0;	
	}
	else if(H >= 120 && H < 180) {
		Rs = 0;
		Gs = C;
		Bs = X;	
	}
	else if(H >= 180 && H < 240) {
		Rs = 0;
		Gs = X;
		Bs = C;	
	}
	else if(H >= 240 && H < 300) {
		Rs = X;
		Gs = 0;
		Bs = C;	
	}
	else {
		Rs = C;
		Gs = 0;
		Bs = X;	
	}
	
	output[0] = (Rs + m) * 255;
	output[1] = (Gs + m) * 255;
	output[2] = (Bs + m) * 255;

    return sf::Color(output[0], output[1], output[2]);
}

void test(sf::VertexArray& plane)
{
    int k = 0;
    for (int x = 0; x <= width; x++)
    {
        for (int y = 0; y <= height; y++)
        {
            plane[k].position = sf::Vector2f(x, y);
            plane[k].color = sf::Color::Black;

            if ((x + y) % 3 == 0)
            {
                plane[k].color = sf::Color::Green;
            }
            k++;
        }
    }
}

void generateMandelbrot(sf::VertexArray& plane) 
{
#pragma omp parallel for
    int yCoord = -1;
    int xCoord = -1;
    int k = 0; //Index for the vertex array.
    for (double y = minIm; y <= maxIm; y += imInc)
    {
        yCoord++;
        for (double x = minRe; x <= maxRe; x += reInc)
        {
            std::cout << x << " + " << y << "i" << std::endl; //Debug print statement to check if the number is correct

            xCoord++;
            complexNumber c;
            c.re = x;
            c.im = y;

            complexNumber zOld;
            zOld.re = c.re;
            zOld.im = c.im;

            double modZ;
            complexNumber zNew;

            sf::Color pixelColor = sf::Color(0,0,0); //By default set to black.
            plane[k].position = sf::Vector2f(xCoord, yCoord); //We assign the co-ordinates beforehand because we know we have to draw this pixel

            //Determining the colour

            for (int iter = 0; iter <= maxIter; iter++)
            {
                zNew.re = zOld.re * zOld.re - zOld.im * zOld.im + c.re; //Real part is a^2 - b^2 + c.re
                zNew.im = (2 * zOld.re * zOld.im) + c.im; //Imaginary part is 2ab + c.im
                zOld.re = zNew.re;
                zOld.im = zNew.im;

                modZ = zNew.re * zNew.re + zNew.im * zNew.im;

                if (modZ >= 4) //Divergence case ==> We need to colour the pixel according to how fast it diverged
                {
                    int hue = (((iter/maxIter) * 360) + 240) % 360; //Adding 240 to make it start on colour
                    sf::Color pixelColor = HSVtoRGB(hue, 255, 255);
                    break; //We can leave the loop since we have now diverged.
                }

            }

            plane[k].color = pixelColor;
            k++;
        }
    }
}

int main() 
{
    sf::RenderWindow window(sf::VideoMode(width, height), "Mandelbrot set explorer");

    sf::VertexArray complexPlane(sf::Points, width * height); // Creating an array of points, with width * height number of them.

    //Initial drawing to be done here
    window.clear();
    window.display();
    test(complexPlane);
    //Event loop
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            //Checks all the window's events that were triggered since the last iteration of the loop
            switch (event.type)
            {
                case (sf::Event::Closed):
                    window.close();
                    break;

                case (sf::Event::KeyPressed):
                    if (sf::Keyboard::isKeyPressed(sf::Keyboard::Enter))
                    {
                        std::cout << "drawing image" << std::endl;
                        generateMandelbrot(complexPlane);
                        std::cout << "image drawn" << std::endl;
                    }  
            }
        }
        window.clear();
        window.draw(complexPlane);
        window.display();
    }

    return 0;
}