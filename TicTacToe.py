def prod(x):
    'Multiplies the elements of a list'
    i = 1
    for j in x:
        i = i*j
    return i

def transp(x):
    'Transposes a 3x3 matrix'
    return [[x[i][j] for i in range(3)] for j in range(3)]

def diag1(x):
    'Takes the 1st diagonal of a 3x3 matrix'
    return [x[i][i] for i in range(3)]

def diag2(x):
    'Takes the 2nd diagonal of a 3x3 matrix'
    return [x[i][2-i] for i in range(3)]

def switch(pl):
    'Maps (1,2) to (2,1) for switching the player'
    return pl % 2 + 1

class Tic:
    'The class of Tic-Tac-Toe boards'

    def __init__(self):
        'Initiates with an empty board and 1st player'
        self.board = [[1 for i in range(3)] for i in range(3)]
        self.player = 1  # takes values 1 or 2

    def __str__(self):
        'Prints the board and whose turn it is'
        dct = {
            1: " . ",
            2: " X ",
            3: " O "
        }
        dct2 = {
            1: "1 (X)",
            2: "2 (O)"
        }
        return """
             1   2   3         
             
         1  {}|{}|{}
            ___+___+___
         2  {}|{}|{}
            ___+___+___
         3  {}|{}|{}
                    Player: {}
        """.format(*[dct[self.board[i][j]] for i in range(3) for j in range(3)], dct2[self.player])

    def play(self, x, y):
        'A valid move is played with this command'
        self.board[x][y] = self.player + 1
        self.player = switch(self.player)

    def unplay(self, x, y):
        'A move is reversed with this command'
        self.board[x][y] = 1
        self.player = switch(self.player)

    def control(self, x, y):
        'Checks if a proposed move is valid'
        entries = {0, 1, 2}
        return x in entries and y in entries and self.board[x][y] == 1

    def reset_board(self):
        'Resets the board'
        self.board = [[1 for i in range(3)] for i in range(3)]
        self.player = 1

    def get_player_input(self):
        'Gets input from a human player'
        a = input("First coordinate:  ")
        b = input("Second coordinate: ")
        if a.isnumeric() and b.isnumeric():
            x = int(a) - 1
            y = int(b) - 1
            if self.control(x, y):
                self.play(x, y)

    def win(self):
        'Checks if the game is won/lost'
        check_row_aux = set(map(prod, self.board))
        check_row = 27 in check_row_aux or 8 in check_row_aux
        check_col_aux = set(map(prod, transp(self.board)))
        check_col = 27 in check_col_aux or 8 in check_col_aux
        check_diags = prod(diag1(self.board)) in {27, 8} or prod(diag2(self.board)) in {27, 8}
        return (check_diags or check_row or check_col), switch(self.player)

    def tie(self):
        'Checks if the game is over with a tie'
        complete = (self.possible_moves() == [])
        return complete and not self.win()[0]

    def possible_moves(self):
        'Lists the possible moves available'
        return [[i,j] for i in range(3) for j in range(3) if self.board[i][j] == 1]

    def minimax(self,maxpl):
        'Uses the minimax algorithm to decide on the optimal move for the AI with infinite depth'
        if self.win()[0]:
            return 1 - 2 * maxpl, [-1,-1]
        if self.tie():
            return 0, [-1,-1]
        if maxpl:
            value, move = -10, [-1,-1]
            for pos_move in self.possible_moves():
                self.play(*pos_move)
                v, m = self.minimax(False)
                if v > value:
                    value, move = v, pos_move
                self.unplay(*pos_move)
            return value, move
        else:
            value, move = +10, [-1,-1]
            for pos_move in self.possible_moves():
                self.play(*pos_move)
                v, m = self.minimax(True)
                if v < value:
                    value, move = v, pos_move
                self.unplay(*pos_move)
            return value, move

    def loop(self):
        'Runs the turns of the game in a loop'
        while not (self.win()[0] or self.tie()):
            print(self)
            human_plays = (self.mode == "1") or (self.mode == "2" and self.player == 1) or (self.mode == "3" and self.player == 2)
            if human_plays:
                self.get_player_input()
            else:
                _, move = self.minimax(True)
                self.play(*move)
        print(self)
        if self.win()[0]:
            print("Game over! Player " + str(self.win()[1]) + " won.")
        else:
            print("Game over! It's a tie.")

    def select_game_mode(self):
        'Asks about the game mode'
        print("""Choose the mode of play:""")
        print("""1 : human vs human""")
        print("""2 : human vs AI""")
        print("""3 : AI vs human""")
        print("""4 : AI vs AI""")
        a = input(" ")
        self.mode = a

    def start(self):
        'Launches the game'
        print(" ")
        print("Welcome to Tic-Tac-Toe, designed by Yigit Yargic and Ekin Igdir!")
        print(" ")
        self.select_game_mode()
        print("""Enjoy the game!""")
        self.loop()
        restart = input("Do you want to play again? (Y/N)")
        if restart in {"Y","y","1","yes","YES","Yes"}:
            self.reset_board()
            self.start()

if __name__ == '__main__':
    a = Tic()
    a.start()
