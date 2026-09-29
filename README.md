# MCTS Tic-Tac-Toe Experiment Runner

A configurable Monte Carlo Tree Search (MCTS) framework for Tic-Tac-Toe that supports:

- MCTS vs MCTS
- MCTS vs Random
- Random vs MCTS
- Configurable simulation counts
- Configurable UCB exploration constants
- Batch experiments
- Parallel execution using Docker Compose
- CSV result logging
- Interactive command-line configuration

This project aims not just to build a Tic-Tac-Toe bot, but to create a small experimentation framework for testing how different MCTS configurations affect performance.

---

## Features

### Monte Carlo Tree Search

The MCTS implementation is built from scratch and includes:

- Selection using UCB1
- Expansion
- Random simulation/rollout
- Backpropagation
- Configurable exploration constant `C`
- Configurable simulation budget

At the end of a search, the move with the most visits is selected.

---

## Experiment Modes

The experiment runner supports:

```text
MCTS vs MCTS
MCTS vs Random
Random vs MCTS
