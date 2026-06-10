class Chess:
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

        # Tworzymy zmienną do przechowywania adresu pola, zbitej figury
        self.captured = None

        # Tworzymy zmienne do przechowywania informacji o tym, czy dany król wykonał już jakiś ruch
        self.white_king = False

        self.black_king = False

        # Tworzymy zmienne do przechowywania informacji o tym, czy dana wieża wykonała już jakiś ruch
        self.white_rook_left_corner = False

        self.white_rook_right_corner = False

        self.black_rook_left_corner = False

        self.black_rook_right_corner = False

        # Tworzymy zmienną do przechowywania pozycji pionka, który wykonuje podwójny ruch, co przyda nam się do bicia w przelocie, a także zmienną do przechowywania poprzedniej lokalizacji figury, która została zbita
        self.en_passant_location = None

        self.previous_en_passant_location = None

    def can_move(self, selected_square, second_square):
        col, row = selected_square
        can_move = False
        # Logika bicia w przelocie
        if self.board[selected_square] == "white_pawn" and self.en_passant_location is not None and (self.en_passant_location == (col - 1, row) or self.en_passant_location == (col + 1, row)) and second_square == (self.en_passant_location[0], self.en_passant_location[1] - 1):
            can_move = True
        elif self.board[selected_square] == "black_pawn" and self.en_passant_location is not None and (self.en_passant_location == (col - 1, row) or self.en_passant_location == (col + 1, row)) and second_square == (self.en_passant_location[0], self.en_passant_location[1] + 1):
            can_move = True
        # Logika pionka
        elif self.board[selected_square] == "white_pawn" or self.board[selected_square] == "black_pawn":
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
            # Tutaj sprawdzamy, czy wiersz lub kolumna zgadza się z pozycją wierzy
            col2, row2 = second_square

            # Tutaj iterujemy sobie przez wszystkie pola między wierzą, a punktem docelowym, najpierw w przypadku kiedy ruch ma się odbyć w prawo lub w lewo
            if col == col2:
                for c in range(min(row, row2) +1, max(row, row2)):
                    if (col, c) in self.board:
                        break
                else:
                    can_move = True
            # Tu analizujemy opcję, poruszania się w górę lub w dół
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

            # Tutaj korzystamy z funkcji abs(x) która podaję nam wartość bezwzględną danej liczby, co w tym przypadku wykorzystujemy do obliczenia wartości bezwzględnej z różnicy col2 - col1 i row2 - row, co pozwala nam potem sprawdzić, czy ich różnica jest sobie równa
            if abs(col2 - col) == abs(row2 - row):
                # Tutaj obliczmy sobię kierunek ruchu
                d_col = (col2 - col) // abs(col2 - col)
                d_row = (row2 - row) // abs(row2 - row)
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
        # Logika roszady, dla każdej z czterech możliwości
        elif self.board[selected_square] == "white_king" and second_square == (6, 7) and self.white_king is False and self.white_rook_right_corner is False and (5, 7) not in self.board and (6, 7) not in self.board and self.is_square_in_check(self.turn, (5, 7)) is False and self.is_square_in_check(self.turn, (6, 7)) is False:
            can_move = True
        elif self.board[selected_square] == "white_king" and second_square == (2, 7) and self.white_king is False and self.white_rook_left_corner is False and (1, 7) not in self.board and (2, 7) not in self.board and (3, 7) not in self.board and self.is_square_in_check(self.turn, (1, 7)) is False and self.is_square_in_check(self.turn, (2, 7)) is False and self.is_square_in_check(self.turn, (3, 7)) is False:
            can_move = True
        elif self.board[selected_square] == "black_king" and second_square == (6, 0) and self.black_king is False and self.black_rook_right_corner is False and (5, 0) not in self.board and (6, 0) not in self.board and self.is_square_in_check(self.turn, (5, 0)) is False and self.is_square_in_check(self.turn, (6, 0)) is False:
            can_move = True
        elif self.board[selected_square] == "black_king" and second_square == (2, 0) and self.black_king is False and self.black_rook_left_corner is False and (1, 0) not in self.board and (2, 0) not in self.board and (3, 0) not in self.board and self.is_square_in_check(self.turn, (1, 0)) is False and self.is_square_in_check(self.turn, (2, 0)) is False and self.is_square_in_check(self.turn, (3, 0)) is False:
            can_move = True
        # Logika króla
        elif (self.board[selected_square] == "white_king" or self.board[selected_square] == "black_king") and (second_square not in self.board or not (("white" in self.board[selected_square] and "white" in self.board[second_square]) or ("black" in self.board[selected_square] and "black" in self.board[second_square]))):
            col2, row2 = second_square

            if (col2, row2) == (col, row +1) or (col2, row2) == (col +1, row +1) or (col2, row2) == (col +1, row) or (col2, row2) == (col +1, row -1) or (col2, row2) == (col, row -1) or (col2, row2) == (col-1, row -1) or (col2, row2) == (col-1, row) or (col2, row2) == (col-1, row +1):
                can_move = True
        return can_move

    # Funkcja zmieniająca tury
    def switch_turn(self):
        if self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"

    # Funkcja wykonująca ruch
    def make_move(self, selected_square, second_square):
        col, row = selected_square
        self.previous_en_passant_location = self.en_passant_location

        # Warunki do roszady
        if self.board[selected_square] == "white_king":
            self.white_king = True
        elif self.board[selected_square] == "black_king":
            self.black_king = True
        elif self.board[selected_square] == "black_rook" and second_square == (7, 0):
            self.black_rook_right_corner = True
        elif self.board[selected_square] == "black_rook" and second_square == (0, 0):
            self.black_rook_left_corner = True
        elif self.board[selected_square] == "white_rook" and second_square == (7, 7):
            self.white_rook_right_corner = True
        elif self.board[selected_square] == "white_rook" and second_square == (0, 7):
            self.white_rook_left_corner = True
        # Warunki do bicia w przelocie
        if self.board[selected_square] == "white_pawn" and second_square == (col, row - 2):
            self.en_passant_location = second_square
        elif self.board[selected_square] == "black_pawn" and second_square == (col, row + 2):
            self.en_passant_location = second_square
        else:
            self.en_passant_location = None
        self.captured = self.board.get(second_square)
        self.board[second_square] = self.board[selected_square]
        del self.board[selected_square]

    # Funkcja sprawdzająca, czy król jest pod szachem
    def is_in_check(self, color):
        for location in self.board:
            if self.board[location] == color + "_king":
                king_pos = location
                break
        for piece in self.board:
            if color not in self.board[piece]:
                if self.can_move(piece, king_pos):
                    return True
        return False

    # Funkcja sprawdzająca, czy dane pole jest atakowane
    def is_square_in_check(self, color, square):
        for piece in self.board:
            if color not in self.board[piece]:
                if self.can_move(piece, square):
                    return True
        return False

    # Funkcja cofająca ruch
    def undo_move(self, selected_square, second_square):
        if self.board[second_square] == "white_king":
            self.white_king = False
        elif self.board[second_square] == "black_king":
            self.black_king = False
        elif self.board[second_square] == "black_rook" and second_square == (7, 0):
            self.black_rook_right_corner = False
        elif self.board[second_square] == "black_rook" and second_square == (0, 0):
            self.black_rook_left_corner = False
        elif self.board[second_square] == "white_rook" and second_square == (7, 7):
            self.white_rook_right_corner = False
        elif self.board[second_square] == "white_rook" and second_square == (0, 7):
            self.white_rook_left_corner = False
        self.board[selected_square] = self.board[second_square]
        del self.board[second_square]
        if self.captured: # jeśli figura została zbita
            self.board[second_square] = self.captured # przywracamy ją
        self.en_passant_location = self.previous_en_passant_location

    # Funkcja sprawdzająca, czy mamy do czynienia z matem
    def is_checkmate(self, color):
        moves = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        for location in self.board:
            if self.board[location] == color + "_king":
                king_pos = location
                break
        for move in moves:
            move = king_pos[0] + move[0], king_pos[1] + move[1]
            if self.can_move(king_pos, move) and move in self.board:
                self.make_move(king_pos, move)
                if not self.is_in_check(color):
                    self.undo_move(king_pos, move)
                    return False
                self.undo_move(king_pos, move)
        for piece in self.board:
            if color in self.board[piece]:
                for col in range(8):
                    for row in range(8):
                        if self.can_move(piece, (col, row)):
                            self.make_move(piece, (col, row))
                            if not self.is_in_check(color):
                                self.undo_move(piece, (col, row))
                                return False
                            self.undo_move(piece, (col, row))
        return True

    def is_stalemate(self, color):
        moves = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        if self.is_in_check(color):
            return False
        for location in self.board:
            if self.board[location] == color + "_king":
                king_pos = location
                break
        for move in moves:
            move = king_pos[0] + move[0], king_pos[1] + move[1]
            if self.can_move(king_pos, move) and move in self.board:
                self.make_move(king_pos, move)
                if not self.is_in_check(color):
                    self.undo_move(king_pos, move)
                    return False
                self.undo_move(king_pos, move)
        for piece in self.board:
            if color in self.board[piece]:
                for col in range(8):
                    for row in range(8):
                        if self.can_move(piece, (col, row)):
                            self.make_move(piece, (col, row))
                            if not self.is_in_check(color):
                                self.undo_move(piece, (col, row))
                                return False
                            self.undo_move(piece, (col, row))
        return True

    # Funkcja wykonująca cały ruch gracza
    def play_turn(self, selected_square, second_square):
        result = ""
        col, row = second_square
        en_passant_before = self.previous_en_passant_location

        if selected_square in self.board and self.turn in self.board[selected_square]:
            if self.can_move(selected_square, second_square):
                self.make_move(selected_square, second_square)
                if self.is_in_check(self.turn):
                    self.undo_move(selected_square, second_square)
                else:
                    # Warunki do roszady
                    if self.board[second_square] == "white_king" and second_square == (6, 7):
                        self.board[(5, 7)] = self.board[(7, 7)]
                        del self.board[(7, 7)]
                    elif self.board[second_square] == "white_king" and second_square == (2, 7):
                        self.board[(3, 7)] = self.board[(0, 7)]
                        del self.board[(0, 7)]
                    elif self.board[second_square] == "black_king" and second_square == (6, 0):
                        self.board[(5, 0)] = self.board[(7, 0)]
                        del self.board[(7, 0)]
                    elif self.board[second_square] == "black_king" and second_square == (2, 0):
                        self.board[(3, 0)] = self.board[(0, 0)]
                        del self.board[(0, 0)]
                    # Warunek do promocji pionka
                    if (self.board[second_square] == "white_pawn" and row == 0) or (self.board[second_square] == "black_pawn" and row == 7):
                        color = self.board[second_square].split("_")[0]
                        while True:
                            piece = input("Podaj nazwę figury (hetman, wierza, goniec, skoczek): ")
                            if piece == "hetman":
                                self.board[second_square] = color +"_queen"
                                break
                            elif piece == "wierza":
                                self.board[second_square] = color +"_rook"
                                break
                            elif piece == "goniec":
                                self.board[second_square] = color + "_bishop"
                                break
                            elif piece == "skoczek":
                                self.board[second_square] = color + "_knight"
                                break
                    # Warunek do bicia w przelocie
                    if en_passant_before is not None and (second_square == (en_passant_before[0], en_passant_before[1] - 1) or second_square == (en_passant_before[0], en_passant_before[1] + 1)):
                        del self.board[en_passant_before]
                    self.switch_turn()
                    if self.is_checkmate(self.turn):
                        self.switch_turn()
                        result = "Checkmate"
                        return result
                    elif self.is_stalemate(self.turn):
                        self.switch_turn()
                        result = "Stalemate"
                        return result
        return False