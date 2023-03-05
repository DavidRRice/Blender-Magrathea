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
file_name = r'C:\Users\srivi\Downloads\StructureEarth.txt'
#DO REGEX HERE
title = file_name.split('\\')[-1].split('.')[0]




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



rof = rofphasechange[0]

#needed for the position for colorRamp as it can only go to 1
my_divisor = 3
rof1 = [x/ my_divisor for x in rofphasechange]
print(rof1)

rof_ = rof1[0]
print(rof1)

lst_of_sphere = []
# to make spheres as a incidator for bounds
for a in rof1:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=a, location=(0.0, 0, 0.0), rotation=(0.0, 0.0, 0.0))
    circle = bpy.context.object
    bpy.ops.object.shade_smooth()
    lst_of_sphere.append(circle)
    

print(lst_of_sphere)

len_sphere = len(lst_of_sphere) - 1

bpy.ops.object.text_add(align='WORLD', radius = 0.1, location = (0,0,0.1+rof_), rotation = (3.14/2,0,3.14-3.14/4))
ob=bpy.context.object
ob.data.body = title


    





outer_material = bpy.data.materials.new("Red Material")
outer_material.diffuse_color = (1, 0, 0, 1)

# Assign the green material to the inner circle



for i in range(0, len_sphere):
    circle_cut = lst_of_sphere[i].modifiers.new(type="BOOLEAN", name = "circle cut")
    circle_cut.object = lst_of_sphere[i+1]
    circle_cut.operation = "DIFFERENCE"
    bpy.context.view_layer.objects.active = lst_of_sphere[i]
    bpy.ops.object.modifier_apply(modifier="circle cut")
    



    
   
    

bpy.ops.mesh.primitive_cube_add(size=rof1[0], location=(0.5*rof1[0], 0.5*rof1[0], 0.5*rof1[0]) ,rotation=(0.0, 0.0, 0.0))
cut_cube = bpy.context.object

for circle in lst_of_sphere[:-1]:
    bool_one = circle.modifiers.new(type="BOOLEAN", name = "bool 1")
    bool_one.object = cut_cube
    bool_one.operation = "DIFFERENCE"
    cut_cube.hide_set(True)



# Ice Dark 1
scene = bpy.context.scene
node_tree = scene.node_tree
Ice = bpy.data.materials.new(name="Ice 1")
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


#Ice 
Ice_1 = Ice.copy()
Ice_1.name = "Ice"
node = Ice_1.node_tree.nodes["Principled BSDF"]
node.inputs["Base Color"].default_value = (0.04,0.6,0.965,1)

#Ice Dark 2
Ice_2 = Ice.copy()
Ice_2.name = "Ice 2"
node = Ice_2.node_tree.nodes["Principled BSDF"]
node.inputs["Base Color"].default_value = (0.044,0.155,0.509,1)

#Ice Dark 3
Ice_3 = Ice.copy()
Ice_3.name = "Ice 3"
node = Ice_3.node_tree.nodes["Principled BSDF"]
node.inputs["Base Color"].default_value = (0.027,0.089,0.284,1)

# Ice Dark 4
Ice_4 = Ice.copy()
Ice_4.name = "Ice 4"
node = Ice_4.node_tree.nodes["Principled BSDF"]
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

#Darker Red Rock
scene = bpy.context.scene
node_tree = scene.node_tree
darker_rock = bpy.data.materials.new(name="Darker Rock")
darker_rock.use_nodes = True
nodes = darker_rock.node_tree.nodes
links = darker_rock.node_tree.links
bsdf =  darker_rock.node_tree.nodes['Principled BSDF']
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


#Darkest Red
darkest_rock = darker_rock.copy()
darkest_rock.name = "Darkest Red Rock"
color_ramp = darkest_rock.node_tree.nodes["ColorRamp"]
color_ramp.color_ramp.elements[1].color = (0.041,0.011,0.008,1)

#Lighter Rock
l_rock = darker_rock.copy()
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



# Darkest Green Rock
light_green = darker_rock.copy()
light_green.name = "Light Green Rock"
color_ramp = light_green.node_tree.nodes["ColorRamp"]
new_color =color_ramp.color_ramp.elements.new(0.350)
color_ramp.color_ramp.elements[0].position = (0.199)
color_ramp.color_ramp.elements[2].position = (0.714)
color_ramp.color_ramp.elements[2].color = (0.088,0.174,0.096,1)
new_color.color = (0.007,0.007,0.006,1)
color_ramp.color_ramp.elements[0].color = (0.067,0.114,0.153,1)

#Lighter Green Rock
darker_green = light_green.copy()
darker_green.name = "Darker Green Rock"
color_ramp = darker_green.node_tree.nodes["ColorRamp"]
color_ramp.color_ramp.elements[2].color = (0.055,0.106,0.060,1)

# Darker Green Rock
darkest_green = light_green.copy()
darkest_green.name = "Darkest Green Rock"
color_ramp = darkest_green.node_tree.nodes["ColorRamp"]
color_ramp.color_ramp.elements[2].color = (0.026,0.049,0.029,1)

