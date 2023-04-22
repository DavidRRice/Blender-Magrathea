# Blender-Magrathea
Blender 3D planet builder: Takes in Magrathea outputs and automatically builds realistic and appealing 3-D interior models

 <p align="center">
<img width = "300" src="planet443%235.png"/>
 </p>

Step-by-Step Instruction:
1. Donwload Blender: https://www.blender.org/download/
2. Once Open - under New File press General
3. In top bar select Scripting
4. At the top of the new pop up window select New - this will create a new Text window
5. Copy and paste code from Blender_Code.py into this new text window
6. Grab file path of Magrathea output file. Instructions to do that are here: https://www.sony.com/electronics/support/articles/00015251
7. On line 17 Replace text inside of the file_name variable (only replace the text in between the quotation marks) with the file path of desired Magrathea output file
8. Press the Run Script button at top right of Text/Code window
9. In the top bar press "Layout"
10. In the top right (Viewport Shading options) select the 3rd sphere which should look like a sphere that is partially shaded in 
11. Interior of planet should be complete now!


How to change the way a material looks:
If you dont like the way a layer looks then select it in the "Layout" tab. Click on the sphere that you want to change and it will get outlined in yellow. Alternatively, you can select a sphere via the 'Scene Collecction" section in the top right. Once a sphere is selected, click on the "Shading" tab in the top toolbar. On the bottom window ensure that "Use Nodes" is checked. Now you should see the Node Setup (bottom window) for the selected material (top window). Each box represents a node and they each code for an aspect of the material. 

If you want to alter the way the material looks you can simply click on a factor in one of the nodes such as Roughness, Sheen, Scale, etc, and entering in a new number. It will get updated in the top window. To make more drastic changes you can also add new nodes via the "Add" button in the top left of the bottom window. This video provides a good introduction to nodes and how to alter materials using them: https://www.youtube.com/watch?v=moKFSMJwpmE&ab_channel=GrantAbbitt. This link gives an overview on what each node does: https://docs.blender.org/manual/en/latest/render/shader_nodes/index.html.

The above steps will show you how to change nodes manually (it will not save if you run the program again). If you would like to change a material programmatically (permanent) you can go to the "Scripting" tab in the top toolbar. Scroll down to 
