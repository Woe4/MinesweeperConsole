'''
Timothy yu
March 8, 2022
Minesweeper
'''

import math
import random
import numpy as np

diffdict = {
    'b':(9, 9, 10),
    'i':(16, 16, 40),
    'e':(16, 30, 99)
}


def GeneratePlayerMap(c, r):
    arr = np.full((r,c), '-')
    return arr

def GenerateGameMap(c, r, m):
    gmap = np.zeros((r,c))
    count = 0
    while count < m:
        bomx = random.randint(0, c-1)
        bomy = random.randint(0, r-1)
        if gmap[bomy][bomx] >= 9: #if same mine chosen 
            continue
        gmap[bomy][bomx] = 9 #9 means bomb. Using 9 (which is greater than the maximum 8) allows me to add to the mine number with no consequence
        if bomy > 0:  #top middle add 1
            gmap[bomy-1][bomx] += 1
        if bomy > 0 and (bomx+1) < c:  #top right add 1
            gmap[bomy-1][bomx+1] += 1
        if bomy > 0 and bomx > 0:  #top left add 1
            gmap[bomy-1][bomx-1] += 1
        if (bomy+1) < r:  #bottom middle add 1
            gmap[bomy+1][bomx] += 1
        if (bomy+1) < r and (bomx+1) < c:  #bottom right add 1
            gmap[bomy+1][bomx+1] += 1
        if (bomy+1) < r and bomx > 0:  #bottom left add 1
            gmap[bomy+1][bomx-1] += 1
        if bomx > 0:  #left middle add 1
            gmap[bomy][bomx-1] += 1
        if (bomx+1) < c:  #right middle add 1
            gmap[bomy][bomx+1] += 1
        
        count += 1 #ensure correct number of mines placed
            
    return gmap
        
def CheckDone(pmap, arr):

    if pmap.size == 81:
        r = 9
        c = 9
    elif pmap.size == 256:
        r = 16
        c = 16
    else:
        r = 30
        c = 16
        
    xcheck = 0
    numdone = 0
    for row in range(0, r):
        for cell in range(0, c):
            if pmap[row][cell] == 'X':
                xcheck += 1
            if (pmap[row][cell] == '-') and (arr[row][cell] < 9):
                numdone += 1
    if xcheck > 0:
        return True, 'loss'
    elif numdone > 0:
        return False
    else:
        return True, 'win'


def OpenSquare(x, y, gmap, pmap):
    if gmap.size == 81:
        r = 9
        c = 9
    elif gmap.size == 256:
        r = 16
        c = 16
    else:
        r = 30
        c = 16
    
    if 0 <= x and x < c  and 0 <= y and y < r:
        if pmap[y][x] == '-':
            if gmap[y][x] > 8:
                pmap[y][x] = 'X'
            else:
                pmap[y][x] = str(gmap[y][x])
            if gmap[y][x] == 0:
                OpenSquare(x, y-1, gmap, pmap)
                OpenSquare(x, y+1, gmap, pmap)
                OpenSquare(x+1, y, gmap, pmap)
                OpenSquare(x-1, y, gmap, pmap)
                OpenSquare(x+1, y-1, gmap, pmap)
                OpenSquare(x+1, y+1, gmap, pmap)
                OpenSquare(x-1, y-1, gmap, pmap)
                OpenSquare(x-1, y+1, gmap, pmap)
    return pmap

def FlagSquare(x, y, gmap, pmap):
    if gmap.size == 81:
        r = 9
        c = 9
    elif gmap.size == 256:
        r = 16
        c = 16
    else:
        r = 30
        c = 16
    
    if 0 <= x and x < c  and 0 <= y and y < r:
        if pmap[y][x] == 'f':
            pmap[y][x] = '-'
        elif pmap[y][x] == '-':
            pmap[y][x] = 'f'
    return pmap


