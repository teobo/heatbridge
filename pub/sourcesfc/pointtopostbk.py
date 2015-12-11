import os
import sys
import Draft
import Fem
import FemGui
import MechanicalAnalysis
import FreeCAD
import FreeCADGui
import ImportGui
import Mesh
import subprocess
import tempfile
from FreeCAD import Vector
import Part
#from ctypes import *

#Fem vector "piece" definition; 
class NG_2D:
    NGParamSetMaxSize=0.2 #18 
    NGParamSetSecondOrder=0
    NGParamSetOptimize=1
    NGParamSetFineness=5 #5
    NGParamSetGrowthRate=0.2
    NGParamSetNbSegPerEdge=15
    NGParamSetNbSegPerRadius=2
    NGParamSetMinSize=1 #5
    NGParamSetUseSurfaceCurvature=1
    NGParamSetFuseEdges=1
    NGParamSetQuadAllowed=0
    #gmshalgoname="meshadapt"
    gmshalgoname="auto"

class Bnd:
    nr = '2'
    T=259

class Body:
    nr = '2'
    k=1.0

class Piece:
    name = 'Piecyo'
    average = 0.0
    Bodies = None # 
    Bnds = None #
    values = None # list cannot be initialized here!
    fempath = os.environ["FEM_PROTO_PATH1"]
    unvfile = os.environ["FEM_UNVFILE1"]
    siftemplfile = os.environ["FEM_SIF_TEMPL_FILE1"]
    siffile = os.environ["FEM_SIF_FILE1"]
    gridpath = os.environ["FEM_ElMER_GRID_PATH1"]
    grid_templ_path= os.environ["FEM_ElMER_GRID_TEMPL_PATH1"]
    epfile = os.environ["FEM_ElMER_EP_FILE1"]
    eptemplfile = os.environ["FEM_ElMER_EP_TEMPL_FILE1"]
    epsourcefile = os.environ["FEM_ElMERPOST_SOURCE1"]
    vtufile=""
    vtuobj=None
    vtuobjview=None
    vtuobjdp=None
    pngfile=""
    brepfile=""
    brepshapeobj=None
    brepgroupobj=None
    ng2D=None # list cannot be initialized here!
    meshobj=None
    mbmode="test_manual"
    Vp_mb1=[8-1,7-1,8-1,6-1] ##
    Vp_mb2=[1-1,2-1]
    mbedges=None
    #
    occpointsL=[] #of constructed
    docfaceL=[] 
    compound0=object #original after drawing
    compound0name="cp0"
    compound1=object #after adding points
    compound1name="cp1"
    femmesh1=object ##original after meshing
    femmesh1name="femmesh1"
    femmesh2=object ##original after meshing
    femmesh2name="femmesh2"
    comp_mb_edges=None #
    comp_mb_edgesstr="cp_mb_edg"
    comp_topo_edges=None #
    comp_topo_edgesstr="cp_tedg" #
    fc_docname="femcalibr2testdoc"

