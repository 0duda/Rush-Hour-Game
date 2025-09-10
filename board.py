from copy import deepcopy
import time 
    
class Board:

    def __init__(self, coordinates):       #initialize the board without the cars
        self.board = [
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ]

        self.rows = 6
        self.cols = 6
        self.cost = 0
        self.game_end = False  #game in progress
        self.game_score = 0
        self.coordinates = coordinates    
    
    def initial_board(self):   #initialize the board with the initial coordinates
        for j in self.coordinates:
            for i in self.coordinates[j]:
                x = i[0]
                y = i[1]
                self.board[x][y] = j
        return self.board
    
    def print_board(self):
        for row in self.board:
            print(' '.join(row))

    def movement(self, id_piece, dir): #hipothetical new coordinates
        new_coordinates = []
        if dir == "up":
            for coord in self.coordinates[id_piece]:
                new_x = coord[0] - 1
                new_coordinates.append((new_x,coord[1]))
        if dir == "down":
            for coord in self.coordinates[id_piece]:
                new_x = coord[0] + 1
                new_coordinates.append((new_x,coord[1]))
        if dir == "right":
            for coord in self.coordinates[id_piece]:
                new_y = coord[1] + 1
                new_coordinates.append((coord[0],new_y))
        if dir == "left":
            for coord in self.coordinates[id_piece]:
                new_y = coord[1] - 1
                new_coordinates.append((coord[0],new_y))
        return new_coordinates
    
    def valid_move(self, new_coordinates, dir, id_piece): #evaluate if the move is valid or not
        if len(new_coordinates) == 0:
            return False
        if (dir == "up" or dir == "down") and "N" <= id_piece <= "Z":   #restriction: horizontal cars and vertical cars
            return False
        if (dir == "right" or dir == "left") and "A" <= id_piece <= "M":
            return False
        for coord in new_coordinates:
            if not (0 <= coord[0] < self.rows and 0 <= coord[1] < self.cols):
                return False #out of the board
            
        x1 = new_coordinates[0][0]
        y1 = new_coordinates[0][1]
        x2 = new_coordinates[-1][0]
        y2 = new_coordinates[-1][1]
        if (dir == 'up' or dir == 'left') and self.board[x1][y1] != '0':     #restriction: colisions between cars
            return False
        if (dir == 'down' or dir == 'right') and self.board[x2][y2] != '0' :   
            return False
        return True

    def update_board(self, new_coordinates, id_piece):
        for i in self.coordinates[id_piece]:
            x = i[0]
            y = i[1]
            self.board[x][y] = "0"
        self.coordinates[id_piece] = new_coordinates
        for j in self.coordinates[id_piece]:
            x = j[0]
            y = j[1]
            self.board[x][y] = id_piece
        

    def print_plays(self,path): #print the plays of the search algorithms
        for d in path:
            id_piece = d[0]
            dir = d[1]
            new_coordinates = self.movement(id_piece, dir)
            self.update_board(new_coordinates, id_piece)
            self.print_board()
            print()
            time.sleep(0.1)   #see the plays of the algorithms


    def possible_moves(self):   #possible moves [(id_piece,direction),...]
        possiblemoves = []
        for id_piece in self.coordinates:
            for direction in ['up', 'down', 'left', 'right']:
                new_coordinates = self.movement(id_piece, direction)
                if self.valid_move(new_coordinates,direction, id_piece) == True:
                    possiblemoves.append((id_piece,direction))
        return possiblemoves


    def check_win(self): #car "X" meet winning location?
        if self.board[2][4] == "X" and self.board[2][5] == "X":
            self.game_end = True
        return self.game_end

    def play(self, dir, id_piece):  #user playing
        new_coordinates =  self.movement(id_piece, dir)
        if self.valid_move(new_coordinates, dir, id_piece):
            self.update_board(new_coordinates, id_piece)
            self.check_win()
            self.print_board()
            self.cost += 1
            return (self.cost,'valid')
        else: 
            print("Move not valid, try again!")
            return (self.cost,'not valid')

    def play2(self, dir, id_piece): #bfs, dfs, a*star, greedy playing
        new_coordinates =  self.movement(id_piece, dir)
        self.update_board(new_coordinates, id_piece)

    def hint_board(self,path):  #give board with the hint move
            id_piece = path[0]
            dir = path[1]
            board_hint = deepcopy(self)
            new_coordinates = self.movement(id_piece, dir)
            board_hint.update_board(new_coordinates, id_piece)
            board_hint.print_board()
    
    def toString(self): #allows comparison between boards visited and not visited in the search algorithms
        s = ""
        grid = self.board
        for i in range(6):
            for j in range(6):
                s += "{}".format(grid[i][j])
        return s
    
    def undo_play(self,id_piece,dir):   #play the undo move
        if dir == 'up':
            dir = 'down'
        elif dir == 'down':
            dir = 'up'
        elif dir == 'right':
            dir = 'left'
        else:
            dir = 'right'
        self.play(dir,id_piece)
        return dir
        
    def cars_block_exit(self): #heuristic 1
        initial_score = 100 
        cars_blocking = 0
        col = self.coordinates["X"][-1][1] #how many cars in front of car "x"
        for i in range (col + 1, 6, 1):
            if self.board[2][i] != '0':
                cars_blocking += 1

        score_reduction = cars_blocking * 5 #each blocking car reduces the score in 5 points
        total_score = initial_score - score_reduction
        return total_score
    
    def manhattan_distance(self): #heuristic 2
        initial_score = 100
        col = self.coordinates["X"][-1][1]
        dist = self.cols - col           #how distant is car "X" from the winning location
        score_reduction = dist * 5
        total_score = initial_score - score_reduction
        return total_score
    