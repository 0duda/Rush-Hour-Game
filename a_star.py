from copy import deepcopy
from board import Board
from datetime import datetime

def solve_game_astar(initial_game_state, heuristic):
    #priority queue with the cost and path of a specific state and a list with the states already visited
    queue = []
    visited_states = []
    path = []
    start_time = datetime.now()  #note the time
    #cost = heuristic value + cost of the previous moves
    #heuristic 1: cars_block exit; heuristic 2: manhattan_distance
    if heuristic == 1:
        cost = initial_game_state.cars_block_exit() + initial_game_state.cost
    elif heuristic ==2:
         cost = initial_game_state.manhattan_distance() + initial_game_state.cost
    queue.append((cost, initial_game_state, path))
    visited_states.append(initial_game_state)
    while queue:
        queue.sort(key=lambda x: x[0])
        #get the node with the lowest total cost from the queue
        cost, current_game_state, current_path = queue.pop(0)

        #game finished
        if current_game_state.check_win() == True:
            end_time = datetime.now()
            time = end_time - start_time #period of time 
            return (current_path,time)
        
        for c in current_game_state.possible_moves():
                id_piece = c[0]
                dir = c[1]
                new_game_state = deepcopy(current_game_state)
                new_game_state.play2(dir, id_piece)
    

                if new_game_state.toString() not in visited_states:
                    visited_states.append(new_game_state.toString())
                    new_path = current_path + [(id_piece,dir)]
                    queue.append((cost + 1,new_game_state, new_path))

    #no path found
    return None