

#Prüfreferenzfall 1: Vergleich mit der analytischen L ösung
#! Prüfreferenzfall 1 to remesh, add points, export to external meshing to reimport 

App.newDocument("Unnamed")

import Draft
A=[0,0,0]
lx=20.0
ly=2*lx
dlx=0
dly=0
rectpx=0
rectpy=0
P=[[[[[0]*3]*2]*2]*7]*4
Facep=[[None]*7]*4
Face=[[None]*7]*4
FaceApp=[]
points=[]
#5 dim list

for dlx in range((4)):
    for dly in range((7)):
	#print "face x y"+str(dlx)+" "+str(dly)
	for rectpx in range((2)):
	    #print "he3"
	    for rectpy in range((2)):
		#print "point xy"+str(rectpx) +" "+str(rectpy)
		x=P[dlx][dly][rectpx][rectpy][0]=A[0]+lx/4*dlx+lx/4*rectpx
		y=P[dlx][dly][rectpx][rectpy][1]=A[1]+ly/7*dly+ly/7*rectpy
		#print (x, y)
		points.append(FreeCAD.Vector(x,y,0))
    #points=[FreeCAD.Vector(-8.86476848228,34.0845698564,10.0),FreeCAD.Vector(-6.70267516031,34.0282967842,10.0),FreeCAD.Vector(-6.70071852918,32.0740852354,10.0),FreeCAD.Vector(-8.8225475258,32.1343288097,10.0)]
	#for i in points: print "points" +str(i)
	Facep[dlx][dly]=[i for i in points]
	Face[dlx][dly]=Draft.makeWire([points[0],points[1],points[3],points[2]],closed=True,face=True,support=None)
	FaceApp.append(App.ActiveDocument.getObject(Face[dlx][dly].Name))
	points=[]

compound=App.activeDocument().addObject("Part::Compound","Compound")
compound.Links= FaceApp
App.ActiveDocument.recompute()

###
import Draft
import Fem
import FemGui
import MechanicalAnalysis
import FreeCAD
import FreeCADGui
import ImportGui
import Mesh
import subprocess
import sys
import tempfile
from FreeCAD import Vector

ImportGui.export([FreeCAD.activeDocument().getObject(compound.Name)], "/tmp/tmp1uqZ27.step")
#command="/usr/bin/gmsh /tmp/tmpNO2czv.step -2 -format unv -o /tmp/Compound018_Mesh.unv -optimize -string Geometry.OCCSewFaces=1;"
command="/usr/bin/gmsh /tmp/tmp1uqZ27.step -2 -format unv -o /tmp/Compound018_Mesh.unv -algo meshadapt -clmax 5,00 -string Geometry.OCCSewFaces=1;"
output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
FreeCAD.Console.PrintMessage(output)
Fem.insert("/tmp/Compound018_Mesh.unv", FreeCAD.ActiveDocument.Name)
a=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
FreeCADGui.ActiveDocument.getObject(a.Name).DisplayMode = "Wireframe"
Gui.SendMsgToActiveView("ViewFit")



# Prüfreferenzfall 2: zweidimensionaler Wärmedurchgang DIN EN ISO 10211 Page 39
#! Prüfreferenzfall 2 to remesh, add points, export to external meshing to reimport 
import Draft
import Fem
import FemGui
import MechanicalAnalysis
import FreeCAD
import FreeCADGui
import ImportGui
import Mesh
import subprocess
import sys
import tempfile
from FreeCAD import Vector


points=[]
FaceApp1=[]
points=[Vector (2.3, 0.6, 0.0), Vector (-3.67394039744e-17, 0.6, 0.0), Vector (0.0, 0.0, 0.0), Vector (2.3, -1.61677042525e-27, 0.0)]
#points=[Vector (50.0, 0.6, 0.0), Vector (-3.67394039744e-17, 0.6, 0.0), Vector (0.0, 0.0, 0.0), Vector (50.0, -1.61677042525e-27, 0.0)]

#points=[Vector (50.0, -1.61677042525e-27, 0.0),Vector (0.0, 0.0, 0.0),Vector (-3.67394039744e-17, 0.6, 0.0),Vector (1.5, 0.6, 0.0),Vector (50.0, 0.6, 0.0)]
points=[Vector (round(i.x,6),round(i.y,6),round(i.z,6)) for i in points]
points
a1=Draft.makeWire(points,closed=True,face=True,support=None)
FaceApp1.append(App.ActiveDocument.getObject(a1.Name))

#points=[Vector (-6.73555739531e-17, 1.1, 0.0), Vector (1.5, 1.1, 0.0), Vector (1.5, 0.6, 0.0), Vector (-2.05966651973e-29, 0.6, 0.0)]
#points=[Vector (round(i.x,6),round(i.y,6),round(i.z,6)) for i in points]
#points
#a1=Draft.makeWire(points,closed=True,face=True,support=None)
#FaceApp1.append(App.ActiveDocument.getObject(a1.Name))

#points=[Vector (50.0, 4.6, 0.0), Vector (50.0, 1.1, 0.0), Vector (1.5, 1.1, 0.0), Vector (1.5, 1.25, 0.0), Vector (0.15, 1.25, 0.0), Vector (0.15, 4.6, 0.0)]
#points=[Vector (round(i.x,6),round(i.y,6),round(i.z,6)) for i in points]
#points
#a1=Draft.makeWire(points,closed=True,face=True,support=None)
#FaceApp1.append(App.ActiveDocument.getObject(a1.Name))

#points=[Vector (-6.73555739531e-17, 1.1, 0.0), Vector (-2.23498040844e-16, 4.75, 0.0), Vector (50.0, 4.75, 0.0), Vector (50.0, 4.6, 0.0), Vector (0.15, 4.6, 0.0), Vector (0.15, 1.25, 0.0), Vector (1.5, 1.25, 0.0), Vector (1.5, 1.1, 0.0)]
#points=[Vector (round(i.x,6),round(i.y,6),round(i.z,6)) for i in points]
#points
#a1=Draft.makeWire(points,closed=True,face=True,support=None)
#FaceApp1.append(App.ActiveDocument.getObject(a1.Name))

