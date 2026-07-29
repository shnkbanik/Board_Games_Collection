# Board Games Collection

A desktop gaming platform built in Python featuring three original strategy board games, each with a computer opponent powered by rule-based and heuristic AI.

Developed as part of COS60010 Tech Inquiry Project at Swinburne University of Technology, 2025. It is intended for educational purposes and is not affiliated with, nor a reproduction of, any commercial board game.

## About the Project

This project reimagines three classic strategy game concepts as standalone digital games, playable against an AI opponent with two difficulty levels. The goal was to design games from scratch — avoiding copyrighted or commercially available titles — while implementing meaningful AI decision-making rather than simple randomness.

The collection includes:

- **Dots and Boxes** — a classic pen-and-paper game where players draw lines to complete boxes and claim territory.
- **Orbit Changer** — an original 4-in-a-row style game on a 4×4 board, with a twist: sections of the board randomly rotate mid-game, shifting pieces and changing the win outlook. Rotation becomes more likely when a player is close to winning, adding tension and unpredictability.
- **Tin Guti** — a sliding-piece alignment game on a 3×3 connected grid, inspired by traditional three-in-a-row games, where pieces move to adjacent empty spaces rather than being freely placed.

Each game supports **Easy** (random-move AI) and **Hard** (heuristic-driven AI) difficulty levels, along with score tracking, in-game instructions, and a shared dashboard for navigating between games.

## Tech Specification

- **Language:** Python 3.13+
- **GUI Library:** Tkinter
- **Image Handling:** Pillow (PIL)

## Installation and Setup

### Prerequisites

- Python 3.13 or later installed on your system
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
   git clone https://github.com/shnkbanik/Board_Games_Collection.git
   cd Board_Games_Collection
```

2. Install the required dependency:
```bash
   pip install Pillow
```

### Running the Application

Run the main file to launch the dashboard:
```bash
python main.py
```

