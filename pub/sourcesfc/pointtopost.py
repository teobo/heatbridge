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
    Rs=0.0

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
    femmesh1=object ##original state after meshing
    femmesh1name="femmesh1"
    femmesh2=object #state after eleminating duplicate
    femmesh2name="femmesh2"
    comp_mb_edges=None #compound of mesh_ boundary_ edges
    comp_mb_edgesstr="cp_mb_edg"
    comp_topo_edges=None #compound of topo edges
    comp_topo_edgesstr="cp_tedg" #
    comp_topo_points=None #compound of topo edges
    comp_topo_pointsstr="cp_t_points" #
    dnL=[] #[a3,a2,aref] #doubles, doubled, ref table
    dnE=[] # [[node ids of first edge],[node ids of first edge],first edge, double edge]    
    egdeN=[] #(nodes per topoedge of a compound)
    faceN=[] # (nodes per topoface(body) of a compound)
    edgeL=[] # list of edges, whereas doubles are marked
    nodeL=[] # list of nodes, whereas doubles are marked
    facesE=[] #rereferenced cleaned table of Elements (not 
    boundaries=[] #[[bnd0from_topo_edge1,bnd2from_top_edge2],[bnd1from_topo_edge5]
    bnd_tegdeL=[] #[[index of topo_edge1,topo_edge2],[topo_edge5]
    bodyflag=[]
    egdegroup=[]
    solutionheader=[]
    solutiondata=[]
    headerline=[]
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
    ###
    Pieces.fempath = "/tmp/elmermesh/"
    ###
    Pieces.siftemplfile = os.environ["FEM_PROTO_FLUX3_PATH"]+'flux_templ_2bodys.sif'
    ###
    Pieces.siffile = "/tmp/elmermesh/"+"flux.sif"
    ###
    Pieces.gridpath = "/tmp/elmermesh/"+"angle/" # where ElmerSolver takes mesh from
    ###
    Pieces.epfile ="/tmp/elmermesh/"+"case.ep"
    Pieces.eptemplfile ="/tmp/elmermesh/"+"angle/TempDist.ep"
    ###
    Pieces.epsourcefile = os.environ["FEM_PROTO_FLUX3_PATH"]+"cmd1.txt"
    Pieces.vtufile = "/tmp/elmermesh/"+"angle/case0001.vtu"
    Pieces.pngfile ="/tmp/elmermesh/"+"elmermesh.png"
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
	else:
	    for j in i.Links:
		i.Document.removeObject(j.Name)
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

    compoundpoi3=FreeCAD.activeDocument().addObject("Part::Compound","Compoundi2")
    compoundpoi3.Links= edgetL
    FreeCAD.ActiveDocument.recompute()

    return compoundpoi3


def checkfordoublenodes(m):
    '''
    check for double nodes
    return [a3,a2,aref] #doubles, first, ref table
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
	    if (index>index1):
		if i==j: 
		    a2.append(m.Nodes.keys()[index])
		    a3.append(m.Nodes.keys()[index1])
		    aref[index]=m.Nodes.keys()[index1]
		    #print str(i)+"double occurred index"+str(m.Nodes.values().index(i))
		    a1=a1+1
		    a=a-1
		    break
	    index1=index1+1
	index=index+1
    #print str(a1)+" doubles "
    #check double nodes end
    return [a3,a2,aref] #doubles, doubled, ref table

def cleanmeshdoubles(femmesh):
    '''
    defunct
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
	    #print "double"
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
		#print "first edge endpoints vectors:" + str(a2) + " " + str(a3)+"double nodes " + str(a) + " " + str(a5) +"first +double edge: " + str(a1) + " " + str(a4) +"\ndoublenodespair1by2: "	 + str(doublenode1)  +" "+ str(doublenode2)   +"\ndoublenodespair3by4: "	 + str(doublenode3)  +" "+ str(doublenode4)
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
	    #print str(elen) +"mface i with 2 double node:" + str(fac) +"to be substituted by:" + str(first_n_plain[double_n_plain.index(elen[0])]) +" to " +str(facesE[fac])+" from " +str(factem)
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
	#print str(m_elem)+"Elementnr"
	#print str(m.getElementNodes(m_elem))+"getElementNodes"
	for m_ne_elem in m.getElementNodes(m_elem):
	    #print str(m_ne_elem)+"ElementNodenr"
	    #print str(m.getNodeById(m_ne_elem)) +"ElementNodenrs xyz"
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

