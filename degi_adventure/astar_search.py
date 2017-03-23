#Cuong Nguyen - AI 605.445 Capstone

import operator

def get_position(current, move):
    return tuple(map(operator.add, current, move))
    
def is_legal_move(world, current):
    if current[0] < 0 or current[0] >= len(world[0]):
        return False
    if current[1] < 0 or current[1] >= len(world[0]):
        return False
    if world[current[1]][current[0]] == 'x':
        return False
    tokens = ['.', '*', '^', '~']
    if world[current[1]][current[0]] not in tokens:
        return False
    return True
    
def get_heuristic(world, costs, current, goal):
    token = world[current[1]][current[0]]
    d = costs[token]
    dx = abs(current[0] - goal[0])
    dy = abs(current[1] - goal[1])
    return d*(dx+dy)
    
def get_cost(world, costs, current, prev_cost):
    token = world[current[1]][current[0]]
    return prev_cost + costs[token]
    
def is_empty(l):
    if l:
        return False
    else:
        return True
        
def is_in_frontier(frontier, current):
    for i in range(0,len(frontier)):
        if current == frontier[i][3]:
            return i
    return -1
    
def build_path(path, start, goal):
    ret_path = [goal]
    current = goal
    while path[current] != start:
        current = path[current]
        ret_path.append(current)
    ret_path.append(start)
    ret_path.reverse()
    return ret_path
    
def a_star_search( world, costs, start, goal, moves):
    if is_legal_move(world, start) == False:
        return []
    if is_legal_move(world, goal) == False:
        return []
    Explorer = []
    Frontier = []
    Path = {}
    g = get_cost(world, costs, start, 0)
    h = get_heuristic(world, costs, start, goal)
    f = g + h
    Frontier.append((f,g,h,start))
    while not is_empty(Frontier):
        current = Frontier.pop(0)
        if current[3] == goal:
            return build_path(Path, start, goal)
        Explorer.append(current[3])
        for move in moves:
            next_move = get_position(current[3], move)
            if is_legal_move(world, next_move) == False:
                continue
            if next_move in Explorer:
                continue
            i = is_in_frontier(Frontier, next_move)
            g = get_cost(world, costs, next_move, current[1])
            h = get_heuristic(world, costs, next_move, goal)
            f = g + h
            if i == -1:
                Frontier.append((f,g,h,next_move))
            elif (f < Frontier[i][0]):
                Frontier[i] = (f,g,h,next_move)
            Frontier.sort()
            Path[next_move] = current[3]
    return []