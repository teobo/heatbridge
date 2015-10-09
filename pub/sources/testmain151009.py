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
testinit151009(Pieces):
    Pieces.append(Piece())
    Pieces[0].Bodies=[]
    Pieces[0].Bodies.append(Body())
    Pieces[0].Bodies.append(Body())
    Pieces[0].Bodies.append(Body())
    Pieces[0].Bodies[0].k=1.0
    Pieces[0].Bodies[1].k=2.0
    Pieces[0].Bodies[2].k=3.0
    Pieces[0].Bnds=[]
    Pieces[0].Bnds.append(Bnd())
    Pieces[0].Bnds.append(Bnd())
    Pieces[0].Bnds[0].T=259
    Pieces[0].Bnds[1].T=292
    #
    #varible number of bodies..
    #FEM Vektor initialization / Prototyping
    i=1
    Pieces.append(Piece())
    Pieces[i].Bodies=[]
    Pieces[1].Bodies.append(Body())
    Pieces[1].Bodies.append(Body())
    Pieces[1].Bodies.append(Body())
    Pieces[1].Bodies[0].k=1.0
    Pieces[1].Bodies[1].k=2.0
    Pieces[1].Bodies[2].k=3.0
    Pieces[1].Bnds=[]
    Pieces[1].Bnds.append(Bnd())
    Pieces[1].Bnds.append(Bnd())
    Pieces[1].Bnds[0].T=259
    Pieces[1].Bnds[1].T=292
    #
    Pieces[i].fempath = os.environ["FEM_PROTO_FLUX3_PATH"] 
    Pieces[i].unvfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle.grd"
    Pieces[i].siftemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+'flux.sif.orig'
    Pieces[i].siffile = os.environ["FEM_PROTO_FLUX3_PATH"]+"flux.sif"
    ##flux.sif.orig, case.sif
    Pieces[i].gridpath = os.environ["FEM_PROTO_FLUX3_PATH"]
    Pieces[i].grid_templ_path= os.environ["FEM_PROTO_FLUX3_PATH"]+"angle"
    Pieces[i].epfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"case.ep"
    Pieces[i].eptemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/TempDist.ep"
    Pieces[i].epsourcefile = os.environ["FEM_PROTO_FLUX3_PATH"]+"cmd1.txt"
    #
    #manually modified sif for unv procession
    i=2
    Pieces.append(Piece())
    Pieces[i].Bodies=[]
    #Pieces[i].Bodies.append(Body())
    #Pieces[i].Bodies.append(Body())
    #Pieces[i].Bodies.append(Body())
    #Pieces[i].Bodies[0].k=1.0
    #Pieces[i].Bodies[1].k=2.0
    #Pieces[i].Bodies[2].k=3.0
    Pieces[i].Bnds=[]
    #Pieces[i].Bnds.append(Bnd())
    #Pieces[i].Bnds.append(Bnd())
    #Pieces[i].Bnds[0].T=259
    #Pieces[i].Bnds[1].T=292
    #
    Pieces[i].fempath = os.environ["FEM_PROTO_FLUX3_PATH"] 
    Pieces[i].unvfile = os.environ["FEM_UNVFILE1"]
    Pieces[i].siftemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+'flux_templ_hand.sif'
    Pieces[i].siffile = os.environ["FEM_PROTO_FLUX3_PATH"]+"flux.sif"
    #
    Pieces[i].gridpath = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/" # where ElmerSolve take it from
    Pieces[i].grid_templ_path= os.environ["FEM_PROTO_FLUX3_PATH"]+os.path.splitext(os.path.basename(os.environ["FEM_UNVFILE1"]))[0] #Elmergrid puts it
    Pieces[i].epfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"case.ep"
    Pieces[i].eptemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/TempDist.ep"
    Pieces[i].epsourcefile = os.environ["FEM_PROTO_FLUX3_PATH"]+"cmd1.txt"
    #
    #manually modified sif for unv procession
    i=3
    Pieces.append(Piece())
    Pieces[i].Bodies=[]
    Pieces[i].Bodies.append(Body())
    Pieces[i].Bodies.append(Body())
    Pieces[i].Bodies.append(Body())
    Pieces[i].Bodies[0].k=1
    Pieces[i].Bodies[1].k=0.03
    Pieces[i].Bodies[2].k=0.10
    Pieces[i].Bnds=[]
    Pieces[i].Bnds.append(Bnd())
    Pieces[i].Bnds.append(Bnd())
    Pieces[i].Bnds[0].T=259
    Pieces[i].Bnds[1].T=292
    #
    Pieces[i].fempath = os.environ["FEM_PROTO_FLUX3_PATH"] 
    Pieces[i].unvfile = os.environ["FEM_UNVFILE1"]
    Pieces[i].siftemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+'flux_templ_2bodys.sif'
    Pieces[i].siffile = os.environ["FEM_PROTO_FLUX3_PATH"]+"flux.sif"
    #
    Pieces[i].gridpath = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/" # where ElmerSolve take it from
    Pieces[i].grid_templ_path= os.environ["FEM_PROTO_FLUX3_PATH"]+os.path.splitext(os.path.basename(os.environ["FEM_UNVFILE1"]))[0] #Elmergrid puts it
    Pieces[i].epfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"case.ep"
    Pieces[i].eptemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/TempDist.ep"
    Pieces[i].epsourcefile = os.environ["FEM_PROTO_FLUX3_PATH"]+"cmd1.txt"
    Pieces[i].vtufile = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/case0001.vtu"
    Pieces[i].pngfile = os.environ["FEM_PROTO_FLUX3_PATH"]+os.path.splitext(os.path.basename(os.environ["FEM_UNVFILE1"]))[0]+".png"
    Pieces[i].brepfile = os.environ["FEM_PROTO_PATH1"] +"Partition_1_erste2D.brep"
#
#
#elmerunv2ep(Pieces[0],1000810) #ok
#elmerunv2ep(Pieces[1],1000111) #ok grid fluux
#elmerunv2ep(Pieces[2],1004811) #ok hand fluux
#elmerunv2ep(Pieces[3],1003811) #python generated sif: freecad:ok salome:ok
#
#prototype vtu viewing
#elmerunv2ep(Pieces[3],1003811) #python generated sif ok 
#

#
#paraviewvtu2pic(Pieces[3],1000110) #prototype pic generation, wireframe, T gradient color display ok
#
#pvsource2point(Pieces[3],1000110,valrep='Surface',x=2,ratva=1.9,selfield='CELL',selelem=[391,392],selpoiname='temperature',selcelname='vtkOriginalCellIds',selcelvis=1,selpoivis=1,gradfield='CELL',i_ele=391,i_x=1,iv=0); #value coloring, selection display,zoom, value printout, ok
del sys.modules["salome_breptovtu"];from salome_breptovtu import *
# reload everything
#pvsource2point(Pieces[3],1000101,valrep='Wireframe',x=0) #clean up a para objects
brep2shapedirs(Pieces[3],1001011) #draws shape from brep, deletes previous, ok
shape2mesh(Pieces[3],debug=1001011)# draws mesh from shape, deletes previous, ok
mesh2bnd_n_unv(Pieces[3],debug=1000141)
