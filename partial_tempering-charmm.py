#!/opt/local/bin/python

import sys, numpy

def get_dihparam(type1,type2,type3,type4,dih_dict):

    if dih_dict.has_key((type1,type2,type3,type4)):
        return dih_dict[(type1,type2,type3,type4)]
    if dih_dict.has_key((type4,type3,type2,type1)):
        return dih_dict[(type4,type3,type2,type1)]
    if dih_dict.has_key(('X',type2,type3,'X')):
        return dih_dict[('X',type2,type3,'X')]
    if dih_dict.has_key(('X',type3,type2,'X')):
        return dih_dict[('X',type3,type2,'X')]

def get_impparam(type1,type2,type3,type4,imp_dict):

    if imp_dict.has_key((type1,type2,type3,type4)):
        return imp_dict[(type1,type2,type3,type4)]
    if imp_dict.has_key((type1,'X','X',type4)):
        return imp_dict[(type1,'X','X',type4)]
    if imp_dict.has_key((type4,'X','X',type1)):
        return imp_dict[(type4,'X','X',type1)]

    return 0,0

inf=open(sys.argv[1],'r')
ouf=open(sys.argv[2],'w')
scale=float(sys.argv[3])
rscale=numpy.sqrt(scale)

lines=inf.readlines()

## find important bits in input top file

atom_types={}
pair_types={}
bond_types={}
constraint_types={}
angle_types={}
dihedral_types={}
improper_types={}
implicit_genborn_params={}
cmap_types={}

iatomtypes_start=lines.index('[ atomtypes ]\n')
ipairtypes_start=lines.index('[ pairtypes ]\n')
ibondtypes_start=lines.index('[ bondtypes ]\n')
iangletypes_start=lines.index('[ angletypes ]\n')
idihtypes_start=lines.index('[ dihedraltypes ]\n')
igbtypes_start=lines.index('[ implicit_genborn_params ]\n')
icmaptypes_start=lines.index('[ cmaptypes ]\n')
inbtype_start=lines.index('[ nonbond_params ]\n')
imoletype_start=lines.index('[ moleculetype ]\n')

## write out header information (unaltered)
for i in range(iatomtypes_start):
    print >> ouf, lines[i][:-1]

## edit atomtypes section
print  >> ouf, "[ atomtypes ]"
for i in range(iatomtypes_start+1,ipairtypes_start-1):
    line=lines[i][:-1]
    if line[0]==';':
        print >> ouf, line
        continue

    data=line.split()
    aname=data[0]
    atnum=int(data[1])
    mass=float(data[2])
    charge=float(data[3])
    ptype=data[4]
    sig=float(data[5])
    eps=float(data[6])
    print >> ouf, "%s %4i %8.3f %8.3f %s %8.4f %8.4f" % (aname,atnum,mass,charge,ptype,sig,eps)
    eps*=scale
    print >> ouf, "%s %s %8.3f %8.3f %s %8.4f %8.4f" % (aname+'_',aname,mass,charge,ptype,sig,eps)

## edit pairtypes section
print  >> ouf, "[ pairtypes ]"
for i in range(ipairtypes_start+1,ibondtypes_start):
    line=lines[i][:-1]
    if line[0]==';':
        print >> ouf, line
        continue

    data=line.split()
    aname1=data[0]
    aname2=data[1]
    sig=float(data[3])
    eps=float(data[4])

    print >> ouf, "%s %s 1 %8.4f %8.4f" % (aname1,aname2,sig,eps)
    print >> ouf, "%s %s 1 %8.4f %8.4f" % (aname1,aname2+'_',sig,rscale*eps)
    print >> ouf, "%s %s 1 %8.4f %8.4f" % (aname1+'_',aname2,sig,rscale*eps)
    print >> ouf, "%s %s 1 %8.4f %8.4f" % (aname1+'_',aname2+'_',sig,scale*eps)

## write out stuff leading up to dihedral data (unaltered)
for i in range(ibondtypes_start,idihtypes_start-1):
    if len(lines[i])>0:
        print >> ouf, lines[i][:-1]

