import bpy
import re
# selects all objects

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete() 

for o in bpy.data.objects:
    if o.hide_viewport or o.hide_render or o.hide_get(): 
        bpy.data.objects.remove(o, do_unlink=True)

radii=[] #Set up the lists we need to put data in
phase=[]
with open(r'C:\Users\srivi\Downloads\Structure443.txt', "r+") as file: #open file
    
    output=""
    with open(r"C:\Users\srivi\Downloads\Structure443.txt") as f:
        for line in f:
            if not line.isspace():
                output+=line
            
    f= open(r"C:\Users\srivi\Downloads\Structure443.txt","w")
    f.write(output)
    lines = file.readlines()
    #Deletes all empty lines and rewrites the file

    for line in lines[len(lines):1:-1]: #Read file backwards and last line
        line = line.strip()
        div=re.split('\t',line) #Splits each line at tabs - aka splits up columns 
        radii.append(float(div[1])) #radii in column 1 change to float
        phase.append(div[6]) #phase name in colun 6

dummyphase='name' #Set up a variable to compare to
rofphasechange=[] #Save radii whenever the phase changes
for i in range(len(phase)):
    if phase[i]!=dummyphase: #check if phase changes
        rofphasechange.append(radii[i])
        dummyphase=phase[i]
# this gets desired values for indicator for boundaries

dummyphase1='name'
rofphasechange1=[]
for i in range(len(phase)):
    if phase[i]!=dummyphase1:
        rofphasechange1.append(phase[i])
        dummyphase1=phase[i]

#gets a (radius,phase) pair 

import bpy
print(rofphasechange)
rof = rofphasechange[0]
print(rof)
#needed for the position for colorRamp as it can only go to 1
my_divisor = 3
rof1 = [x/ my_divisor for x in rofphasechange]
print(rof1)

rof_ = rof1[0]
print(rof1)

lst_of_sphere = []
# to make circles as a incidator for bounds
for a in rof1:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=a, location=(0.0, 0, 0.0), rotation=(0.0, 0.0, 0.0))
    circle = bpy.context.object
    lst_of_sphere.append(circle)
    

print(lst_of_sphere)

len_sphere = len(lst_of_sphere) - 1




    





outer_material = bpy.data.materials.new("Red Material")
outer_material.diffuse_color = (1, 0, 0, 1)

# Assign the green material to the inner circle



for i in range(0, len_sphere):
    circle_cut = lst_of_sphere[i].modifiers.new(type="BOOLEAN", name = "circle cut")
    circle_cut.object = lst_of_sphere[i+1]
    circle_cut.operation = "DIFFERENCE"
    bpy.context.view_layer.objects.active = lst_of_sphere[i]
    bpy.ops.object.modifier_apply(modifier="circle cut")
    

bpy.data.objects["Sphere"].select_set(state=True)
bpy.ops.object.shade_smooth()

bpy.ops.mesh.primitive_cube_add(size=rof1[0], location=(0.5*rof1[0], 0.5*rof1[0], 0.5*rof1[0]) ,rotation=(0.0, 0.0, 0.0))
cut_cube = bpy.context.object

for circle in lst_of_sphere[:-1]:
    bool_one = circle.modifiers.new(type="BOOLEAN", name = "bool 1")
    bool_one.object = cut_cube
    bool_one.operation = "DIFFERENCE"
    cut_cube.hide_set(True)

