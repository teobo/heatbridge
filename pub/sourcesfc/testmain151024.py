
import os
import sys
import math
import re
import FreeCAD

Gui.activateWorkbench("DraftWorkbench")
#add FreeCAD Document if not existing yet



try:
    execfile(os.environ["FEMProjScripts"]+"../local/projenv.py")
except OSError:
    pass




sys.path.insert(0,os.environ["FEMProjScripts"]+"sourcesfc/")
import pointtopost
from pointtopost import *

del sys.modules["pointtopost"]
import pointtopost
from pointtopost import *
# reload everything
#
Pieces=[]
i=0
Pieces.append(Piece)
Pi=Pieces[i]
pointtopost.testinit151024(Pi)
if len(set(FreeCAD.listDocuments())&set([Pi.fc_docname]))==0:
    FreeCAD.newDocument(Pi.fc_docname)

pointtopost.cleandocobjs(Pi.fc_docname)


	       
Pi.occpointsL=pointtopost.dinDINENISO10211_1topoints()
print "draw faces"
Pi.compound0=makefacefrompointsL(Pi.occpointsL)
Pi.compound0.Label=Pi.compound0name+"Pi"+str(Pieces.index(Pi))

#adding point in new compound
Pi.compound1=pointtopost.addpointstoface(Pi.compound0)
Pi.compound1.Label=Pi.compound1name+"Pi"+str(Pieces.index(Pi))

print "gmsh meshing .."
Pi.ng2D.NGParamSetMaxSize="2.2"
Pi.ng2D.NGParamSetMinSize="0.1" 
Pi.ng2D.gmshalgoname="auto"
Pi.femmesh1=pointtopost.gmshmesh(Pi.compound1, Pi.ng2D)
Pi.femmesh1.Label=Pi.femmesh1name+"Pi"+str(Pieces.index(Pi))


print "make mb egdes"
Pi.comp_mb_edges=pointtopost.make_mb_edge(Pi.femmesh1)
Pi.comp_mb_edges.Label=Pi.comp_mb_edgesstr+"Pi"+str(Pieces.index(Pi))

#on howto weed out selected objects
#docobj2L=[Pi.compound0,Pi.compound1,Pi.femmesh1,Pi.comp_mb_edges]
#pointtopost.removeobjectswithchildren(docobj2L)

Pi.comp_topo_edges=pointtopost.make_topo_edge(Pi.compound1)
Pi.comp_topo_edges.Label=Pi.comp_topo_edgesstr+"Pi"+str(Pieces.index(Pi))

Gui.SendMsgToActiveView("ViewFit")
#doubles elimination start
#
Pi.dnL=pointtopost.checkfordoublenodes(Pi.femmesh1.FemMesh)

#pointtopost.cleanmeshdoubles(Pi.femmesh1)
#defunct

#annotate all elements
anno1=pointtopost.visu_annotate_element(Pi.femmesh1.FemMesh)
anno1.Label="Ann_all_Face_"+"Pi"+str(Pieces.index(Pi))
anno1.ViewObject.hide()
anno1.ViewObject.show()
anno1.ViewObject.hide()

#annotate all nodes
anno2=pointtopost.visu_annotate_note(Pi.femmesh1)
anno2.Label="Ann_all_N_"+"Pi"+str(Pieces.index(Pi))
anno2.ViewObject.hide()
anno2.ViewObject.show()
anno2.ViewObject.hide()

#annotate all mesh boundary edges
anno3=pointtopost.visu_annotate_edge_element(Pi.femmesh1.FemMesh)
anno3.Label="Ann_mb_E_"+"Pi"+str(Pieces.index(Pi))
anno3.ViewObject.hide()
anno3.ViewObject.show()
anno3.ViewObject.hide()


#annotate double nodes
anno4=pointtopost.visu_annotate_note(Pi.femmesh1,Pi.dnL[0])
anno4.Label="Ann_double_N_"+"Pi"+str(Pieces.index(Pi))
anno4.ViewObject.hide()
anno4.ViewObject.show()
anno4.ViewObject.hide()

Pi.dnE=pointtopost.finddoubleedges(Pi.femmesh1)

#annotate double edges
anno5=pointtopost.visu_annotate_edge_element(Pi.femmesh1.FemMesh, [i[3] for i in Pi.dnE])
anno5.Label="Ann_double_E_"+"Pi"+str(Pieces.index(Pi))
anno5.ViewObject.hide()
anno5.ViewObject.show()
anno5.ViewObject.hide()


