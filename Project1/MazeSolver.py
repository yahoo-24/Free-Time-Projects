import numpy as np
from colorama import Fore, init, Style

File1 = "Maze1.txt"
File2 = "Maze2.txt"
File3 = "Maze3.txt"
File4 = "Maze4.txt"
File5 = "Maze5.txt"
File6 = "Maze6.txt"
File7 = "Maze7.txt"
File8 = "Maze8.txt"

def readFile(FileName):
    """
    Reads the text file and returns the maze as a 2d array
    """
    file = open(FileName, 'r')
    Row = []
    Maze = []
    while True:
        line = file.readline().strip()
        if line == '':
            break
        for char in line:
            Row.append(char)
        Maze.append(Row)
        Row = []
    return Maze

def SetHeuristics(Maze):
    """
    This function will find the index of the start and end points and return them.
    It will also create a 2d array of the city block distance of each point to the end point and return it.
    Walls are given a default heuristic of 9999.
    """
    for idx, n in np.ndenumerate(Maze):
        if n == 'E':
            End = idx
        elif n == 'S':
            Start = idx

    Temp = []
    Heuristics = []
    counter = 0
    Max = len(Maze[0])
    for idx, n in np.ndenumerate(Maze):
        Heuristic = 9999
        if n != 'W':
            i = np.abs(End[0] - idx[0])
            j = np.abs(End[1] - idx[1])
            Heuristic = i + j
        Temp.append(Heuristic)
        counter += 1
        if counter == Max:
            Heuristics.append(Temp)
            Temp = []
            counter = 0

    return Heuristics, Start, End

def SolveMaze(Maze, Start, Heuristics, End):
    """
    The function initiates the process of solving the maze.
    It generates the first node to explore and calls upon the recursive function Explore.
    The function either returns -1 or a list of the path from S to E.
    """
    """
    -Start from Start
    -Call IgnoreWalls
    -Add Walls to Invalid nodes
    -Explore 4 possible options
    -Check that they are not Invalid or outside the maze
    -Append the possible options and their weight and parent to an array Options
    -If Options is empty then it is a dead end and there is no solution
    -Sort it according to weight and choose the option with least weight
    -IDK
    """
    IMax = len(Maze)
    JMax = len(Maze[0])
    I = Start[0]
    J = Start[1]
    Weight = Heuristics[I][J]
    Options = [[(I, J), Weight, 1, None, [(I, J)]]]
    # [Position of the point, Heuristic (h), Step (g), Parent Node, Path]
    Explored = {}
    return Explore(Maze, Options, (0, IMax), (0, JMax), Heuristics, Explored, End)

def Explore(Maze, Options, IRange, JRange, Heuristics, Explored, End):
    """
    The function recursively explores the possible paths from the current node.
    If those neighbouring nodes have not been explored yet, they are appended to the Options array, and
    the current node is added to the path to get to the new node.
    Should there be no options left, the function returns -1 which indicates no solution.
    If the current node is the destination, then the path is returned
    """
    # No more nodes to explore
    if Options == []:
        return -1
    T = Options.pop()
    I = T[0][0]
    J = T[0][1]
    path = T[4]
    g = T[2]
    if T[0] == End:
        # Call the function PathFinder to find the route
        Path = PathFinder(T[3], Explored, End)
        return Path
    Explored[(I,J)] = T[3]
    # Options for this node has been explored so next time we see this node we move on
    # Explore the 4 directions around the node and add them to Options if they are valid
    if (I + 1) < IRange[1] and Heuristics[I + 1][J] != 9999 and (I + 1, J) not in Explored:
        Weight = Heuristics[I + 1][J] + g
        path.append((I + 1,J))
        Tuple = ([(I + 1,J), Weight, g+1, (I, J), path])
        path.pop()
        Options.append(Tuple)
    if (I - 1) >= IRange[0] and Heuristics[I - 1][J] != 9999 and (I - 1, J) not in Explored:
        Weight = Heuristics[I - 1][J] + g
        path.append((I - 1,J))
        Tuple = ([(I - 1,J), Weight, g+1, (I, J), path])
        path.pop()
        Options.append(Tuple)
    if (J + 1) < JRange[1] and Heuristics[I][J + 1] != 9999 and (I, J + 1) not in Explored:
        Weight = Heuristics[I][J + 1] + g
        path.append((I,J + 1))
        Tuple = ([(I,J + 1), Weight, g+1, (I, J), path])
        path.pop()
        Options.append(Tuple)
    if (J - 1) >= JRange[0] and Heuristics[I][J - 1] != 9999 and (I, J - 1) not in Explored:
        Weight = Heuristics[I][J - 1] + g
        path.append((I,J - 1))
        Tuple = ([(I,J - 1), Weight, g+1, (I, J), path])
        path.pop()
        Options.append(Tuple)
    # Reorder the array so that the lower weight is placed first
    Options = sorted(Options, key=lambda x : x[1], reverse=True)
    return Explore(Maze, Options, IRange, JRange, Heuristics, Explored, End)

def PathFinder(Parent, Explored, End):
    """
    Once the path is found in the Explored function, the function looks for the parent of the end node
    in the Explored dictionary. Once found, it will look for the parent of that node and so on until
    the parent node is None (the start node).
    The array is inverted (such that it has the path from start to end rather than end to start)
    then returned.
    """
    Path = []
    Path.append(Parent)
    while True:
        Parent = Explored[Parent]
        if Parent == None:
            break
        Path.append(Parent)
    Path = Path[::-1]
    Path.append(End)
    return Path

def DrawPath(Result, Maze):
    """
    The function removes the first and last nodes which is the start and finish.
    It then loops through the rest of the array changing the values to '-'.
    """
    Result.pop(0)
    Result.pop()
    for Coordinates in Result:
        I = Coordinates[0]
        J = Coordinates[1]
        Maze[I][J] = '-'
    return Maze

def DisplayMaze(Maze):
    init()
    for row in Maze:
        for item in row:
            if item == 'W':
                print(Fore.RED + '█' + Style.RESET_ALL, end='')
            elif item == '-':
                print(Fore.YELLOW + '█' + Style.RESET_ALL, end='')
            elif item == 'S':
                print(Fore.GREEN + '█' + Style.RESET_ALL, end='')
            elif item == 'E':
                print(Fore.BLUE + '█' + Style.RESET_ALL, end='')
            else:
                print(Fore.WHITE + '█' + Style.RESET_ALL, end='')
        print()

def main():
    # Choose the maze by specifying the file below
    file = input("Enter the file name: ")
    Maze = readFile(file)
    Heuristics, Start, End = SetHeuristics(Maze)
    Result = SolveMaze(Maze, Start, Heuristics, End)
    # The result is either a list of the path or -1
    if type(Result) == list:
        Output = DrawPath(Result, Maze)
        DisplayMaze(Output)
    else:
        print("There is no Path")

if __name__ == "__main__":
    main()
