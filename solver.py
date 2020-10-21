#!/usr/bin/env python3
import random as rnd
import sys

def printgrid(grid):
    res = "\n"
    for i in range(len(grid)):
        if i%3==0: res += " +-----------------------------------+\n"
        for j in range(len(grid[0])):
            if j%3==0: res += " | "
            if grid[i][j]==0: res += " . "
            else: res += " {0} ".format(grid[i][j])
        res += " | \n"
    res += " +-----------------------------------+\n"
    print(res)

def finished(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0: return False

    return True

def getvalues(t, grid, index1, index2 = -1):
    values = []

    # Return row
    if t=='r':
        values = grid[index1]

    # Return column
    if t=='c':
        values = [grid[i][index1] for i in range(9)]

    # Return square
    if t=='s':
        for i in range(3):
            for j in range(3):
                y = index1*3 + i
                x = index2*3 + j
                values.append(grid[y][x])

    return values

def getvalidvalues(r, c, grid):
    row = getvalues('r', grid, r)
    col = getvalues('c', grid, c)
    square = getvalues('s', grid, int(r/3), int(c/3))

    return [x for x in range(1,10) if x not in row and
                                      x not in col and
                                      x not in square]

def findbest(grid):
    best = 9
    position = [0,0]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:

                valids = getvalidvalues(i,j,grid)
                
                if len(valids) < best: 
                    best = len(valids)
                    position = [i,j]

    return position

def gridclone(grid):
    clone = []
    for i in range(len(grid)):
        clone.append([])
        for j in range(len(grid[0])):
            clone[i].append(grid[i][j])

    return clone

def solve(grid):
    while finished(grid)==False:
        modified = False

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    validvalues = getvalidvalues(i,j,grid)
                    if len(validvalues) == 1:
                        grid[i][j] = validvalues[0]
                        modified = True

        if modified == False:
            bestposition = findbest(grid)
            r = bestposition[0]
            c = bestposition[1]

            values = getvalidvalues(r,c,grid)

            while len(values) > 0:
                v = rnd.choice(values)
                clone = gridclone(grid)
                clone[r][c] = v

                outc, gr = solve(clone)
                if outc: return True, gr
                values.remove(v)

            return False, grid

    return True, grid

def main():
    #EXAMPLE
    sudoku = [[0,0,0,0,0,5,0,8,0],
              [3,0,0,6,0,0,7,4,0],
              [0,0,2,8,0,0,0,0,9],
              [0,0,0,0,0,0,3,7,0],
              [0,0,7,0,0,6,0,0,2],
              [0,9,0,4,0,7,0,0,0],
              [0,2,0,0,1,0,0,0,0],
              [0,4,0,0,0,0,0,0,5],
              [5,0,0,0,9,0,1,0,0]]

    print("Original sudoku:")
    printgrid(sudoku)

    print("\n\nSolved sudoku:")
    printgrid(solve(sudoku)[1])

if __name__ == "__main__":
    main()