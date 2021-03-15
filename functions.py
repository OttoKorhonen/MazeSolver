import numpy as np
#hakee ja palauttaa tiedostosta sokkelon
def get_maze():
    data = open("maze-task-second.txt", "r")
    lines = data.readlines()
    maze = [list(i.strip()) for i in lines]
    return maze

#loopataan kaksiulotteinen taulukko läpi ja muutetaan sokkelo ykkösiksi ja nolliksi
def format_maze():
    maze = get_maze()
    walls = []
    exits =[]
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '#':
                maze[i][j] = 1
                walls.append((i,j))
            elif maze[i][j] == 'E':
                exits.append((i,j))
                maze[i][j] = 0
            elif maze[i][j] == '^':
                start = i,j
                maze[i][j] = 0
            else:
                maze[i][j] = 0
                
    return walls, maze, exits, start

def empty_maze():
    walls, maze, exits, start = format_maze()
    m = []
    for i in range(len(maze)):
        m.append([])
        for j in range(len(maze[i])):
            m[-1].append(0)
    i,j = start
    m[i][j] = 1
    return m

def make_step(k, m):
    walls, maze, exits, start = format_maze()
    #m = empty_maze()
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == k:
                if i>0 and m[i-1][j] == 0 and maze[i-1][j] == 0:
                    m[i-1][j] = k + 1
                if j>0 and m[i][j-1] == 0 and maze[i][j-1] == 0:
                    m[i][j-1] = k + 1
                if i<len(m)-1 and m[i+1][j] == 0 and maze[i+1][j] == 0:
                    m[i+1][j] = k + 1
                if j<len(m[i])-1 and m[i][j+1] == 0 and maze[i][j+1] == 0:
                    m[i][j+1] = k + 1

    return m

#and m[exits[1][0]][exits[1][1]] == 0 and m[exits[2][0]][exits[2][1]]==0
def stepping_in_maze():
    m = empty_maze()
    walls, maze, exits, start = format_maze()
    k = 0
    while m[exits[0][0]][exits[0][1]] == 0 :
        k += 1 
        m = make_step(k, m)
    
    return m
    
#selvitetään missä lähin uloskäynti on ja palautetaan sen koordinaatit
def nearest_exit():
    nearestEnd = 0,0
    m = stepping_in_maze()
    walls, maze, exits, start = format_maze()
    for exit in exits:
        if m[exit[0]][exit[1]] != 0:
            nearestEnd = exit[0],exit[1]      
    i, j = nearestEnd

    return i,j

#palauttaa kuljettavan reitin alusta loppuun
def path():
    i, j = nearest_exit()
    m = stepping_in_maze()
    k = m[i][j]
    path = [(i,j)]
    while k > 1:
        if i > 0 and m[i - 1][j] == k-1:
            i, j = i-1, j
            path.append((i, j))
            k-=1
        elif j > 0 and m[i][j - 1] == k-1:
            i, j = i, j-1
            path.append((i, j))
            k-=1
        elif i < len(m) - 1 and m[i + 1][j] == k-1:
            i, j = i+1, j
            path.append((i, j))
            k-=1
        elif j < len(m[i]) - 1 and m[i][j + 1] == k-1:
            i, j = i, j+1
            path.append((i, j))
            k -= 1
        
    return path

def print_maze():
    maze = get_maze()
    route = path()
    
    for i in route:
        maze[i[0]][i[1]] = '.'

    np.savetxt("labyrintti.txt", maze, fmt='%s')
    


