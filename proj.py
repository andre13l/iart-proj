import heapq
from copy import deepcopy
class KlotskiState:
    def __init__(self, board, move_history=[]):
        self.board = board
        self.empty = self.get_empty()
        # create an empty array and append move_history
        self.move_history = [] + move_history + [self.board]

    def __eq__(self, other):
        return self.board == other.board
    
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
        return self.board[3][1] == 1 and self.board[3][2] == 1
            
    def manhattan_distance(self, goal_state):
        distance = 0

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    row, col = divmod(goal_state.board.index(self.board[i][j]), len(self.board[0]))
                    distance += abs(i - row) + abs(j - col)
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
        print("Invalid move!")
        return board

    # Move the piece to the new position
    new_board = [row[:] for row in board]
    row_delta, col_delta = direction
    for r, c in sorted(pieces, reverse=True):
        if new_board[r + row_delta][c + col_delta] == 0:
            new_board[r][c] = 0
            new_board[r + row_delta][c + col_delta] = piece
            #print("|"+ str(r) +","+ str(c) + "|\n" + "|"+ str(row_delta) +","+ str(col_delta) + "|")
            if r-row_delta>=0 and r-row_delta<len(board) and c-col_delta>=0 and c-col_delta<len(board) and new_board[r - row_delta][c - col_delta] == piece:
                new_board[r][c] = piece
                new_board[r - row_delta][c - col_delta] = 0 
            
    return new_board

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end=" ", flush=True)
        print(flush=True)
        
def print_sequence(sequence):
    print("Steps:", len(sequence) - 1)
    # prints the sequence of states
    for state in sequence:
        for row in state:
            print(row)
        print()

def a_star_search(start_state, goal_state, objective_test, successors, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state, goal_state), start_state))
    explored = set()
    
    while frontier:
        (cost, state) = heapq.heappop(frontier)
        
        if objective_test(state):
            return state.move_history
        
        explored.add(state)
        
        for (successor, action_cost) in successors(state):
            if successor not in explored:
                new_cost = cost - heuristic(state, goal_state) + action_cost + heuristic(successor, goal_state)
                heapq.heappush(frontier, (new_cost, successor)) 
    return None

def successors(state):
        for i in range(len(state.board)):
            for j in range(len(state.board[0])):
                if state.board[i][j] != 0:
                    for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        if is_valid_move(state.board, [(i, j)], d):
                            new_board = move_piece(state.board, state.board[i][j], d)
                            yield (KlotskiState(new_board, state.move_history), 1)

def solve_klotski(start_state, goal_state):
    return a_star_search(start_state, goal_state, KlotskiState.is_solved, successors, KlotskiState.manhattan_distance)
    

      
# Create the game object
initial_board = [[2, 1, 1, 3],
                 [2, 1, 1, 3],
                 [4, 5, 5, 6],
                 [0, 7, 0, 6]]

game = KlotskiState(initial_board)

option = input("1- Player or 2- Computer: \n")

if(option=="1"):
    # Play the game
    while not game.is_solved():
        print_board(initial_board)
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
        new_board = move_piece(initial_board, selected_piece, direction)
        
        # Update the board
        initial_board = new_board

    print("Congratulations, you solved the puzzle!")

elif(option=="2"):
    goal_state = [[4, 5, 5, 3],
                 [7, 0, 0, 3],
                 [6, 1, 1, 2],
                 [6, 1, 1, 2]]
    solution = solve_klotski(initial_board, goal_state)
    print_sequence(solution)

else: print("Invalid Input")
