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

### 1. Install the prerequisites

Install Git and Python 3.9 or newer (the Docker image uses Python 3.12).

**Docker Desktop is required for the interactive batch runner described below.** Install it from [Docker Desktop](https://www.docker.com/products/docker-desktop/), open it, and wait for the engine to start. It includes Docker Compose.

Verify both commands work before starting an interactive batch:

```bash
docker info
docker compose version
```

Direct CLI execution runs one experiment locally and does not require Docker.

### 2. Clone this repository

```bash
git clone https://github.com/vihpol/MCTS-Tree-Search-Experimenter.git
cd MCTS-Tree-Search-Experimenter
```

Run all remaining commands from this repository folder.

### 3. Create and activate a Python virtual environment

On macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install the Python dependencies

With the virtual environment activated:

```bash
python -m pip install -r requirements.txt
```

### 5. Start the interactive batch runner

On macOS / Linux:

```bash
python3 board
```

On Windows, use `python board` in the activated virtual environment.

With no arguments, the program displays `MCTS Experiment Simulator` and asks the following questions:

| Prompt | What to enter |
| --- | --- |
| `How many experiments do you want?` | A positive whole number, such as `2`. There is no default. |
| `Number of games [100]:` | Games in this experiment; press Enter for `100`. |
| `X bot:` followed by `1. MCTS`, `2. Random`, and `Choose:` | Enter `1` for MCTS or `2` for Random. |
| `X simulations [500]:` | Only asked for MCTS; press Enter for `500` simulations per move. |
| `X exploration constant [1.4]:` | Only asked for MCTS; press Enter for `1.4`. |
| `O bot:` followed by `1. MCTS`, `2. Random`, and `Choose:` | Enter `1` for MCTS or `2` for Random. |
| `O simulations [500]:` | Only asked for MCTS; press Enter for `500`. |
| `O exploration constant [1.4]:` | Only asked for MCTS; press Enter for `1.4`. |

The games and bot questions repeat for each experiment. Use at least `2` simulations for an MCTS bot so the search can create a child move. Random bots skip the simulation and exploration prompts.

For a small first batch, choose `1` experiment, `10` games, X as `1` (MCTS), `50` X simulations, `1.4` for X's exploration constant, and O as `2` (Random).

After printing each configuration and `Experiments saved!`, the runner automatically:

1. Writes `compose.generated.yaml`.
2. Runs `docker compose -f compose.generated.yaml up --build` to build the local image and run one container per experiment.
3. Combines the per-experiment CSV files into `results/batch_results.csv`.
4. Stops/removes the Compose containers and removes the generated YAML and individual experiment CSV files after a successful merge.

The final success messages are:

```text
Batch finished.
Results saved to results/batch_results.csv
```

### 6. Confirm the CSV was created

On macOS / Linux:

```bash
ls -lh results/*.csv
head -n 3 results/batch_results.csv
```

On Windows (PowerShell):

```powershell
Get-ChildItem .\results\*.csv
Get-Content .\results\batch_results.csv -TotalCount 3
```

Check that `batch_results.csv` appears and contains a header plus experiment data. Each summary row includes `games`, `x_simulation`, `o_simulation`, `x_c`, `o_c`, `O_wins`, `X_wins`, `draws`, `runtime_seconds`, `board`, and `result`. Win/draw counts cover all games in that experiment; `board` and `result` describe only its first game.

A successful batch replaces `batch_results.csv`, so copy it elsewhere before another batch if you want to keep it.

## Direct CLI: Run One Experiment Without Docker

Passing CLI arguments runs **one experiment** with one configuration and the specified number of games. It does not display the interactive prompts or start Docker Compose.

After completing the clone, virtual environment, and dependency steps above, create the output directory and run:

```bash
python -c "from pathlib import Path; Path('results').mkdir(exist_ok=True)"
python board --games 10 --x_type mcts --xsimulations 50 --xc 1.4 --o_type random --osimulations 0 --oc 0 --output single_experiment.csv
```

These commands work in the activated virtual environment on macOS, Linux, and Windows. Supply all the shown flags; the CLI does not provide defaults for them. Bot types are `mcts` or `random`. Use positive game counts and at least `2` simulations for each MCTS bot.

`--output` is a filename inside `results`, so use `single_experiment.csv`, not `results/single_experiment.csv`. The directory must already exist for direct execution. The program appends one summary row per invocation if the output file already exists.

The direct CLI does not print the batch success message. Confirm its output on macOS / Linux with:

```bash
ls -lh results/single_experiment.csv
head -n 3 results/single_experiment.csv
```

Or on Windows (PowerShell):

```powershell
Get-Item .\results\single_experiment.csv
Get-Content .\results\single_experiment.csv -TotalCount 3
```

## Troubleshooting the Interactive Runner

If Docker cannot connect, open Docker Desktop and wait until `docker info` succeeds. If the `docker` command or `docker compose` is unavailable, check the Docker Desktop installation.

If Docker Compose reports a failure, the runner keeps `compose.generated.yaml` for inspection. From the repository folder, use:

```bash
docker compose -f compose.generated.yaml config
docker compose -f compose.generated.yaml up --build
```

The image is built locally from the included `Dockerfile`; you do not need to pull a published `mcts-experiment` image. Once the Docker issue is resolved, run `python3 board` again to use the full batch workflow, including CSV merging and cleanup.