points=[Vector (1.5, 1.1, 0.0), Vector (2.3, 1.1, 0.0), Vector (2.3, 0.6, 0.0), Vector (1.5, 0.6, 0.0)]
points=[Vector (round(i.x,6),round(i.y,6),round(i.z,6)) for i in points]

#points=[Vector (1.5, 1.1, 0.0), Vector (50.0, 1.1, 0.0), Vector (50.0, 0.6, 0.0), Vector (1.5, 0.6, 0.0)]
#points=[Vector (round(i.x,6),round(i.y,6),round(i.z,6)) for i in points]
points
a1=Draft.makeWire(points,closed=True,face=True,support=None)
FaceApp1.append(App.ActiveDocument.getObject(a1.Name))

compound0=App.activeDocument().addObject("Part::Compound","Compound")
compound0.Links= FaceApp1
App.ActiveDocument.recompute()

#!add points to compound 
FaceApp2=[]
for sh1 in compound0.Links:
    compoundtemp=compound0.Shape#??
    for cutitem in list(set(compound0.Links)-set([sh1])):
	compoundtemp=compoundtemp.cut(cutitem.Shape)
    sh4=Part.show(compoundtemp)
    FaceApp2.append(App.ActiveDocument.getObject(App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1].Name))
    #Oxford Rumpelstiltskin FC Style


compound=App.activeDocument().addObject("Part::Compound","Compound")
compound.Links= FaceApp2
App.ActiveDocument.recompute()
#for work around switch comment below and uncomment above 
#compound=compound0
    
ImportGui.export([FreeCAD.activeDocument().getObject(compound.Name)], "/tmp/tmpNO2c.step")
#command="/usr/bin/gmsh /tmp/tmpNO2czv.step -2 -format unv -o /tmp/Compound018_Mesh.unv -optimize -string Geometry.OCCSewFaces=1;"
command="/usr/bin/gmsh /tmp/tmpNO2c.step -2 -format unv -o /tmp/Compound019_Mesh.unv -algo meshadapt -clmax 17,01 -clmax 14,01 -string Geometry.OCCSewFaces=1;"
output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
FreeCAD.Console.PrintMessage(output)
Fem.insert("/tmp/Compound019_Mesh.unv", FreeCAD.ActiveDocument.Name)
femmesh=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
FreeCADGui.ActiveDocument.getObject(femmesh.Name).DisplayMode = "Wireframe"



#!visu lines topo
edgetL=[]
for a in App.ActiveDocument.Compound002.Shape.Edges:
    Part.show(a)
    edgetL.append(App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1])

compoundpoi2=App.activeDocument().addObject("Part::Compound","Compoundi2")
compoundpoi2.Links= edgetL
App.ActiveDocument.recompute()

#!visu make all topolines: mesh edges, between bodies double
a4=[]
#mesh.FemMesh.Edges[1]
for a1 in femmesh.FemMesh.Edges:
    a=femmesh.FemMesh.getElementNodes(a1)
    a2=femmesh.FemMesh.getNodeById(a[0])
    a3=femmesh.FemMesh.getNodeById(a[1])
    #points=[FreeCAD.Vector(-1.35669851303,0.0587738975883,0.0),FreeCAD.Vector(-1.15098953247,-0.264482706785,0.0)]
    points=[a2,a3]
    a4.append(Draft.makeWire(points,closed=False,face=True,support=None))

compoundline=App.activeDocument().addObject("Part::Compound","Compound")
compoundline.Links= a4
App.ActiveDocument.recompute()



#!visu make all nodes as topo points
a1=femmesh.FemMesh.Nodes[1]
a=[]
for i in range(1,len(femmesh.FemMesh.Nodes)):
    a1=femmesh.FemMesh.Nodes[i]
    a.append(Draft.makePoint(a1.x,a1.y,a1.z))

compoundpoi=App.activeDocument().addObject("Part::Compound","Compound")
compoundpoi.Links= a
App.ActiveDocument.recompute()


#!find doubles nodes, double edges as they occur after gmsh unv import   -by "checking for double interboundary edges"
#eleminate edges, nodes and reference them 
#todo: easier: code more structured, functioning though 

m=femmesh.FemMesh

#check double nodes first?
a1=0
for i in m.Nodes.values():
    a=0
    for j in m.Nodes.values(): 
	if i==j: 
	    a=a+1
	if a>1: 
	    print "double occurred"
	    a1=a1+1
	    a=a-1

print str(a1)+" doubles"
#check double nodes end

m=femmesh.FemMesh
nodeP=femmesh.FemMesh.Nodes
refnodes=[-1]*len(femmesh.FemMesh.Nodes)
res=[]
#res=[(-1,-1),(-1,-1),-1,-1]
resvec=[]
edgeE=femmesh.FemMesh.Edges
for a1 in edgeE:
    if res!=[] and len(set([a1]) & set([i[3] for i in res]))!=0:
	print "double" 
	continue
    a=femmesh.FemMesh.getElementNodes(a1)
    a2=femmesh.FemMesh.getNodeById(a[0])
    a3=femmesh.FemMesh.getNodeById(a[1])
    for a4 in set(femmesh.FemMesh.Edges)-set([a1]):
	a5=femmesh.FemMesh.getElementNodes(a4)
	a6=femmesh.FemMesh.getNodeById(a5[0])
	a7=femmesh.FemMesh.getNodeById(a5[1])
	if [a2,a3]==[a6,a7] or [a3,a2]==[a6,a7]:
	    if a2==a6: 
		doublenode1=a[0]
		doublenode2=a5[0]
		doublenode3=a[1]
		doublenode4=a5[1]
	    else:
		doublenode1=a[1]
		doublenode2=a5[0]		
		doublenode3=a[0]
		doublenode4=a5[1]
	    print "first edge endpoints vectors:" + str(a2) + " " + str(a3)+"double nodes " + str(a) + " " + str(a5) +"first +double edge: " + str(a1) + " " + str(a4) +"\ndoublenodespair1by2: "	 + str(doublenode1)  +" "+ str(doublenode2)   +"\ndoublenodespair3by4: "	 + str(doublenode3)  +" "+ str(doublenode4)
	    res.append([a,a5,a1,a4])
	    resvec.append([[a2,a3]])
	    #eleminate double edges
	    edgeE=set(edgeE)-set([a4])
	    #eleminate (hopefully) all double nodes and reference them
	    if doublenode2 in nodeP:
		del nodeP[doublenode2]
		refnodes[doublenode2]=doublenode1
	    if doublenode4 in nodeP: 
		del nodeP[doublenode4]
		refnodes[doublenode4]=doublenode3		
	    #del nodeP[doublenode4]
	    break




