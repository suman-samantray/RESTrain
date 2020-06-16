#!/opt/local/bin/python

import sys
inf=open(sys.argv[1],'r')
ouf=open(sys.argv[2],'w')

lines=inf.readlines()


## find lines containing atom data
i1=lines.index("[ atoms ]\n")+2
i2=lines.index("[ bonds ]\n")-1

for line in lines[:i1]:
    print >> ouf, line[:-1]

for line in lines[i1:i2]:
    if line[0]==';':
        print >> ouf, line[:-1]
        continue
    line=line[:17]+'_'+line[18:]
    print >> ouf, line[:-1]
    print line[:-1]

for line in lines[i2:]:
    print >> ouf, line[:-1]
