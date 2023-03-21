import heapq

class KlotskiState:
    def __init__(self, board):
        self.board = board

    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(tuple(map(tuple, self.board)))
    
    def manhattan_distance(self, goal_state):
        distance = 0

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    row, col = divmod(goal_state.board.index(self.board[i][j]), len(self.board[0]))
                    distance += abs(i - row) + abs(j - col)
        return distance
    
    # Move the empty space in the specified direction
    def move(self, direction, row, col):
        if direction == "up":
            if row > 0 and self.board[row-1][col] == 0:
                self.board[row][col], self.board[row-1][col] = self.board[row-1][col], self.board[row][col]
                self.empty = (row-1, col)
                return True
        elif direction == "down":
            if row < 3 and self.board[row+1][col] == 0:
                self.board[row][col], self.board[row+1][col] = self.board[row+1][col], self.board[row][col]
                self.empty = (row+1, col)
                return True
        elif direction == "left":
            if col > 0 and self.board[row][col-1] == 0:
                self.board[row][col], self.board[row][col-1] = self.board[row][col-1], self.board[row][col]
                self.empty = (row, col-1)
                return True
        elif direction == "right":
            if col < 3 and self.board[row][col+1] == 0:
                self.board[row][col], self.board[row][col+1] = self.board[row][col+1], self.board[row][col]
                self.empty = (row, col+1)
                return True
        return False
    
    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                print(self.board[i][j], end=" ", flush=True)
            print(flush=True)
            
    def is_solved(self):
        return self.board[3][1] == 1 and self.board[3][2] == 1

def get_empty(self, row, col):
    if self.board[row][col] == 0:
        return True
    else:
        return False
# Create the game object
initial_board = [[2, 1, 1, 3],
                 [2, 1, 1, 3],
                 [4, 5, 5, 6],
                 [0, 7, 0, 6]]

game = KlotskiState(initial_board)

# Print the initial board
game.print_board()

# Play the game
while not game.is_solved():
    row=input()
    col=input()
    if get_empty(row,col):
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
        game.print_board()

print("Congratulations, you solved the puzzle!")

def a_star_search(start_state, objective_test, successors, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start_state), start_state))
    explored = set()
    
    while frontier:
        (cost, state) = heapq.heappop(frontier)
        
        if objective_test(state):
            return state
        
        explored.add(state)
        
        for (successor, action_cost) in successors(state):
            if successor not in explored:
                new_cost = cost - heuristic(state) + action_cost + heuristic(successor)
                heapq.heappush(frontier, (new_cost, successor))
                
    return None
