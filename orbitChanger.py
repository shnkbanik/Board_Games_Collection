import tkinter as tk
import random
import math
from common import headline, subHeadline, footer, setBackgroundImage


def showGame(root, backCallback):
    # Set background color
    root.configure(bg="#FFFFFF")

    #createGradient(root, "#fff9c4", "#ffeb3b")
    setBackgroundImage(root, "games.jpg")
    # Headline of the Game03 screen
    headline(root, "#FFFFFF")

    # SUB-Headline of the Game03 screen
    subHeadline(root, "Orbit Changer", "#FFFFFF")

    # Footer text
    footer(root, "#FFFFFF")

    # Create a frame for bottom buttons to place them side by side
    buttonFrame = tk.Frame(root, bg="#FFFFFF")
    buttonFrame.pack(side=tk.BOTTOM, pady=20)

    # Instruction Text
    instructTxt = (
        "Welcome to Orbit Changer!\n\n"
        "How to Play:\n"
        "1. Players take turns placing coins on the 4×4 grid.\n"
        "2. From round 2: Optionally move opponent's coin to adjacent empty space.\n"
        "3. Orbits rotate randomly after moves (more likely when close to winning!).\n"
        "4. Get 4 coins in a row to win AFTER rotation (horizontal, vertical, or diagonal).\n"
        "5. Human plays Blue, Computer plays Red."
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
        popup.configure(bg="#fff9c4")

        label = tk.Label(popup, text="Game Instructions", font=("Arial", 18, "bold"), bg="#fff9c4")
        label.pack(pady=10)

        text_box = tk.Message(popup, text=instructTxt, font=("Arial", 12), width=480, bg="#fff9c4")
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

    # Constant variables
    GRID_SIZE = 4
    CELL_SIZE = 80
    COIN_RADIUS = 25
    BOARD_START_X = 100
    BOARD_START_Y = 100

    # All the variables
    playerScoreVal = 0
    computerScoreVal = 0
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    blueCoinsLeft = 8
    redCoinsLeft = 8
    currentPlayer = "PLAYER"
    roundNumber = 0
    draggedCoin = None
    dragStartPos = None
    gameOver = False
    levelFrame = None
    difficulty = None
    playerMovedOpponent = False
    computerMovedOpponent = False

    # Score update of player
    def updateScoreLabels():
        playerScore.config(text=str(playerScoreVal))
        computerScore.config(text=str(computerScoreVal))

    # Draw Board
    def drawBoard():
        for row in range(GRID_SIZE + 1):
            y = BOARD_START_Y + row * CELL_SIZE
            canvas.create_line(BOARD_START_X, y,
                               BOARD_START_X + GRID_SIZE * CELL_SIZE, y,
                               width=2, fill="black")

        for col in range(GRID_SIZE + 1):
            x = BOARD_START_X + col * CELL_SIZE
            canvas.create_line(x, BOARD_START_Y,
                               x, BOARD_START_Y + GRID_SIZE * CELL_SIZE,
                               width=2, fill="black")

    # Draw Blue Coins on Left Side
    def drawBlueCoins():
        start_x = 30
        start_y = 150
        spacing = 45

        for i in range(blueCoinsLeft):
            y = start_y + i * spacing
            canvas.create_oval(start_x - COIN_RADIUS, y - COIN_RADIUS,
                               start_x + COIN_RADIUS, y + COIN_RADIUS,
                               fill="blue", outline="darkblue", width=2, tags="blue_coin")

    # Draw Red Coins on Right Side
    def drawRedCoins():
        start_x = 470
        start_y = 150
        spacing = 45

        for i in range(redCoinsLeft):
            y = start_y + i * spacing
            canvas.create_oval(start_x - COIN_RADIUS, y - COIN_RADIUS,
                               start_x + COIN_RADIUS, y + COIN_RADIUS,
                               fill="red", outline="darkred", width=2, tags="red_coin")

    # Draw Coin on the board
    def drawCoinOnBoard(row, col, color):
        x = BOARD_START_X + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_START_Y + row * CELL_SIZE + CELL_SIZE // 2
        tag = f"board_coin_{row}_{col}"
        canvas.create_oval(x - COIN_RADIUS, y - COIN_RADIUS,
                           x + COIN_RADIUS, y + COIN_RADIUS,
                           fill=color, outline="dark" + color, width=2, tags=tag)

    # Redraw canvas after selecting level
    def redrawCanvas():
        canvas.delete("all")
        drawBoard()
        drawBlueCoins()
        drawRedCoins()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] is not None:
                    drawCoinOnBoard(row, col, board[row][col])

    # Draw the Animation when roation happens
    def drawRotationAnimation(step=0, max_steps=20):
        if step >= max_steps:
            return

        # Clear previous animation elements
        canvas.delete("rotation_animation")

        # Calculate center of board
        center_x = BOARD_START_X + (GRID_SIZE * CELL_SIZE) // 2
        center_y = BOARD_START_Y + (GRID_SIZE * CELL_SIZE) // 2

        # Calculate rotation angle for this step
        angle = (step / max_steps) * 90  # 90 degrees rotation

        # Draw rotating arcs to show rotation direction (counter-clockwise)
        # Outer orbit arc
        outer_radius = GRID_SIZE * CELL_SIZE // 2 + 20
        canvas.create_arc(
            center_x - outer_radius, center_y - outer_radius,
            center_x + outer_radius, center_y + outer_radius,
            start=angle, extent=270, style=tk.ARC,
            width=4, outline="orange", tags="rotation_animation"
        )

        # Inner orbit arc
        inner_radius = CELL_SIZE
        canvas.create_arc(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            start=angle + 45, extent=270, style=tk.ARC,
            width=4, outline="purple", tags="rotation_animation"
        )

        # Draw "ROTATING..." text with fade effect
        alpha_text = "ROTATING..."
        canvas.create_text(
            center_x, center_y - 180,
            text=alpha_text, font=("Arial", 16, "bold"),
            fill="orange", tags="rotation_animation"
        )

        # Draw rotation arrows
        arrow_angle = math.radians(angle)

        # Top arrow
        arrow_x = center_x + outer_radius * math.cos(arrow_angle)
        arrow_y = center_y - outer_radius * math.sin(arrow_angle)
        canvas.create_text(
            arrow_x, arrow_y,
            text="↺", font=("Arial", 24, "bold"),
            fill="orange", tags="rotation_animation"
        )

        root.update()

        # Continue animation
        root.after(30, lambda: drawRotationAnimation(step + 1, max_steps))

    # Get Grid Position from Mouse Coordinates
    def getGridPosition(x, y):
        if (BOARD_START_X <= x <= BOARD_START_X + GRID_SIZE * CELL_SIZE and
                BOARD_START_Y <= y <= BOARD_START_Y + GRID_SIZE * CELL_SIZE):
            col = (x - BOARD_START_X) // CELL_SIZE
            row = (y - BOARD_START_Y) // CELL_SIZE
            return (row, col)
        return None

    # Check if Click is on Blue Coin Stack
    def isOnBlueCoinStack(x, y):
        if blueCoinsLeft > 0:
            start_x = 30
            start_y = 150
            spacing = 45
            for i in range(blueCoinsLeft):
                coin_y = start_y + i * spacing
                if (start_x - COIN_RADIUS <= x <= start_x + COIN_RADIUS and
                        coin_y - COIN_RADIUS <= y <= coin_y + COIN_RADIUS):
                    return True
        return False

    # Check if Click is on Board Coin
    def getBoardCoinAt(x, y):
        gridPos = getGridPosition(x, y)
        if gridPos:
            row, col = gridPos
            if board[row][col] is not None:
                coin_x = BOARD_START_X + col * CELL_SIZE + CELL_SIZE // 2
                coin_y = BOARD_START_Y + row * CELL_SIZE + CELL_SIZE // 2
                distance = ((x - coin_x) ** 2 + (y - coin_y) ** 2) ** 0.5
                if distance <= COIN_RADIUS:
                    return (row, col, board[row][col])
        return None

    # Check if two positions are adjacent
    def isAdjacent(pos1, pos2):
        row1, col1 = pos1
        row2, col2 = pos2
        return abs(row1 - row2) + abs(col1 - col2) == 1

    # Get all possible moves for opponent coins
    def getPossibleOpponentMoves(opponentColor):
        moves = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == opponentColor:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        newRow, newCol = row + dr, col + dc
                        if (0 <= newRow < GRID_SIZE and 0 <= newCol < GRID_SIZE and
                                board[newRow][newCol] is None):
                            moves.append(((row, col), (newRow, newCol)))
        return moves

    # Count same color coins in each direction
    def countInDirection(row, col, color, drow, dcol):
        count = 0
        r, c = row, col
        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == color:
            count += 1
            r += drow
            c += dcol
        return count

    # Evaluate position strength
    def evaluatePosition(row, col, color):
        if board[row][col] is not None:
            return -1000  # Invalid position

        score = 0
        directions = [
            (0, 1),  # Horizontal right
            (1, 0),  # Vertical down
            (1, 1),  # Diagonal down-right
            (1, -1)  # Diagonal down-left
        ]

        for drow, dcol in directions:
            # Count in both directions
            forward = countInDirection(row + drow, col + dcol, color, drow, dcol)
            backward = countInDirection(row - drow, col - dcol, color, -drow, -dcol)
            total = forward + backward + 1  # +1 for the coin we're placing

            if total >= 4:
                score += 1000  # Winning move
            elif total == 3:
                score += 100  # Very good - one away from winning
            elif total == 2:
                score += 10  # Good - building a line
            elif total == 1:
                score += 1  # Okay - starting a line

        return score

    # Find best move for computer - HARD mode
    def findBestMove(color):
        emptySpaces = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] is None:
                    emptySpaces.append((row, col))

        if not emptySpaces:
            return None

        # Evaluate each position
        bestScore = -1
        bestMoves = []

        # 1 ---> Check if computer can win
        for row, col in emptySpaces:
            score = evaluatePosition(row, col, color)
            if score >= 1000:  # Winning move
                return (row, col)

        # 2--->  Check if need to block blue coin
        opponentColor = "blue" if color == "red" else "red"
        for row, col in emptySpaces:
            opponentScore = evaluatePosition(row, col, opponentColor)
            if opponentScore >= 1000:  # Block opponent's winning move
                return (row, col)
            if opponentScore >= 100:  # Block opponent's strong position
                bestMoves.append((row, col))
                continue

        if bestMoves:
            return random.choice(bestMoves)

        # 3 --->  Find best strategic position
        for row, col in emptySpaces:
            score = evaluatePosition(row, col, color)
            if score > bestScore:
                bestScore = score
                bestMoves = [(row, col)]
            elif score == bestScore:
                bestMoves.append((row, col))

        # If multiple equally good moves, pick one randomly
        return random.choice(bestMoves) if bestMoves else random.choice(emptySpaces)

    # --- Find best opponent coin to move (HARD mode) ---
    def findBestOpponentMoveToDisrupt():
        possibleMoves = getPossibleOpponentMoves("blue")

        if not possibleMoves:
            return None

        # Prioritize disrupting opponent's strong positions
        bestScore = -1
        bestMove = None

        for fromPos, toPos in possibleMoves:
            fromRow, fromCol = fromPos

            # Evaluate how strong the opponent's position is
            score = 0
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

            for drow, dcol in directions:
                forward = countInDirection(fromRow + drow, fromCol + dcol, "blue", drow, dcol)
                backward = countInDirection(fromRow - drow, fromCol - dcol, "blue", -drow, -dcol)
                total = forward + backward + 1

                if total >= 3:
                    score += 100  # Disrupt a strong line
                elif total == 2:
                    score += 10

            if score > bestScore:
                bestScore = score
                bestMove = (fromPos, toPos)

        # If no particularly strong position to disrupt, do it randomly 50% of the time
        if bestScore <= 0 and random.random() < 0.5:
            return random.choice(possibleMoves)

        return bestMove

    # Check for Winner
    def checkWinner():
        # Check horizontal
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE - 3):
                if (board[row][col] is not None and
                        board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]):
                    return board[row][col]

        # Check vertical
        for row in range(GRID_SIZE - 3):
            for col in range(GRID_SIZE):
                if (board[row][col] is not None and
                        board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]):
                    return board[row][col]

        # Check diagonal (top-left to bottom-right)
        for row in range(GRID_SIZE - 3):
            for col in range(GRID_SIZE - 3):
                if (board[row][col] is not None and
                        board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][
                            col + 3]):
                    return board[row][col]

        # Check diagonal (top-right to bottom-left)
        for row in range(GRID_SIZE - 3):
            for col in range(3, GRID_SIZE):
                if (board[row][col] is not None and
                        board[row][col] == board[row + 1][col - 1] == board[row + 2][col - 2] == board[row + 3][
                            col - 3]):
                    return board[row][col]

        return None

    # Check for 3 in a row
    def hasThreeInARow():
        # Check horizontal (3 consecutive)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE - 2):
                if (board[row][col] is not None and
                        board[row][col] == board[row][col + 1] == board[row][col + 2]):
                    return True

        # Check vertical (3 consecutive)
        for row in range(GRID_SIZE - 2):
            for col in range(GRID_SIZE):
                if (board[row][col] is not None and
                        board[row][col] == board[row + 1][col] == board[row + 2][col]):
                    return True

        # Check diagonal (3 consecutive)
        for row in range(GRID_SIZE - 2):
            for col in range(GRID_SIZE - 2):
                if (board[row][col] is not None and
                        board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2]):
                    return True

        # Check anti-diagonal (3 consecutive)
        for row in range(GRID_SIZE - 2):
            for col in range(2, GRID_SIZE):
                if (board[row][col] is not None and
                        board[row][col] == board[row + 1][col - 1] == board[row + 2][col - 2]):
                    return True

        return False

    # Announce the Winner
    def announceWinner(winner):
        nonlocal gameOver, playerScoreVal, computerScoreVal
        gameOver = True

        # Update scores based on winner
        if winner == "blue":
            playerScoreVal += 1
            text = "PLAYER WINS!"
        elif winner == "red":
            computerScoreVal += 1
            text = "COMPUTER WINS!"
        else:
            text = "DRAW!"

        # Update score labels immediately
        updateScoreLabels()

        popup = tk.Toplevel(root)
        popup.title("Game Over")
        tk.Label(popup, text=text, font=("Arial", 18, "bold")).pack(padx=30, pady=20)
        tk.Button(popup, text="Play Again", font=("Arial", 12),
                  command=lambda: [popup.destroy(), resetGame()]).pack(pady=8)
        tk.Button(popup, text="Back to Dashboard", font=("Arial", 12),
                  command=lambda: [popup.destroy(), backCallback()]).pack(pady=8)

    # Rotate Inner Orbit by Counter-Clockwise
    def rotateInnerOrbit():
        temp = board[1][1]
        board[1][1] = board[1][2]
        board[1][2] = board[2][2]
        board[2][2] = board[2][1]
        board[2][1] = temp

    # Rotate Outer Orbit by Counter-Clockwise ---
    def rotateOuterOrbit():
        positions = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 3), (2, 3),
            (3, 3), (3, 2), (3, 1), (3, 0),
            (2, 0), (1, 0)
        ]

        temp = board[positions[0][0]][positions[0][1]]

        for i in range(len(positions) - 1):
            curr_row, curr_col = positions[i]
            next_row, next_col = positions[i + 1]
            board[curr_row][curr_col] = board[next_row][next_col]

        last_row, last_col = positions[-1]
        board[last_row][last_col] = temp

    # Perform the Random Rotation
    def performRotation(callback=None):
        # Start animation
        drawRotationAnimation()

        # Wait for animation to complete, perform actual rotation
        def completeRotation():
            # Clear animation
            canvas.delete("rotation_animation")

            # 50% chance to rotate inner orbit
            if random.random() < 0.5:
                rotateInnerOrbit()

            # 50% chance to rotate outer orbit
            if random.random() < 0.5:
                rotateOuterOrbit()

            redrawCanvas()
            root.update()

            if callback:
                root.after(100, callback)

        # Animation rotate
        root.after(650, completeRotation)  # Increased to 650ms to ensure animation completes

    # Perform 10 Rotations with winner check after EACH rotation
    def perform10Rotations(count=0):
        if count >= 10:
            announceWinner("draw")
            return

        # Show which rotation number
        canvas.delete("rotation_count")
        center_x = BOARD_START_X + (GRID_SIZE * CELL_SIZE) // 2
        center_y = BOARD_START_Y + (GRID_SIZE * CELL_SIZE) // 2
        canvas.create_text(
            center_x, center_y + 180,
            text=f"Rotation {count + 1} of 10",
            font=("Arial", 14, "bold"),
            fill="darkblue", tags="rotation_count"
        )
        root.update()

        def afterRotation():
            canvas.delete("rotation_count")
            canvas.delete("rotation_animation")  # Ensure animation is cleared
            winner = checkWinner()
            if winner:
                announceWinner(winner)
                return

            # Continue to next rotation after 3 seconds
            root.after(3000, lambda: perform10Rotations(count + 1))

        performRotation(callback=afterRotation)

    # Check if Board is Full
    def isBoardFull():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] is None:
                    return False
        return True

    # Decide if Rotation need to happen
    def shouldRotate():
        if roundNumber <= 1:
            return False

        if hasThreeInARow():
            return random.random() < 0.8
        else:
            return random.random() < 0.3

    # Mouse Event for drag and drop
    def onPress(event):
        nonlocal draggedCoin, dragStartPos, playerMovedOpponent

        if gameOver or currentPlayer != "PLAYER":
            return

        if isOnBlueCoinStack(event.x, event.y) and blueCoinsLeft > 0:
            draggedCoin = {"type": "new", "color": "blue"}
            dragStartPos = None
            return

        boardCoin = getBoardCoinAt(event.x, event.y)
        if boardCoin and roundNumber > 1 and not playerMovedOpponent:
            row, col, color = boardCoin
            if color == "red":
                draggedCoin = {"type": "move", "color": "red", "from": (row, col)}
                dragStartPos = (row, col)
            return

    def onRelease(event):
        nonlocal draggedCoin, dragStartPos, blueCoinsLeft, currentPlayer, roundNumber, playerMovedOpponent

        if not draggedCoin or gameOver or currentPlayer != "PLAYER":
            draggedCoin = None
            dragStartPos = None
            return

        gridPos = getGridPosition(event.x, event.y)

        if not gridPos:
            draggedCoin = None
            dragStartPos = None
            return

        row, col = gridPos

        if board[row][col] is not None:
            draggedCoin = None
            dragStartPos = None
            return

        if draggedCoin["type"] == "new":
            board[row][col] = "blue"
            blueCoinsLeft -= 1
            roundNumber += 1
            playerMovedOpponent = False
            redrawCanvas()

            if shouldRotate():
                root.after(500, lambda: performRotation(
                    callback=lambda: checkAfterRotation("PLAYER")
                ))
            else:
                winner = checkWinner()
                if winner:
                    announceWinner(winner)
                elif isBoardFull():
                    perform10Rotations()
                else:
                    currentPlayer = "COMPUTER"
                    root.after(500, computerMove)

        elif draggedCoin["type"] == "move":
            fromRow, fromCol = draggedCoin["from"]
            if isAdjacent((fromRow, fromCol), (row, col)):
                board[fromRow][fromCol] = None
                board[row][col] = "red"
                playerMovedOpponent = True
                redrawCanvas()

        draggedCoin = None
        dragStartPos = None

    # Check winner after the  Rotation
    def checkAfterRotation(lastPlayer):
        nonlocal currentPlayer

        # Clear any remaining animation
        canvas.delete("rotation_animation")

        winner = checkWinner()
        if winner:
            announceWinner(winner)
            return

        if isBoardFull():
            perform10Rotations()
            return

        if lastPlayer == "PLAYER":
            currentPlayer = "COMPUTER"
            root.after(500, computerMove)
        else:
            currentPlayer = "PLAYER"

    # Computer Move - EASY - HARD
    def computerMove():
        nonlocal currentPlayer, redCoinsLeft, roundNumber, computerMovedOpponent

        if gameOver:
            return

        computerMovedOpponent = False

        # 1 ----> Optionally move blue coin
        if roundNumber > 1:
            if difficulty == "EASY":
                # EASY---> Random chance to move Blue coin
                possibleMoves = getPossibleOpponentMoves("blue")
                if possibleMoves and random.random() < 0.3:
                    fromPos, toPos = random.choice(possibleMoves)
                    fromRow, fromCol = fromPos
                    toRow, toCol = toPos

                    board[fromRow][fromCol] = None
                    board[toRow][toCol] = "blue"
                    computerMovedOpponent = True
                    redrawCanvas()
                    root.after(400, lambda: computerMoveContinue())
                    return
            else:
                # HARD----> Strategic blue coin movement
                bestMove = findBestOpponentMoveToDisrupt()
                if bestMove:
                    fromPos, toPos = bestMove
                    fromRow, fromCol = fromPos
                    toRow, toCol = toPos

                    board[fromRow][fromCol] = None
                    board[toRow][toCol] = "blue"
                    computerMovedOpponent = True
                    redrawCanvas()
                    root.after(400, lambda: computerMoveContinue())
                    return

        computerMoveContinue()

    def computerMoveContinue():
        nonlocal currentPlayer, redCoinsLeft, roundNumber, computerMovedOpponent

        # 2 ----> Place computer red coin on board
        emptySpaces = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] is None:
                    emptySpaces.append((row, col))

        if emptySpaces and redCoinsLeft > 0:
            if difficulty == "EASY":
                # EASY: Random placement
                row, col = random.choice(emptySpaces)
            else:
                # HARD: Strategic placement
                bestMove = findBestMove("red")
                if bestMove:
                    row, col = bestMove
                else:
                    row, col = random.choice(emptySpaces)

            board[row][col] = "red"
            redCoinsLeft -= 1
            roundNumber += 1
            computerMovedOpponent = False
            redrawCanvas()

            if shouldRotate():
                root.after(500, lambda: performRotation(
                    callback=lambda: checkAfterRotation("COMPUTER")
                ))
            else:
                winner = checkWinner()
                if winner:
                    announceWinner(winner)
                elif isBoardFull():
                    perform10Rotations()
                else:
                    currentPlayer = "PLAYER"

    # Reset Game
    def resetGame():
        nonlocal board, blueCoinsLeft, redCoinsLeft, currentPlayer, roundNumber, gameOver, draggedCoin, dragStartPos, playerMovedOpponent, computerMovedOpponent, playerScoreVal, computerScoreVal
        board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        blueCoinsLeft = 8
        redCoinsLeft = 8
        currentPlayer = "PLAYER"
        roundNumber = 0
        gameOver = False
        draggedCoin = None
        dragStartPos = None
        playerMovedOpponent = False
        computerMovedOpponent = False
        playerScoreVal = 0
        computerScoreVal = 0
        updateScoreLabels()
        canvas.delete("all")
        createLevelButtons()

    # Start Gamm
    def startGame(level):
        nonlocal difficulty
        try:
            levelFrame.destroy()
        except Exception:
            pass

        difficulty = level
        drawBoard()
        drawBlueCoins()
        drawRedCoins()
        canvas.bind("<ButtonPress-1>", onPress)
        canvas.bind("<ButtonRelease-1>", onRelease)

    # Set the level button
    def createLevelButtons():
        nonlocal levelFrame
        levelFrame = tk.Frame(root, bg="#FFFFFF")
        levelFrame.place(relx=0.5, rely=0.35, anchor="center")

        tk.Button(levelFrame, text="EASY", font=("Arial", 14, "bold"), width=10,
                  bg="#C6EBC9", command=lambda: startGame("EASY")).pack(side="left", padx=10)
        tk.Button(levelFrame, text="HARD", font=("Arial", 14, "bold"), width=10,
                  bg="#E0AED0", command=lambda: startGame("HARD")).pack(side="left", padx=10)

    # Reset Scores
    def resetScores():
        nonlocal playerScoreVal, computerScoreVal
        playerScoreVal = 0
        computerScoreVal = 0
        updateScoreLabels()
        resetGame()

    # --- Initialize ---
    createLevelButtons()
    updateScoreLabels()