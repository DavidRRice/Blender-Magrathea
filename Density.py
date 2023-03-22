import ast  #Should be ok in Blender, but check that you can use this
import re

#Color Options: viridis, plasma, summer, autumn, winter, neon, gem, eclipse, sepia
colorname='viridis' #choose name from above
inf=open('colormaps.txt','r') ##file of 1000 points from each matplotlib colormaps
lines=inf.readlines()
for l in range(len(lines)):
    div=re.split('\s',lines[l])
    if div[1]==colorname: #Find line with name provided
        cmap=ast.literal_eval(lines[l+1]) #Cmap=list of 1000 colors


inf=open('Structure443.txt','r')
lines=inf.readlines()
rad=[]
dens=[]
for line in lines[1:-1]:
    div=re.split('\s{2,}',line)
    rad.append(float(div[1])) #radius Earth Radii
    dens.append(float(div[4])) #density g/cm^3
    inf.close()
    
mindens=1  #minimum density for colormap
maxdens=15 #maximum desnity for colormap

denscolors=[] #list of colors 
densrad=rad[::5]  #list of radii where denscolors colors occur
for i in dens[::5]: #Read every 5th value of density and radii
    normalize=(maxdens-i)/(maxdens-mindens)  #Find position from 0-1 of density between min and max desnity
    location=int(normalize*1000) #Round the above number to nearest thousandth and multiply by 1000
    denscolors.append(cmap[location]) #get colors to apply to given density
    
