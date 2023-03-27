import math
import time
import tkinter
import tkinter.font
import tkinter.messagebox
import mazegen
import ktinter
# from PIL import ImageGrab

sz = 75
n = 7
m = 11
points = []
kc = 0
pt = [[0, 0], [0, 0]]
trace = []
mt = []
dothi = []
line = []
kt = []
cnt = 0
chedo = 0
dh = False
wdth = 1050
hght = 645
tgian = 0


def ktt(x1, y1, x2, y2, x3, y3, x4, y4):
    if ktinter.intersect(x1, y1, x2, y2, x3, y3, x4, y4) == 1: return 1
    else: return 0


def add(x, y):
    points.append([x, y])
    kt[x][y] = 1


def mdl(x1, y1, x2, y2, x3, y3):
    if x1 <= x2 and max(y2, y3) >= y1 >= min(y2, y3): return 1
    else: return 0


def indothi(x, y):
    dem = 0
    for ii in range(len(line)):
        x1 = line[ii][1] * sz; y1 = sz * (line[ii][0] - 1)
        x2 = line[ii][3] * sz; y2 = sz * (line[ii][2] - 1)
        dem += mdl(x, y, x1, y1, x2, y2)
    if dem % 2 == 1: return True
    else: return False


def dijsktra():
    global kc
    l = len(points) + 2
    trace.clear()
    for i in range(0, l + 1):
        trace.append(0)
    dist = [1e7] * l
    dist[0] = 0
    trace[0] = -1
    visit = [False] * l

    for ii in range(l):
        mn = 1e7
        for i in range(0, l):
            if visit[i] == False and dist[i] < mn:
                mn = dist[i]
                u = i
        visit[u] = True

        for v in range(0, l):
            if mt[u][v] > 0 and visit[v] == False and dist[v] > dist[u] + mt[u][v]:
                dist[v] = dist[u] + mt[u][v]
                trace[v] = u
    kc = dist[l - 1]