def visu_annotate_note(femmesh,nodeIDL=[],annostrL=[]):
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
    if annostrL==[]:
	annostr=""
	
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
	    if annostrL!=[]:
		annostr=annostrL[i]
	    anno.LabelText = "i" + str(i+1)+"n" + str(m.Nodes.keys()[i]) +str(annostr)
	    anno.ViewObject.BackgroundColor=(0.5, 0.333, 1.0, 0.0)

    group_m_elem_Anno=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
    #g=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
    group_m_elem_Anno.Group = a
    group_m_elem_Anno.Label="group_m_node_Anno."
    FreeCAD.ActiveDocument.recompute()
    return group_m_elem_Anno

def visu_annotate_edge_element(m, elementIDL=[], groupflag=[],flag=""):
    '''
    visu:annotate boundary element by face eLementID ('Fem::FemMesh, [elementID],[element bodynumber])
    groupflag:[element bodynumber]
    '''
#! visu:annotate Elemend by ELementID (all)
    #m.TypeId
    #'Fem::FemMesh'
    if groupflag==[]:groupflag=[""]*(len(m.Edges)+1)
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
	    #print str(m_elem)+"Elementnr"
	    #print str(m.getElementNodes(m_elem))+"getElementNodes"
	    for m_ne_elem in m.getElementNodes(m_elem):
		#print str(m_ne_elem)+"ElementNodenr"
		#print str(m.getNodeById(m_ne_elem)) +"ElementNodenrs xyz"
		fxyz.append(m.getNodeById(m_ne_elem))
		
	    yres=(fxyz[0].y+fxyz[1].y)/2
	    xres=(fxyz[0].x+fxyz[1].x)/2
	    zres=(fxyz[0].z+fxyz[1].z)/2
	    anno = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel","surveyLabel")
	    #a.append(anno)
	    a.append(FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1])
	    anno.BasePosition = FreeCAD.Vector(xres,yres,zres)
	    LabelTexti = "i" + str(m.Edges.index(m_elem)+1)
	    LabelTextg = "g" +str(groupflag[index])
	    #print "index"+str(index)
	    LabelTexte ="E" + str(m_elem)
	    LabelTextn =" N" +str(m.getElementNodes(m_elem))
	    anno.LabelText =LabelTexti+LabelTextg+LabelTexte+LabelTextn
	    anno.ViewObject.BackgroundColor=(0.5, 0.1, 1.0, 0.0)
	index=index+1
	
    group_m_elem_Anno=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Group")
    #g=App.ActiveDocument.Objects[len(App.ActiveDocument.Objects)-1]
    group_m_elem_Anno.Group = a
    group_m_elem_Anno.Label="group_m_edge_Anno."
    FreeCAD.ActiveDocument.recompute()
    #check double nodes end
    return group_m_elem_Anno

def rereference_elments(femmesh,dnL2,edgeL):
    ''' 
    rereference elements of double node
    two edges ids und node ids
    return rereferenced cleaned table of Elements
    '''
    facesE=[list(femmesh.FemMesh.getElementNodes(fac)) for fac in edgeL+list(femmesh.FemMesh.Faces)]
    #print dnL2
    for i in range(len(facesE)):
	for j in range(len(facesE[i])):
	    firstval=dnL2[femmesh.FemMesh.Nodes.keys().index(facesE[i][j])]
	    if firstval!=0:
		facesE[i][j]=firstval
    return facesE