def dinDINENISO10211_1topoints():
    '''
    fetches predefined point lists of faces
    occpointsL=[]
    (2d )
    '''
    pointsL=[]
    points=[]
    points=[Vector (2.3, 0.6, 0.0), Vector (-3.67394039744e-17, 0.6, 0.0), Vector (0.0, 0.0, 0.0), Vector (2.3, -1.61677042525e-27, 0.0)]
    pointsL.append([Vector (round(i.x,10),round(i.y,6),round(i.z,6)) for i in points])

    points=[Vector (-6.73555739531e-17, 1.1, 0.0), Vector (1.5, 1.1, 0.0), Vector (1.5, 0.6, 0.0), Vector (-2.05966651973e-29, 0.6, 0.0)]
    pointsL.append([Vector (round(i.x,10),round(i.y,6),round(i.z,6)) for i in points])

    points=[Vector (50.0, 4.6, 0.0), Vector (50.0, 1.1, 0.0), Vector (1.5, 1.1, 0.0), Vector (1.5, 1.25, 0.0), Vector (0.15, 1.25, 0.0), Vector (0.15, 4.6, 0.0)]
    pointsL.append([Vector (round(i.x,10),round(i.y,6),round(i.z,6)) for i in points])

    points=[Vector (-6.73555739531e-17, 1.1, 0.0), Vector (-2.23498040844e-16, 4.75, 0.0), Vector (50.0, 4.75, 0.0), Vector (50.0, 4.6, 0.0), Vector (0.15, 4.6, 0.0), Vector (0.15, 1.25, 0.0), Vector (1.5, 1.25, 0.0), Vector (1.5, 1.1, 0.0)]
    pointsL.append([Vector (round(i.x,10),round(i.y,6),round(i.z,6)) for i in points])

    points=[Vector (1.5, 1.1, 0.0), Vector (2.3, 1.1, 0.0), Vector (2.3, 0.6, 0.0), Vector (1.5, 0.6, 0.0)]
    pointsL.append([Vector (round(i.x,10),round(i.y,6),round(i.z,6)) for i in points])
    return pointsL

def testinit151024(Pieces,i=0):
    '''
    prepare Piece with default data
    (3d to be implemented)
    '''
    Pieces.Bodies=[]
    Pieces.Bodies.append(Body())
    Pieces.Bodies.append(Body())
    Pieces.Bodies.append(Body())
    Pieces.Bodies[0].k=1
    Pieces.Bodies[1].k=0.03
    Pieces.Bodies[2].k=0.10
    Pieces.Bnds=[]
    Pieces.Bnds.append(Bnd())
    Pieces.Bnds.append(Bnd())
    Pieces.Bnds[0].T=259
    Pieces.Bnds[1].T=292
    #
    Pieces.fempath = os.environ["FEM_PROTO_FLUX3_PATH"] 
    Pieces.unvfile = os.environ["FEM_UNVFILE1"]
    Pieces.siftemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+'flux_templ_2bodys.sif'
    Pieces.siffile = os.environ["FEM_PROTO_FLUX3_PATH"]+"flux.sif"
    #
    Pieces.gridpath = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/" # where ElmerSolve take it from
    Pieces.grid_templ_path= os.environ["FEM_PROTO_FLUX3_PATH"]+os.path.splitext(os.path.basename(os.environ["FEM_UNVFILE1"]))[0] #Elmergrid puts it
    Pieces.epfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"case.ep"
    Pieces.eptemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/TempDist.ep"
    Pieces.epsourcefile = os.environ["FEM_PROTO_FLUX3_PATH"]+"cmd1.txt"
    Pieces.vtufile = os.environ["FEM_PROTO_FLUX3_PATH"]+"angle/case0001.vtu"
    Pieces.pngfile = os.environ["FEM_PROTO_FLUX3_PATH"]+os.path.splitext(os.path.basename(os.environ["FEM_UNVFILE1"]))[0]+".png"
    Pieces.brepfile = os.environ["FEM_PROTO_PATH1"] +"Partition_1_erste2D.brep"
    Pieces.ng2D=NG_2D
    return Pieces
    
def makefacefrompointsL(occpointsL):
    '''
    return ref to compound of faces mad from lists of vertices (3d too be implemented)
    '''
    docfaceL=[]
    for points in occpointsL:
	a1=Draft.makeWire(points,closed=True,face=True,support=None)
	docfaceL.append(FreeCAD.ActiveDocument.getObject(a1.Name))
    compound0=FreeCAD.activeDocument().addObject("Part::Compound","Compound")
    compound0.Links= docfaceL
    FreeCAD.ActiveDocument.recompute()

    return compound0

