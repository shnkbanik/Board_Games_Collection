import subprocess
import sys
import tkinter as tk

# Dashboard and Main Screen
def dashboard (bg):
    root = tk.Tk()
    root.title("RiotStudio Games - TIP_C03_Team1")
    root.geometry("1000x820")
    root.configure(bg=bg)
    root.resizable(False, False)
    return root

# Headline of the Dashboard
def headline (root, bg):
    line = tk.Label(root,
                    text = "RiotStudio Games",
                    font= ("Arial" , 20, "bold"),
                    bg=bg)
    line.pack(pady = 20)
    return headline

# SUB_Headline of the Dashboard
def subHeadline (root , title , bg):
    line = tk.Label(root,
                    text = title,
                    font= ("Arial" , 15, "bold"),
                    bg=bg)
    line.pack(pady = 20)
    return subHeadline


# Footer text
def footer (root, bg):
    line = tk.Label(root,
                    text= "Developed by TIP_C03_Team1",
                    font= ("Arial" , 12),
                    bg=bg)
    line.pack(side = tk.BOTTOM, pady=20) # Alignment of the footer
    return footer

# Go Back button of each game page
def goBack(root, bg, backCallback):
    gobackBtn = tk.Button(root,
                           text="Back to Dashboard",
                           font=("Arial", 12),
                           bg=bg,
                           command=backCallback)
    gobackBtn.pack(side=tk.BOTTOM, pady=20)
    return gobackBtn

# Instruction button of each game page
def instructBtn (root, instructTxt, bg_clr="#d3d3d3"):
    def showInstruct():
        popup = tk.Toplevel(root)
        popup.title("Game Instructions")
        popup.geometry("500x400")
        popup.configure(bg=bg_clr)

        label = tk.Label(popup, text="Game Instructions", font=("Arial", 18, "bold"), bg=bg_clr)
        label.pack(pady=10)

        text_box = tk.Message(popup, text=instructTxt, font=("Arial", 12), width=480, bg=bg_clr)
        text_box.pack(padx=20, pady=10)

        close_btn = tk.Button(popup, text="Close", font=("Arial", 12), command=popup.destroy)
        close_btn.pack(pady=10)

    btn = tk.Button(root, text="Instruction", font=("Arial", 12), bg=bg_clr, command=showInstruct)
    btn.pack(side=tk.BOTTOM, pady=20, padx=10)  # Changed: removed pady=70, added padx=10
    return btn

# Background Image
def setBackgroundImage(root, image_path):
    try:
        from PIL import Image, ImageTk

        # Load and resize image to fit window
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1000, 820), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label to hold the image
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        return bg_label
    except Exception as e:
        print(f"Error loading background image: {e}")
        # Fallback to solid color if image not found
        root.configure(bg="#d3d3d3")
        return None