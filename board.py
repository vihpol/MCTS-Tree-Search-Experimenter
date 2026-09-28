
import random
import copy
import math
import time
import csv
import os
import argparse

parser = argparse.ArgumentParser()


def checkVariable(board:list[list[str]]):
    if not isinstance(board, list):
        raise TypeError("Board must be a list.")

    if len(board) != 3:
        raise ValueError("Board must contain exactly 3 rows.")

    valid_symbols = {"X", "O", "-"}

    for row in board:
        if not isinstance(row, list):
            raise TypeError("Each row must be a list.")

        if len(row) != 3:
            raise ValueError("Each row must contain exactly 3 elements.")

        for item in row:
            if not isinstance(item, str):
                raise TypeError("Every board element must be a string.")

            if item not in valid_symbols:
                raise ValueError('Board elements must be "X", "O", or "-".')

def TicTacToeboard(board: list[list[str]]):
    checkVariable(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end = " ")
        print()

def isEmpty(board: list[list[str]]):
    empty_positions = []
    checkVariable(board)


    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "-":
                position = (i, j)
                empty_positions.append(position)
    return empty_positions


def placeElement(board: list[list[str]], player):
     checkVariable(board)
     legal_moves = isEmpty(board)
     if not legal_moves:
        raise ValueError("Cannot place an element because the board is full.")
     random_position = random.randint(0, len(legal_moves)-1)
     row, column = legal_moves[random_position]
      
     return row, column

def checkTie(board: list[list[str]]):
    checkVariable(board)
    if ((board[0][0] != '-' 
            and board[0][1] != '-' and  board[0][2] != '-' and board[1][0] != '-'
            and board[1][1] != '-' and board[1][2] != '-' and board[2][0] != '-'
            and board[2][1] != '-' and board[2][2] != '-' )):
        return True
                
            
    return False
def turn(board: list[list[str]]):
    checkVariable(board)
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != "-":
                count += 1
    if count %2  == 0:
        return "X"
    return "O"

def checkWin(board: list[list[str]], player):
       ##check rows
       checkVariable(board)
       if (board[0][0] == player and  board[0][1] == player and  board[0][2] == player):
           return True
       if (board[1][0] == player and  board[1][1] == player and board[1][2] == player): 
           return True
       if (board[2][0] == player and  board[2][1] == player and  board[2][2] == player): 
           return True
       if (board[0][0] == player and board[1][0] == player and  board[2][0] == player): 
           return True
       if (board[0][1] == player and  board[1][1] == player and board[2][1] == player):
           return True
       if (board[0][2] == player and  board[1][2] == player and  board[2][2] == player):
           return True
       if (board[0][0] == player and board[1][1] == player and board[2][2] == player):
           return True
       if (board[0][2] == player and board[1][1] == player and  board[2][0] == player):
           return True
        
       return False; 

board = [["-", "-", "-"], 
         ["-", "-", "-"], 
        ["-", "-", "-"]]
tie_count = 0
x_count = 0
y_count = 0

class Node:
    def __init__(self, board):
        self.board = board
        self.children = []
        self.parent = None
        self.move = None
        self.visits = 0
        self.score = 0
        self.empty_positions = isEmpty(self.board)
    
    def createNewNodes(self):
        copyboard = copy.deepcopy(self.board)
        
        child_node = Node(copyboard)
        child_node.parent = self
        turns = turn(self.board)
        random_position = random.randint(0, len(self.empty_positions)-1)
        row,column =  self.empty_positions[random_position]
        child_node.move = (row,column)
        child_node.board = copyboard
        child_node.board[row][column] = turns
        self.empty_positions.remove((row,column))
        child_node.empty_positions = isEmpty(copyboard)
        
        self.children.append(child_node)

        
        return child_node
    
    def simulation(self, player):
    
        copyboard = copy.deepcopy(self.board) 
    
    
        while True: 
            
            if (checkWin(copyboard, "X") or checkWin(copyboard, "O")) :
                break 
            elif (checkTie(copyboard)):
                break
            current_turn = turn(copyboard)
            row, column = placeElement(copyboard, current_turn)
            copyboard[row][column] = current_turn
            # print(copyboard)  

        if checkWin(copyboard, player):
            return 1
        elif checkTie(copyboard):
            return 0
        else:
            return -1


    def backprop(self, result):
        self.visits += 1
        self.score += result
        
        if self.parent != None:
            self.parent.backprop(result)
        return self
    def ucb1(self, c, mcts_player):
        if self.parent == None:
            return "This is the root"
        if self.visits == 0:
            return float("inf")
        part1 = self.score / self.visits
        thing = (math.log(self.parent.visits))
        quotient = thing / self.visits
        part2 =  c * math.sqrt(quotient)
        
        if turn(self.parent.board) == mcts_player:
            return (part1 + part2)
        return ((-1 * part1) + part2)
    def returnBest(self, mcts_player, c):  
        if len(self.children) > 0:
            results = max(self.children, key=lambda child: child.ucb1(c, mcts_player))
        return results
    def is_leaf(self):
        return len(self.children) == 0
    
    def terminal(self):
        if checkWin(self.board, "X") or checkWin(self.board, "O") or checkTie(self.board):
            return True
        return False



