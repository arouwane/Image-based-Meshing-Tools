"""
Binary image generation 
from a mesh

Many libraries to do this task 
 
Itk :         https://itk.org/ITKExamples/src/Core/Mesh/ConvertTriangleMeshToBinaryImage/Documentation.html
PyVista  :    https://docs.pyvista.org/
PyVoxelizer : https://github.com/p-hofmann/PyVoxelizer
PyMesh:       https://github.com/PyMesh/PyMesh 
stl-to-voxel: https://github.com/cpederkoff/stl-to-voxel
and many others... ?  
"""

import numpy as np 
import matplotlib.pyplot as plt 

vs = 0.01    # Voxel size 
input_file    = 'data/cylinder.stl' 
output_imfile = 'data/results/cylinder-im.tiff'  
vmin = 0    # Minimum grey-level  
vmax = 255  # Maxium  grey-level 

 
 
#%% 
import pymesh 
""" Run this bloc if you want to use Pymesh
Creates a hexahedral finite element mesh from an image 
Go to the final block in order to convert the hex mesh to an image
"""
mesh = pymesh.load_mesh(input_file) 
mesh,_ = pymesh.remove_isolated_vertices(mesh)
grid = pymesh.VoxelGrid(vs)
grid.insert_mesh(mesh);
grid.create_grid();
# grid.dilate(args.dilate); 
# grid.erode(args.erode) ;
out_mesh = grid.mesh ;
# Uncomment to save the voxelized mesh 
# output_file = 'voxelized-'+input_file.rsplit(".",1)[0]+'.msh'
# pymesh.save_mesh(output_file, out_mesh);
# print('The voxelized mesh '+str(output_file)+' was written')
vertices = out_mesh.vertices
cells    = out_mesh.voxels



#%% 
import pyvista

""" Run this bloc if you want to use Pyvista 
Creates a hexahedral finite element mesh from an image 
Go to the final block in order to convert the hex mesh to an image
"""
mesh = pyvista.read(input_file)
out_mesh = pyvista.voxelize(mesh,density=vs)
output_file = 'voxelized-'+input_file.rsplit(".",1)[0]+'.vtk'
out_mesh.save(output_file) # On enregistre sous format vtk pour la sortie 
print('The voxelized mesh '+str(output_file)+' was written')
vertices = out_mesh.points
cells =  out_mesh.cells_dict[12]


#%%
"""
We put the 8 node finite-element mesh in 3D matrix reprensenting the image 
To do so, we determine the integer coordinates of the centers of each voxel 
Then we assign a grey-level value to the voxels 
"""
xminMesh = np.min(vertices[:,0])
xmaxMesh = np.max(vertices[:,0])
yminMesh = np.min(vertices[:,1])
ymaxMesh = np.max(vertices[:,1])
zminMesh = np.min(vertices[:,2])
zmaxMesh = np.max(vertices[:,2])


# Get the center coordinates of each voxel 
x1 = vertices[cells[:,0],0] ; y1 = vertices[cells[:,0],1]; z1 = vertices[cells[:,0],2]
x2 = vertices[cells[:,1],0] ; y2 = vertices[cells[:,1],1]; z2 = vertices[cells[:,1],2]
x3 = vertices[cells[:,2],0] ; y3 = vertices[cells[:,2],1]; z3 = vertices[cells[:,2],2]
x4 = vertices[cells[:,3],0] ; y4 = vertices[cells[:,3],1]; z4 = vertices[cells[:,3],2]
x5 = vertices[cells[:,4],0] ; y5 = vertices[cells[:,4],1]; z5 = vertices[cells[:,4],2]
x6 = vertices[cells[:,5],0] ; y6 = vertices[cells[:,5],1]; z6 = vertices[cells[:,5],2]
x7 = vertices[cells[:,6],0] ; y7 = vertices[cells[:,6],1]; z7 = vertices[cells[:,6],2]
x8 = vertices[cells[:,7],0] ; y8 = vertices[cells[:,7],1]; z8 = vertices[cells[:,7],2]

xc = (x1+x2+x3+x4+x5+x6+x7+x8)/8 
yc = (y1+y2+y3+y4+y5+y6+y7+y8)/8
zc = (z1+z2+z3+z4+z5+z6+z7+z8)/8

Ni = int ( np.ceil( (xmaxMesh-xminMesh)/vs )) 
Nj = int ( np.ceil( (ymaxMesh-yminMesh)/vs ))
Nk = int ( np.ceil( (zmaxMesh-zminMesh)/vs )) 

#Transfer the center of the physical voxels as the indices of in the image domain (i,j,k) 
i = np.ceil((xc-xminMesh)/vs).astype('int')  
j = np.ceil((yc-yminMesh)/vs).astype('int')  
k = np.ceil((zc-zminMesh)/vs).astype('int')

I = np.ones((Ni+2,Nj+2,Nk+2))*vmin
I[i,j,k] = vmax
I = I.transpose((2,1,0)) 

from skimage.io import imsave
I = I.astype('uint8')    
imsave(output_imfile,I,plugin='tifffile')



#%% 
# """ Run this bloc if you want to use stl-to-voxel """
# import stltovoxel
# stltovoxel.convert_file(input_file, output_imfile + '.png' )




