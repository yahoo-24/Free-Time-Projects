#include <iostream>
using namespace std;

char EMPTY = '.';
char X = 'X';
char O = 'O';

struct result {
    int i;
    int j;
};
int checkHorizontal(char board[][3]){
    for (int i = 0; i < 3; i++){
        if (board[i][0] == board[i][1] && 
            board[i][1] == board[i][2]){
                if (board[i][0] == X){
                    return 1;
                }
                else if(board[i][0] == O){
                    return -1;
                }
        }
    }
    return 0;
}
int checkVertical(char board[][3]){
    for (int i = 0; i < 3; i++){
        if (board[0][i] == board[1][i] &&
            board[1][i] == board[2][i]){
                if (board[0][i] == X){
                    return 1;
                }
                else if(board[0][i] == O){
                    return -1;
                }
        }
    }
    return 0;
}
int checkDiagonal(char board[][3]){
    if (board[0][0] == board[1][1] && 
        board[1][1] == board[2][2]){
                if (board[0][0] == X){
                    return 1;
                }
                else if(board[0][0] == O){
                    return -1;
                }
    }
    if (board[2][0] == board[1][1] && board[1][1]
        == board[0][2]){
            if (board[2][0] == X){
                    return 1;
                }
                else if(board[2][0] == O){
                    return -1;
                }
    }
    return 0;
}
int checkWinner(char board[][3]){
    int h = checkHorizontal(board);
    int v = checkVertical(board);
    int d = checkDiagonal(board);
    if (h != 0){
        return h;
    }
    if (v != 0){
        return v;
    }
    if (d != 0){
        return d;
    }
    return 0;
}
bool checkTie(char board[][3]){
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            if (board[i][j] == EMPTY){
                return false;
            }
        }
    }
    return true;
}

void display(char board[][3]){
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            cout << board[i][j] << ' ';
        }
    cout << endl;
    }
}
int MaxValue(char board[][3]);
int MinValue(char board[][3]){
    int result = checkWinner(board);
    if (result != 0){
        return result;
    }
    else{
        bool isTie = checkTie(board);
        if (isTie == true){
            return 0;
        }
    }
    int best = 2;
    for (int k = 0; k < 3; k++){
        for (int j = 0; j < 3; j++){
            if (board[k][j] == EMPTY){
                board[k][j] = O;
                int score = MaxValue(board);
                board[k][j] = EMPTY;
                if (score < best){
                    best = score;
                }
            }
        }
    }
    return best;
}
int MaxValue(char board[][3]){
    int result = checkWinner(board);
    if (result != 0){
        return result;
    }
    else{
        bool isTie = checkTie(board);
        if (isTie == true){
            return 0;
        }
    }
    int best = -2;
    for (int m = 0; m < 3; m++){
        for (int j = 0; j < 3; j++){
            if (board[m][j] == EMPTY){
                board[m][j] = X;
                int score = MinValue(board);
                board[m][j] = EMPTY;
                if (score > best){
                    best = score;
                }
            }
        }
    }
    return best;
}

auto BestMove(char board[][3]){
    int bestI = 0;
    int bestJ = 0;
    int best = -2;
    for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
            if (board[i][j] == EMPTY){
                board[i][j] = X;
                int score = MinValue(board);
                board[i][j] = EMPTY;
                if (score > best){
                    best = score;
                    bestI = i;
                    bestJ = j;
                }
            }
        }
    }
    cout << best << '\n';
    result move;
    move.i = bestI;
    move.j = bestJ;
    return move;
}

int main(){
    
    char board[3][3] = {
        {EMPTY, EMPTY, EMPTY},
        {EMPTY, EMPTY, EMPTY},
        {EMPTY, EMPTY, EMPTY}
    };
    bool stop = false;
    int turn = 0;
    while (stop == false){
        if (turn % 2 == 0){
            auto move = BestMove(board);
            int i = move.i;
            int j = move.j;
            board[i][j] = X;
            display(board);
        }
        else{
            int row;
            int col;
            cout << "Enter the row number 1 to 3: ";
            cin >> row;
            cout << endl;
            cout << "Enter the coloumn number 1 to 3: ";
            cin >> col;
            cout << endl;
            board[row-1][col-1] = O;
        }
        int val = checkWinner(board);
        if (val == 1){
            cout << "X has won";
            stop = true;
        }
        else if(val == -1){
            cout << "O has won";
            stop = true;
        }
        else{
            bool isTie = checkTie(board);
            if (isTie == true){
                cout << "Tie";
                stop = true;
            }
        }
        turn++;
    }
}