Pi.edgeL=mark_deleted_edges(Pi.femmesh1,[i[3] for i in Pi.dnE])

Pi.nodeL=mark_deleted_nodes(Pi.femmesh1,Pi.dnL[2])

Pi.facesE=pointtopost.rereference_elments(Pi.femmesh1,Pi.dnL[2],Pi.edgeL)

Pi.femmesh2=pointtopost.rebuild_mesh(Pi.femmesh1,Pi.nodeL,Pi.facesE)
Pi.femmesh2.Label=Pi.femmesh2name+"Pi"+str(Pieces.index(Pi))


dn2L=pointtopost.checkfordoublenodes(Pi.femmesh2.FemMesh)
#0 doubles 

Pi.egdeN=pointtopost.getnodesbycompoundedge(Pi.femmesh2,Pi.comp_topo_edges)


Pi.faceN=pointtopost.getnodesbycompoundface(Pi.femmesh2,Pi.compound0)
#
#doubles elimination end

#register bodies and boundaries
Pi.bnd_tegdeL=[[1,3],[18]]
Pi.bnd_tegdeL, Pi.Bnds, Pi.Bodies= pointtopost.register_bodies_and_boundaries(Pi.bnd_tegdeL,Pi.Bodies,Pi.Bnds,Pi.compound0)

#get nodes of boundary condition
Pi.boundaries=pointtopost.get_bnd_nodesbytedge(Pi.femmesh2,Pi.comp_topo_edges,Pi.bnd_tegdeL)

pointtopost.visu_bnd_tedge(Pi.comp_topo_edges,Pi.bnd_tegdeL)

Pi.bodyflag=get_elementbodysflag(Pi.femmesh2,Pi.compound0,Pi.faceN) 

Pi.egdegroup=pointtopost.get_edgegroup_and_neighbor(Pi.femmesh2,Pi.compound0,Pi.faceN,Pi.boundaries)


#annotate boundary neighbor cells
anno5=pointtopost.visu_annotate_element(Pi.femmesh2.FemMesh,Pi.egdegroup[1],Pi.bodyflag)
anno5.Label="Ann_bnd_neigh_cells_"+"Pi"+str(Pieces.index(Pi))
anno5.ViewObject.hide()
anno5.ViewObject.show()
anno5.ViewObject.hide()

#annotate boundary edges with edgegroup
anno6=pointtopost.visu_annotate_edge_element(Pi.femmesh2.FemMesh,[],Pi.egdegroup[0])
anno6.Label="Ann_bndgroup_E_"+"Pi"+str(Pieces.index(Pi))
anno6.ViewObject.hide()
anno6.ViewObject.show()
anno6.ViewObject.hide()

#mesh preperation done
##



##
#export to elmer


pointtopost.prepare_elemer_output(Pi.gridpath)

pointtopost.write_elemer_nodes_file(Pi.femmesh2,Pi.gridpath)

pointtopost.write_elmer_elements_file(Pi.femmesh2,Pi.bodyflag,Pi.gridpath)

pointtopost.write_elemer_boundary_file(Pi.femmesh2,Pi.egdegroup,Pi.gridpath)

#writing header file
pointtopost.write_elmer_header_file(Pi.femmesh2,Pi.gridpath)

#export to elmer end
##

#writing sif file
s=pointtopost.write_elmer_sif_file(Pi.siftemplfile,Pi.siffile,Pi.Bodies,Pi.Bnds)

pointtopost.process_elmer_sif_file(Pi.siffile,Pi.epsourcefile,Pi.fempath,1)
#
#postprocessing
Pi.solutionheader, Pi.solutiondata, Pi.headerline=pointtopost.read_ep_result(Pi.epfile)

#coloring by Temperaturescale
pointtopost.gradient_color_mesh(Pi.solutiondata[0][0],Pi.femmesh2)

#annotate double nodes
anno7=pointtopost.visu_annotate_note(Pi.femmesh2,[],["T:"+str(round(float(j),2)) for j in Pi.solutiondata[0][0]])
anno7.Label="Ann_resultT_N_"+"Pi"+str(Pieces.index(Pi))
anno7.ViewObject.hide()
anno7.ViewObject.show()
anno7.ViewObject.hide()
