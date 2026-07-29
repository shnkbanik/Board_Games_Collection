import tkinter as tk
import random
from common import headline, subHeadline, footer, setBackgroundImage


def showGame(root, backCallback):
    # Set background color
    root.configure(bg="#FFFFFF")

    #createGradient(root, "#ffebee", "#ef9a9a")
    setBackgroundImage(root, "games.jpg")
    # Headline of the Game01 screen
    headline(root, "#FFFFFF")

    # SUB-Headline of the Game01 screen
    subHeadline(root, "Tin Guti", "#FFFFFF")

    # Footer text
    footer(root, "#FFFFFF")

    # Create a frame for bottom buttons to place them side by side
    buttonFrame = tk.Frame(root, bg="#FFFFFF")
    buttonFrame.pack(side=tk.BOTTOM, pady=20)

    # Instruction Text
    instructTxt = (
        "Welcome to Tin Guti (3 Beads)!\n\n"
        "How to Play:\n"
        "1. Click on your blue coin to select it.\n"
        "2. Use arrow keys (↑↓←→) to move to adjacent empty position.\n"
        "3. Press ENTER to confirm the move.\n"
        "4. Get 3 of your coins in a row to win!\n"
        "5. You cannot win on your starting line."
    )

    # Instruction button
    instructBtnWidget = tk.Button(buttonFrame, text="Instruction", font=("Arial", 12),
                                  bg="#FFFFFF", command=lambda: showInstruct())
    instructBtnWidget.pack(side=tk.LEFT, padx=10)

    # Go Back button
    gobackBtn = tk.Button(buttonFrame, text="Back to Dashboard", font=("Arial", 12),
                          bg="#FFFFFF", command=backCallback)
    gobackBtn.pack(side=tk.LEFT, padx=10)

    def showInstruct():
        popup = tk.Toplevel(root)
        popup.title("Game Instructions")
        popup.geometry("500x400")
        popup.configure(bg="#ffebee")

        label = tk.Label(popup, text="Game Instructions", font=("Arial", 18, "bold"), bg="#ffebee")
        label.pack(pady=10)

        text_box = tk.Message(popup, text=instructTxt, font=("Arial", 12), width=480, bg="#ffebee")
        text_box.pack(padx=20, pady=10)

        close_btn = tk.Button(popup, text="Close", font=("Arial", 12), command=popup.destroy)
        close_btn.pack(pady=10)

    # Scoreboard
    playerFrame = tk.Frame(root, bg="#FFFFFF")
    playerFrame.place(relx=0.1, rely=0.5, anchor="w")

    playerLabel = tk.Label(playerFrame, text="PLAYER", font=("Arial", 16, "bold"), bg="#FFFFFF")
    playerLabel.pack()
    playerScore = tk.Label(playerFrame, text="0", font=("Arial", 20, "bold"), fg="blue", bg="#FFFFFF")
    playerScore.pack()

    computerFrame = tk.Frame(root, bg="#FFFFFF")
    computerFrame.place(relx=0.9, rely=0.5, anchor="e")
    computerLabel = tk.Label(computerFrame, text="COMPUTER", font=("Arial", 16, "bold"), bg="#FFFFFF")
    computerLabel.pack()
    computerScore = tk.Label(computerFrame, text="0", font=("Arial", 20, "bold"), fg="red", bg="#FFFFFF")
    computerScore.pack()

    # Canvas of Board
    canvas = tk.Canvas(root, width=500, height=500, bg="white", highlightthickness=2, highlightbackground="black")
    canvas.place(relx=0.5, rely=0.55, anchor="center")

    # Constant Value
    GRID_SIZE = 3
    CELL_SIZE = 120
    COIN_RADIUS = 30
    BOARD_START_X = 130
    BOARD_START_Y = 130

    # Position mapping (P1 to P9)
    POSITIONS = {
        0: (0, 0), 1: (0, 1), 2: (0, 2),  # P1, P2, P3
        3: (1, 0), 4: (1, 1), 5: (1, 2),  # P4, P5, P6
        6: (2, 0), 7: (2, 1), 8: (2, 2)  # P7, P8, P9
    }

    # Connected Positions (points)
    ADJACENCY = {
        0: [1, 3, 4],  # P1 → P2, P4, P5
        1: [0, 2, 4],  # P2 → P1, P3, P5
        2: [1, 4, 5],  # P3 → P2, P5, P6
        3: [0, 4, 6],  # P4 → P1, P5, P7
        4: [0, 1, 2, 3, 5, 6, 7, 8],  # P5 → All (center)
        5: [2, 4, 8],  # P6 → P3, P5, P9
        6: [3, 4, 7],  # P7 → P4, P5, P8
        7: [6, 8, 4],  # P8 → P7, P9, P5
        8: [7, 4, 5]  # P9 → P8, P5, P6
    }

    # Winning Lines
    WINNING_LINES = [
        [0, 1, 2],  # P1-P2-P3 (top)
        [3, 4, 5],  # P4-P5-P6 (middle)
        [6, 7, 8],  # P7-P8-P9 (bottom)
        [0, 3, 6],  # P1-P4-P7 (left)
        [1, 4, 7],  # P2-P5-P8 (center)
        [2, 5, 8],  # P3-P6-P9 (right)
        [0, 4, 8],  # P1-P5-P9 (diagonal \)
        [2, 4, 6]  # P3-P5-P7 (diagonal /)
    ]

    # All variables
    playerScoreVal = 0
    computerScoreVal = 0
    board = [None] * 9  # Positions 0-8 (P1-P9)
    currentPlayer = "PLAYER"
    selectedCoin = None  # Position index of selected coin
    previewPosition = None  # Preview position when using arrow keys
    gameOver = False
    levelFrame = None
    difficulty = None

    # Update Scores
    def updateScoreLabels():
        playerScore.config(text=str(playerScoreVal))
        computerScore.config(text=str(computerScoreVal))

    # Canvas coordinates from position
    def getCanvasCoords(pos):
        row, col = POSITIONS[pos]
        x = BOARD_START_X + col * CELL_SIZE
        y = BOARD_START_Y + row * CELL_SIZE
        return (x, y)

    # Draw the board
    def drawBoard():
        # Draw horizontal lines
        for row in range(GRID_SIZE):
            y = BOARD_START_Y + row * CELL_SIZE
            canvas.create_line(BOARD_START_X, y,
                               BOARD_START_X + (GRID_SIZE - 1) * CELL_SIZE, y,
                               width=3, fill="black")

        # Draw vertical lines
        for col in range(GRID_SIZE):
            x = BOARD_START_X + col * CELL_SIZE
            canvas.create_line(x, BOARD_START_Y,
                               x, BOARD_START_Y + (GRID_SIZE - 1) * CELL_SIZE,
                               width=3, fill="black")

        # Draw diagonal lines
        # P1 to P9 (top-left to bottom-right)
        canvas.create_line(BOARD_START_X, BOARD_START_Y,
                           BOARD_START_X + 2 * CELL_SIZE, BOARD_START_Y + 2 * CELL_SIZE,
                           width=3, fill="black")

        # P3 to P7 (top-right to bottom-left)
        canvas.create_line(BOARD_START_X + 2 * CELL_SIZE, BOARD_START_Y,
                           BOARD_START_X, BOARD_START_Y + 2 * CELL_SIZE,
                           width=3, fill="black")

        # Draw position markers (small circles at each point)
        for pos in range(9):
            x, y = getCanvasCoords(pos)
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="gray", outline="black")

    # Draw coins
    def drawCoins():
        canvas.delete("coin")
        canvas.delete("selection")
        canvas.delete("preview")

        for pos in range(9):
            if board[pos] is not None:
                x, y = getCanvasCoords(pos)
                color = "blue" if board[pos] == "PLAYER" else "red"

                # Draw coin
                canvas.create_oval(x - COIN_RADIUS, y - COIN_RADIUS,
                                   x + COIN_RADIUS, y + COIN_RADIUS,
                                   fill=color, outline="dark" + color,
                                   width=3, tags="coin")

                # Highlight selected coin
                if selectedCoin == pos:
                    canvas.create_oval(x - COIN_RADIUS - 5, y - COIN_RADIUS - 5,
                                       x + COIN_RADIUS + 5, y + COIN_RADIUS + 5,
                                       outline="yellow", width=4, tags="selection")

        # Draw preview position
        if previewPosition is not None and board[previewPosition] is None:
            x, y = getCanvasCoords(previewPosition)
            canvas.create_oval(x - COIN_RADIUS, y - COIN_RADIUS,
                               x + COIN_RADIUS, y + COIN_RADIUS,
                               fill="", outline="green", width=3,
                               dash=(5, 5), tags="preview")

    # Redraw canvas after selecting level
    def redrawCanvas():
        canvas.delete("all")
        drawBoard()
        drawCoins()

    # Initialize board and starting position of coins of each player
    def initializeBoard():
        nonlocal board
        board = [None] * 9
        # Human (blue) at P7, P8, P9 (positions 6, 7, 8)
        board[6] = "PLAYER"
        board[7] = "PLAYER"
        board[8] = "PLAYER"
        # Computer (red) at P1, P2, P3 (positions 0, 1, 2)
        board[0] = "COMPUTER"
        board[1] = "COMPUTER"
        board[2] = "COMPUTER"

    # Check for winner
    def checkWinnerOnBoard(test_board):
        for line in WINNING_LINES:
            if (test_board[line[0]] is not None and
                    test_board[line[0]] == test_board[line[1]] == test_board[line[2]]):

                player = test_board[line[0]]

                # RED cannot win on P1-P2-P3 (line [0,1,2])
                if player == "COMPUTER" and line == [0, 1, 2]:
                    continue

                # BLUE cannot win on P7-P8-P9 (line [6,7,8])
                if player == "PLAYER" and line == [6, 7, 8]:
                    continue

                return player

        return None

    # Check the winner
    def checkWinner():
        return checkWinnerOnBoard(board)

    # Announce Winner
    def announceWinner(winner):
        nonlocal gameOver
        gameOver = True

        if winner == "PLAYER":
            text = "PLAYER WINS!"
        else:
            text = "COMPUTER WINS!"

        popup = tk.Toplevel(root)
        popup.title("Game Over")
        tk.Label(popup, text=text, font=("Arial", 18, "bold")).pack(padx=30, pady=20)
        tk.Button(popup, text="Play Again", font=("Arial", 12),
                  command=lambda: [popup.destroy(), resetGame()]).pack(pady=8)
        tk.Button(popup, text="Back to Dashboard", font=("Arial", 12),
                  command=lambda: [popup.destroy(), backCallback()]).pack(pady=8)

    # Set the position from mouse click
    def getPositionFromClick(x, y):
        for pos in range(9):
            cx, cy = getCanvasCoords(pos)
            distance = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if distance <= COIN_RADIUS + 10:
                return pos
        return None

    # Mouse click handling
    def onMouseClick(event):
        nonlocal selectedCoin, previewPosition

        if gameOver or currentPlayer != "PLAYER":
            return

        pos = getPositionFromClick(event.x, event.y)

        if pos is not None and board[pos] == "PLAYER":
            # Select player's coin
            selectedCoin = pos
            previewPosition = None
            redrawCanvas()

    # Keyboard Handling
    def onKeyPress(event):
        nonlocal selectedCoin, previewPosition, currentPlayer

        if gameOver or currentPlayer != "PLAYER" or selectedCoin is None:
            return

        key = event.keysym

        # Arrow key navigation
        if key in ["Up", "Down", "Left", "Right"]:
            handleArrowKey(key)

        # Enter to confirm move
        elif key == "Return":
            if previewPosition is not None and board[previewPosition] is None:
                # Check if move is valid (adjacent)
                if previewPosition in ADJACENCY[selectedCoin]:
                    # Make the move
                    board[previewPosition] = "PLAYER"
                    board[selectedCoin] = None
                    selectedCoin = None
                    previewPosition = None
                    redrawCanvas()

                    # Check for winner
                    winner = checkWinner()
                    if winner:
                        announceWinner(winner)
                        return

                    # Switch to computer
                    currentPlayer = "COMPUTER"
                    root.after(500, computerMove)

    # Arrow key movement of keyboard handling
    def handleArrowKey(key):
        nonlocal previewPosition

        if previewPosition is None:
            previewPosition = selectedCoin

        current_row, current_col = POSITIONS[previewPosition]

        # Calculate new position based on arrow key
        if key == "Up":
            new_row, new_col = current_row - 1, current_col
        elif key == "Down":
            new_row, new_col = current_row + 1, current_col
        elif key == "Left":
            new_row, new_col = current_row, current_col - 1
        elif key == "Right":
            new_row, new_col = current_row, current_col + 1
        else:
            return

        # Find the position index for new coordinates
        for pos, (r, c) in POSITIONS.items():
            if r == new_row and c == new_col:
                # Check if this position is adjacent to selected coin
                if pos in ADJACENCY[selectedCoin]:
                    previewPosition = pos
                    redrawCanvas()
                return

    # Computer Movement
    def computerMove():
        nonlocal currentPlayer

        if gameOver:
            return

        if difficulty == "EASY":
            computerMoveRandom()
        else:
            computerMoveStrategic()

        redrawCanvas()

        # Check for winner
        winner = checkWinner()
        if winner:
            announceWinner(winner)
            return

        currentPlayer = "PLAYER"

    # Computer Random Move - EASY - LEVEL
    def computerMoveRandom():
        # Get all computer coins
        computer_positions = [pos for pos in range(9) if board[pos] == "COMPUTER"]

        # Try each coin until a valid move is found
        random.shuffle(computer_positions)

        for coin_pos in computer_positions:
            # Get adjacent empty positions
            valid_moves = [adj for adj in ADJACENCY[coin_pos] if board[adj] is None]

            if valid_moves:
                # Make random move
                new_pos = random.choice(valid_moves)
                board[new_pos] = "COMPUTER"
                board[coin_pos] = None
                return

    # Validate move of computer - Ensure the move is valid and belongs to computer
    def validateComputerMove(coin_pos, new_pos):
        # Check coin belongs to computer
        if board[coin_pos] != "COMPUTER":
            print(f"ERROR: Position {coin_pos} does not contain COMPUTER coin! Contains: {board[coin_pos]}")
            return False

        # Check new position is empty
        if board[new_pos] is not None:
            print(f"ERROR: Position {new_pos} is not empty! Contains: {board[new_pos]}")
            return False

        # Check positions are adjacent
        if new_pos not in ADJACENCY[coin_pos]:
            print(f"ERROR: Position {new_pos} is not adjacent to {coin_pos}")
            return False

        return True

    # Computer Strategic Move - LEVEL - HARD
    def computerMoveStrategic():
        # 1---> Win if possible
        move = findWinningMove("COMPUTER")
        if move and validateComputerMove(move[0], move[1]):
            board[move[1]] = "COMPUTER"
            board[move[0]] = None
            return

        # 2---> Block player's winning move
        move = findBlockingMove()
        if move and validateComputerMove(move[0], move[1]):
            board[move[1]] = "COMPUTER"
            board[move[0]] = None
            return

        # 3---> Control center position of board
        if board[4] is None:
            computer_positions = [pos for pos in range(9) if board[pos] == "COMPUTER"]
            for coin_pos in computer_positions:
                if 4 in ADJACENCY[coin_pos]:
                    if validateComputerMove(coin_pos, 4):
                        board[4] = "COMPUTER"
                        board[coin_pos] = None
                        return

        # 4---> Give strategic move
        move = findBestStrategicMove()
        if move and validateComputerMove(move[0], move[1]):
            board[move[1]] = "COMPUTER"
            board[move[0]] = None
            return

        # Fallback: Random move
        computerMoveRandom()

    # Check to block the human player -- Find a move to block the player from winning
    def findBlockingMove():
        # Get all computer coins
        computer_positions = [pos for pos in range(9) if board[pos] == "COMPUTER"]

        for coin_pos in computer_positions:
            valid_moves = [adj for adj in ADJACENCY[coin_pos] if board[adj] is None]

            for new_pos in valid_moves:
                # Create a COPY of the board for testing
                test_board = board[:]
                test_board[new_pos] = "COMPUTER"
                test_board[coin_pos] = None

                # Now check if player can win on next move
                player_positions = [pos for pos in range(9) if test_board[pos] == "PLAYER"]

                can_player_win = False
                for player_coin in player_positions:
                    player_valid_moves = [adj for adj in ADJACENCY[player_coin] if test_board[adj] is None]

                    for player_new_pos in player_valid_moves:
                        # Test if player can win
                        test_board2 = test_board[:]
                        test_board2[player_new_pos] = "PLAYER"
                        test_board2[player_coin] = None

                        if checkWinnerOnBoard(test_board2) == "PLAYER":
                            can_player_win = True
                            break

                    if can_player_win:
                        break

                # If this move prevents player from winning, it's a good blocking move
                if not can_player_win:
                    # But first check if player could win before this move
                    original_player_can_win = False
                    for player_coin in player_positions:
                        player_valid_moves = [adj for adj in ADJACENCY[player_coin] if board[adj] is None]

                        for player_new_pos in player_valid_moves:
                            test_board3 = board[:]
                            test_board3[player_new_pos] = "PLAYER"
                            test_board3[player_coin] = None

                            if checkWinnerOnBoard(test_board3) == "PLAYER":
                                original_player_can_win = True
                                break

                        if original_player_can_win:
                            break

                    if original_player_can_win:
                        return (coin_pos, new_pos)

        return None

    # Find the winning move
    def findWinningMove(player):
        positions = [pos for pos in range(9) if board[pos] == player]

        for coin_pos in positions:
            valid_moves = [adj for adj in ADJACENCY[coin_pos] if board[adj] is None]

            for new_pos in valid_moves:
                # Create a COPY of the board for testing
                test_board = board[:]
                test_board[new_pos] = player
                test_board[coin_pos] = None

                # Check if this creates a winning line
                winner = checkWinnerOnBoard(test_board)

                if winner == player:
                    return (coin_pos, new_pos)

        return None

    # Find the best move
    def findBestStrategicMove():
        computer_positions = [pos for pos in range(9) if board[pos] == "COMPUTER"]
        best_score = -1
        best_move = None

        for coin_pos in computer_positions:
            valid_moves = [adj for adj in ADJACENCY[coin_pos] if board[adj] is None]

            for new_pos in valid_moves:
                # Create a COPY of the board for testing
                test_board = board[:]
                test_board[new_pos] = "COMPUTER"
                test_board[coin_pos] = None

                score = evaluatePositionOnBoard(test_board, new_pos, "COMPUTER")

                if score > best_score:
                    best_score = score
                    best_move = (coin_pos, new_pos)

        return best_move

    # Evaluate the position
    def evaluatePositionOnBoard(test_board, pos, player):
        score = 0

        # Check how many winning lines this position is part of
        for line in WINNING_LINES:
            # Skip forbidden winning lines
            if player == "COMPUTER" and line == [0, 1, 2]:
                continue
            if player == "PLAYER" and line == [6, 7, 8]:
                continue

            if pos in line:
                player_count = sum(1 for p in line if test_board[p] == player)
                empty_count = sum(1 for p in line if test_board[p] is None)

                # More coins in a line = better
                if player_count == 2 and empty_count == 1:
                    score += 10
                elif player_count == 1 and empty_count == 2:
                    score += 3

        # Center position
        if pos == 4:
            score += 5

        return score

    # Reset Game
    def resetGame():
        nonlocal board, selectedCoin, previewPosition, currentPlayer, gameOver, playerScoreVal, computerScoreVal
        board = [None] * 9
        selectedCoin = None
        previewPosition = None
        currentPlayer = "PLAYER"
        gameOver = False
        playerScoreVal = 0
        computerScoreVal = 0
        updateScoreLabels()
        canvas.delete("all")
        createLevelButtons()

    # Start Game
    def startGame(level):
        nonlocal difficulty
        try:
            levelFrame.destroy()
        except Exception:
            pass

        difficulty = level
        initializeBoard()
        redrawCanvas()

        # Bind events
        canvas.bind("<Button-1>", onMouseClick)
        root.bind("<KeyPress>", onKeyPress)

    # Create Level Buttons
    def createLevelButtons():
        nonlocal levelFrame
        levelFrame = tk.Frame(root, bg="#FFFFFF")
        levelFrame.place(relx=0.5, rely=0.35, anchor="center")

        tk.Button(levelFrame, text="EASY", font=("Arial", 14, "bold"), width=10,
                  bg="#FFFFFF", command=lambda: startGame("EASY")).pack(side="left", padx=10)
        tk.Button(levelFrame, text="HARD", font=("Arial", 14, "bold"), width=10,
                  bg="#FFFFFF", command=lambda: startGame("HARD")).pack(side="left", padx=10)

    # Initialization of game
    createLevelButtons()
    updateScoreLabels()