def finddoubleedges(femmesh):
    '''
    check for double edges (same nodes)
    return: [[node ids of first edge],[node ids of first edge],first edge, double edge]
    '''
    refnodes=[-1]*len(femmesh.FemMesh.Nodes)
    res=[]
    #res=[(-1,-1),(-1,-1),-1,-1]
    resvec=[]
    edgeE=femmesh.FemMesh.Edges
    for a1 in edgeE:
	if res!=[] and len(set([a1]) & set([i[3] for i in res]))!=0:
	    #print "double double" 
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
		#print "first edge endpoints vectors:" + str(a2) + " " + str(a3)+"double nodes " + str(a) + " " + str(a5) +"first +double edge: " + str(a1) + " " + str(a4) +"\ndoublenodespair1by2: "	 + str(doublenode1)  +" "+ str(doublenode2)   +"\ndoublenodespair3by4: "	 + str(doublenode3)  +" "+ str(doublenode4)
		res.append([a,a5,a1,a4]) #two edges ids and node ids
		resvec.append([[a2,a3]])
		#eleminate double edges
		#edgeE=set(edgeE)-set([a4])
		#eleminate (hopefully) all double nodes and reference them
		#if doublenode2 in nodeP:
		    #del nodeP[doublenode2]
		    #refnodes[doublenode2]=doublenode1
		#if doublenode4 in nodeP: 
		    #del nodeP[doublenode4]
		    #refnodes[doublenode4]=doublenode3		
		#del nodeP[doublenode4]
		break

    ##check double nodes end
    return res

def mark_deleted_edges(femmesh,dnE3):
    '''
    if edge within set of double edge, mark its IDlist place with -1
    '''
    edgeL= list(femmesh.FemMesh.Edges)
    for i in range(len(edgeL)):	
	if len(set([edgeL[i]])&set(dnE3))!=0:
	     edgeL[i]=-1
	
    return edgeL

def mark_deleted_nodes(femmesh,dnL2):
    '''
    if node within set of double nodes, mark its IDlist place with -1
    '''
    nodeL= list(femmesh.FemMesh.Nodes.keys())
    for i in range(len(nodeL)):	
	if dnL2[i]!=0:
	     nodeL[i]=-1
	
    return nodeL

def rebuild_mesh(femmesh,nodeL,facesE):
    '''
    (femmesh,nodeL,facesE)
    '''
    import FreeCAD, Fem
    m = Fem.FemMesh()
    nodeP=femmesh.FemMesh.Nodes.values()
    for n in range(len(nodeL)):
	if nodeL[n]==-1: continue
	#print str(n1) + " :" + str(n)
	n1=nodeP[n]
	#print str(n1) + " :" + str(n)
	m.addNode(n1.x, n1.y, n1.z, n+1)
  
    elemN=nodeL+list(femmesh.FemMesh.Faces)
    for i in range(len(facesE)):
	#print str(facesE[i]) + " " + str(elemN[i])+"  i:" + str(i)
	#loose id's here
	if len(facesE[i])==3:
	    #debug
	    #print "  l"+str(i)+ "i"
	    #if len(set(facesE[i])&set(nodeP))!=3:
		#print str(facesE[i]) +"smash"; continue
	    #debug end
	    m.addFace(facesE[i][0],facesE[i][1],facesE[i][2])
	if len(facesE[i])==2:
	    a=m.addEdge(facesE[i][0],facesE[i][1])

    # ok? 
    Fem.show(m)
    femmesh2=FreeCAD.ActiveDocument.Objects[len(FreeCAD.ActiveDocument.Objects)-1]
    return femmesh2

def getnodesbycompoundface(femmesh,compound0):
    '''
    get nodes per topoface(body)
    '''
    faceN=[]
    for i in [a.Shape.Faces[0] for a in compound0.Links]:
	faceN.append(femmesh.FemMesh.getNodesByFace(i))
    return faceN
    
def getnodesbycompoundedge(femmesh,compountO):
    '''
    get nodes per topoface(body)
    '''
    egdeN=[]
    for i in compountO.Shape.Edges:
	egdeN.append(femmesh.FemMesh.getNodesByEdge(i))
    return egdeN

def get_bnd_nodesbytedge(femmesh,compound,bnd):
    '''
    get bnd nodes per comp_topo_edges
    '''
    boundaries=[]
    #print str(bnd) + ":bnd:"
    for i in bnd:
	bnd_group=[]
	for j in i:
	    #print str(i) + ":j,i:" +str(j)
	    bnd_group.append(femmesh.FemMesh.getNodesByEdge(compound.Shape.Edges[j]))
	boundaries.append(bnd_group)
	#print str(bnd_group) + ":bndgroup"
    return boundaries