#!1find and substitute double nodes in face element nodes
facesE=[femmesh.FemMesh.getElementNodes(fac) for fac in list(edgeE.union(femmesh.FemMesh.Faces))]
first_n_plain=[resi1 for resi in res for resi1 in resi[0]]
double_n_plain=[resi1 for resi in res for resi1 in resi[1]]
elenodes=[]

for fac in range(len(facesE)):
    #print "h3"
    elen=list(set(facesE[fac]) & set(double_n_plain))
    #print "h4"
    if len(elen)>0:
	#print "h4"
	factem=facesE[fac]
	#print "h4.2"
	for i2 in range(len(elen)):
	    #print "h5"
	    lfac=list(facesE[fac])
	    #print "h6 " +str(i2) + " " +str(elen)
	    lfac[lfac.index(elen[i2])]=first_n_plain[double_n_plain.index(elen[i2])]
	    #print "h7"
	    facesE[fac]=tuple(lfac)	
	print str(elen) +"mface i with 2 double node:" + str(fac) +"to be substituted by:" + str(first_n_plain[double_n_plain.index(elen[0])]) +" to " +str(facesE[fac])+" from " +str(factem)
	#elenodes.append(elen)	#fac[fac.index(elen)]=first_n_plain[double_n_plain.index(elen)]
#    if len(elen)==1:print str(elen)+"mface with 1 double node:" + str(fac)

#!rebuild mesh
import FreeCAD, Fem
m = Fem.FemMesh()
for n in nodeP.keys():
    #print str(n1) + " :" + str(n)
    n1=nodeP[n]
    #print str(n1) + " :" + str(n)
    m.addNode(n1.x, n1.y, n1.z, n)


   
elemN=list(edgeE.union(femmesh.FemMesh.Faces))
for i in range(len(facesE)):
    #print str(facesE[i]) + "" + str(elemN[i])
    #loose id's here
    if len(facesE[i])==3:
	#debug
	print "  l"+str(i)+ "i"
	if len(set(facesE[i])&set(nodeP))!=3:
	    print str(facesE[i]) +"smash"; continue
	#debug end
	m.addFace(facesE[i][0],facesE[i][1],facesE[i][2])
    if len(facesE[i])==2:
	a=m.addEdge(facesE[i][0],facesE[i][1])

# ok? 
#Fehlt was! Sichtbar machen wie? show?
Fem.show(m)
femmesh2=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]

#!check double nodes?
a1=0
for i in m.Nodes.values():
    a=0
    for j in m.Nodes.values(): 
	if i==j: 
	    a=a+1
	if a>1: 
	    print str(i)+"double occurred index"+str(m.Nodes.values().index(i))
	    a1=a1+1
	    a=a-1

print str(a1)+" doubles"
#!check double nodes end

#!getnodesbytopoface
#edge diffusecolor does not function
faceN=[]
egdeN=[]
femmesh1=femmesh2.FemMesh
compountO=App.ActiveDocument.Compound002

for i in [a.Shape.Faces[0] for a in compountO.Links]:
    faceN.append(femmesh1.getNodesByFace(i))

#!getnode from all bnd    
for i in compountO.Shape.Edges:
    egdeN.append(App.ActiveDocument.Mesh001.FemMesh.getNodesByEdge(i))


#!#### assigning bnds
bnd1_group=[]
bnd2_group=[]

bnd1_group.append(
femmesh2.FemMesh.getNodesByEdge(compoundpoi2.Shape.Edges[1]))

bnd1_group.append(
femmesh2.FemMesh.getNodesByEdge(compoundpoi2.Shape.Edges[5]))
#compoundpoi heißt lange

bnd2_group.append(
femmesh2.FemMesh.getNodesByEdge(App.ActiveDocument.getObject("Compound002").Shape.Edges[4]))
#### assigning bnds over  
#visu: mark line 3 
a=App.ActiveDocument.Compound003.Links[0] #small lines
a.ViewObject.LineColor= (0.00,0.00,0.00)


#!visu: mark line 3 of bnd long group
elt = App.getDocument("Unnamed").getObject("Compoundi2002").Shape.Edge3
a=compoundpoi2.Links[3].ViewObject.LineColor= (1.00,0.00,0.00)
a=compoundpoi2.Shape.Edges[3]
a.CenterOfMass

#!visu: mark point 3 of bnd group ..



#!## get Elementbodysflag
feln=[]
bodyflag=[-1]*len(femmesh2.FemMesh.Faces)
#f = femmesh.FemMesh.Faces[1]
for f in range(len(femmesh2.FemMesh.Faces)):
    feln.append(femmesh2.FemMesh.getElementNodes(femmesh2.FemMesh.Faces[f]))
    for i in range(len(faceN)):
	if len(set(feln[f])& set(faceN[i]))==3:
	    print "huh" + str(i)+ " Elementiter" + str(f) +" elemid"+ str(femmesh.FemMesh.Faces[f])
	    bodyflag[f]=i+1
	    continue
	else: print "he"+str(i)
#ok

