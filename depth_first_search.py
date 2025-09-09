from copy import deepcopy 
from board import Board 
from datetime import datetime

 

def solve_game_dfs(initial_game_state):
    visited_states = []    #states already visited
    queue = []   
    path = []              #states to explore
    start_time = datetime.now()
    
    #priority queue with the path of a specific state and a list with the states already visited
    queue.append((initial_game_state, path))      
    visited_states.append(initial_game_state)

    while queue:        #queue not empty
        current_game_state, current_path = queue.pop(0)   #pop first tuple out

        #game finished
        if current_game_state.check_win() == True:
            end_time = datetime.now()
            time = end_time - start_time 
            return (current_path,time)
        
        for c in current_game_state.possible_moves():
                id_piece = c[0]
                dir = c[1]
                new_game_state = deepcopy(current_game_state)
                new_game_state.play2(dir, id_piece)

    
                if new_game_state.toString() not in visited_states:
                    visited_states.append(new_game_state.toString())
                    new_path = current_path + [(id_piece,dir)]
                    queue.insert(0,(new_game_state, new_path))

    #no path found
    return None