def get_tedge_bnd_nodesbyselection(femmesh,compountO):
    '''
    return [[1,3],[5]]
    to be implemented
    '''
    return egdeN

def visu_bnd_tedge(compoundO,bnd):
    '''
    
    '''
print str(bnd) + ":bnd:"
k=0.0
print str(bnd) + ":bnd:"
for i in bnd:
    k=k+1
    l=(1.0/len(bnd))*k
    print str(l)+ " "+str((1/len(bnd)))
    for j in i:
	compoundO.Links[j].ViewObject.LineColor= (l,0.33,0.50)
	print str(i) + ":j,l:" +str(l)+ "k:" +str(k)

def get_elementbodysflag(femmesh2,compountO,faceN):
    '''
    #!## get a per node Elementbodysflag
    '''
    
    feln=[]
    bodyflag=[-1]*len(femmesh2.FemMesh.Faces)
    #f = femmesh.FemMesh.Faces[1]
    for f in range(len(femmesh2.FemMesh.Faces)):
	feln.append(femmesh2.FemMesh.getElementNodes(femmesh2.FemMesh.Faces[f]))
	for i in range(len(faceN)):
	    if len(set(feln[f])& set(faceN[i]))==3:
		#print "huh" + str(i)+ " Elementiter" + str(f) +" elemid"+ str(femmesh2.FemMesh.Faces[f])
		bodyflag[f]=i+1
		continue
	    else:
		pass
		#print "he"+str(i)
#ok   
    return bodyflag

def get_edgegroup_and_neighbor(femmesh2,compountO,faceN,bnd):
    '''
    #!##get by edge id: neighbors and bnd Groupflag
    return [groupflag, neighbourelem1, neighbourelem1]
    (Pi.femmesh2,Pi.compound0,Pi.faceN,Pi.boundaries)
    '''
 #!
    #bnd=[]
    #bnd.append(bnd1_group)
    #bnd.append(bnd2_group)
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
		    #print str(i) +" i"+str(femmesh2.FemMesh.getElementNodes(i)) +" getElementNodes"
		    #print bnd[bndg][i1]
		    igroup=bndg++1+igroupbias
	#calculating neigborcells
	ineighbele1=0
	ineighbele2=0
	for e in femmesh2.FemMesh.Faces:
	    s2=set(femmesh2.FemMesh.getElementNodes(i))
	    s1=set(femmesh2.FemMesh.getElementNodes(e))
	    if len(s1&s2)==2: 
		#print " e"+str(e) +" edgeid"+str(i)
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
    
    return [groupflag, neighbourelem1, neighbourelem2]

def prepare_elemer_output(gridpath=""):
    '''
    make and clean export dir
    '''
    #!elmermeshfile mesh.nodes test code 
    import os
    import time
    import sys

    
    if gridpath=="":
	elmer_mesh_path="/tmp/elmermesh/"
    else:
	elmer_mesh_path=gridpath
    
    
    try:
	os.makedirs(elmer_mesh_path)
    except OSError:
	pass

    path=elmer_mesh_path+"mesh.nodes"

    try:
	os.remove(path)
    except OSError:
	pass

    path=elmer_mesh_path+"mesh.elements"

    try:
	os.remove(path)
    except OSError:
	pass

    path=elmer_mesh_path+"mesh.boundary"

    try:
	os.remove(path)
    except OSError:
	pass

    path=elmer_mesh_path+"mesh.header"

    try:
	os.remove(path)
    except OSError:
	pass


    return

def write_elemer_nodes_file(femmesh2,gridpath=""):
    '''
    (femmesh2,gridpath="")
    '''
    elmer_mesh_path=gridpath
    if gridpath=="":elmer_mesh_path="/tmp/elmermesh/"
    mesh_nodes_path=elmer_mesh_path+"mesh.nodes"
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
    return

