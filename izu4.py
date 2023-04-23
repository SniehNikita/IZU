# @author: SniehNikita
# This script solves 4th IZU task

import getopt
import sys
import math

def help():
    print("python izu4.py --input=model-xplagi0b.txt --output=xplagi0b [-g]\n\t -g : generage graphviz file")

def is_all_mp_same_class(mp):
    prev = None
    for item in mp:
        if prev == None:
            prev = mp[item][1]
        else:
            if mp[item][1] != prev:
                return False
            prev = mp[item][1]
    return True

def entropy(mp):
    items = {}
    for item in mp:
        res = mp[item][1]
        if res not in items:
            items[res] = 0
        items[res] += 1
    sum = 0
    for key in items:
        val = items[key] / len(mp) 
        sum -= val * math.log2(val)

    return sum

def get_mp_with_attr(mp, ai_attr):
    nmp = {}
    for item in mp:
        for attr in mp[item]:
            if attr == ai_attr:
                nmp[item] = mp[item]
                break
    return nmp

def expected_info(mp, ai):
    sum = 0
    for attr in attributes[ai]:
        nmp = get_mp_with_attr(mp, attr)
        a = len(nmp)
        b = len(mp)
        c = entropy(nmp)
        sum += (a / b) * c
    return sum

def info_gain(mp, ai):
    return entropy(mp) - expected_info(mp, ai)

def is_attr_in_obj(obj, attr):
    for item in obj:
        if item == attr:
            return True
    return False

def rm_attrs_from_mp(mp, ma, attr):
    new_mp = {}
    for item in mp:
        for i in range(2,len(mp[item])):
            if mp[item][i] == attr:
                new_mp[item] = mp[item].copy()
                break
    return new_mp

def decision_tree(mp, ma):
    global elem_counter
    global parent_elem_name
    global parent_elem_attr
    global parent_elem_num

    buf = ""
    if len(mp) == 0:
        return
    
    if is_graph:
        buf += "\t"

    if is_all_mp_same_class(mp):    
        # === Log part    
        for item in mp:
            i = item
            break
        buf += str(mp[i][1]) + str(elem_counter) +  "  ["
        if is_graph:
            buf += "shape=record, style=rounded, "
        buf += "label=\"" + str(mp[i][1]) + "\"]\n"
        if is_graph:
            buf += "\t"
        buf += str(parent_elem_name) + " -> " + str(mp[i][1]) + str(elem_counter) + " [label=\"" + parent_elem_attr + " {"
        for item in mp:
            buf += str(item) + ","
        buf = buf [:-1]
        buf += "}\"]\n"
        output_file.write(buf)
        elem_counter += 1
        # ==============
        return
    
    gains = {}
    max_gain = None
    for attr in ma:
        gains[attr] = round(info_gain(mp, attr), 4)
        if max_gain == None:
            max_gain = attr
        elif gains[attr] > gains[max_gain]:
            max_gain = attr

    # === Log part 
    # Prints <name> [...]
    buf += str(max_gain) + str(elem_counter) + " ["
    if is_graph:
        buf += "shape=record, "
    buf += "label=\"" + str(max_gain) + "|{"    
    for key in gains:
        buf += str(key) + "=" + str(gains[key]) + "|"
    buf = buf[:-1]
    buf += "}\"]\n"
    # Prints a -> b
    if parent_elem_name != None:
        if is_graph:
            buf += "\t"
        buf += str(parent_elem_name) + " -> " + str(max_gain) + str(elem_counter) + " [label=\"" + parent_elem_attr + " {"
        for item in mp:
            buf += str(item) + ","
        buf = buf [:-1]
        buf += "}\"]\n"
    output_file.write(buf)
    elem_counter += 1
    buf = ""
    # ==============

    lcl_elem_cnt = elem_counter
    for attr in attributes[max_gain]:
        new_ma = ma.copy()
        new_ma.pop(max_gain)
        new_mp = rm_attrs_from_mp(mp, ma, attr)
        parent_elem_name = str(max_gain) + str(lcl_elem_cnt-1)
        parent_elem_attr = attr
        parent_elem_num = lcl_elem_cnt
        decision_tree(new_mp, new_ma)


# =============================
#  Main
# =============================        

elem_counter = 1
parent_elem_name = None
parent_elem_attr = None
parent_elem_num = 0

args = sys.argv[1:]
opts, args = getopt.getopt(args, 'i:o:gh', ["input=", "output="])
is_graph = False

for opt, arg in opts:
    if opt in ["-i", "--input"]:
        input_file_name = arg
    elif opt in ["-o", "--output"]:
        output_file_name = arg
    elif opt in ["-g"]:
        is_graph = True
    elif opt in ["-h"]:
        help()
        exit(0)
        
input_file = open(input_file_name, 'r')
output_file = open(output_file_name, 'w')

attributes = {}
classes = []
objects = {}

is_reading_attributes = False
is_reading_classes = False
is_reading_objects = False
for line in input_file:
    words = line.split()
    if len(words) == 0:
        continue

    if words[0] == '}':
        is_reading_attributes = False
        is_reading_classes = False
        is_reading_objects = False
    elif words[0] == "attributes" and words[1] == '{':
        is_reading_attributes = True
    elif words[0] == "classes" and words[1] == '{':
        is_reading_classes = True
    elif words[0] == "objects" and words[1] == '{':
        is_reading_objects = True
    else:
        if is_reading_attributes:
            attributes[words[0]] = words[2:]
        elif is_reading_classes:
            classes.append(words)
        elif is_reading_objects:
            objects[words[0]] = words

if is_graph:
    output_file.write("digraph {\n")
decision_tree(objects, attributes)
if is_graph:
    output_file.write("}")

input_file.close()
output_file.close()