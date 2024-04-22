import pygame
import sys
import time

import tictactoe as ttt
from button import Button

pygame.init()
size = width, height = 1280, 720

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = ttt.initial_state()
ai_turn = False

algorithm = ""


"""
Main Menu is the starting menu function for the runner code
"""
def main_menu():
    while True:
        #Step 1: Track Mouse Position
        #Step 2: Form the buttons
        #Step 3: Display the buttons
        #Step 4: Implement Button Logic

        #Step 1 (to know when something collides with something on the screen AKA when we click something)
        mouse = pygame.mouse.get_pos()

        #Step 2
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=mediumFont, base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=mediumFont, base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=mediumFont, base_color="#d7fcd4", hovering_color="White")

        #for every button that we have generated up top, we will load onto the screen using an array
        #Step 3
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(mouse)
            button.update(screen)
        #Step 4 (Event Handler)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse):
                    #play(user)
                    algorithm_selector(algorithm)
                #if OPTIONS_BUTTON.checkForInput(mouse):
                    #options()
                if QUIT_BUTTON.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def algorithm_selector(algo):
    while True:
        algo_mouse = pygame.mouse.get_pos()
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if algo == '':
            algo_text = largeFont.render("Which Algo Do You Want to Play Against?",True, white)
            algoRect = algo_text.get_rect()
            algoRect.center = ((width/2),50)
            screen.blit(algo_text,algoRect)

            minMax_BTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                                 text_input="MiniMax", font=mediumFont, base_color="#d7fcd4", hovering_color="White")
            Monte_BTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400),
                                text_input="Monte Carlo Tree Search", font=mediumFont, base_color="#d7fcd4", hovering_color="White")
            Random_BTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 550),
                                text_input="Random", font=mediumFont, base_color="#d7fcd4", hovering_color="White")

        for button in [minMax_BTN, Monte_BTN,Random_BTN]:
            button.changeColor(algo_mouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if minMax_BTN.checkForInput(algo_mouse):
                    algorithm = "MinMax"
                    play(None,algorithm,board,ai_turn)
                if Monte_BTN.checkForInput(algo_mouse):
                    algorithm = "Monte"
                    play(None, algorithm, board, ai_turn)
                if Random_BTN.checkForInput(algo_mouse):
                    algorithm = "Random"
                    play(None,algorithm,board,ai_turn)
        pygame.display.flip()

def play(u,algo,brd,AI):
    # Set user status to none, although its passed in, reiterate it to be none in order for Play Again Loop to be satisfied
    # Screen Fill Black to make next screen
    # Make X and Y button, use similar approach to Main Menu

    user = u
    board = brd
    ai_turn = AI

    while True:
        play_mouse = pygame.mouse.get_pos()
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        if algo == "MinMax":
            if user is None:
                title = largeFont.render("Play Tic-Tac-Toe", True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 50)
                screen.blit(title, titleRect)

                X_BTTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                                text_input="Play as X", font=mediumFont, base_color="#d7fcd4", hovering_color="White")
                Y_BTTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400),
                                text_input="Play as O", font=mediumFont, base_color="#d7fcd4", hovering_color="White")
                BACK_BTTN = Button(image=None, pos=(75, 50),
                                text_input="<BACK", font=mediumFont, base_color="#d7fcd4", hovering_color="White")

                for button in [X_BTTN, Y_BTTN, BACK_BTTN]:
                    button.changeColor(play_mouse)
                    button.update(screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if X_BTTN.checkForInput(play_mouse):
                            time.sleep(0.2)
                            user = ttt.X
                        elif Y_BTTN.checkForInput(play_mouse):
                            time.sleep(0.2)
                            user = ttt.O
                        elif BACK_BTTN.checkForInput(play_mouse):
                            main_menu()


            else:

                # Draw game board
                tile_size = 80
                tile_origin = (width / 2 - (1.5 * tile_size),
                               height / 2 - (1.5 * tile_size))
                tiles = []
                for i in range(3):
                    row = []
                    for j in range(3):
                        rect = pygame.Rect(
                            tile_origin[0] + j * tile_size,
                            tile_origin[1] + i * tile_size,
                            tile_size, tile_size
                        )
                        pygame.draw.rect(screen, white, rect, 3)

                        if board[i][j] != ttt.EMPTY:
                            move = moveFont.render(board[i][j], True, white)
                            moveRect = move.get_rect()
                            moveRect.center = rect.center
                            screen.blit(move, moveRect)
                        row.append(rect)
                    tiles.append(row)

                game_over = ttt.terminal(board)
                player = ttt.player(board)

                # Show title
                if game_over:
                    winner = ttt.winner(board)
                    if winner is None:
                        title = f"Game Over: Tie."
                    else:
                        title = f"Game Over: {winner} wins."
                elif user == player:
                    title = f"Play as {user}"
                else:
                    title = f"Computer thinking..."
                title = largeFont.render(title, True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 30)
                screen.blit(title, titleRect)

                # Check for AI move
                if user != player and not game_over:
                    if ai_turn:
                        time.sleep(0.5)
                        move = ttt.minimax(board)
                        board = ttt.result(board, move)
                        ai_turn = False
                    else:
                        ai_turn = True

                # Check for a user move
                click, _, _ = pygame.mouse.get_pressed()
                if click == 1 and user == player and not game_over:
                    mouse = pygame.mouse.get_pos()
                    for i in range(3):
                        for j in range(3):
                            if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                                board = ttt.result(board, (i, j))

                if game_over:
                    againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
                    again = mediumFont.render("Play Again", True, black)
                    againRect = again.get_rect()
                    againRect.center = againButton.center
                    pygame.draw.rect(screen, white, againButton)
                    screen.blit(again, againRect)
                    click, _, _ = pygame.mouse.get_pressed()
                    if click == 1:
                        mouse = pygame.mouse.get_pos()
                        if againButton.collidepoint(mouse):
                            time.sleep(0.2)
                            user = None
                            board = ttt.initial_state()
                            ai_turn = False
        elif algo == "Random":
            if user is None:
                title = largeFont.render("Play Tic-Tac-Toe", True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 50)
                screen.blit(title, titleRect)

                X_BTTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                                text_input="Play as X", font=mediumFont, base_color="#d7fcd4",
                                hovering_color="White")
                Y_BTTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400),
                                text_input="Play as O", font=mediumFont, base_color="#d7fcd4",
                                hovering_color="White")

                for button in [X_BTTN, Y_BTTN]:
                    button.changeColor(play_mouse)
                    button.update(screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if X_BTTN.checkForInput(play_mouse):
                            time.sleep(0.2)
                            user = ttt.X
                        elif Y_BTTN.checkForInput(play_mouse):
                            time.sleep(0.2)
                            user = ttt.O
            else:
                tile_size = 80
                tile_origin = (width / 2 - (1.5 * tile_size),
                               height / 2 - (1.5 * tile_size))
                tiles = []
                for i in range(3):
                    row = []
                    for j in range(3):
                        rect = pygame.Rect(
                            tile_origin[0] + j * tile_size,
                            tile_origin[1] + i * tile_size,
                            tile_size, tile_size
                        )
                        pygame.draw.rect(screen, white, rect, 3)

                        if board[i][j] != ttt.EMPTY:
                            move = moveFont.render(board[i][j], True, white)
                            moveRect = move.get_rect()
                            moveRect.center = rect.center
                            screen.blit(move, moveRect)
                        row.append(rect)
                    tiles.append(row)

                game_over = ttt.terminal(board)
                player = ttt.player(board)

                if game_over:
                    winner = ttt.winner(board)
                    if winner is None:
                        title = f"Game Over: Tie."
                    else:
                        title = f"Game Over: {winner} wins."
                elif user == player:
                    title = f"Play as {user}"
                else:
                    title = f"Computer thinking..."
                title = largeFont.render(title, True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 30)
                screen.blit(title, titleRect)

                # Check for AI move
                if user != player and not game_over:
                    if ai_turn:
                        time.sleep(0.5)
                        move = ttt.random_move(board)
                        board = ttt.result(board, move)
                        ai_turn = False
                    else:
                        ai_turn = True

                click, _, _ = pygame.mouse.get_pressed()
                if click == 1 and user == player and not game_over:
                    mouse = pygame.mouse.get_pos()
                    for i in range(3):
                        for j in range(3):
                            if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                                board = ttt.result(board, (i, j))
        elif algo == "Monte":
            if user is None:
                title = largeFont.render("Play Tic-Tac-Toe", True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 50)
                screen.blit(title, titleRect)

                X_BTTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                                text_input="Play as X", font=mediumFont, base_color="#d7fcd4",
                                hovering_color="White")
                Y_BTTN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400),
                                text_input="Play as O", font=mediumFont, base_color="#d7fcd4",
                                hovering_color="White")

                for button in [X_BTTN, Y_BTTN]:
                    button.changeColor(play_mouse)
                    button.update(screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if X_BTTN.checkForInput(play_mouse):
                            time.sleep(0.2)
                            user = ttt.X
                        elif Y_BTTN.checkForInput(play_mouse):
                            time.sleep(0.2)
                            user = ttt.O
            else:
                tile_size = 80
                tile_origin = (width / 2 - (1.5 * tile_size),
                               height / 2 - (1.5 * tile_size))
                tiles = []
                for i in range(3):
                    row = []
                    for j in range(3):
                        rect = pygame.Rect(
                            tile_origin[0] + j * tile_size,
                            tile_origin[1] + i * tile_size,
                            tile_size, tile_size
                        )
                        pygame.draw.rect(screen, white, rect, 3)

                        if board[i][j] != ttt.EMPTY:
                            move = moveFont.render(board[i][j], True, white)
                            moveRect = move.get_rect()
                            moveRect.center = rect.center
                            screen.blit(move, moveRect)
                        row.append(rect)
                    tiles.append(row)

                game_over = ttt.terminal(board)
                player = ttt.player(board)

                if game_over:
                    winner = ttt.winner(board)
                    if winner is None:
                        title = f"Game Over: Tie."
                    else:
                        title = f"Game Over: {winner} wins."
                elif user == player:
                    title = f"Play as {user}"
                else:
                    title = f"Computer thinking..."
                title = largeFont.render(title, True, white)
                titleRect = title.get_rect()
                titleRect.center = ((width / 2), 30)
                screen.blit(title, titleRect)

                # Check for AI move
                if user != player and not game_over:
                    if ai_turn:
                        time.sleep(0.5)
                        move = ttt.monte_carlo_tree_search(board,10)
                        board = ttt.result(board, move)
                        ai_turn = False
                    else:
                        ai_turn = True

                click, _, _ = pygame.mouse.get_pressed()
                if click == 1 and user == player and not game_over:
                    mouse = pygame.mouse.get_pos()
                    for i in range(3):
                        for j in range(3):
                            if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                                board = ttt.result(board, (i, j))

                if game_over:
                    againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
                    again = mediumFont.render("Play Again", True, black)
                    againRect = again.get_rect()
                    againRect.center = againButton.center
                    pygame.draw.rect(screen, white, againButton)
                    screen.blit(again, againRect)
                    click, _, _ = pygame.mouse.get_pressed()
                    if click == 1:
                        mouse = pygame.mouse.get_pos()
                        if againButton.collidepoint(mouse):
                            time.sleep(0.2)
                            user = None
                            board = ttt.initial_state()
                            ai_turn = False



        pygame.display.flip()

def quit():
    sys.exit()

main_menu()
