import pygame

class Utils:
    def left_click_event(self):
        # Tutaj sprawdzamy czy mysz została naciśnięta
        mouse_button = pygame.mouse.get_pressed()

        left_click = False
        # Tutaj sprawdzamy czy kliknięty przycisk myszki jest lewy
        if mouse_button[0]:
            # Zmieniamy flagę
            left_click = True
        return left_click

    def get_cords_under_mouse(self, current_turn):
        # Wymiar jednego boku kwadratu
        size_of_row_col = 80

        # Tutaj przeliczamy koordynaty kursora, na adres pola
        x, y = pygame.mouse.get_pos()
        col = x // size_of_row_col
        row = y // size_of_row_col

        # Tutaj zwracamy koordynaty, w zależności od aktualnej tury
        if current_turn == "white":
            return col, row
        elif current_turn == "black":
            new_col = 7 - col
            new_row = 7 - row
            return new_col, new_row