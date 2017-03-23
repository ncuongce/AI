#Cuong Nguyen - AI 605.445 Capstone

from operator import *
import copy
import itertools
import random

def argmax(actions, func):
    max_action = actions[0]; max_value = func(max_action)
    for a in actions:
        value = func(a)
        if value > max_value:
            max_action, max_value = a, value
    return max_action

def q_learning(world, costs, goal, reward, actions, gamma, alpha, max_episode):
    q = {}
    states = set()
    rewards = {}
    for x in range(len(world[0])):
        for y in range(len(world)):
            if world[y][x] in costs:
                rewards[x, y] = costs[world[y][x]]
                states.add((x,y))
            else:
                rewards[x, y] = None
    rewards[goal] = reward
    def get_state(state, action):
        state1 = tuple(map(add, state, action))
        if (state1 in states):
            return state1#move to new state
        else:
            return state#bound back
    def get_actions(state):
        if state == goal:
            return [None]
        else:
            return actions
    def get_greedy_action(state):     
        if (world[state[1]][state[0]] == 'E'):
            rand = random.choice(range(0,100,1))
            if rand <= 65:#65%
                return (0,-1)
            else:
                return random.choice(actions)
        if (world[state[1]][state[0]] == 'F'):
            rand = random.choice(range(0,100,1))
            if rand <= 70:#70%
                return (1,0)
            else:
                return random.choice(actions)
        if (world[state[1]][state[0]] == 'W'):
            rand = random.choice(range(0,100,1))
            if rand <= 75:#75%
                return (0,1)
            else:
                return random.choice(actions)
        if (world[state[1]][state[0]] == 'A'):
            rand = random.choice(range(0,100,1))
            if rand <= 80:#80
                return (-1,0)
            else:
                return random.choice(actions)
        if (world[state[1]][state[0]] == 'V'):
            rand = random.choice(range(0,100,1))
            if rand <= 85:#85
                return (0,-1)
            else:
                return random.choice(actions)
    def get_init_state(goal):
        for a in actions:
            state1 = tuple(map(add, goal, a))
            if state1 in states:
                return state1
        return (0, 0)
    checkpoint = get_init_state(goal)
    def update_checkpoint(checkpoint, state):
        dx1 = abs(state[0]-goal[0])
        dy1 = abs(state[1]-goal[1])
        d1 = dx1+dy1
        dx2 = abs(checkpoint[0]-goal[0])
        dy2 = abs(checkpoint[1]-goal[1])
        d2 = dx2+dy2
        if (d1 > d2):
            checkpoint = state
    def get_utility(s, a):
        return q[(s,a)]
    def get_best_policy():
        pi = {}
        for s in states:
            pi[s] = argmax(actions, lambda a:get_utility(s, a))
        return pi
    for s in states:
        for a in actions:
            q[(s,a)] = 0
    for e in range(max_episode):
        s = checkpoint
        while (s != goal):
            a = get_greedy_action(s)#explore, can also use exploit greedy
            s1 = get_state(s, a)
            r = rewards[s1]
            q[(s,a)] = (1-alpha) * q[(s,a)] + alpha * (r + gamma * max([q[(s1,a1)] for a1 in get_actions(s)]))
            s = s1
            update_checkpoint(checkpoint, s)
    return get_best_policy()