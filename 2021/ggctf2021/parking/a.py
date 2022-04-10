import sys
import time
import string

import os
from z3 import *
sys.setrecursionlimit(10**9)

WALL = -1

blocks = []
board = {}


boardfile = open(sys.argv[1]).read()
header, boardfile = boardfile.split("\n", 1)
W, H = [int(x) for x in header.split()]
flagblocks = {}
target = -1
SZ = 4
target_start = None

walls = []
for line in boardfile.splitlines():
    if not line.strip(): continue
    x,y,w,h,movable = [int(x) for x in line.split()]

    if movable == -1:
        flagblocks[len(blocks)] = (x,y)
    elif movable == -2:
        target = len(blocks)
        target_start = x, y

    for i in range(x, x+w):
        for j in range(y, y+h):
            if movable != 0:
                if (i,j) in board:
                    print("Car overlap at %d, %d" % (i,j))
                    #assert False
                board[(i,j)] = len(blocks)
            else:
                if (i,j) in board and board[i,j] != WALL:
                    print("Wall-car overlap at %d, %d" % (i,j))
                    #assert False
                board[(i,j)] = WALL
    if movable:
        blocks.append([x,y,w,h, movable])
    else:
        walls.append([x,y,w,h])



v = []
flagv = []
s = Solver()

for i in range(64):
    flagv.append(BitVec("FLAG{}".format(i), 1))

cnt = 0
v.append(BitVec("PATH{}".format(cnt), 1))
cnt += 1

def is_horizontal(which):
    x,y,w,h,mv = blocks[which]
    return h == 1

def is_vertical(which):
    x,y,w,h,mv = blocks[which]
    return w == 1

def is_path(x, y):
    return (x, y) not in board

def is_wall(x, y):
    if is_path(x, y):
        return False
    else:
        return board[(x, y)] == -1

def is_car(x, y):
    if is_path(x, y):
        return False
    else:
        return board[(x, y)] != -1

block_path = {}

