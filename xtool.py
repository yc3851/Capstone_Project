import sys

f = open('xnames.asc',"rt")
if f.mode != "rt":
    f.close()
    sys.exit(0)

names = f.readlines()
f.close()

sorted_names = []
for x in names:
    sorted_names.append(x[:-1])

a = len(sorted_names)
for i in range(a-1,-1,-1):
    for j in range(i):
        if sorted_names[j] > sorted_names[j+1]:
            t = sorted_names[j]
            sorted_names[j] = sorted_names[j+1]
            sorted_names[j+1] = t
        if sorted_names[j] == sorted_names[j+1]:
            print("duplicate names",sorted_names[j])
            sys.exit(0)

max = 0
for x in sorted_names:
    if len(x) > max:
        max = len(x)
max += 5

f1 = open("xnames.py","wt")
f1.write('# define values of x_names\n')
ind = 1
for x in sorted_names:
    y = x
    d = max - len(x)
    for i in range(d):
        y = y+' '
    y = y+"="+str(ind)
    ind += 1
    y = y+'\n'
    f1.write(y)

f1.write('\n')
f1.write('def ss(i):\n')
first = True
for x in sorted_names:
    if first:
        f1.write("    if i.nodeid == "+x+":\n")
        first = False
    else:
        f1.write("    elif i.nodeid == "+x+":\n")
    f1.write("        return '"+x+"'\n")
f1.write("    else:\n")
f1.write("        return '????({})'.format(i.nodeid)\n")
f1.write("#end ss\n")

f1.close()
print('xnames.py done')