class gui:
    def __init__(self):
        self.main = tkinter.Tk()

        self.dau = tkinter.Canvas(self.main, height=10)
        self.dau.pack()

        self.tp1 = tkinter.Frame(self.main)
        self.tp1.pack()

        self.bt1 = tkinter.Frame(self.main)
        self.canvas = tkinter.Canvas(self.main, width=wdth, height=hght)
        self.canvas.create_rectangle(50, 10, wdth - 50, hght - 35, fill='white')

        self.canvas.pack()
        self.bt1.pack()

        self.btn1 = tkinter.Button(self.tp1, text='Generate Map', command=self.gen)
        self.btn1.pack(side='left')

        self.btn3 = tkinter.Button(self.tp1, text='Show', command=self.chg)
        self.btn3.pack(side='left')

        self.btn2 = tkinter.Button(self.tp1, text='Find', command=self.xl)
        self.btn2.pack(side='left')

        self.txt1 = tkinter.Label(self.bt1, text='Distance: ')
        self.txt1.pack(side='left')
        self.dxt = tkinter.StringVar()
        self.txt2 = tkinter.Label(self.bt1, textvariable=self.dxt)
        self.txt2.pack(side='left')

        self.txt3 = tkinter.Label(self.bt1, text='Time: ')
        self.txt3.pack(side='left')
        self.tme = tkinter.StringVar()
        self.txt4 = tkinter.Label(self.bt1, textvariable=self.tme)
        self.txt4.pack(side='left')

        self.day = tkinter.Canvas(self.main, height=10)
        self.day.pack()

        self.canvas.bind('<Button-1>', self.draw)

        tkinter.mainloop()

    def dtrace(self):
        v = len(points) + 1
        if len(trace) < v: return
        u = trace[v]
        while u != -1 and v != -1:
            if v == len(points) + 1: x1 = pt[1][0]; y1 = pt[1][1]
            else: x1 = sz * points[v - 1][1]; y1 = 10 + sz * (points[v - 1][0] - 1)

            if u == 0: x2 = pt[0][0]; y2 = pt[0][1]
            else: x2 = sz * points[u - 1][1]; y2 = 10 + sz * (points[u - 1][0] - 1)

            self.canvas.create_line(x1, y1, x2, y2, fill='orange', width=3)
            v = u
            u = trace[v]

    def ve(self):
        self.dmap()
        self.grid()
        self.dclick()
        dijsktra()
        self.ddothi()
        self.dpt()

    def chg(self):
        global chedo, dh
        chedo ^= 1
        if chedo == 1:
            self.ddothi()
            if dh: self.dtrace()
        else:
            self.ve()
            if dh: self.dtrace()

    def dclick(self):
        global cnt
        if pt[0][0] == 0: return
        z = 5
        self.canvas.create_oval(pt[cnt][0] - z, pt[cnt][1] - z, pt[cnt][0] + z, pt[cnt][1] + z, fill='white', width=0)
        myfont = tkinter.font.Font(family='Arial', size=8, weight='bold')
        tmp1 = str(pt[0][0]) + ', ' + str(pt[0][1])
        tmp2 = str(pt[1][0]) + ', ' + str(pt[1][1])

        if cnt == 0:
            self.canvas.create_oval(pt[cnt][0] - z, pt[cnt][1] - z, pt[cnt][0] + z, pt[cnt][1] + z, fill='red', width=0)
            self.canvas.create_text(pt[cnt][0] + 10, pt[cnt][1] + 13, text=tmp1, fill='black', font=myfont)
            x1 = pt[0][0]; y1 = pt[0][1]

            for i in range(0, len(points)):
                mt[0][i + 1] = mt[i + 1][0] = 0
                x2 = sz * points[i][1]; y2 = 10 + sz * (points[i][0] - 1)
                tmpp = True
                for ii in range(0, len(line)):
                    x3 = sz * line[ii][1]; y3 = 10 + sz * (line[ii][0] - 1)
                    x4 = sz * line[ii][3]; y4 = 10 + sz * (line[ii][2] - 1)
                    if ktt(x1, y1, x2, y2, x3, y3, x4, y4) == 1:
                        tmpp = False
                        break

                if tmpp: mt[0][i + 1] = mt[i + 1][0] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            if pt[1][0] != 0 or pt[1][1] != 0:
                mt[0][len(points) + 1] = mt[len(points) + 1][0] = 0
                self.canvas.create_oval(pt[1][0] - z, pt[1][1] - z, pt[1][0] + z, pt[1][1] + z, fill='green', width=0)
                self.canvas.create_text(pt[1][0] + 10, pt[1][1] + 13, text=tmp2, fill='black', font=myfont)
                x2 = pt[1][0]; y2 = pt[1][1]
                tmpp = True
                for ii in range(0, len(line)):
                    x3 = sz * line[ii][1]; y3 = 10 + sz * (line[ii][0] - 1)
                    x4 = sz * line[ii][3]; y4 = 10 + sz * (line[ii][2] - 1)
                    if ktt(x1, y1, x2, y2, x3, y3, x4, y4) == 1:
                        tmpp = False
                        break
                if tmpp: mt[0][len(points) + 1] = mt[len(points) + 1][0] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            cnt = 1
        else:
            mt[0][len(points) + 1] = mt[len(points) + 1][0] = 0
            x1 = pt[1][0]; y1 = pt[1][1]
            for i in range(0, len(points)):
                mt[len(points) + 1][i + 1] = mt[i + 1][len(points) + 1] = 0
                x2 = sz * points[i][1]; y2 = 10 + sz * (points[i][0] - 1)
                tmpp = True
                for ii in range(0, len(line)):
                    x3 = sz * line[ii][1]; y3 = 10 + sz * (line[ii][0] - 1)
                    x4 = sz * line[ii][3]; y4 = 10 + sz * (line[ii][2] - 1)
                    if ktt(x1, y1, x2, y2, x3, y3, x4, y4) == 1:
                        tmpp = False
                        break

                if tmpp: mt[len(points) + 1][i + 1] = mt[i + 1][len(points) + 1] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            x2 = pt[0][0]; y2 = pt[0][1]
            tmpp = True
            for ii in range(0, len(line)):
                x3 = sz * line[ii][1]; y3 = 10 + sz * (line[ii][0] - 1)
                x4 = sz * line[ii][3]; y4 = 10 + sz * (line[ii][2] - 1)
                if ktt(x1, y1, x2, y2, x3, y3, x4, y4) == 1:
                    tmpp = False
                    break
            if tmpp: mt[0][len(points) + 1] = mt[len(points) + 1][0] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            self.canvas.create_oval(pt[cnt][0] - z, pt[cnt][1] - z, pt[cnt][0] + z, pt[cnt][1] + z, fill='green', width=0)
            self.canvas.create_text(pt[cnt][0] + 10, pt[cnt][1] + 13, text=tmp2, fill='black', font=myfont)
            self.canvas.create_oval(pt[0][0] - z, pt[0][1] - z, pt[0][0] + z, pt[0][1] + z, fill='red', width=0)
            self.canvas.create_text(pt[0][0] + 10, pt[0][1] + 13, text=tmp1, fill='black', font=myfont)
            cnt = 0

    def draw(self, event):
        global dh
        x = event.x; y = event.y
        dh = False
        if indothi(x, y):
            pt[cnt][0] = x
            pt[cnt][1] = y
            self.ve()

    def ddothi(self):
        global chedo
        if chedo == 1:
            for i in range(0, len(dothi)):
                self.canvas.create_line(dothi[i][1], dothi[i][0], dothi[i][3], dothi[i][2], fill='yellow', width=1)
            if pt[0][0] != 0:
                for i in range(0, len(points)):
                    if mt[0][i + 1] != 0:
                        self.canvas.create_line(pt[0][0], pt[0][1], sz * points[i][1], sz * (points[i][0] - 1) + 10, fill='blue', width=1)
            if pt[1][0] != 0:
                for i in range(0, len(points)):
                    if mt[len(points) + 1][i + 1] != 0:
                        self.canvas.create_line(pt[1][0], pt[1][1], sz * points[i][1], sz * (points[i][0] - 1) + 10, fill='blue', width=1)
            if mt[0][len(points) + 1] != 0:
                self.canvas.create_line(pt[0][0], pt[0][1], pt[1][0], pt[1][1], fill='blue', width=1)

    def dmap(self):
        self.canvas.delete('all')
        global cnt
        arr = mazegen.gtar()
        self.canvas.create_rectangle(50, 10, wdth - 50, hght - 35, fill='white')
        for i in range(1, n + 2):
            for j in range(1, m + 2):
                if arr[i][j] == '#':
                    self.canvas.create_rectangle(sz * j, 10 + sz * (i - 1), sz * (j + 1), 10 + sz * i, fill='grey', width=0)
        self.canvas.create_line(50, 10, wdth - 50, 10)
        self.canvas.create_line(50, 10, 50, hght - 35)

    def dpt(self):
        myfont = tkinter.font.Font(family='Arial', size=8, weight='bold')
        for i in range(0, len(points)):
            tam = points[i]
            self.canvas.create_oval(sz * tam[1] - 3, 7 + sz * (tam[0] - 1), sz * tam[1] + 3, 13 + sz * (tam[0] - 1), fill='black')
            tmp = str(sz * tam[1]) + ', ' + str(sz * (tam[0] - 1))
            self.canvas.create_text(sz * tam[1] + 10, sz * (tam[0] - 1) + 20, text=i + 1, fill='black', font=myfont)

    def grid(self):
        myfont = tkinter.font.Font(family='Arial', size=8, weight='bold')
        for i in range(1, n + 3):
            for j in range(1, m + 3):
                if j == m + 2:
                    if i == n + 1: self.canvas.create_text(sz * j + 10, 20 + sz * i, text=sz * (j - 1), font=myfont)
                    break
                if i == n + 1:
                    self.canvas.create_text(sz * j + 10, 20 + sz * i, text=sz * (j - 1), font=myfont)
                if i == n + 2:
                    self.canvas.create_text(sz * j - 12, 20 + sz * (i - 1), text=sz * (i - 1), font=myfont)
                    break
                if j == 1:
                    self.canvas.create_text(sz * j - 12, 20 + sz * (i - 1), text=sz * (i - 1), font=myfont)
                self.canvas.create_rectangle(sz * j, 10 + sz * (i - 1), sz * (j + 1), 10 + sz * i, width=1)

    def gen(self):
        global cnt, tgian
        strt = time.time()
        mazegen.reset()
        arr = mazegen.gtar()
        mt.clear()
        points.clear()
        line.clear()
        dothi.clear()
        pt[0][0] = pt[0][1] = pt[1][0] = pt[1][1] = cnt = 0

        for i in range(0, n + 3):
            kt.insert(i, [])
            for j in range(0, m + 3):
                kt[i].insert(j, 0)

        self.canvas.create_rectangle(50, 10, wdth - 50, hght - 35, fill='white')

        for i in range(1, n + 2):
            for j in range(1, m + 2):
                if arr[i][j] == '#':
                    self.canvas.create_rectangle(sz * j, 10 + sz * (i - 1), sz * (j + 1), 10 + sz * i, fill='grey', width=0)

                    if arr[i - 1][j - 1] == '.' and arr[i - 1][j] == arr[i][j - 1]: add(i, j)
                    if arr[i - 1][j + 1] == '.' and arr[i - 1][j] == arr[i][j + 1]: add(i, j + 1)
                    if arr[i + 1][j + 1] == '.' and arr[i + 1][j] == arr[i][j + 1]: add(i + 1, j + 1)
                    if arr[i + 1][j - 1] == '.' and arr[i][j - 1] == arr[i + 1][j]: add(i + 1, j)

        slp = len(points)
        for i in range(0, slp + 3):
            mt.insert(i, [])
            for j in range(0, slp + 3):
                mt[i].insert(j, 0)

        pv = dx = -1
        for i in range(1, n + 2):
            for j in range(1, m + 2):
                if pv == -1:
                    if kt[i][j] == 1: pv = j
                elif kt[i][j] == 1:
                    dx = j
                    line.append([i, pv, i, dx])
                    dothi.append([10 + sz * (i - 1), sz * pv, 10 + sz * (i - 1), sz * dx])
                    pv = -1

        for j in range(1, m + 2):
            for i in range(1, n + 2):
                if pv == -1:
                    if kt[i][j] == 1: pv = i
                elif kt[i][j] == 1:
                    dx = i
                    line.append([pv, j, dx, j])
                    dothi.append([10 + sz * (pv - 1), sz * j, 10 + sz * (dx - 1), sz * j])
                    pv = -1

        for i in range(0, len(points) - 1):
            for j in range(i + 1, len(points)):
                x = 0; y = 0
                if points[i][1] < points[j][1]:
                    y = points[i][1]
                    if points[i][0] < points[j][0]: x = points[i][0]
                    else: x = points[i][0] - 1
                else:
                    y = points[j][1]
                    if points[i][0] < points[j][0]: x = points[j][0] - 1
                    else: x = points[j][0]

                x1 = sz * points[i][1]; y1 = 10 + sz * (points[i][0] - 1)
                x2 = sz * points[j][1]; y2 = 10 + sz * (points[j][0] - 1)

                tmpp = True
                for ii in range(0, len(line)):
                    x3 = sz * line[ii][1]; y3 = 10 + sz * (line[ii][0] - 1)
                    x4 = sz * line[ii][3]; y4 = 10 + sz * (line[ii][2] - 1)
                    if arr[x][y] != '#':
                        if ktt(x1, y1, x2, y2, x3, y3, x4, y4) == 1:
                            tmpp = False
                            break
                    elif min(x1, x2) == min(x3, x4) and max(x1, x2) == max(x3, x4) and min(y1, y2) == min(y3, y4) and max(y1, y2) == max(y3, y4):
                        tmpp = True
                        break
                    else: tmpp = False
                if tmpp:
                    mt[i + 1][j + 1] = mt[j + 1][i + 1] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    dothi.append([y1, x1, y2, x2])

        self.grid()
        self.ddothi()
        self.dpt()
        self.canvas.create_line(50, 10, wdth - 50, 10)
        self.canvas.create_line(50, 10, 50, hght - 35)
        tgian = time.time() - strt

    def xl(self):
        global dh, kc, tgian
        if pt[0][0] != 0 and pt[1][0] != 0:
            dh = True
            strt = time.time()
            dijsktra()
            self.dtrace()
            self.tme.set(time.time() - strt + tgian)
            self.dxt.set(kc)


ttt = gui()
