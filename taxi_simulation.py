
# UD_Functions
def dist(start, end):
    D = 0
    for i in range(min(start, end), max(start, end)):
        D += distance[i]
    return D


def fare(d):
    if (d <= K):
        return I
    else:
        return I + (d - K) * X


def timetrvl(start, end):
    ad_mins = 0
    for i in range(min(start, end), max(start, end)):
        ad_mins += time[i]
    return ad_mins


def timeadd(bgtim, ad_mins):
    hr, mn = map(int, bgtim.split(':'))
    mn += ad_mins
    while (mn >= 60):
        hr += 1
        mn -= 60
    if (hr >= 24):
        hr -= 24
    return str(hr).zfill(2) + ':' + str(mn).zfill(2)


def neartaxi(start):
    d = []
    if (start > 0):
        for i in range(start, P + 1):
            if (i in taxi.values() and dist(i, start) <= Y):
                for j in sorted(taxi.keys()):
                    if (i == taxi[j]):
                        d.append(j)
        for i in range(start - 1, 0, -1):
            if (i in taxi.values() and dist(i, start) <= Y):
                for j in sorted(taxi.keys()):
                    if (i == taxi[j]):
                        d.append(j)
    return d


def taxiassign(start, tme):
    d = neartaxi(start)
    di = {}
    for i in d:
        if (txavil[i] < tme):
            di[i] = dist(start, taxi[i])
    if (len(di) == 0):
        return 'REJECTED'
    if (len(di) == 1):
        for i, j in di.items():
            return i
    else:
        if (sorted(di.values())[0] == sorted(di.values())[1]):
            tx = 0
            small = 999999
            for i in sorted(di.keys()):
                if (revnue[i] < small):
                    tx = i
                    small = revnue[i]
            del small
            if (tx > 0):
                return tx
            else:
                return 'REJECTED'
        else:
            small = sorted(di.values())[0]
            for i in sorted(di.keys()):
                if (di[i] == small):
                    return i


def form(s):
    s = s.replace("\\", "/")
    s = s.replace('\"', '')
    return s


# UD_Functions
# Input_Block
file = open(form(input()), 'r')
N, P = map(int, file.readline().split())
distance = {}
time = {}
temp = list(map(int, file.readline().split()))
for i in range(1, P):
    distance[i] = temp[i - 1]
temp = list(map(int, file.readline().split()))
for i in range(1, P):
    time[i] = temp[i - 1]
K, I, X, Y = map(int, file.readline().split())
B = int(file.readline())
Bookings = []
for i in range(B):
    Bookings.append(list(file.readline().split()))
for i in range(B):
    for j in range(4):
        if (j == 1 or j == 2):
            Bookings[i][j] = int(Bookings[i][j])
taxi = {}
for i in range(N):
    taxi[i + 1] = 1
revnue = {}
for i in range(N):
    revnue[i + 1] = 0
txavil = {}
for i in range(N):
    txavil[i + 1] = '00:00'
op_file = open(r"D:\COLLEGE\SEM 5\NPTEL\Taxi simultion Project\Testcases\output.txt", 'a')
op_file.truncate(0)
# Input_Block
# working_code
for buk in Bookings:
    asintx = taxiassign(buk[1], buk[3])
    if (asintx != 'REJECTED'):
        bill = fare(dist(buk[1], buk[2]))
        endtim = timeadd(buk[3], (timetrvl(taxi[asintx], buk[1]) + timetrvl(buk[1], buk[2])))
        taxi[asintx] = buk[2]
        txavil[asintx] = endtim
        revnue[asintx] += bill
        _asx = 'Taxi-' + str(asintx)
        print(buk[0], _asx, bill, endtim)
        op_file.writelines(buk[0] + ' ' + _asx + " " + str(bill) + " " + endtim + '\n')
    else:
        print(buk[0], 'REJECTED')
        op_file.writelines(buk[0] + ' ' + 'REJECTED' + '\n')
file.close()
op_file.close()
