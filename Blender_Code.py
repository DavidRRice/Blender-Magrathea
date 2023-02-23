import bpy
import re
# selects all objects

for material in bpy.data.materials:
    material.user_clear()
    bpy.data.materials.remove(material)
    
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete() 

for o in bpy.data.objects:
    if o.hide_viewport or o.hide_render or o.hide_get(): 
        bpy.data.objects.remove(o, do_unlink=True)
        
# INSERT FILE PATH IN BETWEEN QUOTATION MARKS
file_name = r'C:\Users\srivi\Downloads\Structure443.txt'
radii=[] #Set up the lists we need to put data in
phase=[]
with open(file_name, "r+") as file: #open file
    
    output=""
    with open(file_name) as f:
        for line in f:
            if not line.isspace():
                output+=line
            
    f= open(file_name,"w")
    f.write(output)
    lines = file.readlines()
    #Deletes all empty lines and rewrites the file

    for line in lines[len(lines):1:-1]: #Read file backwards and last line
        line = line.strip()
        div=re.split('\t',line) #Splits each line at tabs - aka splits up columns 
        radii.append(float(div[1])) #radii in column 1 change to float
        phase.append(div[6]) #phase name in colun 6
        
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        # Set the viewport shading to Material preview
        space_data = area.spaces.active
        if space_data.shading.type != 'MATERIAL':
            space_data.shading.type = 'MATERIAL'
        break
    
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
    

scene = bpy.context.scene
bpy.data.objects["Sphere.008"].select_set(state=True, view_layer = scene.view_layers[0])
bpy.ops.object.shade_smooth()

    
   
    

bpy.ops.mesh.primitive_cube_add(size=rof1[0], location=(0.5*rof1[0], 0.5*rof1[0], 0.5*rof1[0]) ,rotation=(0.0, 0.0, 0.0))
cut_cube = bpy.context.object

for circle in lst_of_sphere[:-1]:
    bool_one = circle.modifiers.new(type="BOOLEAN", name = "bool 1")
    bool_one.object = cut_cube
    bool_one.operation = "DIFFERENCE"
    cut_cube.hide_set(True)



# Ice Material
scene = bpy.context.scene
node_tree = scene.node_tree
Ice = bpy.data.materials.new(name="Ice")
Ice.use_nodes = True
nodes = Ice.node_tree.nodes
bsdf =  Ice.node_tree.nodes['Principled BSDF']
links = Ice.node_tree.links
# Add a diffuse shader and set its location:    
texture = nodes.new("ShaderNodeTexNoise")
texture.location = (-300,100)
coord = nodes.new("ShaderNodeTexCoord")
coord.location = (-600,100)
links.new(coord.outputs["Object"], texture.inputs["Vector"])
links.new(texture.outputs["Fac"], bsdf.inputs["Roughness"])
bsdf.inputs["Base Color"].default_value = (0.08,0.296,1,1)
bsdf.inputs["Transmission"].default_value = (0.909)


#Ice Dark 1
Ice_1 = Ice.copy()
Ice_1.name = "Ice 1"
node = Ice_1.node_tree.nodes["Principled BSDF"]
node.inputs["Base Color"].default_value = (0.04,0.6,0.965,1)

# Ice Dark 2
Ice_2 = Ice.copy()
Ice_2.name = "Ice 2"
node = Ice_2.node_tree.nodes["Principled BSDF"]
node.inputs["Base Color"].default_value = (0.01,0.028,0.079,1)



# Water
scene = bpy.context.scene
node_tree = scene.node_tree
water = bpy.data.materials.new(name="Water")
water.use_nodes = True
nodes = water.node_tree.nodes
bsdf =  water.node_tree.nodes['Principled BSDF']
bsdf.inputs["Base Color"].default_value = (0.036,0.183,0.653,0.472)
bsdf.inputs["Metallic"].default_value = (0.586)
bsdf.inputs["Specular"].default_value = 0.523
bsdf.inputs["Transmission"].default_value = 0.986
bsdf.inputs["Roughness"].default_value = 0.218
links = water.node_tree.links
# Add a diffuse shader and set its location:    
bump = nodes.new("ShaderNodeBump")
bump.inputs["Strength"].default_value = 0.558
bump.location = (-300,100)
links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
mix = nodes.new("ShaderNodeMix")
mix.location = (-600,100)
links.new(mix.outputs["Result"], bump.inputs["Height"])
texture = nodes.new("ShaderNodeTexNoise")
texture.inputs["Roughness"].default_value = 0.717
texture.location = (-900,200)
links.new(texture.outputs["Color"], mix.inputs["A"])
texture_2 = nodes.new("ShaderNodeTexNoise")
texture_2.inputs["Roughness"].default_value = 0.392
texture_2.location = (-900,-200)
links.new(texture_2.outputs["Color"], mix.inputs["B"])

#Lighter Red Rock
scene = bpy.context.scene
node_tree = scene.node_tree
d_rock = bpy.data.materials.new(name="Darker Rock")
d_rock.use_nodes = True
nodes = d_rock.node_tree.nodes
links = d_rock.node_tree.links
bsdf =  d_rock.node_tree.nodes['Principled BSDF']
color_ramp = nodes.new("ShaderNodeValToRGB")
color_ramp.location = (-300,200)
tex = nodes.new("ShaderNodeTexNoise")
tex.location = (-600, 200)
tex.inputs["Scale"].default_value = 19.4
tex.inputs["Detail"].default_value = 15
tex.inputs["Roughness"].default_value = 0.6
links.new(tex.outputs["Fac"], color_ramp.inputs[0] )
links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])
color_ramp.color_ramp.elements[1].position = (0.7)
color_ramp.color_ramp.elements[1].color = (0.156,0.034,0.023,1)

