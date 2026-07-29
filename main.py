import tkinter as tk
from PIL import Image, ImageTk  # You'll need to install Pillow: pip install Pillow
from common import dashboard, headline, footer, setBackgroundImage

# Dashboard and Main Screen
root = dashboard("#FFFFFF")


def showDashboard():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Set background color
    # createGradient(root, "#e3f2fd", "#90caf9")

    # Set background image
    setBackgroundImage(root, "dashboard.jpg")

    # Headline of the Dashboard
    headline(root, "#FFFFFF")

    # Main container frame to center everything
    mainContainer = tk.Frame(root, bg="#e3f2fd")
    mainContainer.place(relx=0.5, rely=0.5, anchor="center")

    # Frame of the Buttons and Images
    frame = tk.Frame(mainContainer, bg="#e3f2fd")
    frame.pack()

    # Game 01 - Tin Guti
    game01Frame = tk.Frame(frame, bg="#e3f2fd")
    game01Frame.pack(side=tk.LEFT, padx=20)

    try:
        # Load and resize image
        tinGutiImg = Image.open("TinGuti.png")
        tinGutiImg = tinGutiImg.resize((200, 200), Image.Resampling.LANCZOS)
        tinGutiPhoto = ImageTk.PhotoImage(tinGutiImg)

        # Image label
        tinGutiImgLabel = tk.Label(game01Frame, image=tinGutiPhoto, bg="#d3d3d3")
        tinGutiImgLabel.image = tinGutiPhoto  # Keep a reference
        tinGutiImgLabel.pack(pady=10)
    except Exception as e:
        # Fallback if image not found
        tk.Label(game01Frame, text="<image>", font=("Arial", 50), bg="#d3d3d3").pack(pady=10)

    # Button
    game01 = tk.Button(game01Frame, text="Tin Guti", width=15, height=2,
                       font=("Arial", 12, "bold"),
                       command=lambda: playGame("tinGuti"))
    game01.pack(pady=10)

    # Game 02 - Dots and Boxes
    game02Frame = tk.Frame(frame, bg="#e3f2fd")
    game02Frame.pack(side=tk.LEFT, padx=20)

    try:
        # Load and resize image
        dotsBoxesImg = Image.open("DotsNBoxes.png")
        dotsBoxesImg = dotsBoxesImg.resize((200, 200), Image.Resampling.LANCZOS)
        dotsBoxesPhoto = ImageTk.PhotoImage(dotsBoxesImg)

        # Image label
        dotsBoxesImgLabel = tk.Label(game02Frame, image=dotsBoxesPhoto, bg="#d3d3d3")
        dotsBoxesImgLabel.image = dotsBoxesPhoto  # Keep a reference
        dotsBoxesImgLabel.pack(pady=10)
    except Exception as e:
        # Fallback if image not found
        tk.Label(game02Frame, text="<image>", font=("Arial", 50), bg="#d3d3d3").pack(pady=10)

    # Button
    game02 = tk.Button(game02Frame, text="Dots and Boxes", width=15, height=2,
                       font=("Arial", 12, "bold"),
                       command=lambda: playGame("dotNbox"))
    game02.pack(pady=10)

    # Game 03 - Orbit Changer
    game03Frame = tk.Frame(frame, bg="#e3f2fd")
    game03Frame.pack(side=tk.LEFT, padx=20)

    try:
        # Load and resize image
        orbitChangerImg = Image.open("OrbitChanger.png")
        orbitChangerImg = orbitChangerImg.resize((200, 200), Image.Resampling.LANCZOS)
        orbitChangerPhoto = ImageTk.PhotoImage(orbitChangerImg)

        # Image label
        orbitChangerImgLabel = tk.Label(game03Frame, image=orbitChangerPhoto, bg="#e3f2fd")
        orbitChangerImgLabel.image = orbitChangerPhoto  # Keep a reference
        orbitChangerImgLabel.pack(pady=10)
    except Exception as e:
        # Fallback if image not found
        tk.Label(game03Frame, text="<image>", font=("Arial", 50), bg="#e3f2fd").pack(pady=10)

    # Button
    game03 = tk.Button(game03Frame, text="Orbit Changer", width=15, height=2,
                       font=("Arial", 12, "bold"),
                       command=lambda: playGame("orbitChanger"))
    game03.pack(pady=10)

    # Footer text
    footer(root, "#FFFFFF")


# Go to Game Page
def playGame(game_module):
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Import and call the game's show function
    if game_module == "tinGuti":
        import tinGuti
        tinGuti.showGame(root, showDashboard)
    elif game_module == "dotNbox":
        import dotNbox
        dotNbox.showGame(root, showDashboard)
    elif game_module == "orbitChanger":
        import orbitChanger
        orbitChanger.showGame(root, showDashboard)


# Show dashboard initially
showDashboard()

# Run the window and keep it alive for next action
root.mainloop()