colors = {'Water (Valencia)':[0.45, 0.87, 0.09, 1], 'Ice VI (ExoPlex)':[0.65, 0.12, 0.34, 1], 'Ice VII (Grande)':[0.23, 0.56, 0.78, 1], "Ice VII' (Grande)":[0.89, 0.34, 0.67, 1], 'Ice X (Grande)':[0.76, 0.23, 0.09, 1], 'Si Pv (Oganov)' :[0.12, 0.89, 0.56, 1], 'Si PPv (Sakai)' : [0.67, 0.34, 0.89, 1], 'Fe hcp (Smith)':[0.67, 0.34, 0.89, 1], "Fe liquid (Anderson)": [0.67, 0.34, 0.89, 1], "Fe bcc (Dorogokupets)" :[0.12, 0.89, 0.56, 1], "Fe fcc (Dorogokupets)" : [0.67, 0.34, 0.89, 1], "Fe hcp (Bouchet)": [0.67, 0.34, 0.89, 1], "Fe hcp (Dorogokupets)": [0.67, 0.34, 0.89, 1], "Fe-7Si (Wicks)":[0.67, 0.34, 0.89, 1], "Fe-15Si (Wicks)" :[0.67, 0.34, 0.89, 1], "Fe Dummy":[0.67, 0.34, 0.89, 1],"Si liquid (Mosenfelder)":[0.45, 0.87, 0.09, 1],
"Si liquid (Wolf)":[0.45, 0.87, 0.09, 1],
"Fo/Ol (Dorogokupets)":[0.45, 0.87, 0.09, 1],
"Wds (Dorogokupets)":[0.45, 0.87, 0.09, 1],
"Rwd (Dorogokupets)":[0.45, 0.87, 0.09, 1],
"Akm (Dorogokupets et al.)":[0.45, 0.87, 0.09, 1],
"Fo/Ol (Sotin)":[0.45, 0.87, 0.09, 1],
"En/Opx (Sotin)":[0.45, 0.87, 0.09, 1],
"Magnesiowustite (Sotin)":[0.65, 0.12, 0.34, 1],
"Brg (Oganov)":[0.65, 0.12, 0.34, 1],
"Brg (Shim)":[0.65, 0.12, 0.34, 1],
"Pv (Dorogokupets)":[0.65, 0.12, 0.34, 1],
"Si PPv (Sakai)":[0.65, 0.12, 0.34, 1],
"Si PPv (Oganov)":[0.65, 0.12, 0.34, 1],
"PPv (Dorogokupets)":[0.65, 0.12, 0.34, 1],
"Si (PREM)":[0.65, 0.12, 0.34, 1],
"Si (PREM, Zeng)":[0.65, 0.12, 0.34, 1],
"Si (Seager)":[0.65, 0.12, 0.34, 1],
"Si Dummy":[0.65, 0.12, 0.34, 1],

"Water (ExoPlex)":[0.23, 0.56, 0.78, 1],
"Water supercritical Dummy":[0.23, 0.56, 0.78, 1],

"Ice Ih":[0.23, 0.56, 0.78, 1],
"Ice Ih (ExoPlex)":[0.23, 0.56, 0.78, 1],
"Ice VI (ExoPlex)":[0.23, 0.56, 0.78, 1],
"Ice VI (Bezacier)":[0.23, 0.56, 0.78, 1],
"Ice VII (Bezacier)":[0.23, 0.56, 0.78, 1],
"Ice VII (ExoPlex)":[0.89, 0.34, 0.67, 1],
"Ice VII (Grande)":[0.89, 0.34, 0.67, 1],
"Ice VII' (Grande)":[0.89, 0.34, 0.67, 1],
"Ice VII (FFH2004, Vinet)":[0.89, 0.34, 0.67, 1],
"Ice VII (FFH2004fit, Vinet fit)":[0.89, 0.34, 0.67, 1],
"Ice VII (FFH2004, BM)":[0.89, 0.34, 0.67, 1],
"Ice VII (FFH2004, thermal)":[0.89, 0.34, 0.67, 1],
"Ice VII (Fei)":[0.76, 0.23, 0.09, 1],
"Ice X (Grande)":[0.76, 0.23, 0.09, 1],
"Ice X (Hermann)":[0.76, 0.23, 0.09, 1],
"Ice (Seager)":[0.76, 0.23, 0.09, 1],
"Ice Dummy":[0.76, 0.23, 0.09, 1],
"Ice (FFH 2004)":[0.76, 0.23, 0.09, 1],
"Ice (FMNR 2009)":[0.76, 0.23, 0.09, 1],}

    
for circle in lst_of_sphere:
    index = lst_of_sphere.index(circle)
    material =  rofphasechange1[index]
    color = colors[material.strip()]
    new_color = bpy.data.materials.new("Material")
    new_color.diffuse_color = color
    circle.data.materials.append(new_color)
    print(color)

print(rofphasechange1)
bpy.context.view_layer.objects.active = lst_of_sphere[0]
# select the sphere