def traverse(which, path, prev):
    global cnt, v, flagv, s, end_count, block_path
    x,y,w,h,mv = blocks[which]

    if which not in block_path:
        block_path[which] = path
    else:
        s.add(path == block_path[which])
        return

    if which == target: # Red block
        s.add(path == 1)
        traverse(board[(x-1, y)], path, which)
        return
    
    if which in flagblocks: # Green blocks
        print("AT FLAG", which, blocks[which])
        s.add(path == flagv[(y-146)//108])
        return

    if is_horizontal(which):
        if is_wall(x-1, y) and is_wall(x+w, y): # close-end
            s.add(path == 0)
            return

        if (is_path(x-1, y) and is_wall(x+w, y)) or (is_wall(x-1, y) and is_path(x+w, y)): # open-end
            if (is_path(x-1, y) and is_wall(x+w, y)) and is_car(x-1, y+1) and (board[(x-1, y+1)] in flagblocks): # Near flag blocks
                s.add(path == ~(flagv[(y+1-146)//108]))
            else:
                s.add(path == 1)
            return

        if (is_wall(x-1, y) and is_car(x+w, y) and is_car(x+w+1, y) and (board[(x+w, y)] != board[(x+w+1, y)]) and w == 2): # right AND-gate
            v.append(BitVec("PATH{}".format(cnt), 1))
            cnt += 1
            v.append(BitVec("PATH{}".format(cnt), 1))
            cnt += 1
            s.add(path == (v[cnt-1] & v[cnt-2]))
            first_path = cnt - 1
            second_path = cnt - 2
            traverse(board[(x+w,y)], v[first_path], which)
            traverse(board[(x+w+1,y)], v[second_path], which)
            return

        if (is_wall(x+w, y) and is_car(x-1, y) and is_car(x-2, y) and (board[(x-1, y)] != board[(x-2, y)]) and w == 2): # left AND-gate
            v.append(BitVec("PATH{}".format(cnt), 1))
            cnt += 1
            v.append(BitVec("PATH{}".format(cnt), 1))
            cnt += 1
            s.add(path == (v[cnt-1] & v[cnt-2]))
            first_path = cnt - 1
            second_path = cnt - 2
            traverse(board[(x-1,y)], v[first_path], which)
            traverse(board[(x-2,y)], v[second_path], which)
            return

        if (is_path(x-1, y) and is_car(x+w, y)):
            if is_vertical(board[(x+w, y)]) and is_vertical(board[(x-2,y)]): # OR-gate
                v.append(BitVec("PATH{}".format(cnt), 1))
                cnt += 1
                v.append(BitVec("PATH{}".format(cnt), 1))
                cnt += 1
                s.add(path == (v[cnt-1] | v[cnt-2]))
                first_path = cnt - 1
                second_path = cnt - 2
                traverse(board[(x+w,y)], v[first_path], which)
                traverse(board[(x-2,y)], v[second_path], which)
                return
            if is_horizontal(board[(x+w, y)]) and is_horizontal(board[(x-2,y)]): # before intersection
                traverse(board[(x-2, y)], path, which)
                return
            if is_vertical(board[(x+w, y)]) and is_horizontal(board[(x-2,y)]): # after intersection
                traverse(board[(x+w, y)], path, which)
                return

        if (is_path(x+w, y) and is_car(x-1, y)):
            if is_vertical(board[(x-1, y)]) and is_vertical(board[(x+w+1,y)]): # OR-gate
                v.append(BitVec("PATH{}".format(cnt), 1))
                cnt += 1
                v.append(BitVec("PATH{}".format(cnt), 1))
                cnt += 1
                s.add(path == (v[cnt-1] | v[cnt-2]))
                first_path = cnt - 1
                second_path = cnt - 2
                traverse(board[(x-1,y)], v[first_path], which)
                traverse(board[(x+w+1,y)], v[second_path], which)
                return
            if is_horizontal(board[(x-1, y)]) and is_horizontal(board[(x+w+1,y)]): # before intersection
                traverse(board[(x+w+1, y)], path, which)
                return
            if is_vertical(board[(x-1, y)]) and is_horizontal(board[(x+w+1,y)]): # after intersection
                traverse(board[(x-1, y)], path, which)
                return
        
        if (is_car(x+w, y) and is_car(x-1, y)): # Between 2 cars
            if board[(x+w, y)] == prev:
                traverse(board[(x-1, y)], path, which)
            elif board[(x-1, y)] == prev:
                traverse(board[(x+w, y)], path, which)
            elif blocks[prev][0] == x:
                traverse(board[(x+w, y)], path, which)
            elif blocks[prev][0] == x+w-1:
                traverse(board[(x-1, y)], path, which)
            else:
                print("ERROR BETWEEN 2 CARS HORZ", which)
                sys.exit(-1)
            return

        if (is_wall(x+w, y) and is_car(x-1, y)): # Left car right wall
            if board[(x-1, y)] != prev:
                traverse(board[(x-1, y)], path, which)
            else:
                print("ERROR BETWEEN WALL CAR VERT", which, blocks[which])
            return

        if (is_car(x+w, y) and is_wall(x-1, y)): # Left wall right car
            if board[(x+w, y)] != prev:
                traverse(board[(x+w, y)], path, which)
            else:
                print("ERROR BETWEEN WALL CAR VERT", which, blocks[which])
            return

        
    if is_vertical(which):
        if is_wall(x, y-1) and is_wall(x, y+h): # close-end
            s.add(path == 0)
            return

        if (is_path(x, y-1) and is_wall(x, y+h)) or (is_wall(x, y-1) and is_path(x, y+h)): # open-end
            s.add(path == 1)
            return

        if (is_wall(x, y-1) and is_car(x, y+h) and is_car(x, y+h+1) and (board[(x, y+h)] != board[(x, y+h+1)]) and h == 2): # down AND-gate
            v.append(BitVec("PATH{}".format(cnt), 1))
            cnt += 1
            v.append(BitVec("PATH{}".format(cnt), 1))
            cnt += 1
            s.add(path == (v[cnt-1] & v[cnt-2]))
            first_path = cnt - 1
            second_path = cnt - 2
            traverse(board[(x, y+h)], v[first_path], which)
            traverse(board[(x, y+h+1)], v[second_path], which)
            return

        if (is_wall(x, y+h) and is_car(x, y-1) and is_car(x, y-2) and (board[(x, y-1)] != board[(x, y-2)]) and h == 2): # up AND-gate
            v.append(BitVec("PATH{}".format(cnt), 1))
            cnt += 1
            v.append(BitVec("PATH{}".format(cnt), 1))
            cnt += 1
            s.add(path == (v[cnt-1] & v[cnt-2]))
            first_path = cnt - 1
            second_path = cnt - 2
            traverse(board[(x, y-1)], v[first_path], which)
            traverse(board[(x, y-2)], v[second_path], which)
            return

        if (is_path(x, y-1) and is_car(x, y+h)):
            if is_horizontal(board[(x, y+h)]) and is_horizontal(board[(x, y-2)]): # OR-gate
                v.append(BitVec("PATH{}".format(cnt), 1))
                cnt += 1
                v.append(BitVec("PATH{}".format(cnt), 1))
                cnt += 1
                s.add(path == (v[cnt-1] | v[cnt-2]))
                first_path = cnt - 1
                second_path = cnt - 2
                traverse(board[(x, y+h)], v[first_path], which)
                traverse(board[(x, y-2)], v[second_path], which)
                return
            if is_vertical(board[(x, y+h)]) and is_vertical(board[(x, y-2)]): # Intersection
                traverse(board[(x, y-2)], path, which)
                return
            if is_horizontal(board[(x, y+h)]) and is_vertical(board[(x, y-2)]): # after intersection
                traverse(board[(x, y+h)], path, which)
                return

        if (is_path(x, y+h) and is_car(x, y-1)):
            if is_horizontal(board[(x, y-1)]) and is_horizontal(board[(x, y+h+1)]): # OR-gate
                v.append(BitVec("PATH{}".format(cnt), 1))
                cnt += 1
                v.append(BitVec("PATH{}".format(cnt), 1))
                cnt += 1
                s.add(path == (v[cnt-1] | v[cnt-2]))
                first_path = cnt - 1
                second_path = cnt - 2
                traverse(board[(x, y-1)], v[first_path], which)
                traverse(board[(x, y+h+1)], v[second_path], which)
                return
            if is_vertical(board[(x, y-1)]) and is_vertical(board[(x, y+h+1)]): # before intersection
                traverse(board[(x, y+h+1)], path, which)
                return
            if is_horizontal(board[(x, y-1)]) and is_vertical(board[(x, y+h+1)]): # after intersection
                traverse(board[(x, y-1)], path, which)
                return
        
        if (is_car(x, y+h) and is_car(x, y-1)): # Between 2 cars
            if board[(x, y+h)] == prev:
                traverse(board[(x, y-1)], path, which)
            elif board[(x, y-1)] == prev:
                traverse(board[(x, y+h)], path, which)
            elif blocks[prev][1] == y:
                traverse(board[(x, y+h)], path, which)
            elif blocks[prev][1] == y+h-1:
                traverse(board[(x, y-1)], path, which)
            else:
                print("ERROR BETWEEN 2 CARS VERT", which, blocks[which])
                sys.exit(-1)
            return

        if (is_wall(x, y+h) and is_car(x, y-1)): # Down car up wall
            if board[(x, y-1)] != prev:
                traverse(board[(x, y-1)], path, which)
            else:
                print("ERROR BETWEEN WALL CAR VERT", which, blocks[which])
                sys.exit(-1)
            return

        if (is_car(x, y+h) and is_wall(x, y-1)): # Up wall down car
            if board[(x, y+h)] != prev:
                traverse(board[(x, y+h)], path, which)
            else:
                print("ERROR BETWEEN WALL CAR VERT", which, blocks[which])
                sys.exit(-1)
            return

        print("UNKNOWN TYPE", which, blocks[which])
        sys.exit(-1)

traverse(target, v[0], -1)

sol_count = 0
solutions = []

print("Checking")

while sol_count < 5 and s.check() == sat:
    model = s.model()
    result = [model[flagv[i]].as_long() for i in range(64)]
    flagbits = ''.join([str(i) for i in result])
    flag = b"CTF{"
    while flagbits:
        byte, flagbits = flagbits[:8], flagbits[8:]
        flag += bytes([ int(byte[::-1], 2) ])
    flag += b"}"
    print(flag)

    solutions.append(flagbits)
    sol_count += 1

    print("sol_count=", sol_count)

    cond = True
    for i in range(64):
        cond = And(cond, flagv[i] == result[i])

    s.add(Not(cond))
