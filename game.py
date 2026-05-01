import pygame
from utils import Utils
from piece import Piece
utils = Utils()
pygame.init()

# Tworzymy sobie ekran
screen = pygame.display.set_mode((640,640))

# Importujemy tło
background = pygame.image.load('res/board.png')

# Tutaj dodajemy zmienną start_square, która będzie przechowywać aktualnie wybrane pole
start_square = None

# Tutaj dodajemy zmienną która będzie przechowywać pozycję docelową
second_square = None

# Tworzymy zmienną do przechowywania pozycji startowej po resecie
selected_square = None

board = {
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

piece = Piece("./res/pieces.png", 6, 2)

running = True
while running:
    # RGB = Red, Green, Blue (ustawimy kolor tła)
    screen.fill((0, 0, 0))
    # Tło ekranu
    screen.blit(background, (0, 0))
    # Tutaj mamy pętle która zaczyna się od sprawdzenia czy użytkownik używa lewego przycisky myszy
    if utils.left_click_event():
        if start_square is None:
            start_square = utils.get_cords_under_mouse()
        else:
            # Tutaj zapisujemy sobie koordynaty myszy
            second_square = utils.get_cords_under_mouse()
            selected_square = start_square
            start_square = None
    if selected_square is not None:
        col, row = selected_square
        rect = pygame.Rect(col * 80, row * 80, 80, 80)
        pygame.draw.rect(screen, (255, 0, 0), rect, 3)

        # Logika pionka
        if selected_square in board and (board[selected_square] == "white_pawn" or board[selected_square] == "black_pawn") and second_square not in board:
            # Tutaj analizujemy dwa przypadki jeden dla białego drugi dla czarnego pionka
            if board[selected_square] == "white_pawn":
                direction = -1
            else:
                direction = 1
            # Tutaj również analizujemy dwa przypadki jeden dla ruchu startowego o 2, a takżę ten normalny
            if second_square == (col, row + direction) or (second_square == (col, row + direction * 2) and (row == 6 or row == 1) and (col, row + direction) not in board):
                col, row = second_square
                piece.draw(screen, board[selected_square], (col * 80, row * 80))
                board[second_square] = board[selected_square]
                del board[selected_square]
        # Logika wierzy
        elif selected_square in board and (board[selected_square] == "white_rook" or board[selected_square] == "black_rook") and second_square not in board:
            # Tutaj sprawdzamy czy wiersz lub kolumna zgadza się z pozycją wierzy
            col2, row2 = second_square

            # Tutaj iterujemy sobie przez wszystkie pola między wierzą a punktem docelowym, najpierw w przypadku kiedy ruch ma się odbyć w prawo lub w lewo
            if col == col2:
                for c in range(min(row, row2) +1, max(row, row2)):
                    if (col, c) in board:
                        break
                else:
                    piece.draw(screen, board[selected_square], (col2 * 80, row2 * 80))
                    board[second_square] = board[selected_square]
                    del board[selected_square]
            # Tu analizujemy opcję w której wierza porusza się w górę lub w dół
            elif row == row2:
                for c in range(min(col, col2) +1, max(col, col2)):
                    if (c, row) in board:
                        break
                else:
                    piece.draw(screen, board[selected_square], (col2 * 80, row2 * 80))
                    board[second_square] = board[selected_square]
                    del board[selected_square]
        # Logika skoczka
        elif selected_square in board and (board[selected_square] == "white_knight" or board[selected_square] == "black_knight") and second_square not in board:
            col2, row2 = second_square

            if (col2, row2) == (col +2, row +1) or (col2, row2) == (col +2, row -1) or (col2, row2) == (col + 1, row +2) or (col2, row2) == (col-1, row +2) or (col2, row2) == (col +1, row -2) or (col2, row2) == (col-1, row -2) or (col2, row2) == (col-2, row +1) or (col2, row2) == (col-2, row -1):
                piece.draw(screen, board[selected_square], (col2 * 80, row2 * 80))
                board[second_square] = board[selected_square]
                del board[selected_square]
        # Logika gońca
        elif selected_square in board and (board[selected_square] == "white_bishop" or board[selected_square] == "black_bishop") and second_square not in board:
            col2, row2 = second_square
            # Tutaj obliczmy sobię kierunek ruchu
            d_col = (col2 - col) // abs(col2 - col)
            d_row = (row2 - row) // abs(row2 - row)

            # Tutaj korzystamy z funkcji abs(x) która podaję nam wartość bezwzględną danej liczby, co w tym przypadku wykorzystujemy do obliczenia wartości bezwzględnej z różnicy col2 - col1 i row2 - row, co pozwala nam potem sprawdzić czy ich różnica jest sobie równa
            if abs(col2 - col) == abs(row2 - row):
                # Tutaj iterujemy sobie przez wszystkie pola między polem docelowym a startowym, z wykorzystaniem funkcji zip, która łaczy nam iterowalne elementy, w tym przypadku pierwsza wartość to punkt startowy + kierunek kolumny, druga wartość to punkt końcowy a trzecia, to o ile się poruszamy, analogiczną sytuację mamy w rzędach
                for c, r in zip(range(col + d_col, col2, d_col), range(row + d_row, row2, d_row)):
                    if (c, r) in board:
                        break
                else:
                    piece.draw(screen, board[selected_square], (col2 * 80, row2 * 80))
                    board[second_square] = board[selected_square]
                    del board[selected_square]
        # Logika hetmana
        elif selected_square in board and(board[selected_square] == "white_queen" or board[selected_square] == "black_queen") and second_square not in board:
            col2, row2 = second_square

            if abs(col2 - col) == abs(row2 - row):
                d_col = (col2 - col) // abs(col2 - col)
                d_row = (row2 - row) // abs(row2 - row)
                for c, r in zip(range(col + d_col, col2, d_col), range(row + d_row, row2, d_row)):
                    if (c, r) in board:
                        break
                else:
                    piece.draw(screen, board[selected_square], (col2 * 80, row2 * 80))
                    board[second_square] = board[selected_square]
                    del board[selected_square]
            elif row == row2:
                for c in range(min(col, col2) + 1, max(col, col2)):
                    if (col, c) in board:
                        break
                else:
                    piece.draw(screen, board[selected_square], (col2 * 80, row2 * 80))
                    board[second_square] = board[selected_square]
                    del board[selected_square]
            elif col == col2:
                for c in range(min(row, row2) + 1, max(row, row2)):
                    if (c, row) in board:
                        break
                else:
                    piece.draw(screen, board[selected_square], (col2 * 80, row2 * 80))
                    board[second_square] = board[selected_square]
                    del board[selected_square]


    # Tutaj renderujemy wszystkie figury
    for i in board:
        col, row = i
        piece.draw(screen, board[i], (col * 80, row * 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()