import heapq

class KlotskiState:
    def __init__(self, board, move_history=[]):
        self.board = board
        (self.blank_row, self.blank_col) = self.get_empty()
        # create an empty array and append move_history
        self.move_history = [] + move_history + [self.board]

    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(tuple(map(tuple, self.board)))
    
    def get_empty(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)

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
    
    
    # Move the empty space in the specified direction func
    def move(self, func, row, col):
        # decorator function to add to history everytime a move is made
        # functions with @move will apply this decorator
        def wrapper(self):
            state = KlotskiState(self.board, self.move_history)
            value = func(state, row, col)
            if value:
                return state
            else:
                return None
            
        return wrapper
    
    @move
    def up(self, row, col):
        # moves the blank upwards
        if self.blank_row == 0:
            return False
        else:
            self.board[row][col], self.board[row-1][col] = self.board[row-1][col], self.board[row][col]
            self.blank_row -= 1
            return True

    @move
    def down(self, row, col):
        # moves the blank downwards
        if row < 3 and self.board[row][col] == 0:
            self.board[row][col], self.board[row+1][col] = self.board[row+1][col], self.board[row][col]
            self.blank_row += 1
            return True

    @move
    def left(self, row, col):
        # moves the blank left
        if col > 0 and self.board[row][col] == 0:
            self.board[row][col], self.board[row][col-1] = self.board[row][col-1], self.board[row][col]
            self.blank_col -= 1
            return True

    @move
    def right(self, row, col):
        # moves the blank right
        if col < 3 and self.board[row][col] == 0:
            self.board[row][col], self.board[row][col+1] = self.board[row][col+1], self.board[row][col]
            self.blank_col += 1
            return True
        
    

def print_sequence(sequence):
    print("Steps:", len(sequence) - 1)
    # prints the sequence of states
    for state in sequence:
        for row in state:
            print(row)
        print()

def a_star_search(start_state, objective_test, successors, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state), start_state))
    explored = set()
    
    while frontier:
        (cost, state) = heapq.heappop(frontier)
        
        if objective_test(state):
            return state.move_history
        
        explored.add(state)
        
        for (successor, action_cost) in successors(state):
            if successor not in explored:
                new_cost = cost - heuristic(state) + action_cost + heuristic(successor)
                heapq.heappush(frontier, (new_cost, successor))
                
    return None

def solve_klotski(start_board):
    start_state = KlotskiState(start_board)

    def objective_test(state):
        return state.is_solved()

    def successors(state):
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

        return successors

    def heuristic(state):
        return state.manhattan_distance(KlotskiState([[2, 5, 5, 3], [2, 0, 0, 3], [4, 1, 1, 6], [7, 1, 1, 6]]))

    solved_state = print_sequence(a_star_search(start_state, objective_test, successors, heuristic))
    
    if solved_state:
        print("Solution:")
        solved_state.print_board()
    else:
        print("No solution found.")

      
# Create the game object
initial_board = [[2, 1, 1, 3],
                 [2, 1, 1, 3],
                 [4, 5, 5, 6],
                 [0, 7, 0, 6]]

game = KlotskiState(initial_board)

# Print the initial board
game.print_board()

option = int(input("1- Player or 2- Computer: \n"))

if(option==1):
    # Play the game
    while not game.is_solved():
        row=int(input())
        col=int(input())
        print("("+ str(row) + ","+ str(col) + ")")
        if game.is_empty(row,col):
            move = input("Enter move (up/down/left/right): ")
            if move == "up":
                if not game.move(up, row, col):
                    print("Invalid move!")
            elif move == "down":
                if not game.move(down, row, col):
                    print("Invalid move!")
            elif move == "left":
                if not game.move(left, row, col):
                    print("Invalid move!")
            elif move == "right":
                if not game.move(right, row, col):
                    print("Invalid move!")
            else:
                print("Invalid move!")
            game.print_board()
        else: print("Invalid index!")

    print("Congratulations, you solved the puzzle!")

elif(option==2):
    solve_klotski(initial_board)

else: print("Invalid Input")
