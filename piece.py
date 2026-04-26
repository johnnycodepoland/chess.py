import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, filename,  cols, rows):
        pygame.sprite.Sprite.__init__(self)
        # Tutaj zapisujemy sobie indeksy tych figur z pliku
        self.pieces = {
            "white_pawn":   5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook":   4,
            "white_king":   0,
            "white_queen":  1,
            "black_pawn":   11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook":   10,
            "black_king":   6,
            "black_queen":  7
        }
        # Tutaj załadowujemy sobie plik z figurami, convert_alpha pozwala dodać obrazkom przeźroczystość
        self.spritesheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.cell_count = self.rows * self.cols

        self.rect = self.spritesheet.get_rect()

        h = self.rect.height // self.rows
        w = self.rect.width // self.cols

        # Tutaj pętla for i in range(self.cell_count), iteruje nam przez każdy poszczególny indeks i wypisuje wysokość, szerokość i koordynaty do wycięcia
        self.cells = [(i % self.cols * w, i // self.cols * h, w, h ) for i in range(self.cell_count)]

    def draw(self, surface, piece_name, coords):
        index = self.pieces[piece_name]
        surface.blit(self.spritesheet, coords, self.cells[index])


