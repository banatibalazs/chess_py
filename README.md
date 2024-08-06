# Chess Game

This project is a chess game implemented in Python using the Tkinter library for the graphical user interface (GUI). The game supports different types of players, including human players and AI players with various strategies.

## Features

- **Human vs Human**: Two human players can play against each other.
- **Human vs AI**: A human player can play against an AI player.
- **AI vs AI**: Two AI players can play against each other.
- **AI Strategies**: The AI players can use different strategies such as Random, Greedy and Alpha-Beta pruning (in process).
- **Timer**: Optional timer for each player.
- **Game Saving**: The game state can be saved and loaded.
- **Move History**: Keeps track of the move history.
- **GUI**: Interactive GUI using Tkinter.

## Demo

### Main Menu
<img src="/resources/demo_images/main_menu.png" alt="Main Menu" height="200"/>

### Game Board

<p>
<img src="/resources/demo_images/starting.png" alt="Special Moves" width="200"/>
<img src="/resources/demo_images/king_in_check.png" alt="Main Menu" width="200"/>
</p>

### Special Moves

<p>
<img src="/resources/demo_images/castling.png" alt="Special Moves" width="200"/>
<img src="/resources/demo_images/en_passant.png" alt="Special Moves" width="200"/>
<img src="/resources/demo_images/pawn_promotion.png" alt="Special Moves" width="200"/>
</p>

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/chess-game.git
    cd chess-game
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the main script to start the game:
```sh
python src/main.py
```

## Project Structure

```plaintext
Chess Game Project
├── README.md
├── requirements.txt
└── src
    ├── controller
    │   └── (game logic and controllers)
    ├── model
    │   ├── pieces
    │   │   └── (different chess pieces, e.g., Pawn, Rook, Knight, etc.)
    │   └── (data models for the game)
    ├── view
    │   └── (GUI components)
    └── main.py (entry point of the application)
```
