import numpy as np
#hakee ja palauttaa tiedostosta sokkelon
def get_maze():
    data = open("maze-task-first.txt", "r")
    lines = data.readlines()
    maze = [list(i.strip()) for i in lines]
    return maze

#loopataan kaksiulotteinen taulukko läpi ja muutetaan
#sokkelo ykkösiksi ja nolliksi
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

#metodi palauttaa taulukon, jossa on tyhjä labyrintti
#taulukossa numero 1 on aloituspaikka
def empty_maze():
    walls, maze, exits, start = format_maze()
    empty_maze = []
    for i in range(len(maze)):
        empty_maze.append([])
        for j in range(len(maze[i])):
            empty_maze[-1].append(0)
    i,j = start
    empty_maze[i][j] = 1
    #print(empty_maze)
    return empty_maze

#funktiolle annetaan parametrina arvot k ja mz, funktiossa on kaksi sisäkkäistä
#looppia, jos parametrin mz[i][j] arvot ovat samat kuin k arvo
#katsotaan onko ympäröivä arvo 0 eli tyhjä ruutu
def make_step(k, mz):
    walls, maze, exits, start = format_maze()

    for i in range(len(mz)):
        for j in range(len(mz[i])):
            if mz[i][j] == k:
                if i>0 and mz[i-1][j] == 0 and maze[i-1][j] == 0:
                    mz[i-1][j] = k + 1
                if j>0 and mz[i][j-1] == 0 and maze[i][j-1] == 0:
                    mz[i][j-1] = k + 1
                if i<len(mz)-1 and mz[i+1][j] == 0 and maze[i+1][j] == 0:
                    mz[i+1][j] = k + 1
                if j<len(mz[i])-1 and mz[i][j+1] == 0 and maze[i][j+1] == 0:
                    mz[i][j+1] = k + 1

    return mz

#Pitää muokata metodia toistamaan looppi niin monta kertaa,
#kun sokkelossa on uloskäyntejä
#and mz[exits[1][0]][exits[1][1]] == 0 and mz[exits[2][0]][exits[2][1]]==0
def stepping_in_maze():
    mz = empty_maze()
    walls, maze, exits, start = format_maze()
    k = 0
    while mz[exits[0][0]][exits[0][1]] == 0 :
        k += 1
        print(mz)
        mz = make_step(k, mz)
    
    return mz
    
#selvitetään missä lähin uloskäynti on ja palautetaan sen koordinaatit
def nearest_exit():
    nearestEnd = 0,0
    mz = stepping_in_maze()
    walls, maze, exits, start = format_maze()
    for exit in exits:
        if mz[exit[0]][exit[1]] != 0:
            nearestEnd = exit[0],exit[1]      
    i, j = nearestEnd

    return i,j

#palauttaa kuljettavan reitin alusta loppuun
#funktiossa määritellään muuttuja exit, joka on ulospääsy.
#Etsitään viereinen arvo exit-1, siirrytään siihen
#vähennetään exit-arvoa yhdellä
#samaa toistetaan, kunnes exit-arvo on lähdön arvo
def path():
    i, j = nearest_exit()
    m = stepping_in_maze()
    exit = m[i][j]
    path = [(i,j)]
    steps = 0
    while exit > 1:
        steps += 1
        if i > 0 and m[i - 1][j] == exit-1:
            i, j = i-1, j
            path.append((i, j))
            exit-=1
        elif j > 0 and m[i][j - 1] == exit-1:
            i, j = i, j-1
            path.append((i, j))
            exit-=1
        elif i < len(m) - 1 and m[i + 1][j] == exit-1:
            i, j = i+1, j
            path.append((i, j))
            exit-=1
        elif j < len(m[i]) - 1 and m[i][j + 1] == exit-1:
            i, j = i, j+1
            path.append((i, j))
            exit -= 1
     
    return path, steps

#metodissa edellä tehty kokonaisuus tulostetaan
#tiedostoon nimeltä labyrintti.txt
def print_maze():
    maze = get_maze()
    route, steps = path()

    steps = 0
    for i in route:
        maze[i[0]][i[1]] = '.'
        steps += 1
    
    maze[i[0]][i[1]] = '^'
    print(f"{steps} steps taken")

    np.savetxt("labyrintti.txt", maze, fmt='%s')
    