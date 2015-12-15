# -*- coding: utf-8 -*-
# GUI for 2D FEM heat conduction inside of FreeCAD
# Author: teobo
# 
# License: LGPL v 2.1gui_mode
# Version: 04/12/2015
print "pp_config"
import fem2dheatconductiongui
#assign stepfiles to pieces[i].compound1
if len(FreeCAD.listDocuments())==0:
    FreeCAD.newDocument(Pi.fc_docname)

stepdir=os.environ["FEMProjScripts"]+"testbed2/stepzoo1/"#directory for step-zoo
stepfiles=os.listdir(stepdir)
#index zero shall be occupied

#indPI=len(Pieces)
indPI=1 #overwrite existing

for i in range(indPI,len(stepfiles)+indPI):
    FaceApp2=[]
    Pieces.append(Piece)
    Pieces[i].stepfile=stepdir+stepfiles[i-indPI]
    print fem2dheatconductiongui.Pieces[i].stepfile
    obj_nr_before=len(FreeCAD.ActiveDocument.Objects)
    Pieces[i].compound0=ImportGui.insert(Pieces[i].stepfile,FreeCAD.ActiveDocument.Name)
    obj_nr_after=len(FreeCAD.ActiveDocument.Objects)
    #print str(i)  +"i  " + str(obj_nr_after) +"after  " + str(obj_nr_before)+"before  " 
    #if i==2:break
    for i1 in FreeCAD.ActiveDocument.Objects[obj_nr_before:obj_nr_after]:
	FaceApp2.append(i1)
    Pi=Pieces[i]
    Pi.currentPi_index=i
    print "Pi.currentPi_index=i="+str(i)
    Pi.compound0=FreeCAD.activeDocument().addObject("Part::Compound","Compound")
    Pi.compound0.Links= FaceApp2
    Pi.compound0.Label=Pi.compound0name+"Pi"+str(Pi.currentPi_index)
    print "Pi"+str(Pi.currentPi_index)
    FreeCAD.ActiveDocument.recompute()
    