#include <iostream>
#include <cmath>
#include <SFML/Window.hpp>
#include <SFML/Graphics.hpp>

int width = 1000;
int height = 1000;

int main() 
{
    sf::RenderWindow window(sf::VideoMode(width, height), "Mandelbrot set explorer");

    sf::VertexArray complexPlane(sf::Points, width * height); // Creating an array of points, with width * height number of them.

    //Initial drawing to be done here
    window.clear(sf::Color::White);
    //Event loop
    
    sf::CircleShape shape(50);
    shape.setOutlineColor(sf::Color::Black);
    window.draw(shape);
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
            }
        }
        window.display();
    }

    return 0;
}