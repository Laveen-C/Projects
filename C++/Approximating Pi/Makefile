all: compile link clean

compile:
	g++ -c *.cpp -I"C:\Program Files (x86)\SFML\include"

link:
	g++ *.o -o main -L"C:\Program Files (x86)\SFML\lib" -lsfml-graphics -lsfml-window -lsfml-system

clean:
	del *.o