def write_elmer_header_file(femmesh2,gridpath=""):
    '''
    (femmesh2,gridpath="")
    '''
    #nodes elements boundary-elements
    #nof_types
    #type-code nof_elements
    #type-code nof_elements
    elmer_mesh_path=gridpath
    if gridpath=="":elmer_mesh_path="/tmp/elmermesh/"
    mesh_nodes_path=elmer_mesh_path+"mesh.header"
    mesh_head_path=elmer_mesh_path+"mesh.header"

    meshheadf= open(mesh_head_path, 'a') #'a' opens the file for appending


    line=str(femmesh2.FemMesh.NodeCount)\
    +" "+str(femmesh2.FemMesh.FaceCount)\
    +" "+str(femmesh2.FemMesh.EdgeCount)\
    +"\n"+str(2)\
    +"\n303 "+str(femmesh2.FemMesh.FaceCount)\
    +"\n202 "+str(femmesh2.FemMesh.EdgeCount)
    meshheadf.write(line)#'a' opens the file for appendingf.write(line)

    meshheadf.close() #'a' opens the file for 
    return

def write_elmer_elements_file(femmesh2,bodyflag,gridpath=""):
    '''
    (femmesh2,bodyflag,gridpath="")
    '''
    #!elmermeshfile elements test code 
    #e1 body type n1 ... nn
    #1 1 404 1 2 32 31
    elmer_mesh_path=gridpath
    if gridpath=="":elmer_mesh_path="/tmp/elmermesh/"
    mesh_nodes_path=elmer_mesh_path+"mesh.elements"

    mesh_element_path=elmer_mesh_path+"mesh.elements"

    meshelementf= open(mesh_element_path, 'a') #'a' opens the file for appending
    #meshelementf.write("huia\n")


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

    meshelementf.close()   
    #ok

    return

def write_elemer_boundary_file(femmesh2,egdegroupL,gridpath=""):
    '''
    #!produce elmer boundary file femmesh2,egdegroupL,gridpath="")
    '''
    
    #e1 bndry p1 p2 type n1 ... nn
    #1 5 1 0 202 9 4

    groupflag=egdegroupL[0]
    neighbourelem1=egdegroupL[1]
    neighbourelem2=egdegroupL[2]
  
    elmer_mesh_path=gridpath
    if gridpath=="":elmer_mesh_path="/tmp/elmermesh/"
    mesh_nodes_path=elmer_mesh_path+"mesh.boundary"

    mesh_bnd_path=elmer_mesh_path+"mesh.boundary"

    meshebndf= open(mesh_bnd_path, 'a') #'a' opens the file for appending


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
    meshebndf.close() #'a' opens the file for appendingf.close()   

    return 

