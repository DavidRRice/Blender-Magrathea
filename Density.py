#Color Options: viridis, plasma, summer, autumn, winter, neon, gem, eclipse, sepia
colorname='viridis'
inf=open('colormaps.txt','r')
lines=inf.readlines()
for l in range(len(lines)):
    div=re.split('\s',lines[l])
    if div[1]==colorname:
        cmap=ast.literal_eval(lines[l+1])


inf=open('Structure443.txt','r')
lines=inf.readlines()
rad=[]
dens=[]
for line in lines[1:-1]:
    div=re.split('\s{2,}',line)
    rad.append(float(div[1]))
    dens.append(float(div[4]))
    inf.close()
    
mindens=1
maxdens=15

denscolors=[]
densrad=rad[::5]
for i in dens[::5]:
    normalize=(maxdens-i)/(maxdens-mindens)
    location=int(normalize*1000)
    print(location)
    denscolors.append(cmap[location])
    
