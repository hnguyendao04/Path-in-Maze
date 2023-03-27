import random

arr = []
n = 7
m = 11


def reset():
    arr.clear()
    for i in range(0, n + 3):
        arr.insert(i, [])
        for j in range(0, m + 3):
            arr[i].insert(j, '#')

    q = [[2, 2, 0]]

    while len(q) > 0:
        t = random.choice(q)
        q.remove(t)
        if arr[t[0]][t[1]] == '.' or chk(t[0], t[1], t[2]) == 0: continue
        arr[t[0]][t[1]] = '.'
        temp(t[0] - 1, t[1], 1, q)
        temp(t[0] + 1, t[1], 2, q)
        temp(t[0], t[1] - 1, 3, q)
        temp(t[0], t[1] + 1, 4, q)

    for i in range(1, n + 2):
        for j in range(1, m + 2):
            print(arr[i][j], end='')
        print()


def chk(x, y, h):
    if h == 1:
        if arr[x][y - 1] == '.' or arr[x - 1][y - 1] == '.' or arr[x - 1][y] == '.' or arr[x - 1][y + 1] == '.' or arr[x][y + 1] == '.': return 0
        else: return 1
    elif h == 2:
        if arr[x][y - 1] == '.' or arr[x + 1][y - 1] == '.' or arr[x + 1][y] == '.' or arr[x + 1][y + 1] == '.' or arr[x][y + 1] == '.': return 0
        else: return 1
    elif h == 3:
        if arr[x][y - 1] == '.' or arr[x - 1][y - 1] == '.' or arr[x - 1][y] == '.' or arr[x + 1][y] == '.' or arr[x + 1][y - 1] == '.': return 0
        else: return 1
    else:
        if arr[x - 1][y] == '.' or arr[x - 1][y + 1] == '.' or arr[x][y + 1] == '.' or arr[x + 1][y + 1] == '.' or arr[x + 1][y] == '.': return 0
        else: return 1


def check(x, y, h):
    if x == 1 or y == 1 or x == n + 1 or y == m + 1 or arr[x][y] == '.' or chk(x, y, h) == 0: return 0
    else: return 1


def temp(x, y, h, q):
    if check(x, y, h) == 1:
        q.append([x, y, h])


def gtar():
    return arr
