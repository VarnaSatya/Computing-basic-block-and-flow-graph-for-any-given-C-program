from taConv import *
from graphviz import Digraph
N=0

def AncestorWithLowestSemi(v,ancestor,dfnum,semi):
    u=v
    while ancestor[v]!=None:
        if dfnum[semi[v]]<dfnum[semi[u]]:
            u=v
        v=ancestor[v]
    return u

def Link(p,n,ancestor):
    ancestor[n]=p

def DFS(p,n,dfnum,vertex,parent,predecessor):
    global N
    #print(n.name)
    predecessor[n]=predecessor[n].union({p})
    if dfnum[n]==0:
        dfnum[n]=N
        vertex[N]=n
        parent[n]=p
        N=N + 1
        for w in n.child:
            DFS(n,w,dfnum,vertex,parent,predecessor)

def dominators(r):
    global N
    bucket={}
    dfnum={}
    semi={}
    ancestor={}
    idiom={}
    samedom={}
    best={}
    vertex={}
    parent={}
    global predecessor
    predecessor={}
    bucket[None]=[]
    for i in b.keys():
        bucket[b[i]]=set()
        dfnum[b[i]]=0
        semi[b[i]]=b[i]
        ancestor[b[i]]=None
        idiom[b[i]]=None
        samedom[b[i]]=None
        predecessor[b[i]]=set()

    DFS(None,r,dfnum,vertex,parent,predecessor)

    
    
    for i in range(N-1,-1,-1):
        n=vertex[i]
        p=parent[n]
        s=p
        for v in predecessor[n]:
            if v==None:
                continue
            if dfnum[v]<=dfnum[n]:
                sd=v
            else:
                sd=semi[AncestorWithLowestSemi(v,ancestor,dfnum,semi)]
            
            if sd!=None and s!=None:
                if dfnum[sd]<dfnum[s]:
                    s=sd
        if s==None:
            s=n
        semi[n]=s
        bucket[s]=bucket[s].union({n})
        Link(p,n,ancestor)
        
        for v in bucket[p]:
            y=AncestorWithLowestSemi(v,ancestor,dfnum,semi)
            if semi[y]==semi[v]:
                idiom[v]=p
            else:
                samedom[v]=y

            bucket[p]=set()
        
    for i in range(1,N):
        n=vertex[i]
        if samedom[n]!=None:
            idiom[n]=idiom[samedom[n]]
    return idiom

idiom=dominators(start)
for i in idiom.keys():
    if idiom[i]!=None:
        idiom[i].dom=idiom[i].dom.union({i})

ch=1
d={}

dot = Digraph(comment='DOM TREE')
for i in bl:
    d[i]=chr(ch)
    dot.node(d[i],i.name)
    ch=ch+1

ed=[]
for i in idiom.keys():
    if idiom[i]!=None:
        ed.append(d[idiom[i]]+d[i])
dot.edges(ed)

dot.render('domTree',view=True)

