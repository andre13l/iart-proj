import heapq
import time
import psutil
from copy import deepcopy
from collections import deque
import os
class KlotskiState:
    def __init__(self, board, move_history=[], cost=0):
        self.board = deepcopy(board)
        self.empty = self.get_empty()
        self.cost = cost
        # create an empty array and append move_history
        self.move_history = [] + move_history + [self.board]

    def __eq__(self, other):
        return self.board == other.board
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def __hash__(self):
        return hash(tuple(map(tuple, self.board)))

    def is_empty(self, row, col):
        if self.board[row][col] == 0:
            return True
        else:
            return False
        
    def get_empty(self):
        count = 0
        empty1 = 0 
        empty2 = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0 and count==0:
                    empty1 = (i, j)
                    count+=1
                elif self.board[i][j] == 0:
                    empty2 = (i, j)
        empty = [empty1, empty2]
        return empty
    
    def is_solved(self):
        return self.board[4][1] == 1 and self.board[4][2] == 1
            
    def manhattan_distance(self, goal_state):
        distance = 0
        flat_goal_board = [val for sublist in goal_state.board for val in sublist]
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    #print(f'i->{i}, j-> {j}\n')
                    #print(f'atual state: {self.board}, goal state: {goal_state.board}')
                    # Use the index function on the flattened lists
                    index = flat_goal_board.index(self.board[i][j])
                    row, col = divmod(index, len(self.board[0]))
                    distance += abs(i - row) + abs(j - col)
                    #print(row, col)
                    #print(distance)
        return distance
    
f = open("output.txt", "w")

# Define function to check if the move is valid
def is_valid_move(board, piece_positions, direction):
    row, col = piece_positions[0]
    row_delta, col_delta = direction
    
    # Check if the move is within the board boundaries
    if not (0 <= row + row_delta < len(board) and 0 <= col + col_delta < len(board[0])):
        return False
    
    # Check if the destination cell is empty or has the same piece as the moving one
    if board[row + row_delta][col + col_delta] not in [0, board[row][col]]:
        return False
    
    # Check if there are any obstacles in the way
    for r, c in piece_positions:
        if board[r + row_delta][c + col_delta] != 0 and (r + row_delta, c + col_delta) not in piece_positions:
            return False
    
    return True


# Define function to move the selected piece in the specified direction
def move_piece(board, piece, direction):
    pieces = []
    
    # Find the positions of the pieces to move
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == piece:
                pieces.append((i, j))

    # Check if the move is valid
    if not is_valid_move(board, pieces, direction):
        return board

    # Move the piece to the new position
    new_board = [row[:] for row in board]
    row_delta, col_delta = direction
    for r, c in sorted(pieces, reverse=True):
        if new_board[r + row_delta][c + col_delta] == 0:
            new_board[r][c] = 0
            new_board[r + row_delta][c + col_delta] = piece
            if r-row_delta>=0 and r-row_delta<len(board) and c-col_delta>=0 and c-col_delta<len(board[r]) and new_board[r - row_delta][c - col_delta] == piece:
                new_board[r][c] = piece
                new_board[r - row_delta][c - col_delta] = 0 
            #print("|"+ str(r) +","+ str(c) + "|\n" + "|"+ str(row_delta) +","+ str(col_delta) + "|\n")

    return new_board

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end=" ", flush=True)
        print(flush=True)

def successors(state):
    for i in range(len(state.board)):
        for j in range(len(state.board[0])):
            if state.board[i][j] != 0:
                for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if is_valid_move(state.board, [(i, j)], d):
                        new_board = move_piece(state.board, state.board[i][j], d)
                        #print_board(new_board)
                        yield (KlotskiState(new_board, state.move_history, cost=1), 1)

def a_star_search(start_state, goal_state, objective_test, successors, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state, goal_state), start_state))
    explored = set()
    #print_board(start_state.board)
    while frontier:
        (cost, state) = heapq.heappop(frontier)
        
        if objective_test(state):
            f.write("\nPuzzle Solved!\n")
            return state.move_history
        
        explored.add(state)
        
        for (successor, action_cost) in successors(state):
            if successor not in explored:
                new_cost = cost - heuristic(state, goal_state) + action_cost + heuristic(successor, goal_state)
                heapq.heappush(frontier, (new_cost, successor)) 

    f.write("No solution found!!")
    return None

def a_star_solve(start_state, goal_state):
    return a_star_search(start_state, goal_state, KlotskiState.is_solved, successors, KlotskiState.manhattan_distance)
def bfs(start_state, objective_test, successors, depth_limit=None):
    frontier = []
    heapq.heappush(frontier, start_state)
    explored = set()
    
    start_state.depth = 0
    
    while frontier:
        state = heapq.heappop(frontier)
        
        if objective_test(state):
            f.write("\nPuzzle Solved!\n")
            return state.move_history
        
        explored.add(state)
        
        if depth_limit is None or state.depth <= depth_limit:
            for (successor, _) in successors(state):
                successor.depth = state.depth + 1
                if successor not in explored:
                    heapq.heappush(frontier, successor) 

    f.write("No solution found!!") 
    return None
    

def bfs_solve(start_state):
    return bfs(start_state, KlotskiState.is_solved, successors, 13)

def dfs(start_state, objective_test, successors, depth_limit):
    frontier = [(start_state, 0)]
    explored = set()

    while frontier:
        state, depth = frontier.pop()

        if depth > depth_limit:
            continue

        if objective_test(state):
            f.write("\nPuzzle Solved!\n")
            return state.move_history
        
        explored.add(state)
        
        successors_list = list(successors(state))
        successors_list.reverse()

        for (successor, _) in successors_list:
            if successor not in explored:
                frontier.append((successor, depth + 1))

    f.write("No solution found!!") 
    return None


