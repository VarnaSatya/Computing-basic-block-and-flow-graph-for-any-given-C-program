import re
class block:
    def __init__(self,n):
        self.name=n
        self.instr=[] #instructions present in the block
        self.child=[] #0-false, 1-true
        self.dom=set([self]) #what self dominates, storing the dom tree in same structure as CFG
        self.aorig=set() #original variables present in the block

    def disp(self):
        print()
        print(self.name)
        
        for i in self.instr:
            print(i)
            '''
        if self.falseN!=None:
            print(self.falseN.name)
        print(list(map(lambda x:x.name,self.child)))
        print(self.aorig)
        print('DOM',list(map(lambda x: (x.name),self.dom)))
        '''
        




var=set()
f = open("ta.txt", "r") #change ta.txt to any other file with three address code
t=f.read()
l=[0]   #leaders
blN=[]
s=t.split('\n')

for i in range(len(s)):
    if 'goto ' in s[i]:
        l.append(i+1)
        blN.append(s[i][s[i].find('goto ')+5:])
    if s[i][:len(s[i])-1] in blN:
        if i not in l:
            l.append(i)
        blN.remove(s[i][:len(s[i])-1])

for i in blN:
    l=l+list(filter(lambda x: i+':' in s[x],range(len(s))))

l.sort()

j=1
cur=None
start=None
b={}
bl=[]
for i in range(len(s)):
    if i in l:
        temp=cur
        cur=block('B'+str(j))
        bl.append(cur)
        b[s[i].strip()]=cur
        if temp==None:
            start=cur
        else:
            temp.child.append(cur)
        j=j+1
    cur.instr.append(s[i])
    x=s[i]
    if s[i].find('goto ')!=-1:
        x=s[i][:s[i].find('goto ')]
    for k in re.findall('\w\w*:?',x):
        if k=='if' or k.isnumeric() or ':' in k:
            continue
        cur.aorig=cur.aorig.union({k})
        var=var.union({k})

    
numNodes=len(b.keys())

cur=start
temp=cur
while cur!=None:
    if len(cur.child)>0:
        temp=cur.child[0]
    else:
        temp=None
    i=cur.instr[len(cur.instr)-1]
    if 'goto' in i:
        if 'if ' not in i:
            cur.child=[b[i[i.find('goto ')+5:].strip()+':']]
        else:
            cur.child.append(b[i[i.find('goto ')+5:].strip()+':'])

    cur=temp

print('CFG\n\n')
for i in bl:
    i.disp()
