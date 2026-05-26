import pygame
from utils import Utils
from piece import Piece
from chess import Chess

class Game:
    def __init__(self):
        # Inicjalizacja biblioteki pygame
        pygame.init()
        # Tworzymy sobie ekran
        self.screen = pygame.display.set_mode((640, 640))

        # Importujemy tło
        self.background = pygame.image.load('res/board.png')

        # Tutaj dodajemy zmienną start_square, która będzie przechowywać aktualnie wybrane pole
        self.start_square = None

        # Tutaj dodajemy zmienną, która będzie przechowywać pozycję docelową
        self.second_square = None

        # Tworzymy zmienną do przechowywania pozycji startowej po resecie
        self.selected_square = None

        # Tutaj wywołujemy wszystkie potrzebne klasy
        self.piece = Piece("./res/pieces.png", 6, 2)
        self.chess = Chess()
        self.utils = Utils()

    def start_game(self):
        """Funkcja zawiera główną pętlę gry"""
        running = True
        # Główna pętla gry
        while running:
            # RGB = Red, Green, Blue (ustawimy kolor tła)
            self.screen.fill((0, 0, 0))
            # Tło ekranu
            self.screen.blit(self.background, (0, 0))

            # Tutaj mamy pętle która, zaczyna się od sprawdzenia czy, użytkownik używa lewego przycisky myszy
            if self.utils.left_click_event():
                if self.start_square is None:
                    self.start_square = self.utils.get_cords_under_mouse(self.chess.turn)
                else:
                    # Tutaj zapisujemy sobie koordynaty myszy
                    self.second_square = self.utils.get_cords_under_mouse(self.chess.turn)
                    self.selected_square = self.start_square
                    self.start_square = None
            if self.selected_square is not None:
                col, row = self.selected_square
                if self.chess.turn == "white":
                    rect = pygame.Rect(col * 80, row * 80, 80, 80)
                    pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
                elif self.chess.turn == "black":
                    new_col = 7 - col
                    new_row = 7 - row
                    rect = pygame.Rect(new_col * 80, new_row * 80, 80, 80)
                    pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
                if self.chess.play_turn(self.selected_square, self.second_square):
                    print(f"Wygrywa", self.chess.turn)
                    running = False

            # Tutaj renderujemy wszystkie figury, w zależności od tury
            if self.chess.turn == "white":
                for i in self.chess.board:
                    col, row = i
                    self.piece.draw(self.screen, self.chess.board[i], (col * 80, row * 80))
            elif self.chess.turn == "black":
                for i in self.chess.board:
                    col, row = i
                    new_col = 7 - col
                    new_row = 7 - row
                    self.piece.draw(self.screen, self.chess.board[i], (new_col * 80, new_row * 80))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()