#!get by edge id: neighbors and bnd Groupflag
bnd=[]
bnd.append(bnd1_group)
bnd.append(bnd2_group)
a=0
groupflag=[-1]*len(femmesh2.FemMesh.Edges)
neighbourelem1=[0]*len(femmesh2.FemMesh.Edges)
neighbourelem2=[0]*len(femmesh2.FemMesh.Edges)
#bnd=[]
igroupbias=len(faceN)+1
for i in femmesh2.FemMesh.Edges:
    igroup=0+igroupbias
    #print str(i) +" imEdge " 
    #femmesh2.FemMesh.getElementNodes(i)
    #print str(i) +" i"+str(femmesh2.FemMesh.getElementNodes(i)) +" getElementNodes"+ str(femmesh2.FemMesh.getElementNodes(i)) +" getElementNodes" 
    for bndg in range(len(bnd)):
	#print "bngd"
	#print bndg
	for i1 in range(len(bnd[bndg])):
	    #print bnd[bndg][i1]
	    if len(set(bnd[bndg][i1])&set(list(femmesh2.FemMesh.getElementNodes(i))))==2 :
		#point1=bnd[bndg][i1]
		#point2=bnd[bndg][i1][i2+1]
		#print str(femmesh2.FemMesh.getElementNodes(i)) +" getElementNodes"
		print str(i) +" i"+str(femmesh2.FemMesh.getElementNodes(i)) +" getElementNodes"
		print bnd[bndg][i1]
		igroup=bndg++1+igroupbias
    ineighbele1=0
    ineighbele2=0
    for e in femmesh2.FemMesh.Faces:
	s2=set(femmesh2.FemMesh.getElementNodes(i))
	s1=set(femmesh2.FemMesh.getElementNodes(e))
	if len(s1&s2)==2: 
	    print " e"+str(e) +" edgeid"+str(i)
	    if ineighbele1!=0:
		ineighbele2=e
	    else:
		ineighbele1=e
	    a=a+1
	    #print str(femmesh2.FemMesh.getElementNodes(i)) +" getElementNodes"
    groupflag[femmesh2.FemMesh.Edges.index(i)]=igroup
    neighbourelem1[femmesh2.FemMesh.Edges.index(i)]=ineighbele1
    neighbourelem2[femmesh2.FemMesh.Edges.index(i)]=ineighbele2
#ok

a

#! visu:annotate Elemend by ELementID (all)
m.TypeId
#'Fem::FemMesh'
bodyflag=[""]*len(m.Faces)
fxyz=[]
a=[]
index=0
for m_elem in m.Faces:
    index=index+1
    #a=[]
    fxyz=[]
    print str(m_elem)+"Elementnr"
    print str(m.getElementNodes(m_elem))+"getElementNodes"
    for m_ne_elem in m.getElementNodes(m_elem):
	print str(m_ne_elem)+"ElementNodenr"
	print str(m.getNodeById(m_ne_elem)) +"ElementNodenrs xyz"
	fxyz.append(m.getNodeById(m_ne_elem))
	
    yres=(fxyz[0].y+fxyz[1].y+fxyz[2].y)/3
    xres=(fxyz[0].x+fxyz[1].x+fxyz[2].x)/3
    zres=(fxyz[0].z+fxyz[1].z+fxyz[2].z)/3
    anno = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","surveyLabel")
    #a.append(anno)
    a.append(App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1])
    anno.BasePosition = FreeCAD.Vector(xres,yres,zres)
    anno.LabelText = "i" + str(m.Faces.index(m_elem)+1)+"b" +str(bodyflag[index])+  "E" + str(m_elem)+" N" +str(m.getElementNodes(m_elem))


group_m_elem_Anno=App.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
#g=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
group_m_elem_Anno.Group = a
group_m_elem_Anno.Label="group_m_elem_Anno."
App.ActiveDocument.recompute()

#! visu:annotate Nodes by id
m.TypeId
#'Fem::FemMesh'
fxyz=[]
a=[]
#nodes=[33,34]
#nodes=faceN[0]
#nodes=faceN[1]
nodes=m.Nodes.keys()
flag=0
for i in range(len(m.Nodes)): 
    #m.Nodes.values()[i]
    #m.Nodes.keys()[i]
    if set([m.Nodes.keys()[i]]) & set(nodes):
    #selective displaying..
	anno = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","surveyLabel")
	#a.append(anno)
	a.append(App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1])
	anno.BasePosition = m.Nodes.values()[i]
	anno.LabelText = "i" + str(i+1)+"n" + str(m.Nodes.keys()[i])
	anno.ViewObject.BackgroundColor=(0.5, 0.3330000042915344, 1.0, 0.0)

group_m_elem_Anno=App.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
#g=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
group_m_elem_Anno.Group = a
group_m_elem_Anno.Label="group_m_node_Anno."
App.ActiveDocument.recompute()
#ok
##
################
##################


#!elmermeshfile mesh.nodes test code 
import os
import time
import sys

elmer_mesh_path="/home/kubuntu/Dropbox/desktopproj/EBProjekte/Lernprojekte/AutoCADLernen140221/FEM/githeatbridge/pub/testbed1/salome_erste2D/"+"elmermesh2/"
#elmer_mesh_path="/tmp/elmermesh/"
try:
    os.mkdir(elmer_mesh_path)
except OSError:
    pass

mesh_nodes_path=elmer_mesh_path+"mesh.nodes"

try:
    os.remove(mesh_nodes_path)
except OSError:
    pass

meshnodef= open(mesh_nodes_path, 'a') #'a' opens the file for appending
#meshnodef.write("hi\n")
for nodeid_index in range(0,femmesh2.FemMesh.NodeCount):
    nodeid=femmesh2.FemMesh.Nodes.keys()[nodeid_index]