def addpointstoface(compound0):
    '''
    add vertex at every intersection of touching edges
    prepare for gmsh-style meshing
    ugly workaround (3d to be implemented)
    '''
    FaceApp2=[]
    for sh1 in compound0.Links:
	compoundtemp=compound0.Shape#??
	for cutitem in list(set(compound0.Links)-set([sh1])):
	    compoundtemp=compoundtemp.cut(cutitem.Shape)
	sh4=Part.show(compoundtemp)
	FaceApp2.append(FreeCAD.ActiveDocument.getObject(FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1].Name))
	#Oxford Rumpelstiltskin FC Style
    compound=FreeCAD.activeDocument().addObject("Part::Compound","Compound")
    compound.Links= FaceApp2
    FreeCAD.ActiveDocument.recompute()

    return compound

def gmshmesh(compound, NG2D, name=""):
    '''
    export, mesh compound at gmsh, reimport as .unv
    (3d to be implemented)
    '''
    if name =="": name="m_"+compound.Label
    #
    ImportGui.export([FreeCAD.activeDocument().getObject(compound.Name)], "/tmp/tmpNO2c.step")
    #
    command="/usr/bin/gmsh /tmp/tmpNO2c.step -2 -format unv -o /tmp/"+name+".unv -algo "+str(NG2D.gmshalgoname)+" -clmax " +str(NG2D.NGParamSetMaxSize)+" -clmin "+str(NG2D.NGParamSetMinSize)+" -string Geometry.OCCSewFaces=1;"
    #command="/usr/bin/gmsh /tmp/tmpNO2c.step -2 -format unv -o /tmp/Compound019_Mesh.unv -algo auto -string Geometry.OCCSewFaces=1;"

    #command="g"
    #
    #print command
    output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
    FreeCAD.Console.PrintMessage(output)
    #
    Fem.insert("/tmp/"+name+".unv", FreeCAD.ActiveDocument.Name)
    #Fem.insert("/tmp/Compound019_Mesh.unv", FreeCAD.ActiveDocument.Name)
    femmesh=FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1]
    FreeCADGui.ActiveDocument.getObject(femmesh.Name).DisplayMode = "Wireframe"
    return femmesh

def make_mb_edge(femmesh):
    '''
    make all bodies confining boundary mesh edges
    (3d to be implemented)
    '''
    a4=[]
    #mesh.FemMesh.Edges[1]
    for a1 in femmesh.FemMesh.Edges:
	a=femmesh.FemMesh.getElementNodes(a1)
	a2=femmesh.FemMesh.getNodeById(a[0])
	a3=femmesh.FemMesh.getNodeById(a[1])
	#points=[FreeCAD.Vector(-1.35669851303,0.0587738975883,0.0),FreeCAD.Vector(-1.15098953247,-0.264482706785,0.0)]
	points=[a2,a3]
	a4.append(Draft.makeWire(points,closed=False,face=True,support=None))

    compoundline=FreeCAD.activeDocument().addObject("Part::Compound","Compound")
    compoundline.Links= a4
    FreeCAD.ActiveDocument.recompute()

    return compoundline

def removeobjectswithchildren(docobjL):
    '''
    document object list  
    '''
    for i in docobjL:
	try:
	    tid=i.TypeId
	except BaseException:
	    continue

	if str(tid)=='Fem::FemMeshObject':
	    i.Document.removeObject(i.Name)
	if str(tid)=='App::DocumentObjectGroup':
	    i.removeObjectsFromDocument() #mean: delete childs
	    i.Document.removeObject(i.Name) # delete object
	    continue
	if str(tid)=='Part::Compound':	    
	    for j in i.Links:
		i.Document.removeObject(j.Name)
	    i.Document.removeObject(i.Name)
	    continue
	i.Document.removeObject(i.Name)
    return 
#ok

def cleandocobjs(fc_docname):
    '''
    remove all objects from document   
    '''
    docobjL=FreeCAD.getDocument(fc_docname).Objects
    for i in docobjL:i.Document.removeObject(i.Name)