## read in diheral data
dih=True
imp=False
print >> ouf, "[ dihedraltypes ]"
for i in range(idihtypes_start+1,igbtypes_start-1):
    if dih and len(lines[i])==0:
        dih=False
        imp=True
    print >> ouf, lines[i][:-1]
    if lines[i]=='\n':
        continue
    if lines[i][0]==';':
        continue
    if lines[i][:-1]=='[ dihedraltypes ]':
        dih=False
        imp=True
        continue
    data=lines[i].split()
    [atom1,atom2,atom3,atom4]=[a for a in data[:4]]
    if dih:
        phi=float(data[5])
        k=float(data[6])
        multi=int(data[7])
        dihedral_types[atom1,atom2,atom3,atom4]=[phi,k,multi]
    elif imp:
        phi=float(data[5])
        k=float(data[6])
        improper_types[atom1,atom2,atom3,atom4]=[phi,k]

## write out generalisedborn stuff (unaltered)
for i in range(igbtypes_start,icmaptypes_start-1):
    print >> ouf, lines[i][:-1]

## write out cmap stuff (scaled)
print >> ouf, "[ cmaptypes ]"
print >> ouf

for i in range(icmaptypes_start+2,inbtype_start-3):
    if lines[i]=='\n':
        print >> ouf
        continue
    if lines[i][0]=='C':
        print >> ouf, lines[i][:-1]
        continue
    data=lines[i][:-2].split()
    if len(data)==10:
        line_out=''
        for d in data:
            line_out=line_out+" %8.4f" % (scale*float(d))
        line_out=line_out+'\\'
    else:
        line_out=''
        for d in data:
            line_out=line_out+" %8.4f" % (scale*float(d))
    print >> ouf, line_out

## write out NBfix stuff (unaltered)
for i in range(inbtype_start-2,imoletype_start):
    print >> ouf, lines[i][:-1]

## scan through file until atom types are found
for istop in range(imoletype_start,100000):
    print >> ouf, lines[istop]
    if lines[istop]=='[ atoms ]\n':
        break
iatoms=istop

atom_types=[]
print >> ouf, '[ atoms ]'
for i in range(iatoms+1,iatoms+10000):

    if lines[i]=='\n':
        print >> ouf
        break
    if lines[i][0]==';':
        print >> ouf, lines[i][:-1]
        continue
    data=lines[i].split()
    serial=int(data[0])
    atype=data[1]
    ires=int(data[2])
    resname=data[3]
    aname=data[4]
    q=rscale*float(data[6])
    mass=float(data[7])
    atom_types.append(data[1])

    print >> ouf, "%6d  %5s  %6d  %3s  %5s  %6d %8.3f  %8.3f " % (serial,atype,ires,resname,aname,serial,q,mass)

ibonds=i+2
print >> ouf, '[ bonds ]'
for i in range(ibonds,ibonds+100000):
    print >> ouf, lines[i][:-1]
    if lines[i]=='[ dihedrals ]\n':
        break

idihedrals=i+1
for i in range(idihedrals,idihedrals+100000):

    if lines[i]=='\n':
        print >> ouf
        break

    if lines[i][0]==';':
        print >> ouf, lines[i][:-1]
        continue
    data=lines[i].split()
    i1=int(data[0])
    i2=int(data[1])
    i3=int(data[2])
    i4=int(data[3])
    type1=atom_types[i1-1][:-1]
    type2=atom_types[i2-1][:-1]
    type3=atom_types[i3-1][:-1]
    type4=atom_types[i4-1][:-1]

    phi,k,m=get_dihparam(type1,type2,type3,type4,dihedral_types)
    k*=scale
    print >> ouf, "%4i %4i %4i %4i %4i %8.3f %8.3f %4i" % (i1,i2,i3,i4,9,phi,k,m)

iimp=i+2
print >> ouf, '[ dihedrals ]'
for i in range(iimp,iimp+10000):

    if lines[i]=='\n':
        print >> ouf
        break
    if lines[i][0]==';':
        print >> ouf, lines[i][:-1]
        continue
    data=lines[i].split()

    i1=int(data[0])
    i2=int(data[1])
    i3=int(data[2])
    i4=int(data[3])
    type1=atom_types[i1-1][:-1]
    type2=atom_types[i2-1][:-1]
    type3=atom_types[i3-1][:-1]
    type4=atom_types[i4-1][:-1]

    phi,k=get_impparam(type1,type2,type3,type4,improper_types)
    k*=scale
    print >> ouf, "%4i %4i %4i %4i %4i %8.3f %8.3f" % (i1,i2,i3,i4,2,phi,k)

## print everything else unaltered to file

for line in lines[i:]:
    print >> ouf, line[:-1]
