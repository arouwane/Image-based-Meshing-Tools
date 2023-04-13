from mesher.mesher import MeshFromSurface
from skimage import measure 
from skimage.filters import gaussian 
from skimage.io import imread 
import numpy as np  


file        = 'data/foam.tiff'
output_mesh = 'data/results/foam-mesh.vtk'
thrsh = 127 
sigma_gaussian = 1

im = imread(file)  # Original volume 
imb = gaussian(im, sigma_gaussian, preserve_range=True) # Blured volume 

# We extend the external boundary of the voxel domain
# in order to get a closed watertight surface
ni = imb.shape[0]  
nj = imb.shape[1]  
nk = imb.shape[2]  
ib = np.array([0,ni-1])
jb = np.array([0,nj-1])
kb = np.array([0,nk-1])
eps = -10 # Grey-level value at the boundaries 
imb [np.ix_(ib,np.arange(nj),np.arange(nk))]  =  eps
imb [np.ix_(np.arange(ni),jb,np.arange(nk))]  =  eps
imb [np.ix_(np.arange(ni),np.arange(nj),kb)]  =  eps


# Extracting the surface using the Marching cubes algorithm 
verts, faces, _ , _ = measure.marching_cubes(imb, level =thrsh, spacing=(1,1,1), allow_degenerate=False) 

mesh = MeshFromSurface(verts, faces, facet_size=1.5)

# Exporting as a vtk 
mesh.write(output_mesh)