#ok

def make_topo_edge(compoundpoi2):
    '''
    make all bodies confining boundary mesh edges
    (3d to be implemented)
    '''
    #!visu lines topo
    edgetL=[]
    for a in compoundpoi2.Shape.Edges:
	Part.show(a)
	edgetL.append(FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1])

    compoundpoi2=FreeCAD.activeDocument().addObject("Part::Compound","Compoundi2")
    compoundpoi2.Links= edgetL
    FreeCAD.ActiveDocument.recompute()

    return compoundpoi2


def checkfordoublenodes(m):
    '''
    check for double nodes
    return [a3,a2,aref] #doubles, doubled, ref table
    '''
    aref=[0]*len(m.Nodes.values())
    a2=[]
    a3=[]
    a1=0
    index=0
    for i in m.Nodes.values():
	a=0
	index1=0
	for j in m.Nodes.values():
	    #if m.Nodes.keys()[index]==m.Nodes.keys()[index1]:continue
	    #trivial case
	    if (index<index1):
		if i==j: 
		    a2.append(m.Nodes.keys()[index])
		    a3.append(m.Nodes.keys()[index1])
		    aref[index1]=m.Nodes.keys()[index]
		    #print str(i)+"double occurred index"+str(m.Nodes.values().index(i))
		    a1=a1+1
		    a=a-1
	    index1=index1+1
	index=index+1

    print str(a1)+" doubles"
    #check double nodes end
    return [a3,a2,aref] #doubles, doubled, ref table

def cleanmeshdoubles(femmesh):
    '''
    find doubles nodes, double edges as they occur after gmsh (2d) unv import   -by "checking for double interboundary edges"
    eleminate edges, nodes and rereference 
    '''
    #m=femmesh.FemMesh
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
	    m.addFace(facesE[i][0],facesE[i][1],facesE[i][2])
	if len(facesE[i])==2:
	    a=m.addEdge(facesE[i][0],facesE[i][1])

    Fem.show(m)
    femmesh2=femmesh1.Document.Objects[len(femmesh1.Document.Objects)-1]
    return femmesh2

def visu_annotate_element(m, elementIDL=[], bodyflag=[]):
    '''
    visu:annotate Elemend by face eLementID ('Fem::FemMesh, [elementID],[element bodynumber])
    bodyflag:[element bodynumber]
    '''
#! visu:annotate Elemend by ELementID (all)
    #m.TypeId
    #'Fem::FemMesh'
    if bodyflag==[]:bodyflag=[""]*(len(m.Faces)+1)
    if elementIDL==[]:
	facesL=m.Faces
    else: facesL=elementIDL
    fxyz=[]
    a=[]
    index=0
    for m_elem in facesL:
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
	a.append(FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1])
	anno.BasePosition = FreeCAD.Vector(xres,yres,zres)
	LabelTexti = "i" + str(m.Faces.index(m_elem)+1)
	LabelTextb = "b" +str(bodyflag[index])
	#print "index"+str(index)
	LabelTexte ="E" + str(m_elem)
	LabelTextn =" N" +str(m.getElementNodes(m_elem))
	anno.LabelText =LabelTexti+LabelTextb+LabelTexte+LabelTextn

    group_m_elem_Anno=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
    #g=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
    group_m_elem_Anno.Group = a
    group_m_elem_Anno.Label="group_m_elem_Anno."
    FreeCAD.ActiveDocument.recompute()
    #check double nodes end
    return group_m_elem_Anno

