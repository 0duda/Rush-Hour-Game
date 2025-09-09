from board import Board
from breadth_first_search import solve_game_bfs
from depth_first_search import solve_game_dfs
from a_star import solve_game_astar
from greedy import solve_game_greedy
from levels import *
from copy import deepcopy
from datetime import datetime
 

def start():
    print("Hello!\n")
    print("Welcome to the terminal version of the Rush Hour Game!\n")
    print("You can start with an easy difficulty or challenge yourself and choose medium or difficult levels.\n")
    print("Rules: To win the game the car X has to meet the end of his row. You can't move a car to a position occupied or out of the board.")
    print("       Vertical cars only move up and down, horizontal cars only move right and left.\n")

    start = input("Are you ready for the challenge? (yes/no) ")
    while start not in ['YES','yes','NO','no','quit']:
        print("I didn't understand, try again!")
        start = input("Ready to start the game? (yes/no) ")

    if start in ['yes', 'YES']:
        menu()
    if start in ['no','NO','quit']:
        print("Ok, hope I see you soon!")
        quit()

def menu():
    difficulty = input ("Choose the difficulty: (easy/medium/difficult) ")
    while difficulty not in ["EASY","easy","Easy","MEDIUM","medium","Medium","Difficult","DIFFICULT","difficult"]:
        print("I didn't understand, try again!")
        difficulty = input ("Choose the difficulty: (easy/medium/difficult) ")
    level = input("Choose the level: (1/2/3/4) ")
    while level not in ["1","2","3","4"]:
        print("I didn't understand, try again!")
        level = input("Choose the level: (1/2/3/4) ")
        
    if difficulty in ["EASY","easy","Easy"]:
        game(int(level))
    if difficulty in ["MEDIUM","medium","Medium"]:
        game(4 + int(level))
    if difficulty in ["Difficult","DIFFICULT","difficult"]:
        game(8 + int(level))

def game(level):
    level = int(level)
    game_levels = deepcopy(levels[level-1])
    board = Board(game_levels)
    board.initial_board()
    player = input("Who is playing? (Player/PC) ")
    while player not in ["Player","player","PLAYER","PC","pc","Pc"]:
        print("I didn't understand, try again!")
        player = input("Who is playing? (Player/PC) ")
    print()
    if player in ['PC','pc','Pc']:
        pc(board,level)
    else:
        playing(board,level)

def pc(board,level):
        player = input("Choose PC with... (BFS/DFS/A*STAR1/A*STAR2/GREEDY1/GREEDY2) ")
        while player not in ['bfs','BFS','Bfs','dfs','DFS','Dfs','A*STAR1','a*star1','A*star1','greedy1','GREEDY1','Greedy1','A*STAR2','a*star2','A*star2','greedy2','GREEDY2','Greedy2']:
            print("I didn't understand, try again!")
            player = input("PC with: (BFS/DFS/A*STAR/GREEDY) ")
        print()
        board.print_board()
        print()
        if player in ['bfs','BFS','Bfs']:
            path,time = solve_game_bfs(board)
        elif player in ['dfs','DFS','Dfs']:
            path,time = solve_game_dfs(board)
        elif player in ['A*STAR1','a*star1','A*star1']:
            path,time = solve_game_astar(board,1)
        elif player in ['A*STAR2','a*star2','A*star2']:
            path,time = solve_game_astar(board,2)
        elif player in ['greedy1','GREEDY1','Greedy1']:
            path,time = solve_game_greedy(board,1)
        else:
            path,time = solve_game_greedy(board,2)
        board.print_plays(path)
        print("Game solved in",len(path),"movements and in this time",time,"!\n")
        end_level(level)

def playing(board,level):
        print("Type 'menu' to return to the menu")
        print("Type 'restart' to restart the game")
        print("Type 'quit' to quit the game\n")
        cost = 0
        board.print_board()
        print()
        path,time = solve_game_bfs(board)
        id_piece2 = 'n'
        dir2 = 'n'
        start_time = datetime.now()
        while board.check_win() == False:
            id_piece = input("Choose the car you want to move, ask for a hint or undo previous move: (Ex.: A/hint/undo) ")
            if id_piece in ['menu','MENU','Menu']:
                menu()
            if id_piece in ['quit','QUIT','quit']:
                print("Ok, hope I see you soon!")
                quit()
            if id_piece in ['hint','HINT','Hint']:
                hint(board, level)
            elif id_piece in ['undo','UNDO','Undo']:
                if id_piece2 == 'n':
                    print("You haven't made a move yet!")
                else: 
                    dir2 = board.undo_play(id_piece2,dir2)
            elif id_piece in ['restart','Restart','RESTART']:
                game(level)
            else: 
                dir = input("In what direction? (up/down/right/left) ")
                while dir not in ['up','down','right','left']:
                    print("I didn't understand, try again!")
                    dir = input("In what direction? (up/down/right/left) ")                
                cost,value = board.play(dir, id_piece.upper())
                if value == 'valid':
                    id_piece2 = id_piece.upper()
                    dir2 = dir
        end_time = datetime.now()
        time = end_time - start_time
        if len(path) >= cost:
            print("Good, you won the game in",cost,"movements and in this time",time,"!")
        else:
            print("Good, you won the game in",cost,"movements but you could have done it in",len(path),"! You took this time",time,".")
        end_level(level)

def end_level(level):
        next = input("Next level? (yes/no) ")
        while next not in ["yes", "YES", "Yes", "NO", "No", "no"]:
            print("I didn't understand, try again!")
            next = input("Next level? (yes/no) ")
        if next in ["yes", "YES","Yes"]:
            print()
            if level == 12:
                print("There's no more levels, you'll return to the menu.")
                print()
                menu()
            game(level + 1)
        next = input("Menu or quit? (menu/quit) ")
        while next not in ["MENU", "Menu","menu","quit", "QUIT", "quit", "Quit"]:
            print("I didn't understand, try again!")
            next = input("Menu or quit? (menu/quit) ")
        if next in ["MENU", "Menu","menu"]:
            print()
            menu()
        else:
            print("Ok, hope I see you soon!")
            quit()
        
def hint(board,level):
    path,time = solve_game_bfs(board) #the algorithm bfs is one of the algorithms with the best performance
    path = path[0]
    print("Hint:")
    board.hint_board(path)
    print(path)
    print()
           

start()
    
        
    