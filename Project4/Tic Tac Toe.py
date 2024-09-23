Board = [["","",""],
         ["","",""],
         ["","",""]]


def CheckHor(Board):
    if Board[0][0] == Board[0][1] == Board[0][2] and Board[0][0] != '':
        if Board[0][0] == 'X':
            g = 1
        else:
            g = -1
        return True, g
    elif Board[1][0] == Board[1][1] == Board[1][2] and Board[1][0] != '':
        if Board[1][0] == 'X':
            g = 1
        else:
            g = -1
        return True, g
    elif Board[2][0] == Board[2][1] == Board[2][2] and Board[2][0] != '':
        if Board[2][0] == 'X':
            g = 1
        else:
            g = -1
        return True, g
    else:
        return False, -2


def CheckVer(Board):
    if Board[0][0] == Board[1][0] == Board[2][0] and Board[0][0] != '':
        if Board[0][0] == 'X':
            g = 1
        else:
            g = -1
        return True, g
    elif Board[0][1] == Board[1][1] == Board[2][1] and Board[0][1] != '':
        if Board[0][1] == 'X':
            g = 1
        else:
            g = -1
        return True, g
    elif Board[0][2] == Board[1][2] == Board[2][2] and Board[0][2] != '':
        if Board[0][2] == 'X':
            g = 1
        else:
            g = -1
        return True, g
    else:
        return False, -2


def CheckDia(Board):
    if Board[0][0] == Board[1][1] == Board[2][2] and Board[0][0] != '':
        if Board[0][0] == 'X':
            g = 1
        else:
            g = -1
        return True, g
    elif Board[2][0] == Board[1][1] == Board[0][2] and Board[1][1] != '':
        if Board[2][0] == 'X':
            g = 1
        else:
            g = -1
        return True, g
    else:
        return False, -2


def CheckTie(Board):
    a = Board[0]
    b = Board[1]
    c = Board[2]
    if '' not in a and '' not in b and '' not in c:
        return True
    else:
        return False


def CheckWinner(Board):
    check,g = CheckVer(Board)
    if check:
        return g
    check2,g = CheckDia(Board)
    if check2:
        return g
    check3,g = CheckHor(Board)
    if check3:
        return g
    if CheckTie(Board):
        return 0
    else:
        return None


def bestMove(Board):
    Best = -10
    for i in range(3):
        for j in range(3):
            if Board[i][j] == '':
                Board[i][j] = 'X'
                score = MinVal(Board)
                Board[i][j] = ''
                if score > Best:
                    Best = score
                    optMoveR = i
                    optMoveC = j
    Board[optMoveR][optMoveC] = 'X'
    return Board


def MaxVal(Board):
    z = CheckWinner(Board)
    if z != None:
        return z
    else:
        Best = -10
        for i in range(3):
            for j in range(3):
                if Board[i][j] == '':
                    Board[i][j] = 'X'
                    score = MinVal(Board)
                    Board[i][j] = ''
                    if score > Best:
                        Best = score
        return Best


def MinVal(Board):
    z = CheckWinner(Board)
    if z  != None:
        return z
    else:
        Best = 10
        for i in range(3):
            for j in range(3):
                if Board[i][j] == '':
                    Board[i][j] = 'O'
                    score = MaxVal(Board)
                    Board[i][j] = ''
                    if score < Best:
                        Best = score
        return Best   


def display():
    print("    1    2   3")
    for i in range(3):
        print(f"{i+1} {Board[i]}")

t = [0,2,4,6,8]
op = [1,2,3]
def main():
    global Board
    for i in range(9):
        if i in t:
            choiceR = int(input("Row: 1 to 3: "))
            choiceC = int(input("Coloumn :1 to 3: "))
            while Board[choiceR-1][choiceC-1] != ''  or choiceR not in op or choiceC not in op:
                choiceR = int(input("Error R: 1 to 3: "))
                choiceC = int(input("Error C: 1 to 3: "))                
            Board[choiceR-1][choiceC-1] = 'O'
        else:
            Board = bestMove(Board)
        end = CheckWinner(Board)
        display()
        if end != None:
            if end == 1:
                print('X wins')
            elif end == 0:
                print('Tie')
            else:
                print('O wins')
            break


main()

