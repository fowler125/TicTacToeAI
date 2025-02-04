# Tic-Tac-Toe AI

## Overview
Tic-Tac-Toe AI is a Python-based game that allows players to compete against an AI opponent using different algorithms. The game features a graphical user interface (GUI) built with `pygame`, and three AI strategies:

- **Minimax Algorithm**: A perfect strategy that ensures the best possible move.
- **Monte Carlo Tree Search (MCTS)**: A probabilistic decision-making AI.
- **Random AI**: Selects moves randomly.

## Features
- Play Tic-Tac-Toe against three different AI strategies.
- Interactive GUI using `pygame`.
- Supports player vs AI gameplay.
- AI difficulty varies based on the chosen algorithm.

## Installation
### Prerequisites
Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/).

### Clone the Repository
```bash
git clone https://github.com/fowler125/TicTacToeAI.git
cd TicTacToeAI
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## How to Run the Game
Run the following command to start the game:
```bash
python main.py
```
![image](https://github.com/user-attachments/assets/6d27b014-7363-473e-9c3f-99901642b46c)

## How It Works
1. The game launches a Tic-Tac-Toe board.
2. Players select an AI opponent (Minimax, MCTS, or Random AI).
3. The game proceeds with player vs AI moves.
4. The game ends when there is a winner or a draw.

## AI Strategies
### Minimax Algorithm
- Evaluates all possible moves.
- Uses recursion to determine the best possible outcome.
- Ensures optimal play.

### Monte Carlo Tree Search (MCTS)
- Simulates multiple random plays.
- Uses statistics to determine the best move.
- Balances exploration and exploitation.

### Random AI
- Chooses moves at random.
- Provides an easy difficulty setting.

## Future Improvements
- Implement a neural network-based AI.
- Add multiplayer mode (online or local).
- Improve UI with animations and sound effects.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any inquiries or support, feel free to reach out via GitHub issues.

---
Enjoy playing Tic-Tac-Toe with AI! 🎮