#Darker Rock
l_rock = d_rock.copy()
l_rock.name = "Lighter Rock"
color_ramp = l_rock.node_tree.nodes["ColorRamp"]
color_ramp.color_ramp.elements[1].color = (0.726, 0.138, 0.088,1)

# Iron Core
scene = bpy.context.scene
node_tree = scene.node_tree
i_core = bpy.data.materials.new(name="Iron Core")
i_core.use_nodes = True
nodes = i_core.node_tree.nodes
links = i_core.node_tree.links
bsdf =  i_core.node_tree.nodes['Principled BSDF']
color_ramp = nodes.new("ShaderNodeValToRGB")
color_ramp.location = (-300,100)
links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])
musgrave = nodes.new("ShaderNodeTexMusgrave")
musgrave.location = (-600,100)
links.new(musgrave.outputs[0], color_ramp.inputs[0])
coord = nodes.new("ShaderNodeTexCoord")
coord.location = (-900,100)
links.new(coord.outputs["Object"], musgrave.inputs[0])
musgrave.inputs["Scale"].default_value = 51
musgrave.inputs["Dimension"].default_value = 0
musgrave.inputs["Detail"].default_value = 15
bsdf.inputs["Metallic"].default_value = 1
color_ramp.color_ramp.elements[1].color = (0.319,0.319,0.319,1)
color_ramp.color_ramp.elements[0].color = (0.051,0.044,0.041,1)
musgrave.musgrave_type = "MULTIFRACTAL"

colors = {
'Water (Valencia)':water,
'Ice (Valencia)':Ice, 
'Ice VI (ExoPlex)':[0.65, 0.12, 0.34, 1], 
'Ice VII (Grande)':[0.23, 0.56, 0.78, 1], 
"Ice VII' (Grande)":Ice,
'Ice X (Grande)':[0.76, 0.23, 0.09, 1],
'Si Pv (Oganov)' :d_rock, 
'Si PPv (Sakai)' : l_rock, 
'Fe hcp (Smith)':i_core, 
"Fe liquid (Anderson)": [0.67, 0.34, 0.89, 1], 
"Fe bcc (Dorogokupets)" :[0.12, 0.89, 0.56, 1], 
"Fe fcc (Dorogokupets)" : [0.67, 0.34, 0.89, 1],
"Fe hcp (Bouchet)": [0.67, 0.34, 0.89, 1], 
"Fe hcp (Dorogokupets)": [0.67, 0.34, 0.89, 1],
"Fe-7Si (Wicks)":[0.67, 0.34, 0.89, 1], 
"Fe-15Si (Wicks)" :[0.67, 0.34, 0.89, 1],
"Fe Dummy":[0.67, 0.34, 0.89, 1],
"Si liquid (Mosenfelder)":[0.45, 0.87, 0.09, 1],
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
"Si PPv (Sakai)":l_rock,
"Si PPv (Oganov)":[0.65, 0.12, 0.34, 1],
"PPv (Dorogokupets)":[0.65, 0.12, 0.34, 1],
"Si (PREM)":[0.65, 0.12, 0.34, 1],
"Si (PREM, Zeng)":[0.65, 0.12, 0.34, 1],
"Si (Seager)":[0.65, 0.12, 0.34, 1],
"Si Dummy":[0.65, 0.12, 0.34, 1],

"Ice (ExoPlex)":[0.23, 0.56, 0.78, 1],
"Ice supercritical Dummy":[0.23, 0.56, 0.78, 1],

"Ice Ih":[0.23, 0.56, 0.78, 1],
"Ice Ih (ExoPlex)":[0.23, 0.56, 0.78, 1],
"Ice VI (ExoPlex)":Ice,
"Ice VI (Bezacier)":[0.23, 0.56, 0.78, 1],
"Ice VII (Bezacier)":[0.23, 0.56, 0.78, 1],
"Ice VII (ExoPlex)":Ice,
"Ice VII (Grande)":Ice_1,
"Ice VII' (Grande)":Ice_1,
"Ice VII (FFH2004, Vinet)":[0.89, 0.34, 0.67, 1],
"Ice VII (FFH2004fit, Vinet fit)":[0.89, 0.34, 0.67, 1],
"Ice VII (FFH2004, BM)":[0.89, 0.34, 0.67, 1],
"Ice VII (FFH2004, thermal)":[0.89, 0.34, 0.67, 1],
"Ice VII (Fei)":[0.76, 0.23, 0.09, 1],
"Ice X (Grande)":Ice_2,
"Ice X (Hermann)":[0.76, 0.23, 0.09, 1],
"Ice (Seager)":[0.76, 0.23, 0.09, 1],
"Ice Dummy":[0.76, 0.23, 0.09, 1],
"Ice (FFH 2004)":[0.76, 0.23, 0.09, 1],
"Ice (FMNR 2009)":[0.76, 0.23, 0.09, 1],}







   
for circle in lst_of_sphere:
    index = lst_of_sphere.index(circle)
    material =  rofphasechange1[index].strip()
    color = colors[material]
    
    
    
    circle.data.materials.append(color)
    print(color)

print(rofphasechange1)

bpy.context.view_layer.objects.active = lst_of_sphere[0]
# select the sphere
