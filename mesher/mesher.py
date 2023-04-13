"""
Image-based mesh generation using CGAL
with one phase segmentation 
It takes as input a reconstructed tomographic volume
and generates the volumetric mesh 
"""

# Importing CGAL 
# Need to install the python bindings 
# https://pypi.org/project/cgal-bindings/


from CGAL.CGAL_Polyhedron_3 import Polyhedron_3
from CGAL.CGAL_Mesh_3 import Mesh_3_Complex_3_in_triangulation_3
from CGAL.CGAL_Mesh_3 import Polyhedral_mesh_domain_3
from CGAL.CGAL_Mesh_3 import Mesh_3_parameters
from CGAL.CGAL_Mesh_3 import Default_mesh_criteria
from CGAL import CGAL_Mesh_3

import meshio
import os 
 
from skimage.filters import gaussian 
from skimage.io import imread
from skimage import measure 



def SurfaceToOffFile(verts, faces, filename):
    """ 
    Surface (vertices and faces) to offset file 
    """ 
    with open(filename+".off", "w") as f: 
        f.write('OFF\n')
        f.write(str(verts.shape[0])+' '+str(faces.shape[0])+' '+str(0)+'\n\n')
        # loop over nodes 
        for i in range(verts.shape[0]):
            f.write(str(verts[i,0])+' '+str(verts[i,1])+' '+str(verts[i,2])+'\n')
        # loop over triangles 
        for i in range(faces.shape[0]):
            f.write('3  '+str(faces[i,0])+' '+str(faces[i,1])+' '+str(faces[i,2])+'\n')
        f.write(' ')

def MeshFromSurface(verts, faces, facet_size, facet_angle=30):
    """ 
    Returns a meshio object mesh 
    """
    
    offSurfFile = 'temp-off-file'

    SurfaceToOffFile(verts, faces, offSurfFile )
 
    #Create input polyhedron as an offset file 
    polyhedron=Polyhedron_3(offSurfFile+'.off') ; 
    os.remove(offSurfFile+'.off')  

    #Create domain
    domain = Polyhedral_mesh_domain_3(polyhedron) 
    params = Mesh_3_parameters()

    # // Mesh criteria
    # Mesh_criteria criteria(facet_angle=30, facet_size=0.1, facet_distance=0.025,
    #                        cell_radius_edge_ratio=2, cell_size=0.1); 
    #Mesh criteria (no cell_size set)
    criteria = Default_mesh_criteria()
    criteria.facet_angle(facet_angle).facet_size(facet_size) 
    #Mesh generation
    c3t3=CGAL_Mesh_3.make_mesh_3(domain,criteria,params)
    
    c3t3.output_to_medit(offSurfFile+'.mesh')
    
    
    feMesh = meshio.read(offSurfFile+'.mesh')
    os.remove(offSurfFile+'.mesh')  
    return feMesh 
 
 

    