#    line=str(nodeid)+" -1 "+str(femmesh2.FemMesh.getNodeById(nodeid).x)\
#    +" "+str(femmesh2.FemMesh.getNodeById(nodeid).y)\
#    +" "+str(femmesh2.FemMesh.getNodeById(nodeid).z)+"\n"
    nodeid=femmesh2.FemMesh.Nodes.keys()[nodeid_index]
    line=str(nodeid_index+1)+" -1 "+str(femmesh2.FemMesh.getNodeById(nodeid).x)\
    +" "+str(femmesh2.FemMesh.getNodeById(nodeid).y)\
    +" "+str(femmesh2.FemMesh.getNodeById(nodeid).z)+"\n"

    meshnodef.write(line)
    #print line

meshnodef.close()   
#ok

#!elmermeshfile elements test code 
#e1 body type n1 ... nn
#1 1 404 1 2 32 31

mesh_element_path=elmer_mesh_path+"mesh.elements"
try:
    os.remove(mesh_element_path)
except OSError:
    pass

meshelementf= open(mesh_element_path, 'a') #'a' opens the file for appending
#meshelementf.write("huia\n")


t1=time.time()

for element_index in range(len(femmesh2.FemMesh.Faces)):
    elementid=femmesh2.FemMesh.Faces[element_index]
    #nodesmfac=femmesh2.FemMesh.getElementNodes(elementid)
    #line=str(elementid)+" "+str(bodyflag[element_index])\
    #+" 303 "+str(nodesmfac[0])\
    #+" "+str(nodesmfac[1])+" "+str(nodesmfac[2])+"\n"
    nodesmfac=[femmesh2.FemMesh.Nodes.keys().index(i)+1 for i in list(femmesh2.FemMesh.getElementNodes(elementid))]

    line=str(element_index+1)+" "+str(bodyflag[element_index])\
    +" 303 "+str(nodesmfac[0])\
    +" "+str(nodesmfac[1])+" "+str(nodesmfac[2])+"\n"
    meshelementf.write(line)
    #print line

print t1-time.time()
meshelementf.close()   
#ok

#!produce elmer boundary file
#e1 bndry p1 p2 type n1 ... nn
#1 5 1 0 202 9 4
#id ,selbst gewählt 

mesh_bnd_path=elmer_mesh_path+"mesh.boundary"
try:
    os.remove(mesh_bnd_path)
except OSError:
    pass

meshebndf= open(mesh_bnd_path, 'a') #'a' opens the file for appending

t1=time.time()

for bnd_index in range(len(femmesh2.FemMesh.Edges)):
    bndid=femmesh2.FemMesh.Edges[bnd_index]
#    nodesmedg=femmesh2.FemMesh.getElementNodes(bndid)
    #line=str(bndid)+" "+str(groupflag[bnd_index])\
    #+" "+str(neighbourelem1[bnd_index])\
    #+" "+str(neighbourelem2[bnd_index])\
    #+" 202 "+str(nodesmedg[0])\
    #+" "+str(nodesmedg[1])+"\n"
    nodesmedg=[femmesh2.FemMesh.Nodes.keys().index(i)+1 for i in list(femmesh2.FemMesh.getElementNodes(bndid))]
    if neighbourelem2[bnd_index]!=0:
	neighb2=femmesh2.FemMesh.Faces.index(neighbourelem2[bnd_index])
    else:
	neighb2=0
    
    line=str(bnd_index+1)+" "+str(groupflag[bnd_index])\
    +" "+str(femmesh2.FemMesh.Faces.index(neighbourelem1[bnd_index])+1)\
    +" "+str(neighb2+1)\
    +" 202 "+str(nodesmedg[0])\
    +" "+str(nodesmedg[1])+"\n"
    meshebndf.write(line)#'a' opens the file for appendingf.write(line)

print t1-time.time()
meshebndf.close() #'a' opens the file for appendingf.close()   

#ok

#nodes elements boundary-elements
#nof_types
#type-code nof_elements
#type-code nof_elements
mesh_head_path=elmer_mesh_path+"mesh.header"
try:
    os.remove(mesh_head_path)
except OSError:
    pass

meshheadf= open(mesh_head_path, 'a') #'a' opens the file for appending

t1=time.time()

line=str(femmesh2.FemMesh.NodeCount)\
+" "+str(femmesh2.FemMesh.FaceCount)\
+" "+str(femmesh2.FemMesh.EdgeCount)\
+"\n"+str(2)\
+"\n303 "+str(femmesh2.FemMesh.FaceCount)\
+"\n202 "+str(femmesh2.FemMesh.EdgeCount)
meshheadf.write(line)#'a' opens the file for appendingf.write(line)

print t1-time.time()
meshheadf.close() #'a' opens the file for appendingf.close()   

#ok
##
#gui
import os
import sys
try:
    execfile(os.environ["FEMProjScripts"]+"../local/projenv.py")
except OSError:
    pass

fem2dheatconductiongui.MeshGmsh.close(fem2dheatconductiongui.d)
del sys.modules["pointtopost"]
del sys.modules["fem2dheatconductiongui"]
import pointtopost
import fem2dheatconductiongui

#from fem2dheatconductiongui import Pi
#from fem2dheatconductiongui import Pieces
# no no

#### test start up gui end

###
import Mesh
import MeshPart

mesh=FreeCAD.ActiveDocument.addObject("Mesh::Feature","Mesh")
mesh.Mesh=MeshPart.meshFromShape(Shape=Pi.compound1.Shape,GrowthRate=0.1,SegPerEdge=1,SegPerRadius= 1,SecondOrder=0,Optimize=1,AllowQuad=0)
FreeCADGui.ActiveDocument.getObject(Pi.compound1.Name).DisplayMode = "Wireframe"
#>>> del __doc__, __mesh__
#a=mesh.Mesh.Points[1]
#a.x a.y; a.z
#a=mesh.Mesh.Facets[1]
#a=mesh.Mesh.Facets[1]
#>>> a.PointIndices
##(30L, 37L, 61L)

import FreeCAD, Fem
m = Fem.FemMesh()
#mesh=App.ActiveDocument.Mesh004
nodeP=mesh.Mesh.Points
for n in range(len(nodeP)):
    #print str(n1) + " :" + str(n)
    n1=nodeP[n]
    #print str(n1) + " :" + str(n)
    m.addNode(n1.x, n1.y, n1.z, n+1)

