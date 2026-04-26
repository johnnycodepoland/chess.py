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

    def get_cords_under_mouse(self):
        # Wymiar jednego boku kwadratu
        size_of_row_col = 80

        # Tutaj przeliczamy koordynaty kursora, na adres pola
        x, y = pygame.mouse.get_pos()
        return (x // size_of_row_col, y // size_of_row_col)