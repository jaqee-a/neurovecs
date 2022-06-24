from operator import length_hint
from sim import drop
from sim2 import drop2
import matplotlib.pyplot as plt

def write(a, file):
    f = open(file, 'w')
    for e in a :
        f.write(str(e)+" ")
    f.close()

def read():
    f = open("tex.txt", 'r')
    e = f.read()
    l = e.split(' ')
    for i in range(len(l)):
        if l[i] != '' :
           l[i] = float(l[i])
        else :
            l.pop(i)


t, d, e, f = drop()
t1,d1,e1,f1 = drop2()

write(t, 't.txt')
write(d, 'd.txt')
write(e, 'e.txt')
write(f, 'f.txt')


write(t1, 't1.txt')
write(d1, 'd1.txt')
write(e1, 'e1.txt')
write(f1, 'f1.txt')



plt.plot(t, d, label="Force")
plt.plot(t1, d1, label="Proposal")

plt.xlim([60, 500])
plt.xlabel("Time (s)")
plt.ylabel("Data rate (Mbps)")
#plt.ylabel("User Connectivity (%)")

plt.legend()

"""
plt.plot(t, f, label="Force")
plt.plot(t1, f1, label="Proposal")

plt.xlim([60, 500])
plt.xlabel("Time (s)")
plt.ylabel("Standard deviation")

plt.legend()"""

plt.show()