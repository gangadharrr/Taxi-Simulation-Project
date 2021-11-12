from tkinter import *
from tkinter import ttk
from tkinter import filedialog
global file_add,txtarea,revnue
revnue={}
file_add=''
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
def input_block():
    global K, I, X, Y,N, P,taxi,revnue,time,txavil,distance
    file = open((file_add), 'r')
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
    op_file = open("output.txt", 'a')
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
            _fxf=buk[0] + ' ' + _asx + " " + str(bill) + " " + endtim + '\n'
            txtarea.insert(END,_fxf)
            op_file.writelines(buk[0] + ' ' + _asx + " " + str(bill) + " " + endtim + '\n')
        else:
            _fxf =buk[0] + ' ' + 'REJECTED' + '\n'
            txtarea.insert(END, _fxf)
            op_file.writelines(buk[0] + ' ' + 'REJECTED' + '\n')
    file.close()
    op_file.close()
ws = Tk()
ws.title("TaxiSimulation Project")
ws.geometry("1000x800")
ws['bg']='#fb0'
def mydel():
    try:
        label_1.pack_forget()
    except:
        pass
    try:
        txtarea.delete(1.0,END)
    except:
        pass
    try:
        txtarea2.delete(1.0,END)
    except:
        pass
    try:
        txtarea3.delete(1.0,END)
    except:
        pass
    try:
        pathh.delete(0,END)
    except:
        pass
def openFile():
    global label_1,file_add
    try:
        tf = filedialog.askopenfilename(
        title="Open Text file",
        filetypes=(("Text Files", "*.txt"),)
        )
        pathh.insert(END, tf)
        file_add=tf
        tf = open(tf)
        data = tf.read()
        txtarea2.insert(END, data)
        tf.close()
    except:
        label_1 = Label(ws, fg="red", text="No file selected.")
        label_1.pack(side=RIGHT, pady=10, padx=10)

def rnve():
    strngs=''
    for i in sorted(revnue.keys()):
        strngs+='Taxi-'+str(i)+" = "+str(revnue[i])+'\n'
    txtarea3.insert(END, strngs)

labeltit=Label(text='Taxi Simulation')
labeltit.pack(side=TOP,pady=30)
pathh = Entry(ws)
pathh.pack(side=TOP, expand=False, fill=X, padx=10,pady=20)

Button(
    ws,
    text="Open File",
    command=openFile
    ).pack(side=TOP, padx=20)



runblc=Button(ws,text='RUN',command=input_block)
runblc.pack(side=TOP,pady=10)

rnveblc=Button(ws,text='Revenue',command=rnve)
rnveblc.pack(side=TOP,pady=10)

deletebttn=Button(ws,text='Clear',command=mydel)
deletebttn.pack(side=TOP,pady=10)

button_exit = Button(ws,
                     text = "Exit",
                     command = exit)
button_exit.pack(side=TOP, padx=10)

labelinp=Label(text='Input')
labelinp.pack(side=LEFT,padx=20)
txtarea2 = Text(ws,width=30, height=20)
txtarea2.pack(side=LEFT,padx=10)
labelop=Label(text='Output')
labelop.pack(side=LEFT,padx=10)
txtarea = Text(ws,width=30, height=20)
txtarea.pack(side=LEFT,padx=10)

labelrn=Label(text='Revenue')
labelrn.pack(side=LEFT,padx=10)
txtarea3 = Text(ws,width=30, height=20)
txtarea3.pack(side=LEFT,padx=10)

ws.mainloop()