facesE=mesh.Mesh.Facets
for i in range(len(facesE)):
    #print str(facesE[i]) + " " + str(elemN[i])+"  i:" + str(i)
    #loose id's here
    if len(facesE[i].PointIndices)==3:
	#debug
	print "  l"+str(i)+ "i"
	#if len(set(facesE[i])&set(nodeP))!=3:
	    #print str(facesE[i]) +"smash"; continue
	#debug end
	m.addFace(facesE[i].PointIndices[0]+1,facesE[i].PointIndices[1]+1,facesE[i].PointIndices[2]+1)
    #if len(facesE[i])==2:
	#a=m.addEdge(facesE[i][0],facesE[i][1])



Fem.show(m)  
femmesh2=FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1]

###boundary register interfaces
#compountO=App.ActiveDocument.Compound001
edgeN=pointtopost.getnodesbycompoundedge(femmesh2,Pi.compound1)

import Draft
for i in range(500): Draft.makePoint(float(-2 +i),-1.0,0.0)
# uncomment for testing with several objects

import time
t1=time.time()

#### init_write_spreadsheet
spreadsh=None
#spreadsh=Pi.spreedsheet
if spreadsh==None:
    App.activeDocument().addObject('Spreadsheet::Sheet','Spreadsheet')
    spreadsh=FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1]
#    spreadsh.Label = "pp"

