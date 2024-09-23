# Maze Solver

## Description
This project solves mazes using the A* algorithm. It explores the maze and finds the shortest route to the end point
if it exists.
The code makes use of 2 modules: the colorama module which allows me to print the result in a way that
the user can see the path easily and the make the maze look visually appealing, the NumPy module where I used ndenumerate and abs.

## Installation
To start, download the file and install the dependencies using: pip install -r requirements.txt

### Usage Instructions
There are 8 mazes with the code. To run the code for a specific maze, just run the code and it will prompt you to write the file name or you can manually change the code to run a specific file by setting line190 to be 'FileN' (where N is the file number) instead of 'file'.
You can add more mazes if you wish.
The maze must have equal number elements in all the rows as well as equal number of elements on all the columns. 'W' stands for walls. '.' are for nodes that can be moved to. 'S' stands for start. 'E' is for end.

## Features
- Quickly finds the optimal solution to a 2d maze if it exists.
- Prints the solution using colours making it easily interpretable.

## Technologies Used
- Python
