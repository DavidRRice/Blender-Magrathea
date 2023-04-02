import ast  #Should be ok in Blender, but check that you can use this
import re
import bpy




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

if rofphasechange1[0].strip() != "Water (Valencia)":
    surface = rof1[0] * 1.015
    rof1.insert(0, surface)
    rofphasechange1.insert(0, "Exo Planet Surface")
elif rofphasechange1[0][0:2] == "Ice":
    surface = rof1[0] * 1.015
    rof1.insert(0, surface)
    rofphasechange1.insert(0, "Exo Planet Ice Surface")

lst_of_sphere = []
rof2 = []
# to make spheres as a incidator for bounds

bpy.ops.mesh.primitive_uv_sphere_add(radius=10*rof1[0], location=(0.0, 0, 0.0), rotation=(0.0, 0.0, 0.0))
circle = bpy.context.object
bpy.ops.object.shade_smooth()


rof_ = 10*rof1[0]


len_sphere = len(lst_of_sphere) - 1


bpy.ops.mesh.primitive_cube_add(size=rof_, location=(0.5*rof_, 0.5*rof_, 0.5*rof_) ,rotation=(0.0, 0.0, 0.0))
cut_cube = bpy.context.object


lst_of_sphere.append(circle)
circle = lst_of_sphere[0]
bool_one = circle.modifiers.new(type="BOOLEAN", name = "bool 1")
bool_one.object = cut_cube
bool_one.operation = "DIFFERENCE"
cut_cube.hide_set(True)


#ALL CODE BELOW HERE IS FOR COLOR MAP/ DENSITY STUFF 
#CODE ABOVE IS ALL FOR MAKING SPHERES AND IS FROM OTHER FOLDER
#if you want to get rid of the sphere just delete the code above and work with the color map below
#



#Color Options: viridis, plasma, summer, autumn, winter, neon, gem, eclipse, sepia
file_name = r"C:\Users\srivi\Downloads\colormaps.txt"
colorname='plasma' #choose name from above
inf=open(file_name,'r') ##file of 1000 points from each matplotlib colormaps
lines=inf.readlines()
for l in range(len(lines)):
    div=re.split('\s',lines[l])
    if div[1]==colorname: #Find line with name provided
        cmap=ast.literal_eval(lines[l+1]) #Cmap=list of 1000 colors


inf=open(r"C:\Users\srivi\Downloads\Structure443.txt",'r')
lines=inf.readlines()
rad=[]
dens=[]
for line in lines[1:-1]:
    div=re.split('\s{2,}',line)
    rad.append(float(div[1])) #radius Earth Radii
    dens.append(float(div[4])) #density g/cm^3
    inf.close()
    
#Color Options: viridis, plasma, summer, autumn, winter, neon, gem, eclipse, sepia
file_name = r"C:\Users\drice\OneDrive\Desktop\Blender\colormaps.txt"
colorname='plasma' #choose name from above
inf=open(file_name,'r') ##file of 1000 points from each matplotlib colormaps
lines=inf.readlines()
for l in range(len(lines)):
    div=re.split('\s',lines[l])
    if div[1]==colorname: #Find line with name provided
        cmap=ast.literal_eval(lines[l+1]) #Cmap=list of 1000 colors


inf=open(r"C:\Users\drice\OneDrive\Desktop\Blender\StructMant4.txt",'r')
lines=inf.readlines()
rad=[]
dens=[]
for line in lines[1:-1]:
    div=re.split('\s{2,}',line)
    rad.append(float(div[1])) #radius Earth Radii
    dens.append(float(div[4])) #density g/cm^3
    inf.close()
    
mindens=3  #minimum density for colormap
maxdens=6 #maximum desnity for colormap
stepsize=(maxdens-mindens)/40

#denscolors=[] #list of colors 
#densrad=rad[::42]  #list of radii where denscolors colors occur
#for i in dens[::42]: #Read every 5th value of density and radii
#    normalize=(maxdens-i)/(maxdens-mindens)  #Find position from 0-1 of density between min and max desnity
#    location=int(normalize*1000) #Round the above number to nearest thousandth and multiply by 1000
#    denscolors.append(cmap[location]) #get colors to apply to given density
    
denscolors=[]
densrad=[]
dumbdens=0
for i in range(len(dens)):
    if dens[i] > dumbdens+stepsize:
        normalize=(maxdens-dens[i])/(maxdens-mindens)  #Find position from 0-1 of density between min and max desnity
        location=int(normalize*1000) #Round the above number to nearest thousandth and multiply by 1000
        denscolors.append(cmap[location]) #get colors to apply to given density 
        densrad.append(rad[i])
        dumbdens=dens[i]

#Surface Mars
scene = bpy.context.scene
node_tree = scene.node_tree
ice_surface = bpy.data.materials.new(name="Exoplanet Ice Surface")
ice_surface.use_nodes = True
nodes = ice_surface.node_tree.nodes
links = ice_surface.node_tree.links
bsdf =  ice_surface.node_tree.nodes['Principled BSDF']

color_ramp = nodes.new("ShaderNodeValToRGB")
color_ramp.location = (-500,300)
 
texture_gradient = nodes.new("ShaderNodeTexGradient")
texture_gradient.location = (-750, 300)
texture_gradient.gradient_type = "SPHERICAL"


links.new(texture_gradient.outputs["Color"], color_ramp.inputs["Fac"])

mapping= nodes.new("ShaderNodeMapping")
mapping.location = (-900,300)
links.new(mapping.outputs["Vector"], texture_gradient.inputs["Vector"])
mapping.inputs["Location"].default_value[0] = -1.02
mapping.inputs["Location"].default_value[1] = -1.02
mapping.inputs["Location"].default_value[2] = -1.02
mapping.inputs["Scale"].default_value[0] = 2.04
mapping.inputs["Scale"].default_value[1] = 2.04
mapping.inputs["Scale"].default_value[2] = 2.04


tex_coord = nodes.new("ShaderNodeTexCoord")
tex_coord.location = (-1200, 300)
links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])



normalized_radius = []
old_min = min(densrad)
old_max = max(densrad)
new_min = 0
new_max = 1



color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])


for old_radius in densrad:
    new_value = ((old_radius - old_min) / (old_max - old_min)) + 0
    normalized_radius.append(new_value)


location = 0
for radius in normalized_radius:
    color_ramp.color_ramp.elements.new(radius)
    color_ramp.color_ramp.elements[normalized_radius.index(radius)].color = denscolors[normalized_radius.index(radius)]

print(denscolors)    

color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[-1])


circle.data.materials.append(ice_surface)
