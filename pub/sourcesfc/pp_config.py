## -*- coding: utf-8 -*-
## GUI for 2D FEM heat conduction inside of FreeCAD
## Author: teobo
## 
## License: LGPL v 2.1gui_mode
## Version: 04/12/2015
#print "pp_config"
import fem2dheatconductiongui
import shutil

try:FreeCAD.closeDocument(FreeCAD.ActiveDocument.Name)
except:pass

if len(set(FreeCAD.listDocuments())&set([Pi.fc_docname]))==0:
    FreeCAD.newDocument(Pi.fc_docname)


# set up some test unit
#load sample files
#assign stepfiles to pieces[i].compound1: tedious
stepdir=os.environ["FEMProjScripts"]+"testbed2/stepzoo1/"#directory for step-zoo
stepfiles=sorted(os.listdir(stepdir))
#index zero shall be occupied
print str(len(stepfiles))+" "+str(stepfiles)
indPI=len(Pieces)

for i in range(indPI,len(stepfiles)+indPI):
    FaceApp2=[]
    Pieces.append(Piece())
    Pieces[i].stepfile=stepdir+stepfiles[i-indPI]
    #print fem2dheatconductiongui.Pieces[i].stepfile
    obj_nr_before=len(FreeCAD.ActiveDocument.Objects)
    Pieces[i].compound0=ImportGui.insert(Pieces[i].stepfile,FreeCAD.ActiveDocument.Name)
    obj_nr_after=len(FreeCAD.ActiveDocument.Objects)
    print str(i)  +"i  " + str(obj_nr_after) +"after  " + str(obj_nr_before)+"before  " 
    #if i==2:break
    for i1 in FreeCAD.ActiveDocument.Objects[obj_nr_before:obj_nr_after]:
	FaceApp2.append(i1)
    Pi=Pieces[i]
    pointtopost.testinit151024(Pi,Pieces.index(Pi)) #other structures
    Pi.compound0=FreeCAD.activeDocument().addObject("Part::Compound","Compound")
    Pi.compound0.Links= FaceApp2
    Pi.compound0.Label=Pi.compound0name+"Pi"+str(Pieces.index(Pi))

FreeCAD.ActiveDocument.recompute()

print "pi.fempath" + Pi.fempath
#
#unittest: the 3 pieces start:
import time
t1=time.time()
procflag=0
if procflag!=0:
    i=3;Pi=Pieces[i]
    pointtopost.testinit151024(Pi,Pieces.index(Pi))
    #t.gui_point2post()
    #comment out here
    print t1-time.time()

procflag=1
if procflag!=0:
    i=1;Pi=Pieces[i]
    pointtopost.testinit151024(Pi,Pieces.index(Pi))

    #remove whole dir for testing purpose
    #if os.path.exists(Pi.fempath):	
    #    shutil.rmtree(Pi.fempath)

    # put cvs file from template
    if not os.path.exists(fem2dheatconductiongui.Pi.csvfile):
	try:os.makedirs(Pi.fempath)
	except:pass
	dst=Pi.fempath+"spreadsheetfile.csv" #
	src=os.environ["FEM_PROTO_FLUX3_PATH"]+"elmermesh"+str(Pieces.index(Pi))+'/spreadsheetfile.csv'
	shutil.copyfile(src,dst)   

    t.gui_point2post("11101302")#

    #visu
    t.gui_visu("7,8,11,12,13,15,16") 
    t.gui_visu("15,17") #prefined for 
    for i in [Pi.femmesh2]+[Pi.anno8]:
	i.ViewObject.Visibility=True
    
    #pointtopost.drop_pic(Pi.femmesh1,Pi.femmesh2,Pi.pngfile) # ok

print t1-time.time()
procflag=0
if procflag!=0:
    i=2;Pi=Pieces[i]
    pointtopost.testinit151024(Pi,Pieces.index(Pi))

    # put cvs file from template
    if not os.path.exists(fem2dheatconductiongui.Pi.csvfile):
	try:os.makedirs(Pi.fempath)
	except:pass
	dst=Pi.fempath+"spreadsheetfile.csv" #
	src=os.environ["FEM_PROTO_FLUX3_PATH"]+"elmermesh"+str(Pieces.index(Pi))+'/spreadsheetfile.csv'
	shutil.copyfile(src,dst)   

    t.gui_point2post("11101302")#
    t.gui_visu("7,8,11,12,13,15,16") #run 11,12,13 controll to be implemented,#scale color
    t.gui_visu("15,17")

print t1-time.time()


print t1-time.time()
procflag=0
if procflag!=0:
    i=4;Pi=Pieces[i]
    pointtopost.testinit151024(Pi,Pieces.index(Pi))

    # put cvs file from template
    if not os.path.exists(fem2dheatconductiongui.Pi.csvfile):
	try:os.makedirs(Pi.fempath)
	except:pass
	dst=Pi.fempath+"spreadsheetfile.csv" #
	src=os.environ["FEM_PROTO_FLUX3_PATH"]+"elmermesh"+str(Pieces.index(Pi))+'/spreadsheetfile.csv'
	shutil.copyfile(src,dst)   

    #t.gui_point2post("11000702")#
    t.gui_point2post("1110202")#
    t.gui_point2post("1110707")#
    t.set_le_cmd_line_opt_mesh("line")
    #t.gui_visu("7,8,11,12,13,15,16") #run 11,12,13 controll to be implemented,#scale color
    t.gui_visu("15,17")




#unittest: the 3 pieces end:
#ok: restarted freecad
#ok rm -r /tmp/elmermesh1:ok replace csv before: ok
#


#fem2dheatconductiongui.gui_annotate_all()
#t.gui_annotate_all()
#glob_le_opt_pp="11001302" # no effect,?

#pointtopost.man_mv_obj_dir(Pieces)
#group objects


