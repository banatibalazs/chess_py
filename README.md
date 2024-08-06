# Chess Game

This project is a chess game implemented in Python using the Tkinter library for the graphical user interface (GUI). The game supports different types of players, including human players and AI players with various strategies.

## Features

- **Human vs Human**: Two human players can play against each other.
- **Human vs AI**: A human player can play against an AI player.
- **AI vs AI**: Two AI players can play against each other.
- **AI Strategies**: The AI players can use different strategies such as Random, Greedy, Minimax, and Alpha-Beta pruning.
- **Timer**: Optional timer for each player.
- **Game Saving**: The game state can be saved and loaded.
- **Move History**: Keeps track of the move history.
- **GUI**: Interactive GUI using Tkinter.

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

- `src/controller/`: Contains the game logic and controllers.
- `src/model/`: Contains the data models for the game.
- `src/view/`: Contains the GUI components.
- `src/main.py`: The entry point of the application.

## Key Classes

### `Game`
Manages the overall game logic, including player turns, move validation, and game state updates.

### `Player`
Represents a player in the game. There are different subclasses for human players and AI players with different strategies.

### `ChessGui`
Handles the graphical user interface using Tkinter.

### `GuiController`
Acts as a bridge between the game logic and the GUI, updating the GUI based on the game state.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