#Gui.ActiveDocument.setEdit(spreadsh.Name)
c=["","A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]  

i1=3
spreadsh.set(c[i1]+str(2), "bnd_index")
for i in range(19):     
    spreadsh.set(c[i1]+str(i+2), "_bnd_index"+str(i))
    App.ActiveDocument.recompute()

print t1-time.time()
spreadsh.exportFile("/tmp/2.csv")
App.ActiveDocument.removeObject("Spreadsheet")
spreadsh.importFile("/tmp/2.csv")
#work around
#open question: 
#connect to the api
#position load directly..
#reload/

libreoffice /tmp/1.csv 


# Execution time for above script
#-0.185786008835 without points 
#-16.4981470108 with existing 500 Points, 
#--accepting rule at line 275 ("bnd_index")
#--(end of buffer or a NUL)
#--EOF (start condition 0)
#--accepting rule at line 275 ("bnd_index")
#--(end of buffer or a NUL)
#--EOF (start condition 0)
#... repeating


#as well: reaction time slow, too slow to work on it:
#Error message on each gui cell entry:
#--accepting rule at line 149 (",")
#--accepting rule at line 149 (",")
#--accepting rule at line 149 (",")
#--(end of buffer or a NUL)
#--accepting rule at line 144 (" ")
#--(end of buffer or a NUL)
#--EOF (start condition 0)
#--accepting rule at line 149 (",")
#--accepting rule at line 149 (",")
#--(end of buffer or a NUL)
#--accepting rule at line 144 (" ")
#--(end of buffer or a NUL)
#--EOF (start condition 0)


#
#### write_bnd_pi_spreadsheet
spreadsh=None
#spreadsh=Pi.spreedsheet
if spreadsh==None:
    spreadsh=App.activeDocument().addObject('Spreadsheet::Sheet','Spreadsheet')

#    spreadsh=FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1]
#    spreadsh.Label = "pp"

#Gui.ActiveDocument.setEdit(spreadsh.Name)
c=["","A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]  

i1=1
spreadsh.set(c[i1]+str(1), "bnd_index")
for i in range(len(Pi.Bnds)):     
    spreadsh.set(c[i1]+str(i+2), str(i))
    App.ActiveDocument.recompute()

i1=2
spreadsh.set(c[i1]+str(1), "bnd_name")
for i in range(len(Pi.Bnds)):     
    spreadsh.set(c[i1]+str(i+2), str(Pi.Bnds[i].name))
    App.ActiveDocument.recompute()


i1=3
spreadsh.set(c[i1]+str(1), "Rs")
for i in range(len(Pi.Bnds)):     
    spreadsh.set(c[i1]+str(i+2), str(Pi.Bnds[i].Rs))
    App.ActiveDocument.recompute()

i1=4
spreadsh.set(c[i1]+str(1), "T_ext")
for i in range(len(Pi.Bnds)):     
    spreadsh.set(c[i1]+str(i+2), str(Pi.Bnds[i].T))
    App.ActiveDocument.recompute()

i1=5
spreadsh.set(c[i1]+str(1), "tedge(i)")
for i in range(len(Pi.Bnds)):     
    spreadsh.set(c[i1]+str(i+2), str(Pi.Bnds[i].T))
    App.ActiveDocument.recompute()


i1=6
spreadsh.set(c[i1]+str(1), "body_index")
for i in range(len(Pi.Bodies)):     
    spreadsh.set(c[i1]+str(i+2), str(i))
    App.ActiveDocument.recompute()

i1=7
spreadsh.set(c[i1]+str(1), "K")
for i in range(len(Pi.Bodies)):     
    spreadsh.set(c[i1]+str(i+2), str(Pi.Bodies[i].k))
    App.ActiveDocument.recompute()

i1=8
spreadsh.set(c[i1]+str(1), "body_nane")
for i in range(len(Pi.Bodies)):     
    spreadsh.set(c[i1]+str(i+2), str(Pi.Bodies[i].name))
    App.ActiveDocument.recompute()

#i1=9
#spreadsh.set(c[i1]+str(1), "body_name")
#for i in range(len(Pi.Bnds)):     
    #spreadsh.set(c[i1]+str(i+2), str(Pi.Bnds[i].T))
    #App.ActiveDocument.recompute()

#i1=5
#Pi.spreedsheet.set(c[i1]+str(1), "k")
#for i in range(len(Pi.Bnds)):     
    #Pi.spreedsheet.set(c[i1]+str(i+2), str(Pi.Bnds[i].T))
    #App.ActiveDocument.recompute()
##Pi.spreedsheet.set('C'+str(1), "k")
##for i in range(len(Pi.Bnds)):     
    ##Pi.spreedsheet.set('c'+str(i+2), str(Pi.Bnds[i].T))
    ##App.ActiveDocument.recompute()


#int(str(Pi.bnd_tegdeL[0]))



Pi.bnd_tegdeL=[[1,3],[18]]

Pi.bnd_tegdeL, Pi.Bnds, Pi.Bodies= pointtopost.register_bodies_and_boundaries(Pi.bnd_tegdeL,Pi.Bodies,Pi.Bnds,Pi.compound0)

##
a=len(Pi.compound0.Links)-len(kL)
#pseudocode writeboundarybndtospread end
#

#play with spreadsheet start
#open access the the rows numerically
#tile 

import WebGui
from StartPage import StartPage
WebGui.openBrowserHTML(StartPage.handle(),'file://' + App.getResourceDir() + 'Mod/Start/StartPage/','Start page')
App.newDocument("Unnamed")
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")
Gui.activateWorkbench("SpreadsheetWorkbench")
App.activeDocument().addObject('Spreadsheet::Sheet','Spreadsheet')

FreeCADGui.ActiveDocument.Spreadsheet.show() #does nothing

App.ActiveDocument.Spreadsheet.setColumnWidth('B', 159) # does nothing..
App.ActiveDocument.recompute()
Gui.ActiveDocument.setEdit(App.ActiveDocument.ActiveObject.Name) 
# shows the spreadsheat window.. 


from PySide import QtGui
from PySide import QtCore

mainWindow	= FreeCADGui.getMainWindow()
pcDW		= mainWindow.findChild(QtGui.QDockWidget, "Python console")
pcPTE		= pcDW.findChild(QtGui.QPlainTextEdit, "Python console")
dockWidgets = mainWindow.findChildren(QtGui.QDockWidget)

toplevel = QtGui.qApp.topLevelWidgets()


from PySide import QtGui
from PySide import QtCore
 
def getMainWindow():
   toplevel = QtGui.qApp.topLevelWidgets()
   for i in toplevel:
      if i.metaObject().className() == "Gui::MainWindow":
         return i
   raise Exception("No main window found")


mw=getMainWindow()

[i.metaObject().className() for i in mw.findChildren(QtGui.QMainWindow)]
#['WebGui::BrowserView', 'Gui::View3DInventor', 'SpreadsheetGui::SheetView']
sg=mw.findChildren(QtGui.QMainWindow)[2]
sg.setWindowTitle("uff")
sg.size()
#PySide.QtCore.QSize(1074, 374)
sg.size()
#PySide.QtCore.QSize(400, 300)
sg.size()
#PySide.QtCore.QSize(498, 300)
sg.resize(200,200)
sg.pos() #inner frame..
sg.setVisible(0)
sg.setVisible(1)
ig=mw.findChildren(QtGui.QMainWindow)[2]
QtGui.qApp.objectName()
u'freecad'
QtGui.QWorkspace.cascade()
#Traceback (most recent call last):
#  File "<input>", line 1, in <module>
#TypeError: descriptor 'cascade' of 'PySide.QtGui.QWorkspace' object needs an argument
mw.resize(900,500) #ok
mw.setGeometry(0,0,500,500)
a=sg.parentWidget()
a.pos()
#PySide.QtCore.QPoint(107, 39)
#ok
a.hide()
a.show()
#ok
sg.resize(451, 362)
a.resize(451, 362)
#ok
a.setGeometry(130,140,350, 450)
# positions spreadsheet window in view window: missing link
sg.minimumSizeHint()
#PySide.QtCore.QSize(400, 300)
sg.setMinimumSize(200,200)
a.setMinimumSize(200,200)
sg.resize(200, 200)
a.resize(200, 200)
#ok
a.showMinimized() 
a.showNormal()
a.setGeometry(10,140,350, 450) #ok
App.ActiveDocument.Spreadsheet001.setColumnWidth('A', 70)
App.ActiveDocument.recompute()
#ok

#ok
len(mw.children())
#155 ?

mw.setGeometry(       250, 250, 400, 150)
#window moves


    
#annotate and color mesh faces: bodies
Pi.compound1.ViewObject.Visibility=0
a=[]
lenlinks=len(Pi.compound0.Links)
for m_elem in range(lenlinks):
    anno = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","surveyLabel")
    #a.append(anno)
    a.append(FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1])
    anno.BasePosition = Pi.compound0.Links[m_elem].Shape.BoundBox.Center
    LabelTexti = "" + str(Pi.Bodies[m_elem].name)
    LabelTextb = " k:" +str(Pi.Bodies[m_elem].k)
    #print "index"+str(index)
    LabelTexte =" i:" + str(m_elem)
    anno.LabelText=LabelTexti+LabelTextb+LabelTexte
    Pi.compound1.Links[m_elem].ViewObject.ShapeColor=(0.1+m_elem*(0.9/lenlinks),0.00,1-+m_elem*(0.9/lenlinks))
    Pi.compound1.Links[m_elem].ViewObject.Visibility=1
    
group_m_elem_Anno=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
#g=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
group_m_elem_Anno.Group = a
group_m_elem_Anno.Label="Bodies_Anno."
FreeCAD.ActiveDocument.recompute()
#check double nodes end


# colors and annotate boundary edges
pointtopost.visu_bnd_tedge(Pi.comp_topo_edges,Pi.bnd_tegdeL,Pi.Bnds)

#ok


write_bnd_spreadsheet_to_pi(Pi.Bnds,Pi.Bodies,Pi.spreedsheet):
    
#fem2dheatconductiongui.pointtopost.Piece.Bnds[0].Rs
#0.4   

#change into while from for for -check first in row blank?
#
spreadvar=[""]*3
spreadvar[1]=str(Pi.bnd_tegdeL[1])
spreadvar[0]=str(Pi.bnd_tegdeL[0])
spreadvar[2]=""

#""=spreadsh.get(c[i1]+str(i+2))
bnd_tegdeL=Pi.bnd_tegdeL
Bnds=Pi.Bnds
#flag="read"
flag=""
i1=5

#spreadsh.set(c[i1]+str(1), "tedge(i)")
if flag=="read":
    bnd_tegdeL=[]
    a_tempL=[]
    i=0
    #a_temp=spreadsh.get(c[i1]+str(i+2))
    a_temp=spreadvar[i]
    while a_temp!="":
	a_tempL=[]
	for i4 in [i3 for i3 in re.split('\n|\ |\]|\[|\,',a_temp) if i3]:
	    #print str(i4) + "  READ"
	    a_tempL.append(int(i4))
	bnd_tegdeL.append(a_tempL )
	i=i+1
	a_temp=spreadvar[i]
	#a_temp=spreadsh.get(c[i1]+str(i+2))
else:
    for i in range(len(Bnds)): 
	spreadvar[i]=str(bnd_tegdeL[i])
	#spreadsh.set(c[i1]+str(i+2), str(bnd_tegdeL[i]))
   


#prototype code man_mv_obj_dir
#lenlinks=len(FreeCAD.ActiveDocument.Objects)-1
piL=fem2dheatconductiongui.Pieces#
ungroup_flag=1
for m_elem in piL:
    a=[]
    if ungroup_flag!=0:
	try:FreeCAD.ActiveDocument.removeObject(m_elem.group.Name)
	except BaseException:
	    pass
	continue
    
    for a1 in [m_elem.compound0,\
    m_elem.compound0,m_elem.compound1,m_elem.femmesh1,\
    m_elem.comp_mb_edges,m_elem.comp_topo_edges,m_elem.comp_topo_points,\
    m_elem.femmesh2,m_elem.spreedsheet,m_elem.anno1,\
    m_elem.anno1,m_elem.anno2,m_elem.anno3,\
    m_elem.anno4,m_elem.anno5,m_elem.anno6,\
    m_elem.anno5_1,\
    m_elem.anno7,m_elem.anno8]:
	try: 
	    a1.TypeId!=""
	    a.append(a1)
	except BaseException:pass
    try: 
	m_elem.group.TypeId=='App::DocumentObjectGroup'
    except BaseException:
	m_elem.group=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
    
    m_elem.group.Group = a
    a1_name= "Group"+"Pi"+str(fem2dheatconductiongui.Pieces.index(m_elem))
    #for a3 in FreeCAD.ActiveDocument.getObjectsByLabel(a1_name):
    m_elem.group.Label=a1_name
    print a1_name
    FreeCAD.ActiveDocument.recompute()





-pngfile
-activeview # else?
-isolate the one piece, putoff all other objects

### drop pic per piece
FreeCADGui.SendMsgToActiveView("ViewFit")
Gui.SendMsgToActiveView("ViewSelection")
Gui.SendMsgToActiveView("ViewSelection")
FreeCADGui.activeDocument().activeView().viewRight()
FreeCADGui.SendMsgToActiveView("ViewFit")
time.sleep(1)
FreeCAD.ActiveDocument.recompute()
time.sleep(1)
FreeCADGui.activeDocument().activeView().saveImage( fem2dheatconductiongui.Pi.pngfile, 1000, 1000, 'Current')

#hide all
vis_obj=FreeCAD.ActiveDocument.Objects
flag=False

for i in vis_obj:i.ViewObject.Visibility=flag

#show some for registering
#vis_obj=fem2dheatconductiongui.Pi.compound0.Links
vis_obj=fem2dheatconductiongui.Pi.comp_topo_edges.Links

#vis_obj=[fem2dheatconductiongui.Pi.compound0,fem2dheatconductiongui.Pi.comp_topo_edges]
flag=True
for i in vis_obj:
    i.ViewObject.Visibility=flag
    #i.Name="tedge_ind"+str(i)

#show bodies colored
vis_obj=fem2dheatconductiongui.Pi.compound0.Links
#vis_obj=fem2dheatconductiongui.Pi.comp_topo_edges.Links
#vis_obj=[fem2dheatconductiongui.Pi.compound0,fem2dheatconductiongui.Pi.comp_topo_edges]
flag=True
for i in vis_obj:
    i.ViewObject.Visibility=flag

#result mesh colored with boudary anno
#vis_obj=fem2dheatconductiongui.Pi.compound0.Links
#vis_obj=fem2dheatconductiongui.Pi.comp_topo_edges.Links
#hide all first
vis_obj=FreeCAD.ActiveDocument.Objects
flag=False
for i in vis_obj:
    i.ViewObject.Visibility=flag

vis_obj=[fem2dheatconductiongui.Pi.femmesh1]
flag=True
t.gui_visu() #run 11,12,13 to be implemented
# to implemented boundary anno, lowest T on bnd
for i in vis_obj:
    i.ViewObject.Visibility=flag
    i.ViewObject.DisplayMode = "Wireframe"

vis_obj=[fem2dheatconductiongui.Pi.femmesh2]
flag=True
for i in vis_obj:
    i.ViewObject.Visibility=flag
    i.ViewObject.DisplayMode = "Faces & Wireframe"

FreeCADGui.Snapper.grid.off()
FreeCADGui.SendMsgToActiveView("ViewFit")

FreeCADGui.activeDocument().activeView().saveImage( fem2dheatconductiongui.Pi.pngfile, 1000, 1000, 'Current')

#call from commandline
fem2dheatconductiongui.MeshGmsh.gui_visu(fem2dheatconductiongui.t,"7,8,11,12,13,15")


#call from commandline
vis_obj=fem2dheatconductiongui.Pi.compound0.Links +fem2dheatconductiongui.Pi.comp_topo_edges.Links
flag=True
for i in vis_obj:
    i.ViewObject.Visibility=flag

fem2dheatconductiongui.MeshGmsh.gui_visu(fem2dheatconductiongui.t,"17".)

#
Draft.makeWire([i.Point for i in a.Vertexes])