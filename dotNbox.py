import tkinter as tk
import random
from common import headline, subHeadline, footer, setBackgroundImage


def showGame(root, backCallback):
    root.configure(bg="#FFFFFF")

    # createGradient(root, "#e8f5e9", "#a5d6a7")
    setBackgroundImage(root, "games.jpg")
    headline(root, "#FFFFFF")  # Headline
    subHeadline(root, "Dots and Boxes", "#FFFFFF")  # Subheadline
    footer(root, "#FFFFFF")  # Footer

    # Create a frame for bottom buttons to place them side by side
    buttonFrame = tk.Frame(root, bg="#FFFFFF")
    buttonFrame.pack(side=tk.BOTTOM, pady=20)

    # Instruction text
    instructTxt = (
        "Welcome to Dots and Boxes!\n\n"
        "How to Play:\n"
        "1. Click and drag between adjacent dots to draw a line.\n"
        "2. When you complete a box, you get another turn.\n"
        "3. Player always starts first!\n"
        "4. When all boxes are filled, the winner is displayed."
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
        popup.configure(bg="#E8FFDB")

        label = tk.Label(popup, text="Game Instructions", font=("Arial", 18, "bold"), bg="#E8FFDB")
        label.pack(pady=10)

        text_box = tk.Message(popup, text=instructTxt, font=("Arial", 12), width=480, bg="#E8FFDB")
        text_box.pack(padx=20, pady=10)

        close_btn = tk.Button(popup, text="Close", font=("Arial", 12), command=popup.destroy)
        close_btn.pack(pady=10)

    # Scoreboard
    playerFrame = tk.Frame(root, bg="#FFFFFF")
    playerFrame.place(relx=0.1, rely=0.5, anchor="w")

    playerLabel = tk.Label(playerFrame, text="PLAYER", font=("Arial", 16, "bold"), bg="#FFFFFF")
    playerLabel.pack()  # Middle-Left - Title - Player
    playerScore = tk.Label(playerFrame, text="0", font=("Arial", 20, "bold"), fg="blue", bg="#FFFFFF")
    playerScore.pack()  # Middle-Left - Score - Player

    computerFrame = tk.Frame(root, bg="#FFFFFF")
    computerFrame.place(relx=0.9, rely=0.5, anchor="e")
    computerLabel = tk.Label(computerFrame, text="COMPUTER", font=("Arial", 16, "bold"), bg="#FFFFFF")
    computerLabel.pack()  # Middle-Right - Title - Computer
    computerScore = tk.Label(computerFrame, text="0", font=("Arial", 20, "bold"), fg="red", bg="#FFFFFF")
    computerScore.pack()  # Middle-Right - Score - Computer

    # Canvas of Board
    canvas = tk.Canvas(root, width=500, height=500, bg="white", highlightthickness=2, highlightbackground="black")
    canvas.place(relx=0.5, rely=0.55, anchor="center")

    # Declared Variables
    gridSize = None  # number of dots per row / column
    cellSize = None  # distance between two rows
    dots = {}
    lines = set()
    boxes = {}
    playerScoreVal = 0
    computerScoreVal = 0
    currentPlayer = "PLAYER"
    gameOver = False
    levelFrame = None
    dragStart = None  # stores first dot during click-and-drag
    computerLogic = None

    def updateScoreLabels():
        playerScore.config(text=str(playerScoreVal))
        computerScore.config(text=str(computerScoreVal))

    # Create consistency
    # Draw Line Point A to B
    # Draw Line Point B to A
    def lineKey(point1, point2):
        return tuple(sorted([point1, point2]))

    # Only Horizontal and Vertical drawing is acceptance
    # Eliminate the Diagonal drawing
    def is_adjacent(point1, point2):
        (row1, column1), (row2, column2) = point1, point2
        return abs(row1 - row2) + abs(column1 - column2) == 1

    # Game board according to the selection of Level (4X4 / 5X5 grid)
    def drawDots():
        canvas.delete("all")
        dots.clear()
        start_x = 50
        start_y = 50
        for row in range(gridSize):
            for column in range(gridSize):
                x = start_x + column * cellSize
                y = start_y + row * cellSize
                canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
                dots[(row, column)] = (x, y)

    # Drawing a line from Point1 to Point2
    # According to Player the Line color is different
    def drawLineOnCanvas(point1, point2, player):
        x1, y1 = dots[point1]
        x2, y2 = dots[point2]
        color = "blue" if player == "PLAYER" else "red"
        canvas.create_line(x1, y1, x2, y2, width=3, fill=color)

    def checkForCompletedBoxes(player):
        nonlocal playerScoreVal, computerScoreVal
        scored_any = False
        for row in range(gridSize - 1):
            for column in range(gridSize - 1):
                top = lineKey((row, column), (row, column + 1))
                bottom = lineKey((row + 1, column), (row + 1, column + 1))
                left = lineKey((row, column), (row + 1, column))
                right = lineKey((row, column + 1), (row + 1, column + 1))
                box_key = (row, column)
                # Check already checked or not. If checked then continue
                if box_key in boxes:
                    continue

                if top in lines and bottom in lines and left in lines and right in lines:
                    boxes[box_key] = player
                    # Write first letter of the name of each player
                    x1, y1 = dots[(row, column)]
                    x2, y2 = dots[(row + 1, column + 1)]
                    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                    letter = "P" if player == "PLAYER" else "C"
                    color = "blue" if player == "PLAYER" else "red"
                    canvas.create_text(cx, cy, text=letter, font=("Arial", 20, "bold"), fill=color)
                    if player == "PLAYER":
                        playerScoreVal += 1
                    else:
                        computerScoreVal += 1
                    scored_any = True
        if scored_any:
            updateScoreLabels()
        return scored_any

    # Check the winner who won
    def checkWinner():
        nonlocal gameOver
        if gameOver:
            return
        total_boxes = (gridSize - 1) * (gridSize - 1)
        if len(boxes) == total_boxes:
            gameOver = True
            if playerScoreVal > computerScoreVal:
                text = "PLAYER WINS!"
            elif computerScoreVal > playerScoreVal:
                text = "COMPUTER WINS!"
            else:
                text = "DRAW!"

            popup = tk.Toplevel(root)
            popup.title("Game Over")
            tk.Label(popup, text=text, font=("Arial", 18, "bold")).pack(padx=30, pady=20)
            tk.Button(popup, text="Play Again", font=("Arial", 12),
                      command=lambda: [popup.destroy(), resetGame()]).pack(pady=8)
            tk.Button(popup, text="Back to Dashboard", font=("Arial", 12),
                      command=lambda: [popup.destroy(), backCallback()]).pack(pady=8)

    # Random Computer move for Easy Level
    def computerMove():
        nonlocal currentPlayer
        if gameOver:
            return
        possible = []
        for row in range(gridSize):
            for column in range(gridSize):
                p = (row, column)
                if column + 1 < gridSize:
                    k = lineKey(p, (row, column + 1))
                    if k not in lines:
                        possible.append(k)
                if row + 1 < gridSize:
                    k = lineKey(p, (row + 1, column))
                    if k not in lines:
                        possible.append(k)
        if not possible:
            checkWinner()
            return

        chosen = random.choice(possible)
        lines.add(chosen)
        drawLineOnCanvas(*chosen, "COMPUTER")
        scored = checkForCompletedBoxes("COMPUTER")
        checkWinner()

        if scored:
            root.after(400, computerMove)
        else:
            currentPlayer = "PLAYER"

    # Strategic Computer move for Hard Level
    def computerMoveStrategic():
        nonlocal currentPlayer

        if gameOver:
            return

        completing_moves = []
        safe_moves = []
        risky_moves = []

        # Evaluating the movement of human
        def evaluate_move(move):
            lines.add(move)
            completed = False
            risky = False

            for row in range(gridSize - 1):
                for column in range(gridSize - 1):
                    top = lineKey((row, column), (row, column + 1))
                    bottom = lineKey((row + 1, column), (row + 1, column + 1))
                    left = lineKey((row, column), (row + 1, column))
                    right = lineKey((row, column + 1), (row + 1, column + 1))
                    sides = [top, bottom, left, right]
                    filled = sum(1 for s in sides if s in lines)

                    # If move affects this box
                    if move in sides:
                        if filled == 4:
                            completed = True
                        elif filled == 3:
                            risky = True
            lines.remove(move)
            if completed:
                return +1
            elif risky:
                return -1
            else:
                return 0

        # 1 ---> Collect all possible moves
        possible_moves = []
        for row in range(gridSize):
            for column in range(gridSize):
                p = (row, column)
                if column + 1 < gridSize:
                    k = lineKey(p, (row, column + 1))
                    if k not in lines:
                        possible_moves.append(k)
                if row + 1 < gridSize:
                    k = lineKey(p, (row + 1, column))
                    if k not in lines:
                        possible_moves.append(k)

        # 2---> Classify all the moves
        for move in possible_moves:
            score = evaluate_move(move)
            if score > 0:
                completing_moves.append(move)
            elif score == 0:
                safe_moves.append(move)
            else:
                risky_moves.append(move)

        # 3---> Choose best possible move
        if completing_moves:
            chosen = random.choice(completing_moves)
        elif safe_moves:
            chosen = random.choice(safe_moves)
        else:
            chosen = random.choice(risky_moves)

        # 4 ---> Initiate the move
        lines.add(chosen)
        drawLineOnCanvas(*chosen, "COMPUTER")
        scored = checkForCompletedBoxes("COMPUTER")
        checkWinner()

        if scored:
            root.after(400, computerMoveStrategic)
        else:
            currentPlayer = "PLAYER"

    # Mouse Events creation
    def getNearestDot(x, y, tol=18):
        for (row, column), (dx, dy) in dots.items():
            if abs(x - dx) <= tol and abs(y - dy) <= tol:
                return (row, column)
        return None

    def onPress(event):
        nonlocal dragStart
        dragStart = getNearestDot(event.x, event.y)

    def onRelease(event):
        nonlocal dragStart, currentPlayer
        if not dragStart or currentPlayer != "PLAYER" or gameOver:
            dragStart = None
            return

        endDot = getNearestDot(event.x, event.y)
        if not endDot or endDot == dragStart:
            dragStart = None
            return

        if not is_adjacent(dragStart, endDot):
            dragStart = None
            return

        key = lineKey(dragStart, endDot)
        if key in lines:
            dragStart = None
            return

        lines.add(key)
        drawLineOnCanvas(dragStart, endDot, "PLAYER")
        scored = checkForCompletedBoxes("PLAYER")
        checkWinner()

        if not scored:
            currentPlayer = "COMPUTER"
            root.after(500, computerLogic)

        dragStart = None

    # Reset / Level Setup
    def resetGame():
        nonlocal gridSize, cellSize, lines, boxes, dots, currentPlayer, gameOver, playerScoreVal, computerScoreVal
        lines.clear()
        boxes.clear()
        dots.clear()
        gameOver = False
        currentPlayer = "PLAYER"
        playerScoreVal = 0
        computerScoreVal = 0
        updateScoreLabels()
        createLevelButtons()
        canvas.delete("all")

    def startGame(size):
        nonlocal gridSize, cellSize, computerLogic
        try:
            levelFrame.destroy()
        except Exception:
            pass
        gridSize = size
        cellSize = 130 if size == 4 else 100
        drawDots()
        canvas.bind("<ButtonPress-1>", onPress)
        canvas.bind("<ButtonRelease-1>", onRelease)

        if gridSize == 4:
            computerLogic = computerMove
        else:
            computerLogic = computerMoveStrategic

    def createLevelButtons():
        nonlocal levelFrame
        levelFrame = tk.Frame(root, bg="#FFFFFF")
        levelFrame.place(relx=0.5, rely=0.35, anchor="center")

        tk.Button(levelFrame, text="EASY", font=("Arial", 14, "bold"), width=10,
                  bg="#C6EBC9", command=lambda: startGame(4)).pack(side="left", padx=10)
        tk.Button(levelFrame, text="HARD", font=("Arial", 14, "bold"), width=10,
                  bg="#E0AED0", command=lambda: startGame(5)).pack(side="left", padx=10)

    createLevelButtons()
    updateScoreLabels()