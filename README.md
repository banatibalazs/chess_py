# Chess Game

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/release/python-380/)
[![Tkinter](https://img.shields.io/badge/Tkinter-8.6-blue)](https://docs.python.org/3/library/tkinter.html)
[![Pillow](https://img.shields.io/badge/Pillow-10.4.0-blue)](https://python-pillow.org/)
[![NumPy](https://img.shields.io/badge/NumPy-2.0.1-blue)](https://numpy.org/)


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

### Possible outcomes:
- **Checkmate**: The game ends when a player's king is in checkmate.
- **Resignation**: A player can resign at any time to end the game.
- **Time Expiration**: The game ends when a player's time runs out.
- **Stalemate**: The game ends when a player's king is not in check, but the player has no legal moves.
- **Threefold Repetition**: The game ends in a draw when the same position occurs three times with the same player to move.
- **Insufficient Material**: The game ends in a draw when neither player has sufficient material to checkmate the opponent.


## Demo Images
 
<p>
<img src="/resources/demo_images/main_menu.png" alt="Main Menu" height="200"/>
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

### UML Diagram

The UML diagram was generated using `pyreverse` and Graphviz.

```sh
cd src
pyreverse -o png -p chess_game .
```

UML is in the `documentation/uml` folder.

## Possible Improvements (for the Future)
   
- **Database Integration**: Add database integration to store game data, player statistics, etc.
- **Alpha-Beta Pruning**: Implement the Alpha-Beta pruning strategy for the AI player.
- **Game Analysis**: Add game analysis features such as move suggestions, game evaluation, etc.
- **Refactoring**: Refactor the codebase to improve readability and maintainability.
- **Themes**: Add different themes for the game board and pieces.
- **Sound Effects**: Add sound effects for different game events.
- **Unit Tests**: Add unit tests to ensure the correctness of the game logic.
- **Documentation**: Add detailed documentation for the project.
- **Online Multiplayer**: Implement online multiplayer support.
