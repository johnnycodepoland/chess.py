class Game:
    def __init__(self):
        self.board = {
            (0, 0): "black_rook",
            (1, 0): "black_knight",
            (2, 0): "black_bishop",
            (3, 0): "black_queen",
            (4, 0): "black_king",
            (5, 0): "black_bishop",
            (6, 0): "black_knight",
            (7, 0): "black_rook",
            (0, 1): "black_pawn",
            (1, 1): "black_pawn",
            (2, 1): "black_pawn",
            (3, 1): "black_pawn",
            (4, 1): "black_pawn",
            (5, 1): "black_pawn",
            (6, 1): "black_pawn",
            (7, 1): "black_pawn",
            (0, 7): "white_rook",
            (1, 7): "white_knight",
            (2, 7): "white_bishop",
            (3, 7): "white_queen",
            (4, 7): "white_king",
            (5, 7): "white_bishop",
            (6, 7): "white_knight",
            (7, 7): "white_rook",
            (0, 6): "white_pawn",
            (1, 6): "white_pawn",
            (2, 6): "white_pawn",
            (3, 6): "white_pawn",
            (4, 6): "white_pawn",
            (5, 6): "white_pawn",
            (6, 6): "white_pawn",
            (7, 6): "white_pawn",
        }
        # Tworzymy zmienną do przechowywania aktualnego ruchu
        self.turn = "white"

    def can_move(self, selected_square, second_square):
        col, row = selected_square
        can_move = False

        # Logika pionka
        if (self.board[selected_square] == "white_pawn" or self.board[selected_square] == "black_pawn"):
            # Tutaj analizujemy dwa przypadki jeden dla białego drugi dla czarnego pionka
            if self.board[selected_square] == "white_pawn":
                direction = -1
            else:
                direction = 1
            # Tutaj również analizujemy dwa przypadki jeden dla ruchu startowego o 2 pola, a także ten standardowy o 1 pole
            if (second_square == (col, row + direction) or (second_square == (col, row + direction * 2) and (row == 6 or row == 1) and (col, row + direction) not in self.board)) and second_square not in self.board:
                col, row = second_square
                can_move = True
            elif ((second_square == (col +1, row + direction)) or (second_square == (col -1, row + direction))) and (second_square in self.board) and not (("white" in self.board[selected_square] and "white" in self.board[second_square]) or ("black" in self.board[selected_square] and "black" in self.board[second_square])):
                col, row = second_square
                can_move = True
        # Logika wierzy
        elif (self.board[selected_square] == "white_rook" or self.board[selected_square] == "black_rook") and (second_square not in self.board or not (("white" in self.board[selected_square] and "white" in self.board[second_square]) or ("black" in self.board[selected_square] and "black" in self.board[second_square]))):
            # Tutaj sprawdzamy czy wiersz lub kolumna zgadza się z pozycją wierzy
            col2, row2 = second_square

            # Tutaj iterujemy sobie przez wszystkie pola między wierzą a punktem docelowym, najpierw w przypadku kiedy ruch ma się odbyć w prawo lub w lewo
            if col == col2:
                for c in range(min(row, row2) +1, max(row, row2)):
                    if (col, c) in self.board:
                        break
                else:
                    can_move = True
            # Tu analizujemy opcję w której wierza porusza się w górę lub w dół
            elif row == row2:
                for c in range(min(col, col2) +1, max(col, col2)):
                    if (c, row) in self.board:
                        break
                else:
                    can_move = True
        # Logika skoczka
        elif (self.board[selected_square] == "white_knight" or self.board[selected_square] == "black_knight") and (second_square not in self.board or not (("white" in self.board[selected_square] and "white" in self.board[second_square]) or ("black" in self.board[selected_square] and "black" in self.board[second_square]))):
            col2, row2 = second_square

            if (col2, row2) == (col +2, row +1) or (col2, row2) == (col +2, row -1) or (col2, row2) == (col + 1, row +2) or (col2, row2) == (col-1, row +2) or (col2, row2) == (col +1, row -2) or (col2, row2) == (col-1, row -2) or (col2, row2) == (col-2, row +1) or (col2, row2) == (col-2, row -1):
                can_move = True
        # Logika gońca
        elif (self.board[selected_square] == "white_bishop" or self.board[selected_square] == "black_bishop") and (second_square not in self.board or not (("white" in self.board[selected_square] and "white" in self.board[second_square]) or ("black" in self.board[selected_square] and "black" in self.board[second_square]))):
            col2, row2 = second_square
            # Tutaj obliczmy sobię kierunek ruchu
            d_col = (col2 - col) // abs(col2 - col)
            d_row = (row2 - row) // abs(row2 - row)

            # Tutaj korzystamy z funkcji abs(x) która podaję nam wartość bezwzględną danej liczby, co w tym przypadku wykorzystujemy do obliczenia wartości bezwzględnej z różnicy col2 - col1 i row2 - row, co pozwala nam potem sprawdzić czy ich różnica jest sobie równa
            if abs(col2 - col) == abs(row2 - row):
                # Tutaj iterujemy sobie przez wszystkie pola między polem docelowym a startowym, z wykorzystaniem funkcji zip, która łaczy nam iterowalne elementy, w tym przypadku pierwsza wartość to punkt startowy + kierunek kolumny, druga wartość to punkt końcowy a trzecia, to o ile się poruszamy, analogiczną sytuację mamy w rzędach
                for c, r in zip(range(col + d_col, col2, d_col), range(row + d_row, row2, d_row)):
                    if (c, r) in self.board:
                        break
                else:
                    can_move = True
        # Logika hetmana
        elif (self.board[selected_square] == "white_queen" or self.board[selected_square] == "black_queen") and (second_square not in self.board or not (("white" in self.board[selected_square] and "white" in self.board[second_square]) or ("black" in self.board[selected_square] and "black" in self.board[second_square]))):
            col2, row2 = second_square

            if abs(col2 - col) == abs(row2 - row):
                d_col = (col2 - col) // abs(col2 - col)
                d_row = (row2 - row) // abs(row2 - row)
                for c, r in zip(range(col + d_col, col2, d_col), range(row + d_row, row2, d_row)):
                    if (c, r) in self.board:
                        break
                else:
                    can_move = True
            elif row == row2:
                for c in range(min(col, col2) + 1, max(col, col2)):
                    if (c, row) in self.board:
                        break
                else:
                    can_move = True
            elif col == col2:
                for c in range(min(row, row2) + 1, max(row, row2)):
                    if (col, c) in self.board:
                        break
                else:
                    can_move = True
        # Logika króla
        elif (self.board[selected_square] == "white_king" or self.board[selected_square] == "black_king") and (second_square not in self.board or not (("white" in self.board[selected_square] and "white" in self.board[second_square]) or ("black" in self.board[selected_square] and "black" in self.board[second_square]))):
            col2, row2 = second_square

            if (col2, row2) == (col, row +1) or (col2, row2) == (col +1, row +1) or (col2, row2) == (col +1, row) or (col2, row2) == (col +1, row -1) or (col2, row2) == (col, row -1) or (col2, row2) == (col-1, row -1) or (col2, row2) == (col-1, row) or (col2, row2) == (col-1, row +1):
                can_move = True
        return can_move

    def switch_turn(self):
        if self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"

    def make_move(self, selected_square, second_square):
        col, row = selected_square

        self.board[second_square] = self.board[selected_square]
        del self.board[selected_square]