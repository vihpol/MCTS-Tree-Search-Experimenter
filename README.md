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
MCTS vs MCTS
MCTS vs Random
Random vs MCTS

## Instructions for Use

### 1. Install Docker Desktop

Download and install Docker Desktop:

https://www.docker.com/products/docker-desktop/

Make sure Docker Desktop is running before starting the program.

You can verify Docker is running with:

```bash
docker info
```

### 2. Clone the repository
```bash
 git clone <your-repository-url>
 cd <repository-folder>
```

### 3.  Create a Python virtual environment
```bash
python3 -m venv .venv
```

### .macOS / Linux
```bash
source .venv/bin/activate
```

### Windows
```bash
.venv\Scripts\activate
```

### 4. Install the Python dependencies
```bash
pip install -r requirements.txt
```

### 5. Run it on the terminal
```bash
python3 board
```

```text
