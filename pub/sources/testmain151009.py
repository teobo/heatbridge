import sys
import salome
import GEOM
from salome.geom import geomBuilder
from salome import sg
import math
import SALOMEDS

salome.salome_init()
import os
import sys
import salome
import GEOM
from salome.geom import geomBuilder
from salome import sg
import math
import SALOMEDS
import re


#execfile(r"/home/kubuntu/salome/appli_V7_4_0/salomescripts/150902runsessionscript_testfor_nogui_.py")
#clean up object browser


#delobjregex("Sphere") #ok
#delobjregex("Sphere","t") #ok
#delobjregex(".*phere.*[^4]$","s") #ok

execfile(os.environ["FEMProjScripts"]+"../local/projenv.py")
#normally already done
    
###
#FEM Vektor initialization / Prototyping
Pieces=[]
testinit151009(Pieces)

#
#
#elmerunv2ep(Pieces[0],1000810) #ok
#elmerunv2ep(Pieces[1],1000111) #ok grid fluux
#elmerunv2ep(Pieces[2],1004811) #ok hand fluux
#elmerunv2ep(Pieces[3],1003811) #python generated sif: freecad:ok salome:ok
del sys.modules["salome_breptovtu"];from salome_breptovtu import *
# reload everything
#
Pieces=[]
testinit151009(Pieces)
#pvsource2point(Pieces[3],1000101,valrep='Wireframe',x=0) #clean up a para objects
brep2shapedirs(Pieces[3],1001011) #draws shape from brep, deletes previous, ok
shape2mesh(Pieces[3],debug=1001011)# draws mesh from shape, deletes previous, ok
mesh2bnd_n_unv(Pieces[3],debug=1000141)
#prototype vtu viewing
elmerunv2ep(Pieces[3],1003811) #python generated sif ok 
#

#
paraviewvtu2pic(Pieces[3],1000110) #prototype pic generation, wireframe, T gradient color display ok
#
pvsource2point(Pieces[3],1000110,valrep='Surface',x=2,ratva=1.9,selfield='CELL',selelem=[391,392],selpoiname='temperature',selcelname='vtkOriginalCellIds',selcelvis=1,selpoivis=1,gradfield='CELL',i_ele=391,i_x=1,iv=0); #value coloring, selection display,zoom, value printout, ok