def visu_annotate_note(femmesh,nodeIDL=[]):
    '''
    visu:annotate nodes by nodesID ('Fem::FemMesh, [nodeID])
    '''
    #! visu:annotate Nodes by id
    femmesh.TypeId
    m=femmesh.FemMesh
    #'Fem::FemMesh'
    fxyz=[]
    a=[]
    #nodes=[33,34]
    #nodes=faceN[0]
    #nodes=faceN[1]
    if nodeIDL==[]:
	nodes=m.Nodes.keys()
    else:nodes=nodeIDL
    flag=0
    for i in range(len(m.Nodes)): 
	#m.Nodes.values()[i]
	#m.Nodes.keys()[i]
	if set([m.Nodes.keys()[i]]) & set(nodes):
	#selective displaying..
	    anno = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","surveyLabel")
	    #a.append(anno)
	    a.append(FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1])
	    anno.BasePosition = m.Nodes.values()[i]
	    anno.LabelText = "i" + str(i+1)+"n" + str(m.Nodes.keys()[i])
	    anno.ViewObject.BackgroundColor=(0.5, 0.333, 1.0, 0.0)

    group_m_elem_Anno=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
    #g=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
    group_m_elem_Anno.Group = a
    group_m_elem_Anno.Label="group_m_node_Anno."
    FreeCAD.ActiveDocument.recompute()
    return group_m_elem_Anno

def visu_annotate_edge_element(m, elementIDL=[], bodyflag=[]):
    '''
    visu:annotate boundary element by face eLementID ('Fem::FemMesh, [elementID],[element bodynumber])
    bodyflag:[element bodynumber]
    '''
#! visu:annotate Elemend by ELementID (all)
    #m.TypeId
    #'Fem::FemMesh'
    if bodyflag==[]:bodyflag=[""]*(len(m.Faces)+1)
    if elementIDL==[]:
	facesL=m.Edges
    else: facesL=elementIDL
    fxyz=[]
    a=[]
    index=0
    for m_elem in m.Edges:
	if set([m.Edges[index]]) & set(facesL):	    
	    #a=[]
	    fxyz=[]
	    print str(m_elem)+"Elementnr"
	    print str(m.getElementNodes(m_elem))+"getElementNodes"
	    for m_ne_elem in m.getElementNodes(m_elem):
		print str(m_ne_elem)+"ElementNodenr"
		print str(m.getNodeById(m_ne_elem)) +"ElementNodenrs xyz"
		fxyz.append(m.getNodeById(m_ne_elem))
		
	    yres=(fxyz[0].y+fxyz[1].y)/2
	    xres=(fxyz[0].x+fxyz[1].x)/2
	    zres=(fxyz[0].z+fxyz[1].z)/2
	    anno = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","surveyLabel")
	    #a.append(anno)
	    a.append(FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1])
	    anno.BasePosition = FreeCAD.Vector(xres,yres,zres)
	    LabelTexti = "i" + str(m.Edges.index(m_elem)+1)
	    LabelTextb = "b" +str(bodyflag[index])
	    #print "index"+str(index)
	    LabelTexte ="E" + str(m_elem)
	    LabelTextn =" N" +str(m.getElementNodes(m_elem))
	    anno.LabelText =LabelTexti+LabelTextb+LabelTexte+LabelTextn
	    anno.ViewObject.BackgroundColor=(0.5, 0.1, 1.0, 0.0)
	index=index+1
	
    group_m_elem_Anno=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
    #g=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
    group_m_elem_Anno.Group = a
    group_m_elem_Anno.Label="group_m_edge_Anno."
    FreeCAD.ActiveDocument.recompute()
    #check double nodes end
    return group_m_elem_Anno


def rereference_elments(femmesh,dnL2):
    ''' 
    rereference elements of double node)
    two edges ids und node ids
    return cleaned table of Elements
    '''
    facesE=[list(femmesh.FemMesh.getElementNodes(fac)) for fac in list(set(femmesh.FemMesh.Edges).union(set(femmesh.FemMesh.Faces)))]
    for i in range(len(facesE)):
	for j in range(len(facesE[i])):
	    firstval=dnL2[femmesh.FemMesh.Nodes.keys().index(facesE[i][j])]
	    if firstval!=0:
		facesE[i][j]=firstval    
    return facesE

