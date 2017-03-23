#Cuong Nguyen - AI 605.445 Capstone

from q_learning import *
from decision_tree import *
from astar_search import *
from successive_elimination import *

def read_plane(file_name):
    with open(file_name, 'r') as f:
        plane_data = [x for x in f.readlines()]
    f.closed
    plane = []
    for line in plane_data:
        line = line.strip()
        if line == "": continue
        plane.append([x for x in line])
    return plane

def print_policy(world, policy):
    moves = {(0,-1):'^', (1,0):'>', (0,1):'v', (-1,0):'<'}
    for y in range(len(world)):
        str = ""
        for x in range(len(world[0])):
            if (x, y) in policy:
                str += moves[policy[(x,y)]]
            else:
                str += 'x'
        print str
        
def print_path(world, path):
    if path:
        str_path = "The path steps:\n"
        for p in path:
            str_path += "->"+str(p)
        print str_path
        str_map = "The path map (path is marked in <>, D is Degi,\n"
        str_map += "E is Earth shrine,  F is Fire shrine,  W is Water shrine,  A is Wind shrine,  V is Void shrine):\n"
        for x in range(0, len(world[0])):
            for h in range(0, len(world[0])):
                str_map += '----'
            str_map += '-\n'
            for y in range(0, len(world[0])):
                if (y,x) in path:
                    str_map += '|' + '<' + world[x][y] + '>'
                else:
                    str_map += '| ' + world[x][y] + ' '
            str_map += '|\n'
        for h in range(0, len(world[0])):
            str_map += '----'
        str_map += '-\n'
        print str_map
    else:
        print "Couldn't find the path"

def print_world(world):
    for y in range(len(world)):
        str = ""
        for x in range(len(world[0])):
            str += world[y][x]
        print str

def get_random_position():
    x = random.choice(range(0,10,1))
    y = random.choice(range(0,10,1))
    return (x,y)
    