def OpenFlagSquare(x, y, gmap, pmap):
    if gmap.size == 81:
        r = 9
        c = 9
    elif gmap.size == 256:
        r = 16
        c = 16
    else:
        r = 30
        c = 16
    
    if 0 <= x and x < c  and 0 <= y and y < r:
        
        flagnum = int(pmap[y][x])        
        count = 0
        
        if pmap[y-1][x] == 'f':
            count += 1
        if pmap[y+1][x] == 'f':
            count += 1
        if pmap[y][x+1] == 'f':
            count += 1
        if pmap[y][x-1] == 'f':
            count += 1
        if pmap[y-1][x+1] == 'f':
            count += 1
        if pmap[y+1][x+1] == 'f':
            count += 1
        if pmap[y-1][x-1] == 'f':
            count += 1
        if pmap[y+1][x-1] == 'f':
            count += 1
        
        if count == flagnum:
            OpenSquare(x, y-1, gmap, pmap)
            OpenSquare(x, y+1, gmap, pmap)
            OpenSquare(x+1, y, gmap, pmap)
            OpenSquare(x-1, y, gmap, pmap)
            OpenSquare(x+1, y-1, gmap, pmap)
            OpenSquare(x+1, y+1, gmap, pmap)
            OpenSquare(x-1, y-1, gmap, pmap)
            OpenSquare(x-1, y+1, gmap, pmap)
    return pmap
            
        
        
def ShowMapDone(pmap, gmap):
    
    if gmap.size == 81:
        r = 9
        c = 9
    elif gmap.size == 256:
        r = 16
        c = 16
    else:
        r = 30
        c = 16
        
    for y in range(r):
        for x in range(c):
            if gmap[y][x] > 8:
                pmap[y][x] = 'X'
    print(pmap)


def PlayGame(numcols, numrows, numofmines):
    
    PlayerMap = GeneratePlayerMap(numcols, numrows)
    
    GameMap = GenerateGameMap(numcols, numrows, numofmines)
    #print(GameMap)
    
    while not CheckDone(PlayerMap, GameMap):
        opentype = input('Flag(f) or open(o)? ')
        if opentype == 'f':
            xcoord = input('Pick an x coord to flag: ')
            ycoord = input('Pick an y coord to flag: ')
            try:
                xcoord = int(xcoord)-1# -1 to account for array index starting at 0
                ycoord = int(ycoord)-1
            except:
                print('Enter integer coordinates.')
                continue
            if xcoord+1 > numcols or xcoord < 0 or ycoord < 0 or ycoord+1>numrows:
                print('Out of bounds.')
                continue
            
            PlayerMap = FlagSquare(xcoord, ycoord, GameMap, PlayerMap)
            np.set_printoptions(formatter={'numpystr': '{}'.format})
            print(PlayerMap)
            continue
        
        xcoord = input('Pick an x coord to open: ') 
        ycoord = input('Pick an y coord to open: ')
        try:
            xcoord = int(xcoord)-1# -1 to account for array index starting at 0
            ycoord = int(ycoord)-1
        except:
            print('Enter integer coordinates.')
            continue
        
        if xcoord+1 > numcols or xcoord < 0 or ycoord < 0 or ycoord+1>numrows:
            print('Out of bounds.')
            continue
        
        try:
            if int(PlayerMap[ycoord][xcoord]) > 0:
                PlayerMap = OpenFlagSquare(xcoord, ycoord, GameMap, PlayerMap)
                np.set_printoptions(formatter={'numpystr': '{}'.format})
                print(PlayerMap)
                continue
        except:
            pass
        PlayerMap = OpenSquare(xcoord, ycoord, GameMap, PlayerMap)
        np.set_printoptions(formatter={'numpystr': '{}'.format})
        print(PlayerMap)
        
    if CheckDone(PlayerMap, GameMap) == (True, 'loss'):
        print('You don messed')
        print('gg')
    else:
        print('wp dont come again')
        print('not gg')
        
    ShowMapDone(PlayerMap, GameMap)
    print('gg')


difficulty = input('Difficulty? Beginner(b), Intermediate (i), Expert (e) :')
cols = diffdict[difficulty][0]
rows = diffdict[difficulty][1]
mines = diffdict[difficulty][2]

PlayGame(cols, rows, mines)