def write_elmer_sif_file(siftemplfile,siffile,Bodies,Bnds):
    '''
    #sif manipulation
    sif preparation body, boundary and material blocks generation
    '''
    import re
    stdin, stdout = os.popen2('cp %s %s' % (siftemplfile,siffile));a1=stdout.read()
    
    #get text of file in one variable: s
    fh=open(siffile)
    s=fh.read();fh.close()
    
    #manipulate "Material" blocks
    pattern="\nMaterial.*?\nEnd"
    it=re.findall(pattern,s,re.MULTILINE+re.DOTALL)
    #got occurences in s:
    #['\nMate...End', '\nMate...End'..]
    a=[ite.span() for ite in re.finditer(pattern,s,re.MULTILINE+re.DOTALL)]
    #[(3089, 3166), (3167,..]
    # get the last index
    indlast=list(a[len(a)-1])[1]
    #get the first index for that pattern
    ind=list(a[0])[0]
    #take one matched passage as template
    subpassage=it[0]
    #remove original occurrences of passage
    s=s[:ind]+s[indlast:]
    for i in range(len(Bodies)):
	#print "append Materialblock"
	#duplicate sif Bodyparapgraph
	#within the pattern's last found passage substitute:
	subpattern='M(aterial\ )[0-9]+?'
	substitutepattern="Material "+ str(i+1)
	subpassage=it[0]
	it1= re.sub(subpattern, substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)
	#
	subpattern='M(aterial)[0-9]+?'
	substitutepattern="Material"+ str(i+1)
	subpassage=it1
	it2= re.sub(subpattern,substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)
	#
	subpattern='Conductivity = [0-9]*\.?[0-9]*'
	substitutepattern="Conductivity = "+ str(Bodies[i].k)
	subpassage=it2
	it3= re.sub(subpattern,substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)
	#
	s=s[:ind]+"\n"+it3+s[ind:]
	#reglued 
	ind=ind+len(it3)+1
	
    #manipulate "Body" blocks
    pattern="\nBody.*?\nEnd"
    it=re.findall(pattern,s,re.MULTILINE+re.DOTALL)
    #got occurences in s:
    #['str', 'str1'..]
    a=[ite.span() for ite in re.finditer(pattern,s,re.MULTILINE+re.DOTALL)]
    #[(3089, 3166), (3167,..]
    # get the last index
    indlast=list(a[len(a)-1])[1]
    #get the first index for that pattern
    ind=list(a[0])[0]
    subpassage=it[0]
    #remove original occurrences of passage
    s=s[:ind]+s[indlast:]
    for i in range(len(Bodies)):
	#change contents: Body number
	subpattern='(Body\ )[0-9]+?'
	substitutepattern="Body "+ str(i+1)
	subpassage=it[0]
	it1= re.sub(subpattern, substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)
    
	#change contents: Target Bodies number	
	subpattern='Target Bodies\(1\) = [0-9]+?'
	substitutepattern="Target Bodies(1) = "+ str(i+1)
	subpassage=it1
	it2= re.sub(subpattern, substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)

	#change contents:  Body number	
	subpattern='Body[0-9]+?'
	substitutepattern="Body"+ str(i+1)
	subpassage=it2
	it3= re.sub(subpattern, substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)

	#change contents: Body Material number
	subpattern='(Material = )[0-9]+?'
	substitutepattern="Material = "+ str(i+1)
	subpassage=it3
	it4= re.sub(subpattern, substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)

	s=s[:ind]+"\n"+it4+s[ind:]
	#reglued 
	ind=ind+len(it4)+1

    #manipulate "Boundary Condition" blocks
    pattern="\nBoundary.*?\nEnd"
    it=re.findall(pattern,s,re.MULTILINE+re.DOTALL)
    #got occurences in s:
    #['str', 'str1'..]
    a=[ite.span() for ite in re.finditer(pattern,s,re.MULTILINE+re.DOTALL)]
    #[(3089, 3166), (3167,..]
    # get the last index
    indlast=list(a[len(a)-1])[1]
    #get the first index for that pattern
    ind=list(a[0])[0]
    
    #remove original occurrences of passage
    s=s[:ind]+s[indlast:]
    for i in range(len(Bnds)):
	#change contents: Target Boundary number	
	subpattern='(  Target Boundaries\(1\) =) [0-9]+?'
	substitutepattern="  Target Boundaries(1) = "+ str(len(Bodies)+i+1)
	subpassage=it[0]
	it2= re.sub(subpattern, substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)

	#change contents:  Boundary Temperature
	subpattern='Temperature = [0-9]*\.?[0-9]*'
	substitutepattern="External Temperature = "+ str(Bnds[i].T)
	substitutepattern2 = "\n  Heat Transfer Coefficient = "+ str(1/Bnds[i].Rs)
	subpassage=it2	
	it3= re.sub(subpattern, substitutepattern+substitutepattern2,subpassage,flags=re.MULTILINE+re.DOTALL)

	#change contents:  Boundary Condition 1
	subpattern='Boundary Condition [0-9]*'
	substitutepattern="Boundary Condition "+ str(i+1)
	subpassage=it3	
	it4= re.sub(subpattern, substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)

	#change contents:  Boundary Condition 1
	subpattern='Name = \".*\"'
	substitutepattern="Name = "+ ' \"'+str(Bnds[i].T) + "_" +  str(Bnds[i].Rs) + "_" + str(i)+ '\"'
							
	subpassage=it4	
	it5= re.sub(subpattern, substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)

	s=s[:ind]+"\n"+it5+s[ind:]
	#reglue 
	ind=ind+len(it5)+1
	
    fh=open(siffile,"w")
    fh.write(s);fh.close()	
    return s , siffile

