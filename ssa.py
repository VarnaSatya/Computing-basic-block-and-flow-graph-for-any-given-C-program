from taConv import *
from dom import *
from functools import reduce
import re
import copy

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

def top(x):
    return x[len(x)-1]

def returnVar(s):
    var=[]
    if s.find('goto ')!=-1:
        s=s[:s.find('goto ')]
    for k in re.findall('\w\w*:?',s):
        if k=='if' or k.isnumeric() or ':' in k or k=='φ':
            continue
        var.append(k)
    return var

def initialization(bl):
    count={}
    stack={}
    for a in var:
        count[a]=0
        stack[a]=[]
        stack[a].append(0)
    t1=list(stack.keys())
    t1.sort()
    rename(start,stack,count)


def rename(n,stack,count):
    sOld=copy.deepcopy(n.instr)
    for k in range(len(n.instr)):
        s=' '+n.instr[k]+' '
        n.instr[k]=s
        var=returnVar(s)
        tempVar=var
        if 'φ' not in s:
            if 'if' not in s and len(var)>0:
                tempVar=var[1:]  #replace only varibles that are being used and not defined
            for x in tempVar:
                if x not in stack.keys():
                    continue
                i=top(stack[x])
                n.instr[k]=s.replace(' '+x+' ',' '+x+'_'+str(i)+' ')
                n.instr[k]=n.instr[k].replace('-'+x+' ',' '+x+'_'+str(i)+' ')
                

        #count only assignment and not uses
        if len(var)>0 and 'if' not in s and 'goto' not in s and var[0] in count.keys():
            count[var[0]]=count[var[0]]+1
            i=count[var[0]]
            stack[var[0]].append(i)
            n.instr[k]=n.instr[k].replace(' '+var[0]+' ',' '+var[0]+'_'+str(i)+' ',1)
            n.instr[k]=n.instr[k].replace('\t'+var[0]+' ','\t'+var[0]+'_'+str(i)+' ',1)


    for y in n.child:
        #make all predecessor values into a list instead of set before calling this function for the first time
        j=predecessor[y].index(n)
        for k in range(len(y.instr)):
            line=y.instr[k]
            if 'φ' in line:
                #suppose the jth operand of the φ-function is a
                a=returnVar(line)
                a=a[0]
                if a.find('_')!=-1:
                    a=a[:a.find('_')]
                a=a.strip()
                #j+1 accounting for it with the lhs a present
                ind=findnth(line,a,j+1)
                if ind!=-1 and a in allVar: #so that it actually has that variable
                    y.instr[k]=line[:ind]+a+'_'+str(top(stack[a]))+line[ind+len(a):]
    
    for x in n.dom: #child it wrt dom tree
        if x==n:
            continue
        rename(x,stack,count)

    
    for i in sOld:
        var=returnVar(i)
        if len(var)>0:
            if var[0] in stack.keys():
                if len(stack[var[0]])>1:
                    stack[var[0]].pop()
                

 
def placePhi(defsites,DF,aphi,predecessor):
    for n in bl:
        for a in n.aorig:
            if a not in defsites.keys():
                defsites[a]=set()
            else:
                defsites[a]=defsites[a].union({n})
        
        
    
    for a in var:
        aphi[a]=set()
        W=defsites[a]
        while W!=set():
            n=W.pop()
            for Y in DF[n]:
                if Y not in aphi[a]:
                    line=a+' = φ( '
                    for numPred in range(len(predecessor[Y])):
                        line=line+a+' , '
                    line=line[:len(line)-2]+')'
                    Y.instr.insert(0,line)
                    aphi[a]=aphi[a].union({Y})
                    if a not in Y.aorig:
                        W=W.union({Y})


def computeDF(n,DF):
    S=set()
    for y in n.child:   #dflocal
        if idiom[y]!=n:
            S=S.union({y})

    for c in n.dom: #dfup
        if c==n:
            continue
        computeDF(c,DF)
        for w in DF[c]:
            if w not in n.dom:
                S=S.union({w})
    DF[n]=S


DF={}

computeDF(start,DF)
aphi={}
defsites={}


for i in predecessor.keys():
    predecessor[i]=list(predecessor[i])

placePhi(defsites,DF,aphi,predecessor)

allVar=var
    
initialization(bl)

print('\n\nSSA\n\n')
for i in bl:
    i.disp()
    