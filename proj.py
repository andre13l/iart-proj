import heapq
from copy import deepcopy
class KlotskiState:
    def __init__(self, board, move_history=[]):
        self.board = deepcopy(board)
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
    
    def is_solved(self):
        return self.board[3][1] == 1 and self.board[3][2] == 1
    
    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                print(self.board[i][j], end=" ", flush=True)
            print(flush=True)
            
    def manhattan_distance(self, goal_state):
        distance = 0

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    row, col = divmod(goal_state.board.index(self.board[i][j]), len(self.board[0]))
                    distance += abs(i - row) + abs(j - col)
        return distance
    
    def children(self):
        # returns the possible moves
        functions = [self.up, self.down, self.left, self.right]

        children = []
        for func in functions:
            child = func()
            if child:
                children.append(child)

        return children
    
    # Move the empty space in the specified direction
    def move(self, direction, row, col):

        state = KlotskiState(self.board, self.move_history)
        if direction == "up":
            return self.up(row, col)
        elif direction == "down":
            return self.down(row, col)
        elif direction == "left":
            return self.left(row, col)
        elif direction == "right":
            return self.right(row, col)
        return False
        
    def up(self, row, col):
        # moves the blank upwards
        if row == 0:
            return False 
        else:
            self.board[row][col] = self.board[row - 1][col]
            self.board[row - 1][col] = 0
            self.print_board()
            return True

    def down(self, row, col):
        # moves the blank downwards
        if row == len(self.board) - 1:
            return False
        else:
            self.board[row][col] = self.board[row + 1][col]
            self.board[row + 1][col] = 0
            self.print_board()
            return True

    def left(self, row, col):
        # moves the blank left
        if col == 0:
            return False
        else:
            self.board[row][col] = self.board[row][col - 1]
            self.board[row][col - 1] = 0
            self.print_board()
            return True

    def right(self, row, col):
        # moves the blank right
        if col == len(self.board[0]) - 1:
            return False
        else:
            self.board[row][col] = self.board[row][col + 1]
            self.board[row][col + 1] = 0
            self.print_board()
            return True

def print_sequence(sequence):
    print("Steps:", len(sequence) - 1)
    # prints the sequence of states
    for state in sequence:
        for row in state:
            print(row)
        print()

def a_star_search(start_state, objective_test, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state), start_state))
    explored = set()
    
    while frontier:
        (cost, state) = heapq.heappop(frontier)
        
        if objective_test(state):
            return state.move_history
        
        explored.add(state)
        
        for successor in start_state.children():
            if successor not in explored:
                heapq.heappush(frontier, (cost + heuristic(successor), successor))  
    return None

def solve_klotski(start_board):
    start_state = KlotskiState(start_board)

    def objective_test(state):
        return state.is_solved()

    '''def successors(state):
        successors = []
        empty_row, empty_col = state.get_empty()

        # Try to move the block above the empty space down
        if empty_row > 0 and state.board[empty_row - 1][empty_col] != 0:
            new_state = KlotskiState([row[:] for row in state.board])
            new_state.move(up, empty_row, empty_col)
            successors.append((new_state, 1))

        # Try to move the block below the empty space up
        if empty_row < 3 and state.board[empty_row + 1][empty_col] != 0:
            new_state = KlotskiState([row[:] for row in state.board])
            new_state.move(down, empty_row, empty_col)
            successors.append((new_state, 1))

        # Try to move the block to the left of the empty space right
        if empty_col > 0 and state.board[empty_row][empty_col - 1] != 0:
            new_state = KlotskiState([row[:] for row in state.board])
            new_state.move(left, empty_row, empty_col)
            successors.append((new_state, 1))

        # Try to move the block to the right of the empty space left
        if empty_col < 3 and state.board[empty_row][empty_col + 1] != 0:
            new_state = KlotskiState([row[:] for row in state.board])
            new_state.move(right, empty_row, empty_col)
            successors.append((new_state, 1))

        return successors'''


    def heuristic(state):
        return state.manhattan_distance(KlotskiState([[2, 5, 5, 3], [2, 0, 0, 3], [4, 1, 1, 6], [7, 1, 1, 6]]))

    print_sequence(a_star_search(start_state, objective_test, heuristic))
    

      
# Create the game object
initial_board = [[2, 1, 1, 3],
                 [2, 1, 1, 3],
                 [4, 5, 5, 6],
                 [0, 7, 0, 6]]

game = KlotskiState(initial_board)

# Print the initial board
game.print_board()

option = input("1- Player or 2- Computer: \n")

if(option=="1"):
    # Play the game
    while not game.is_solved():
        row=int(input("Enter row index: "))
        col=int(input("Enter col index: "))
        print("("+ str(row) + ","+ str(col) + ")")
        if game.is_empty(row,col):
            
            move = input("Enter move (up/down/left/right): ")
            if move == "up":
                if not game.move("up", row, col):
                    print("Invalid move!")
            elif move == "down":
                if not game.move("down", row, col):
                    print("Invalid move!")
            elif move == "left":
                if not game.move("left", row, col):
                    print("Invalid move!")
            elif move == "right":
                if not game.move("right", row, col):
                    print("Invalid move!")
            else:
                print("Invalid move!")
            
        else: print("Invalid index!")

    print("Congratulations, you solved the puzzle!")

elif(option=="2"):
    solve_klotski(initial_board)

else: print("Invalid Input")
