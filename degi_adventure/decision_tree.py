#Cuong Nguyen - AI 605.445 Capstone

import numpy as np
import csv
import random
import math

def log2(x):
    return math.log10(x) / math.log10(2)
    
def remove(items, item):
    return [i for i in items if i != item]
    
def count(data, value):
    cnt = 0
    for d in data:
        if (d['class'] == value):
            cnt += 1
    return cnt
    
def IsDataHomogeneous(data):
    tmp = data[0]['class']
    for d in data:
        if d['class'] != tmp:
            return False
    return True

def get_subdata(data, attr):
    values = {'sun':['rising','setting'], 
              'moon':['waxing','waning'], 
              'season':['fall', 'summer', 'winter', 'spring']}
    return [(v, [d for d in data if d[attr] == v]) for v in values[attr]]

def entropy(data):
    values = remove([count(data, v) for v in ['map01', 'map02', 'map03', 'map04']], 0)
    s = float(sum(values))
    return sum([-(v/s)*log2(v/s) for v in values])
    
def gain(data, attr):
    n = float(len(data))
    r = 0
    for (v, subdata) in get_subdata(data, attr):
        r += (len(subdata)/n)*entropy(subdata)
    return entropy(data) - r
    
def majority_label(data):
    maps = ['map01', 'map02', 'map03', 'map04']
    sets = [[d for d in data if d['class'] == m] for m in maps]
    best_set = sets[0]
    best_map = maps[0]
    for i in range(len(sets)):
        if len(sets[i]) > len(best_set):
            best_set = sets[i]
            best_map = maps[i]
    return best_map
    
def pick_best_attribute(data, attributes):
    best_attr = attributes[0]
    best_attr_gain = gain(data, best_attr)
    for attr in attributes:
        attr_gain = gain(data, attr)
        if (attr_gain > best_attr_gain):
            best_attr = attr
            best_attr_gain = attr_gain
    return best_attr
    
def read_map_characteristics(file_name):
    data = []
    attributes = ['sun', 'moon', 'season']
    with open('map_characteristics.txt', 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in datareader:
            inputs = [v for v in row]
            d = {}
            d['class'] = inputs[3]
            index = 0
            for a in attributes:
                d[a] = inputs[index]
                index += 1
            data.append(d)
    random.shuffle(data)
    return data, attributes
    
class Node:
    def __init__(self, attribute, children=None):
        self.attribute = attribute
        if children != None:
            self.children = children
        else:
            self.children = {}
    def add(self, attr, child):
        self.children[attr] = child
        return self
    def classify(self, test_data):
        child = self.children[test_data[self.attribute]]
        if isinstance(child, Node):
            return child.classify(test_data)
        else:
            return child
    def __repr__(self):
        return 'Node(%r, %r)' % (self.attribute, self.children)
        
def id3(data, attributes, default=None):
    if len(data) == 0:
        return default
    elif IsDataHomogeneous(data):
        return data[0]['class']
    elif len(attributes) == 0:
        return majority_label(data)
    else:
        best_attr = pick_best_attribute(data, attributes)
        node = Node(best_attr)
        for (value, subdata) in get_subdata(data, best_attr):
            child = id3(subdata, remove(attributes, best_attr), majority_label(data))
            node.add(value, child)
        return node