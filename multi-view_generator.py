"""
This file takes a 3D model as an stl file, centers it, then generates png images of the model from different view angles. These view angles can be adjusted 
"""

import stl
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d

#read stl from model_path
model_path = './3DModels/slide-cap.stl'
raw_stl_mesh = stl.mesh.Mesh.from_file(model_path)

#Function to ensure model is centered on origin prior to generating images from different views
def center_points_on_origin(mesh_data):
    vertices = mesh_data.points
    print("vertices before are")
    print(vertices)
    center = np.mean(vertices, axis=0)
    print("old mean is ", center)
    translation = -center
    translated_vertices = vertices + translation
    print("new vertices")
    print(translated_vertices)
    # Update the vertices in the mesh
    mesh_data.points = translated_vertices
    print("new mean is ", np.mean(translated_vertices, axis=0))
    return mesh_data

"""
captures images of stl_mesh from a specified elev and azim angle. 
elev controls rotation about the x axis (i.e. front view, top view, etc.)
azim controls rotation about the z axis (front view, side view, etc.)
dist is an experimentally determined fixed parameter that scales the png photos.
"""
def generate_save_figure(stl_mesh,elev,azim, dist):         
    figure = pyplot.figure(figsize=(10,10))
    axes = figure.add_axes(mplot3d.Axes3D(figure, auto_add_to_figure=False))
    axes.grid(False)
    axes._axis3don=False    
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_mesh.vectors))
    scale = stl_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    axes.view_init(elev=elev,azim=azim)
    axes.autoscale(True)
    axes.dist = dist
    figure.savefig('./Images/elev({})-azim({}).png'.format(elev,azim), box_inches="tight")   
    print('saved elev {}, azim {}'.format(elev,azim))
    del figure,axes,scale
    pyplot.close('all')

#Code to generate images
centered_stl_mesh = center_points_on_origin(raw_stl_mesh)
for elev in range(0, 180, 30):
    print(elev)
    for azim in range(0, 360, 45):
        print(azim)
        generate_save_figure(centered_stl_mesh,elev,azim, 7)

#Ignore below calculations done for determining dist parameter above.
"""
def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz

def find_diagonal(a, b, c):
    d1_2 = (a ** 2) + (b ** 2)
    d2 = (d1_2 + c ** 2) ** 0.5
    return d2


minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(centered_stl_mesh)
l = maxx - minx 
h = maxy - miny
w = maxz - minz
print("l h w are ", l, h, w)
		print("diagonal is", find_diagonal(l, h, w))
"""



