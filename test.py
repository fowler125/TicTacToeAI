import pygame
import random
import math
import sys

# Constants
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
FONT = pygame.font.SysFont('comicsans', 80)


# Functions
def draw_board():
    WIN.fill(BG_COLOR)
    for row in range(BOARD_ROWS):
        pygame.draw.line(WIN, LINE_COLOR, (0, row * SQUARE_SIZE + LINE_WIDTH), (WIDTH, row * SQUARE_SIZE + LINE_WIDTH),
                         LINE_WIDTH)
        for col in range(BOARD_COLS):
            pygame.draw.line(WIN, LINE_COLOR, (col * SQUARE_SIZE + LINE_WIDTH, 0),
                             (col * SQUARE_SIZE + LINE_WIDTH, HEIGHT), LINE_WIDTH)


def draw_markers():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(WIN, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(WIN, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(WIN, CIRCLE_COLOR,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def is_winner(board, letter):
    # Check rows
    for row in board:
        if all(cell == letter for cell in row):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == letter for row in range(BOARD_ROWS)):
            return True
    # Check diagonals
    if all(board[i][i] == letter for i in range(BOARD_ROWS)):
        return True
    if all(board[i][BOARD_ROWS - 1 - i] == letter for i in range(BOARD_ROWS)):
        return True
    return False


def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True


def minimax(board, depth, is_maximizing):
    if is_winner(board, 'X'):
        return -10 + depth, None
    elif is_winner(board, 'O'):
        return 10 - depth, None
    elif is_board_full(board):
        return 0, None

    if is_maximizing:
        best_score = -math.inf
        best_move = None
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score, _ = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_score, best_move
    else:
        best_score = math.inf
        best_move = None
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score, _ = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    if score < best_score:
                        best_score = score
                        best_move = (row, col)
        return best_score, best_move


def monte_carlo_simulation(board):
    empty_squares = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == ' ']
    return random.choice(empty_squares)


def random_step(board):
    return random.choice(
        [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == ' '])


def get_computer_move(board, algorithm='minimax'):
    if algorithm == 'minimax':
        _, move = minimax(board, 0, True)
    elif algorithm == 'monte_carlo':
        move = monte_carlo_simulation(board)
    elif algorithm == 'random_step':
        move = random_step(board)
    return move


def display_menu(selected_algorithm):
    font = pygame.font.SysFont('comicsans', 40)
    menu = [
        ('Minimax', 'minimax'),
        ('Monte Carlo', 'monte_carlo'),
        ('Random Step', 'random_step')
    ]
    menu_height = len(menu) * 50
    menu_rect = pygame.Rect(WIDTH - 200, HEIGHT // 2 - menu_height // 2, 200, menu_height)
    pygame.draw.rect(WIN, BG_COLOR, menu_rect)
    for i, (text, algo) in enumerate(menu):
        color = (255, 255, 255) if algo != selected_algorithm else (0, 255, 0)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH - 100, HEIGHT // 2 - menu_height // 2 + 50 * i + 25))
        WIN.blit(text_surface, text_rect)
    return menu_rect


def main():
    global board
    board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    turn = random.choice(['X', 'O'])
    selected_algorithm = None

    while not selected_algorithm:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH - 200 <= x <= WIDTH and HEIGHT // 2 - 75 <= y <= HEIGHT // 2 + 75:
                    selected_algorithm = 'minimax' if HEIGHT // 2 - 75 <= y <= HEIGHT // 2 - 25 else \
                        'monte_carlo' if HEIGHT // 2 - 25 <= y <= HEIGHT // 2 + 25 else \
                            'random_step'
        WIN.fill(BG_COLOR)
        pygame.draw.rect(WIN, (255, 255, 255), (WIDTH - 200, HEIGHT // 2 - 75, 200, 150))
        font = pygame.font.SysFont('comicsans', 40)
        text_surface1 = font.render("Minimax", True, (0, 0, 0))
        text_surface2 = font.render("Monte Carlo", True, (0, 0, 0))
        text_surface3 = font.render("Random Step", True, (0, 0, 0))
        WIN.blit(text_surface1, (WIDTH - 100 - text_surface1.get_width() // 2, HEIGHT // 2 - 50))
        WIN.blit(text_surface2, (WIDTH - 100 - text_surface2.get_width() // 2, HEIGHT // 2))
        WIN.blit(text_surface3, (WIDTH - 100 - text_surface3.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if turn == 'X':
                    row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        if is_winner(board, 'X'):
                            game_over = True
                        elif is_board_full(board):
                            game_over = True
                        turn = 'O'
            if turn == 'O' and not game_over:
                row, col = get_computer_move(board, algorithm=selected_algorithm)
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    if is_winner(board, 'O'):
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    turn = 'X'

        draw_board()
        draw_markers()
        display_menu_rect = display_menu(selected_algorithm)
        if game_over:
            if is_winner(board, 'X'):
                text = FONT.render('Player X wins!', True, CROSS_COLOR)
            elif is_winner(board, 'O'):
                text = FONT.render('Player O wins!', True, CIRCLE_COLOR)
            else:
                text = FONT.render('It\'s a tie!', True, (255, 255, 255))
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)

        pygame.display.update()


if __name__ == "__main__":
    main()
