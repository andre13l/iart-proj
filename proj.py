import heapq
import time
import psutil
from copy import deepcopy
from collections import deque
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
        # Flatten the self.board and goal_state.board temporarily
        flat_board = [val for sublist in self.board for val in sublist]
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

def print_sequence(sequence):
    # prints the sequence of states
    for state in sequence:
        for row in state:
            print(row)
        print()

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
            print("\nPuzzle Solved!\n")
            return state.move_history
        
        explored.add(state)
        
        for (successor, action_cost) in successors(state):
            if successor not in explored:
                new_cost = cost - heuristic(state, goal_state) + action_cost + heuristic(successor, goal_state)
                heapq.heappush(frontier, (new_cost, successor)) 

    print("No solution found!!")
    return None

def a_star_solve(start_state, goal_state):
    return a_star_search(start_state, goal_state, KlotskiState.is_solved, successors, KlotskiState.manhattan_distance)
def bfs(start_state, objective_test, successors):
    frontier = []
    heapq.heappush(frontier, start_state)
    explored = set()
    #print_board(start_state.board)
    while frontier:
        state = heapq.heappop(frontier)
        
        if objective_test(state):
            print("\nPuzzle Solved!\n")
            return state.move_history
        
        explored.add(state)
        
        for (successor,_) in successors(state):
            if successor not in explored:
                heapq.heappush(frontier, successor) 

    print("No solution found!!")
    return None
    

def bfs_solve(start_state):
    return bfs(start_state, KlotskiState.is_solved, successors)

def dfs(start_state, objective_test, successors):
    frontier = []
    frontier.append(start_state)
    explored = set()
    #print_board(start_state.board)
    while frontier:
        state = frontier.pop()
        
        if objective_test(state):
            print("\nPuzzle Solved!\n")
            return state.move_history
        
        explored.add(state)
        
        for (successor,_) in successors(state)[::-1]:
            if successor not in explored:
                frontier.append(successor) 

    print("No solution found!!")
    return None

def dfs_solve(start_state):
    return dfs(start_state, KlotskiState.is_solved,successors)
# Create the game object
initial_board = [[4, 9, 8, 5],
                 [6, 1, 1, 7],
                 [2, 1, 1, 3],
                 [14, 10, 11, 3], 
                 [12, 0, 0, 13]]

game = KlotskiState(initial_board)

option = input("1-Player \n2-A* \n3-BFS \n4-DFS \n")

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
    goal_state = [
                [2, 6, 7, 3],
                [14, 4, 5, 3],
                [10, 0, 0, 11],
                [12, 1, 1, 13], 
                [8, 1, 1, 9]]
    
    game_final = KlotskiState(goal_state)
    solution = a_star_solve(game, game_final)
    if(solution!=None):
        memory_used = psutil.Process().memory_info().rss / 1024 / 1024  # in MB
        print_sequence(solution)
        print("Number of moves", len(solution)-1)
        print("Memory used:", memory_used, "MB")
        print("Time spent:", time.process_time(), "seconds")

elif(option=="3"):
   
    solution = bfs_solve(game)
    if(solution!=None):
        memory_used = psutil.Process().memory_info().rss / 1024 / 1024  # in MB
        print_sequence(solution)
        print("Number of moves", len(solution)-1)
        print("Memory used:", memory_used, "MB")
        print("Time spent:", time.process_time(), "seconds")

elif(option=="4"):
   
    solution = dfs_solve(game)
    if(solution!=None):
        memory_used = psutil.Process().memory_info().rss / 1024 / 1024  # in MB
        print_sequence(solution)
        print("Number of moves", len(solution)-1)
        print("Memory used:", memory_used, "MB")
        print("Time spent:", time.process_time(), "seconds")
else: print("Invalid Input")