def dfs_solve(start_state):
    return dfs(start_state, KlotskiState.is_solved,successors, 20)

# Create the game object
initial_board1 = [[4, 9, 8, 5],
                 [6, 11, 10, 7],
                 [2, 0, 12, 3],
                 [0, 1, 1, 3], 
                 [14, 1, 1, 13]]
initial_board2 = [[4, 9, 8, 5],
                 [6, 11, 10, 7],
                 [2, 1, 1, 3],
                 [12, 1, 1, 3], 
                 [14, 0, 0, 13]]
initial_board3 = [[4, 9, 8, 5],
                 [6, 11, 10, 7],
                 [1, 1, 12, 3],
                 [1, 1, 0, 3], 
                 [14, 2, 0, 13]]
initial_board4 = [[2, 7, 7, 8],
                 [2, 1, 1, 8],
                 [3, 1, 1, 9],
                 [3, 5, 6, 9], 
                 [4, 0, 0, 10]]

os.system('cls' if os.name == 'nt' else 'clear')     # limpar a tela
print("\n\n##########################################################\n")
print("\n##---------------------KLOTSKI GAME---------------------##\n")
print("\n##########################################################\n\n")
print(" MENU INICIAL: Digite o NIVEL de jogo desejado\n\n")
print("\t(1) Nivel 1\n")
print("\t(2) Nivel 2\n")
print("\t(3) Nivel 3\n")
print("\t(4) Nivel 4\n\n")
print("\t(5) Sair\n\n")

board_choice = input()
if(board_choice=="1"):
    initial_board=initial_board1
    goal_state = [[4, 9, 8, 5],
                 [6, 11, 10, 7],
                 [2, 0, 12, 3],
                 [0, 1, 1, 3], 
                 [14, 1, 1, 13]]
elif(board_choice=="2"):
    initial_board=initial_board2
    goal_state = [[4, 9, 8, 5],
                 [6, 11, 10, 7],
                 [2, 0, 0, 3],
                 [12, 1, 1, 3], 
                 [14, 1, 1, 13]]   
elif(board_choice=="3"):
    initial_board=initial_board3
    goal_state=[[4, 9, 8, 5],
                 [6, 11, 10, 7],
                 [14, 0, 0, 3],
                 [2, 1, 1, 3], 
                 [12, 1, 1, 13]]
elif(board_choice=="4"):
    initial_board=initial_board4  
    goal_state = [[3, 2, 9, 8],
                 [3, 2, 9, 8],
                 [7, 7, 4, 6],
                 [10, 1, 1, 0], 
                 [5, 1, 1, 0]]
elif(board_choice=="5"):
    exit()       
else:
    print("invalid board choice!!!\n")

game = KlotskiState(initial_board)
os.system('cls' if os.name == 'nt' else 'clear')     # limpar a tela

print("\n\n##########################################################\n")
print("\n##---------------------KLOTSKI GAME---------------------##\n")
print("\n##########################################################\n\n")
print(" MENU INICIAL: Digite o MODO de jogo desejado\n\n")
print("\t(1) Player Mode\n")
print("\t(2) Computer Mode | A* search |\n")
print("\t(3) Computer Mode | BFS search |\n")
print("\t(4) Computer Mode | DFS search |\n\n")
print("\t(5) Sair\n\n")
# Processar a opção escolhida     
option = input()

if(option=="1"):
    # Play the game
    while not game.is_solved():
        print_board(game.board)
        # Get input from the user for the piece to move
        selected_piece = int(input("Enter the number of the piece to move: "))
        
        # Get input from the user for the direction to move the piece
        direction = input("Enter the direction to move the piece (up, down, left, right): ")
        if direction == "up":
            direction = (-1, 0)
        elif direction == "down":
            direction = (1, 0)
        elif direction == "left":
            direction = (0, -1)
        elif direction == "right":
            direction = (0, 1)
        else:
            print("Invalid direction!")
            continue
        
        # Move the piece in the specified direction
        new_board = move_piece(game.board, selected_piece, direction)
        
        # Update the board
        game.board = new_board

    print("\nCongratulations, you solved the puzzle!\n")

elif(option=="2"):
    
    game_final = KlotskiState(goal_state)
    solution = a_star_solve(game, game_final)
    if(solution!=None):
        memory_used = psutil.Process().memory_info().rss / 1024 / 1024  # in MB
        for state in solution:
            for row in state:
                f.write(str(row))
                f.write("\n")
            f.write("\n")
        
        f.write("Number of moves: " + str(len(solution)-1) + "\n")
        f.write("Memory used: " + str(memory_used) + " MB\n")
        f.write("Time spent: " +  str(time.process_time()) + " seconds\n")

elif(option=="3"):

    solution = bfs_solve(game)
    if(solution!=None):
        memory_used = psutil.Process().memory_info().rss / 1024 / 1024  # in MB
        for state in solution:
            for row in state:
                f.write(str(row))
                f.write("\n")
            f.write("\n")
        
        f.write("Number of moves: " + str(len(solution)-1) + "\n")
        f.write("Memory used: " + str(memory_used) + " MB\n")
        f.write("Time spent: " +  str(time.process_time()) + " seconds\n")

elif(option=="4"):
   
    solution = dfs_solve(game)
    if(solution!=None):
        memory_used = psutil.Process().memory_info().rss / 1024 / 1024  # in MB
        for state in solution:
            for row in state:
                f.write(str(row))
                f.write("\n")
            f.write("\n")
        
        f.write("Number of moves: " + str(len(solution)-1) + "\n")
        f.write("Memory used: " + str(memory_used) + " MB\n")
        f.write("Time spent: " +  str(time.process_time()) + " seconds\n")

elif(option==5): exit() 
else: print("Invalid Input")

f.close()
