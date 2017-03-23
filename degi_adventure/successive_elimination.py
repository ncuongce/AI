#Cuong Nguyen - AI 605.445 Capstone

from operator import *
import copy
import itertools

def remove_column(game, col):
    for row in game:
        del row[col]
        
def remove_row(l, row):
    l.pop(row)
    
def compare_lt(l1, l2):
    return all(map(lt, l1, l2))
    
def compare_le(l1, l2):
    return all(map(le, l1, l2))
    
def find_lt(l):
    found = None
    for x,y in itertools.combinations(l, 2):
        if (compare_lt(x, y)):
            found = x
            break
        if (compare_lt(y, x)):
            found = y
            break
    if (found == None):
        return -1
    for i in range(0, len(l)):
        if (l[i] == found):
            return i
            
def find_le(l):
    found = None
    for x,y in itertools.combinations(l, 2):
        if (compare_le(x, y)):
            found = x
            break
        if (compare_le(y, x)):
            found = y
            break
    if (found == None):
        return -1
    for i in range(0, len(l)):
        if (l[i] == found):
            return i
            
def find_indices(game, strategy):
    for i,l1 in enumerate(game):
        for j,l2 in enumerate(l1):
            if l2 == strategy:
                return (i, j)
    return ('None', 'None')
    
def solve_game_p1(game, weak=False):
    game_p1 = copy.deepcopy(game)
    while len(game_p1) > 1:
        cmp_list = []
        new_list = []
        for row in game_p1:
            new_list = [item[0] for item in row]
            cmp_list.append(new_list)
        if (weak == False):
            index = find_lt(cmp_list)
        elif (weak == True):
            index = find_le(cmp_list)
        if index == -1:
            return ('None', 'None')
        remove_row(game_p1, index)
        cmp_list = []
        new_list = []
        for i in range(0, len(game_p1[0])):
            new_list = [item[i][1] for item in game_p1]
            cmp_list.append(new_list)
        if (weak == False):
            index = find_lt(cmp_list)
        elif (weak == True):
            index = find_le(cmp_list)
        if index == -1:
            return ('None', 'None')
        remove_column(game_p1, index)
    return find_indices(game, game_p1[0][0])
    
def solve_game_p2(game, weak=False):
    game_p2 = copy.deepcopy(game)
    while len(game_p2) > 1:
        cmp_list = []
        new_list = []
        for i in range(0, len(game_p2[0])):
            new_list = [item[i][1] for item in game_p2]
            cmp_list.append(new_list)
        if (weak == False):
            index = find_lt(cmp_list)
        elif (weak == True):
            index = find_le(cmp_list)
        if index == -1:
            return ('None', 'None')
        remove_column(game_p2, index)
        cmp_list = []
        new_list = []
        for row in game_p2:
            new_list = [item[0] for item in row]
            cmp_list.append(new_list)
        if (weak == False):
            index = find_lt(cmp_list)
        elif (weak == True):
            index = find_le(cmp_list)
        if index == -1:
            return ('None', 'None')
        remove_row(game_p2, index)
    return find_indices(game, game_p2[0][0])
    
def solve_game(game, weak=False):
    p1 = solve_game_p1(game, weak)
    if (p1 == ('None', 'None')):
        p2 = solve_game_p2(game, weak)
        return p2
    else:
        return p1