def register_bodies_and_boundaries(bnd_tegdeL,Bodies,Bnds,compound0):
    '''
    #register:
    fill body and boundary structures for further processing: Rs, T, k, 
    to be implemented: read from file
    '''
    bnd_tegdeL=[[1,3],[18]]
    bnd_rs=[0.13,0.10]
    kL=[0.03,0.03,0.03,0.1,0.33]
    Bodies=[]
    for i in range(len(compound0.Links)):
	Bodies.append(Body())
	Bodies[i].k=kL[i]
    Bnds=[]
    TL=[292,259]
    for i in range(len(bnd_tegdeL)):
	Bnds.append(Bnd())
	Bnds[i].T=TL[i]
	Bnds[i].Rs=bnd_rs[i]
    return bnd_tegdeL, Bnds, Bodies

def process_elmer_sif_file(siffile,epsourcefile,fempath,debug=1001):
    '''
    run Elmer
    '''
    os.chdir("%s" % fempath)
    stdin, stdout = os.popen2('echo %s > ELMERSOLVER_STARTINFO ; ElmerSolver;'% os.path.basename(siffile));a=stdout.read() #popen2 wait until finished - hopefully
    #optionally viewing
    print a
    if int(str(debug)[len(str(debug))-1])==1:stdin, stdout = os.popen2('killall ElmerPost; ElmerPost source %s' % epsourcefile)

def read_ep_result(epfile):
    '''
    reading  from an elmer ep file 
    -the results
    -some header info
    -too be implemented: reading nodes, elements, boundary data, vector vars, multiple timesteps: to be tested, non binary 
    see nic.funet.fi/pub/sci/physics/elmer/doc/ElmerSolverManual.pdf page 124
    nn ne nf nt scalar: name vector: name ...
    x0 y0 z0
    ...        ! nn rows of node coordinates (x,y,z)
    xn yn zn
    group-name element-type i0 ... in
    ...        ! group data and element decriptions
    group-name element-type i0 ... in
    #time 1 timestep1 time1
    vx vy vz p ...
    ...        ! nn rows
    vx vy vz p ...
    #time 2 timestep2 time
    '''
    import re
    frd_file = open(epfile, "r")
    solutionheader = []
    solutiondata = [] #[[result vars2][results var2],[timestep2]
    solutiondatasection=[]#[timestep1]
    headerflag=""
    lc=1 #linecounter
    str_frd_file=frd_file.readlines()
    n_str_frd_file=len(str_frd_file)
    for line in str_frd_file:
	#check if we found header section
	# is first line
	if lc==1:
	    headerline=[i for i in re.split('\n|\ |:',line) if i]
	#
	#
        #Check if we found solution data
	#time n t time n is the order number of the solution data set,t is the simulation timestep number, and time is the current simulation time
        if re.search('time',line)!=None:
            solutionheaderline=[i for i in re.split('\n|\ |:',line) if i]
            solutionheader.append(solutionheaderline)
            #if not the first timestep section append the last to stack
            if headerflag=="solution":solutiondata.append(solutiondatasection)
            solutiondatasection=[]
            headerflag="solution"
            continue
        #is line last line of file== is last solution line: append last section data
        if headerflag=="solution":
            solutiondataline=[i for i in re.split('\n|\ |:',line) if i]
            #print solutiondataline
            #we need to redim first: unfortunately, such as [[], []]
	    if solutiondatasection==[]:
		for i in range(len(solutiondataline)): solutiondatasection.append([])
	    #we need to transpose 2:
	    for i in range(len(solutiondataline)):
		solutiondatasection[i].append(solutiondataline[i])
	    #print str(n_str_frd_file)+" "+ str(lc)
	    if n_str_frd_file-1==lc:
		solutiondata.append(solutiondatasection)
	#end solution data	
	#print str(solutiondata)+" "+ str(lc)
	lc=lc+1
    frd_file.close()
    
    return solutionheader, solutiondata, headerline

def gradient_color_mesh(solutiondata,femmesh2):
    a1=[float(i) for i in solutiondata]
    b=femmesh2.FemMesh.Nodes.keys()
    femmesh2.ViewObject.setNodeColorByScalars(b,[i-min(a1) for i in a1])