#Lava
scene = bpy.context.scene
node_tree = scene.node_tree
lava = bpy.data.materials.new(name="Lava")
lava.use_nodes = True
nodes = lava.node_tree.nodes
links = lava.node_tree.links
bsdf =  lava.node_tree.nodes['Principled BSDF']
material = lava.node_tree.nodes["Material Output"]
material.location = (500,285)
l = material.inputs[0].links[0]
links.remove(l)
shader = nodes.new("ShaderNodeMixShader")
shader.location = (306,283)
links.new(bsdf.outputs[0], shader.inputs[1])
links.new(shader.outputs[0], material.inputs["Surface"])
emission = nodes.new("ShaderNodeEmission")
emission.location =(100,-400)
emission.inputs["Color"].default_value = (0.2, 0.011, 0.003, 1)
emission.inputs["Strength"].default_value = 57
links.new(emission.outputs["Emission"], shader.inputs[2])
color_ramp = nodes.new("ShaderNodeValToRGB")
color_ramp.location = (50, 600)
links.new(color_ramp.outputs["Color"], shader.inputs["Fac"])
texture = nodes.new("ShaderNodeTexNoise")
bump = nodes.new("ShaderNodeBump")
bump.location = (-300,0)
texture.location = (-300, 650)
links.new(texture.outputs["Color"], bump.inputs["Height"])
links.new(texture.outputs["Color"], color_ramp.inputs["Fac"])
links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
bsdf.inputs["Base Color"].default_value = (0.012,0.012,0.012,1)
texture.inputs["Scale"].default_value = 11
texture.inputs["Distortion"].default_value = 1.3
color_ramp.color_ramp.elements[0].position = 0.4




colors = {
'Water (Valencia)':water,

'Si Pv (Oganov)' :darker_rock, 
'Si PPv (Sakai)' : l_rock, 
"Si liquid (Mosenfelder)":lava,
"Si liquid (Wolf)":lava,
"Si PPv (Sakai)":l_rock,
"Si PPv (Oganov)":l_rock,
"PPv (Dorogokupets)":darkest_rock,
"Si (PREM)":l_rock,
"Si (PREM, Zeng)": l_rock ,
"Si (Seager)":l_rock,
"Si Dummy":l_rock,

'Fe hcp (Smith)':i_core, 
"Fe liquid (Anderson)": lava, 
"Fe bcc (Dorogokupets)" :i_core, 
"Fe fcc (Dorogokupets)" : i_core,
"Fe hcp (Bouchet)": i_core, 
"Fe hcp (Dorogokupets)": i_core,
"Fe-7Si (Wicks)":i_core, 
"Fe-15Si (Wicks)" :i_core,
"Fe Dummy":i_core,



"Fo/Ol (Dorogokupets)":light_green,
"Wds (Dorogokupets)":darker_green,
"Rwd (Dorogokupets)":darkest_green,
"Akm (Dorogokupets et al.)":light_green,
"Fo/Ol (Sotin)":light_green,
"En/Opx (Sotin)":light_green,
"Magnesiowustite (Sotin)":light_green,
"Brg (Oganov)":darker_rock,
"Brg (Shim)":darker_rock,
"Pv (Dorogokupets)":darker_rock,

'Ice (Valencia)':Ice, 
"Ice (ExoPlex)":Ice,
"Ice supercritical Dummy":Ice,
"Ice supercritical Dummy":Ice,
"Ice (Seager)":Ice,
"Ice Dummy":Ice,
"Ice (FFH 2004)":Ice,
"Ice (FMNR 2009)":Ice,

"Ice Ih":Ice_1,
"Ice Ih (ExoPlex)":Ice_1,

'Ice VI (ExoPlex)':Ice_2, 
"Ice VI (ExoPlex)":Ice_2,
"Ice VI (Bezacier)":Ice_2,

'Ice VII (Grande)':Ice_3, 
"Ice VII' (Grande)":Ice_3,
"Ice VII (Bezacier)":Ice_3,
"Ice VII (ExoPlex)":Ice_3,
"Ice VII (Grande)":Ice_3,
"Ice VII' (Grande)":Ice_3,
"Ice VII (FFH2004, Vinet)":Ice_3,
"Ice VII (FFH2004fit, Vinet fit)":Ice_3,
"Ice VII (FFH2004, BM)":Ice_3,
"Ice VII (FFH2004, thermal)":Ice_3,
"Ice VII (Fei)":Ice_3,

'Ice X (Grande)':Ice_4,
"Ice X (Grande)":Ice_4,
"Ice X (Hermann)":Ice_4,}


for circle in lst_of_sphere:
    index = lst_of_sphere.index(circle)
    material =  rofphasechange1[index].strip()
    color = colors[material]
    
    
    
    circle.data.materials.append(color)
    print(color)

print(rofphasechange1)

bpy.context.view_layer.objects.active = lst_of_sphere[0]
# select the sphere