def MCTSsearch(board: list[list[str]], player, simulation_request, c):
    checkVariable(board)
    root = Node(board)
    current = root
    simulation_counter = 0
    while simulation_counter <  simulation_request:
        if current.terminal():
            result = current.simulation(player)
            current.backprop(result)
            simulation_counter += 1
            current = root
            continue
        if current.is_leaf():
            if current.visits == 0:
                result = current.simulation(player)
                
                current.backprop(result)
                simulation_counter += 1
                # print(f"current score: {current.score} ")
            else:
                if len(current.empty_positions) > 0:
                    if not current.terminal():
                        current = current.createNewNodes()
                        result_child = current.simulation(player)
                        current.backprop(result_child)
                        simulation_counter +=1
                        current = root 
        else:
            if len(current.empty_positions) > 0:
                if not current.terminal():
                    current = current.createNewNodes()
                    result_child = current.simulation(player)
                    current.backprop(result_child)
                    simulation_counter +=1
                    current = root
            else:
                current = current.returnBest(player, c)

    # print(f"root visits {root.visits}")
    # print(f"root score {root.score}")
    # print(f"board {root.board}")
    # print(f"simulation {simulation_counter}")
    # print(f"root children: {len(root.children)}")
    # for child in root.children:
    #     print(
    #     "move:", child.move,
    #     "visits:", child.visits,
    #     "score:", child.score,
    #     "children:", len(child.children)
    #     )

    # moves = [child.move for child in root.children]
    # print(moves)
    # print(len(moves), len(set(moves)))

    if len(root.children) == 0:
        return None
    results = max(root.children, key=lambda child: child.visits)
    return results.move
def run_experiment(games, o_simulation, x_simulation, o_c, x_c, mcts_player):
    O_wins = 0
    X_wins = 0
    draws = 0
    finished_games = []

    start_time = time.time()

    for game_number in range(games):
        board = [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"]
        ]

        while True:
            current_player = turn(board)

            if current_player == "X":
                row, column = MCTSsearch(
                    board,
                    "X",
                    x_simulation,
                    x_c
                )
            else:
                row, column = MCTSsearch(
                    board,
                    "O",
                    o_simulation,
                    o_c
                )

            board[row][column] = current_player

            if checkWin(board, current_player):
                if "X" == mcts_player:
                    X_wins += 1
                    result = "MCTS X win"
                else:
                    O_wins += 1
                    result = "MCTS O won"

                finished_games.append({
                    "game": game_number + 1,
                    "result": result,
                    "board": copy.deepcopy(board)
                })

                break

            if checkTie(board):
                draws += 1

                finished_games.append({
                    "game": game_number + 1,
                    "result": "draw",
                    "board": copy.deepcopy(board)
                })

                break

    end_time = time.time()

    return {
        "games": games,
        "x_simulation": x_simulation,
        "o_simulation": o_simulation,
        "x_c": x_c,
        "o_c": o_c,
        "O_wins": O_wins,
        "X_wins": X_wins,
        "draws": draws,
        "runtime_seconds": end_time - start_time,
        "board": finished_games[0]["board"],
        "result": finished_games[0]["result"]
    }

def save_experiment_summary(result, filename="results/results.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fieldnames = [
        "games",
        "x_simulation",
        "o_simulation",
        "x_c",
        "o_c",
        "O_wins",
        "X_wins",
        "draws",
        "runtime_seconds",
        "board",
        "result"
    ]

    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            key: result[key]
            for key in fieldnames
        })
parser.add_argument("--games", type = int)
parser.add_argument("--osimulation", type = int)
parser.add_argument("--xsimulation", type = int)
parser.add_argument("--oc", type = int )
parser.add_argument("--ox", type = int)
parser.add_argument("--mcts_player", type = str)
args = parser.parse_args()

results = run_experiment(args.games, o_simulation = args.osimulation, x_simulation = args.xsimulation, o_c = args.oc, x_c= args.ox,mcts_player= args.mcts_player)
save_experiment_summary(results)

# for simulations in [100, 500, 1000]:
#     for c in [0.5, 1,4, 2.0]:
#         results = run_experiment(100, o_simulation = simulations, x_simulation = simulations, o_c = c, x_c= c,mcts_player= "X")

#         save_experiment_summary(results)

 







 