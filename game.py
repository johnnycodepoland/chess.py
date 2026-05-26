import pygame
from utils import Utils
from piece import Piece
from chess import Chess
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

# Tutaj wywołujemy wszystkie potrzebne klasy
piece = Piece("./res/pieces.png", 6, 2)
chess = Chess()
utils = Utils()

# Główna pętla gry
running = True
while running:
    # RGB = Red, Green, Blue (ustawimy kolor tła)
    screen.fill((0, 0, 0))
    # Tło ekranu
    screen.blit(background, (0, 0))

    # Tutaj mamy pętle która zaczyna się od sprawdzenia czy użytkownik używa lewego przycisky myszy
    if utils.left_click_event():
        if start_square is None:
            start_square = utils.get_cords_under_mouse(chess.turn)
        else:
            # Tutaj zapisujemy sobie koordynaty myszy
            second_square = utils.get_cords_under_mouse(chess.turn)
            selected_square = start_square
            start_square = None
    if selected_square is not None:
        col, row = selected_square
        if chess.turn == "white":
            rect = pygame.Rect(col * 80, row * 80, 80, 80)
            pygame.draw.rect(screen, (255, 0, 0), rect, 3)
        elif chess.turn == "black":
            new_col = 7 - col
            new_row = 7 - row
            rect = pygame.Rect(new_col * 80, new_row * 80, 80, 80)
            pygame.draw.rect(screen, (255, 0, 0), rect, 3)

        if selected_square in chess.board and chess.turn in chess.board[selected_square]:
            if chess.can_move(selected_square, second_square):
                chess.make_move(selected_square, second_square)
                if chess.is_in_check(chess.turn):
                    chess.undo_move(selected_square, second_square)
                else:
                    chess.switch_turn()
                    if chess.is_checkmate(chess.turn):
                        chess.switch_turn()
                        print(f"Wygrywa", chess.turn)
                        running = False
    # Tutaj renderujemy wszystkie figury, w zależności od tury
    if chess.turn == "white":
        for i in chess.board:
            col, row = i
            piece.draw(screen, chess.board[i], (col * 80, row * 80))
    elif chess.turn == "black":
        for i in chess.board:
            col, row = i
            new_col = 7 - col
            new_row = 7 - row
            piece.draw(screen, chess.board[i], (new_col * 80, new_row * 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()