def main():
    #Game Tittle
    print "  ___           _ _        _      _             _                "
    print " |   \ ___ __ _(_| )___   /_\  __| |_ _____ _ _| |_ _  _ _ _ ___ "
    print " | |) / -_) _` | |/(_-<  / _ \/ _` \ V / -_) ' \  _| || | '_/ -_)"
    print " |___/\___\__, |_| /__/ /_/ \_\__,_|\_/\___|_||_\__|\_,_|_| \___|"
    print "          |___/                                                  "
    print ""
    
    print "Hix hix, Degi's parents have been captured by Elemental King!!!"
    print "Degi is trying to rescue his parents"
    
    planes_elements = {'E':'Earth', 'F':'Fire', 'W':'Water', 'A':'Wind', 'V':'Void'}
    planes_costs = { 'E': 1, 'F': 1, 'W': 1, 'A': 1, 'V': 1}
    planes_actions = [(0,-1), (1,0), (0,1), (-1,0)]
    map_costs = { '.': 1, '*': 3, '^': 5, '~': 7}
    map_moves = [(0,-1), (1,0), (0,1), (-1,0)]
    #right answer is -5,-5
    game1 = [[(-5, -5), (-1, -10)], [(-10, -1), (-2, -2)]]
    #right answer is 20,20
    game2 = [[(10,10), (14,12), (14,15)], [(12,14), (20,20), (28,15)], [(15,14), (15,28), (25,25)]]
    
    planes_map = read_plane("planes_map.txt")
    print "The elemental plane map looks like below: (Earth: E, Fire: F, Water: W, Wind: A,Void: V)"
    print_world(planes_map)
    print "Degi is learning the elemental planes to find the path to where his parents captured..."
    print "It takes around 15 seconds, please wait..."
    planes_policy = q_learning(planes_map, planes_costs, (9,9), 100, planes_actions, 0.9, 0.1, 100)
    print "Degi found the path going through the elemental planes:"
    print_policy(planes_map, planes_policy)
    print ""
    
    map_chars, map_attrs = read_map_characteristics('map_characteristics.txt')
    map_decision_tree = id3(map_chars, map_attrs)
    
    play_game = 'y'
    planes_position = (0,0)
    while planes_position != (9,9):
        print "Degi is in " + planes_elements[planes_map[planes_position[1]][planes_position[0]]] + " plane"
        
        map_char = {}
        map_char['sun'] = random.choice(['rising', 'setting'])
        map_char['moon'] = random.choice(['waxing', 'waning'])
        map_char['season'] = random.choice(['fall', 'summer', 'winter', 'spring'])
        print "Because Sun is " + map_char['sun'] + " and Moon is " + map_char['moon'] + " in " + map_char['season'] + " season,"
        
        map_name = map_decision_tree.classify(map_char)
        print "Degi knows that he is in " + map_name
        plane_map = read_plane(map_name+".txt")
        
        shrine_positions = []
        while (len(shrine_positions) != 5):
            p = get_random_position()
            if ((p not in shrine_positions) and (plane_map[p[1]][p[0]] != '^') and (plane_map[p[1]][p[0]] != '~')):
                shrine_positions.append(p)
        
        degi_position = get_random_position()
        while (degi_position in shrine_positions):
            degi_position = get_random_position()
        
        print "Degi is randomly dropped at " + str(degi_position) + " in " + map_name
        
        planes_move = planes_policy[planes_position]
        planes_position = tuple(map(add, planes_position, planes_move))
        plane_name = planes_elements[planes_map[planes_position[1]][planes_position[0]]]
        if (plane_name == 'Earth'):
            shrine_position = shrine_positions[0]
        elif (plane_name == 'Fire'):
            shrine_position = shrine_positions[1]
        elif (plane_name == 'Water'):
            shrine_position = shrine_positions[2]
        elif (plane_name == 'Wind'):
            shrine_position = shrine_positions[3]
        elif (plane_name == 'Void'):
            shrine_position = shrine_positions[4]
        print "Degi needs to find the path to " + plane_name + " shrine"
        print plane_name + " shrine is at " + str(shrine_position) + " in " + map_name
        
        path = a_star_search(plane_map, map_costs, degi_position, shrine_position, map_moves)
        print "Degi's path going through the plane looks like below:"
        plane_map[degi_position[1]][degi_position[0]] = 'D'
        plane_map[shrine_positions[0][1]][shrine_positions[0][0]] = 'E'
        plane_map[shrine_positions[1][1]][shrine_positions[1][0]] = 'F'
        plane_map[shrine_positions[2][1]][shrine_positions[2][0]] = 'W'
        plane_map[shrine_positions[3][1]][shrine_positions[3][0]] = 'A'
        plane_map[shrine_positions[4][1]][shrine_positions[4][0]] = 'V'
        print_path(plane_map, path)
        print "Degi is now at " + plane_name + " shrine portal"
        print "Opps, there is " + plane_name + " spirit," 
        print "and the spirit wants to challenge Degi to play a game called - Answer Right or Die "
        
        while (play_game == 'y'):
            print "Find the pure strategy Nash Equilibrium of a Normal Form Game below:"
            game = random.choice([game1, game2])
            nash = solve_game(game)
            game_answer = (game[nash[1]][nash[0]])
            
            print game
            print "Please type which stratery is your answer in format x,y:"
            while (True):
                try:
                    user_answer = tuple(int(x.strip()) for x in raw_input().split(','))
                except ValueError:
                    print "Please type in correct format:"
                    continue
                break
            if (user_answer == game_answer):
                print "Degi got right answer, he can move on!!!"
                break
            else:
                print "Degi got wrong answer but the spirit is bored, he wants to play another game"
        print ""
        if (play_game == 'y'):
            #this is for debugging to see the Elemental King's last game for grading only
            print "Do you want to skip playing all games with spirits (this is for Professor's debugging)? [y or n]"
            if (raw_input() == 'y'):
                play_game = 'n'
        print ""
        
    print "Degi is finally at where Degi's parents are being held by The Elemental King"
    print "Degi needs to defeat The Elemental King to rescue his parents!!!"
    print "The Elemental King wants to challenge Degi to play a last game"
    print "Find the pure strategy Nash Equilibrium of a Normal Form Game below:"
        
    while (True):
        #the right answer is None, None
        game = [[(9,4), (5,2), (5,5)], [(6,10), (2,8), (7,10)], [(2,8), (8,3), (9,8)]]
        game_answer = solve_game(game)
        
        print game
        print "Please type which stratery is your answer in format x,y:"
        while (True):
            try:
                user_answer = tuple(x.strip() for x in raw_input().split(','))
            except ValueError:
                print "Please type in correct format:"
                continue
            break
        if (user_answer == game_answer):
            print "Degi got right answer, he defeated The Elemental King!!!"
            break
        else:
            print "Degi got wrong answer but The Elemental King is bored, he lets Degi try again"
    
    print ""
    print "Degi finally defeats The Elemental King to rescue his parents!!!"
    print "They now can live happily together and forever after..."
    
if __name__ == '__main__':
    main()