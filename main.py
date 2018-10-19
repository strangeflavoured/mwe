import networkx as nx
import tkinter as tk
#import matplotlib.pyplot as plt
import numpy as np

nodes=('A','B','C','D')
edges=(('A','B'),('D','A'),('D','B'),('C','D'))

G=nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)


p=nx.kamada_kawai_layout(G)

cord=[i for i in p.values()]

#fig,ax=plt.subplots(1,1)
#nx.draw_networkx(G, pos=p)
#plt.show()

xmin=np.amin([i[0] for i in p.values()])
xmax=np.amax([i[0] for i in p.values()])
xl=xmax-xmin
ymin=np.amin([i[1] for i in p.values()])
ymax=np.amax([i[1] for i in p.values()])
yl=ymax-ymin


canvaswidth=750
canvasheight=500
nodesize=10
window=tk.Tk()
canvas=tk.Canvas(window,width=canvaswidth, height=canvasheight, bg='white')
canvas.pack(fill='both',expand='yes')

def transformx(a):
    return (a-xmin)*650/xl+50

def transformy(a):
    return (ymax-cord[i][1])*400/yl+50

ids={}
wids={}
edict={}
for i,j in enumerate(nodes):
    xtraf=transformx(cord[i][0])
    ytraf=transformy(cord[i][1])
    x0=xtraf-nodesize
    x1=xtraf+nodesize
    y0=ytraf-nodesize
    y1=ytraf+nodesize
    J=canvas.create_oval(x0,y0,x1,y1,fill='red')
    w=canvas.create_text(xtraf,ytraf,text=j)
    ids[nodes[i]]=J
    wids[w]=J
    edict[J]=[]

for k,l in enumerate(edges):    
    x0=np.mean((float(canvas.coords(ids[l[0]])[0]),float(canvas.coords(ids[l[0]])[2])))
    x1=np.mean((float(canvas.coords(ids[l[1]])[0]),float(canvas.coords(ids[l[1]])[2])))
    y0=np.mean((float(canvas.coords(ids[l[0]])[1]),float(canvas.coords(ids[l[0]])[3])))
    y1=np.mean((float(canvas.coords(ids[l[1]])[1]),float(canvas.coords(ids[l[1]])[3])))
    ID=canvas.create_line(x0,y0,x1,y1,arrow=tk.LAST)
    edict[ids[l[0]]].append((ID,0))
    edict[ids[l[1]]].append((ID,1))
    canvas.tag_lower(ID)

wdict={v: k for k, v in wids.items()}

def onClick(event):
    global item,push
    global stick,name
    item=canvas.find_enclosed(event.x-20, event.y-20, event.x+20, event.y+20)
    if item:
        push=True
        for i,j in enumerate(item):
            if j in edict.keys():
                stick=edict[j]
                if j in wdict.keys():
                    name=wdict[j]

def onRelease(event):
    global item,push
    global stick,name
    item=None    
    name=None
    push=False
    stick=None
    window.update()
    
def onDrag(event):
    if push:
        global stick,item,name
        x=event.x
        y=event.y
        if item[0] in edict.keys():
            canvas.coords(item[0],x+nodesize,y+nodesize,x-nodesize,y-nodesize)
            canvas.coords(name,x,y)
        if stick:                
            for i,j in enumerate(stick):
                if j[1]==0:
                    canvas.coords(j[0],x,y,canvas.coords(j[0])[2],canvas.coords(j[0])[3])
                elif j[1]==1:
                    canvas.coords(j[0],canvas.coords(j[0])[0],canvas.coords(j[0])[1],x,y)
        window.update()

item=None
stick=None
name=None
push=None

window.bind('<ButtonRelease-1>',onRelease)
window.bind('<Button-1>',onClick)    
window.bind('<B1-Motion>',onDrag)

window.mainloop()
