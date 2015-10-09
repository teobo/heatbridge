import os
import sys
import salome
import GEOM
from salome.geom import geomBuilder
from salome import sg
import math
import SALOMEDS
import re
salome.salome_init()


#Fem vector "piece" definition; 
class NG2D:
    NGParamSetMaxSize=12 #18 
    NGParamSetSecondOrder=0
    NGParamSetOptimize=1
    NGParamSetFineness=5 #5
    NGParamSetGrowthRate=0.2
    NGParamSetNbSegPerEdge=15
    NGParamSetNbSegPerRadius=2
    NGParamSetMinSize=2 #5
    NGParamSetUseSurfaceCurvature=1
    NGParamSetFuseEdges=1
    NGParamSetQuadAllowed=0

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
    ng2D=NG2D
    meshobj=None
    mbmode="test_manual"
    Vp_mb1=[8-1,7-1,8-1,6-1] ##
    Vp_mb2=[1-1,2-1]
    mbedges=None

def testinit151009(Pieces):
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


def delobjregex(complaint="Shape*",s="s",module=''): #http://www.salome-platform.org/forum/forum_10/366900504 much more complicated?? #removes or selects 
    import re
    if module=='':
	mods=["SMESH", "GEOM"]
    else: mods=[module]
    for compName in mods:
	comp = salome.myStudy.FindComponent(compName)
	if comp:
	    iterator = salome.myStudy.NewChildIterator( comp )
	    while iterator.More():
		sobj = iterator.Value()
		print sobj.GetID() + "  " +complaint
		sobject = salome.myStudy.FindObjectID(sobj.GetID())
		print sobject.GetName()
		if re.match(complaint,sobject.GetName())!=None:
		    print "regex"
		    if s!="s":
			print "del"
			salome.sg.Erase(sobj.GetID())
			gg = salome.ImportComponentGUI("GEOM")
			gg.UpdateViewer()
			salome.myStudy.NewBuilder().RemoveObjectWithChildren( sobj )
		    else:
			salome.sg.AddIObject(sobj.GetID())
			salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
			print "he"		    
		iterator.Next()
    salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
   

def displaysalomeplease(i5=100, debug=4, complaint='',complaint1='' ):
    import SalomePyQt 
    #i5[4:1 activate VTK-Viewer [2:2Erase :1DisplayAll [3:1 Fitall
    #complaint1!='' vtk, else occ. complaint1: obj to display
    #displaysalomeplease(10021, 4,)# ok erase occ
    #displaysalomeplease(11021, 4,groupName) #__display only groupname in vtk-viewer
    #FitAll()o #2:100, DisplayAll() #3 10 (erase 20), VTKViewer")[0]) #1000 
    #
    #salome.sg.ResetView() #?: = Fitall? Fitall in VTK case nearer
    #gg.UpdateViewer()
    #error
    #0. something with "mesh update" (from context menu)
    #1. Konsole or Funktion sg.Display: hover over case: Solution occ: gg.UpdateViewer()
    gg = salome.ImportComponentGUI("GEOM")
    sg = SalomePyQt.SalomePyQt()
    if int(str(i5)[len(str(i5))-4])==0:
	sg.activateView(sg.getActiveView())
	sg.activateView(sg.findViews("OCCViewer")[0])
	if complaint1!="":
	    a=salome.myStudy.FindObjectByName(complaint,"GEOM")[0].GetID()
	    salome.sg.Display(a)
	if int(str(i5)[len(str(i5))-2])==2:salome.sg.EraseAll()
	for i in salome.sg.getAllSelected():salome.sg.Display(i)
	salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
	salome.sg.UpdateView() #?was
	if int(str(i5)[len(str(i5))-2])==1:salome.sg.DisplayAll() #3 10
	if int(str(i5)[len(str(i5))-3])==1:salome.sg.FitAll() #2:100
	else:gg.UpdateViewer()	
    #salome.sg.FitAll()
    if int(str(i5)[len(str(i5))-4])==1:
	sg.activateView(sg.findViews("VTKViewer")[0]) 
	if int(str(i5)[len(str(i5))-2])==2:salome.sg.EraseAll()
	salome.sg.UpdateView()
	if complaint!="":	
	    a=salome.myStudy.FindObjectByName(complaint,"SMESH")[0].GetID()
	    salome.sg.Display(a) #only if vtk-viewer activated
	for i in salome.sg.getAllSelected():salome.sg.Display(i)
	if int(str(i5)[len(str(i5))-2])==1: salome.sg.DisplayAll()# forelast digit     
	if int(str(i5)[len(str(i5))-3])==1:salome.sg.FitAll() #2:100
	else:gg.UpdateViewer()
	import iparameters
	if debug!=4:iparameters.getSession().restoreVisualState(1)
    if int(str(i5)[len(str(i5))-4])==2:
	sg.activateView(sg.findViews("ParaView")[0]) 


def restoresalomeiparm(module='ParaViS',splitflag=1):
    import salome
    import iparameters
    ipar = iparameters.IParameters(salome.myStudy.GetCommonParameters("Interface Applicative", 1), True)
    #ipar.setProperty("AP_ACTIVE_VIEW", "ParaView_0_0")
    if splitflag==1:
	ipar.setProperty("AP_ACTIVE_VIEW", "VTKViewer_0_0")
	ipar.setProperty("AP_WORKSTACK_INFO", "00000001000000000000000201000000020000014a000002e9000000040000000100000001000000080000001a00560054004b005600690065007700650072005f0030005f00300000000102000000040000000200000001000000080000001a004f00430043005600690065007700650072005f0030005f00300000000002000000080000001800500061007200610056006900650077005f0030005f00300000000102")
    ipar.setProperty("AP_ACTIVE_MODULE", module)
    ipar.setProperty("AP_SAVEPOINT_NAME", "GUI state: 2")
    #?
    #ipar.append("AP_MODULES_LIST", "Geometry")
    #ipar.append("AP_MODULES_LIST", "Mesh")
    #ipar.append("AP_MODULES_LIST", "ParaViS")
    ipar.append("AP_VIEWERS_LIST", "ParaView_1")
    ipar.append("AP_VIEWERS_LIST", "OCCViewer_2")
    ipar.append("AP_VIEWERS_LIST", "VTKViewer_3")
    iparameters.getSession().restoreVisualState(1)

#zoomobj(-1,-1,-1,-1,obj_name1,obj_name2,"OCCViewer")# ok
#zoomobj(-1,-1,-1,-1,obj_name1,obj_name2) #ok
#zoomobj(50,0,0,9,[""],obj_name2) #ok
def zoomobj(x=-1,y=-1,z=-1,r=-1,obj_name1=[],obj_name2=[],viewer="VTKViewer"):
    salome.sg.EraseAll()
    gg = salome.ImportComponentGUI("GEOM")
    sg.activateView(sg.findViews(viewer)[0])
    if r!=-1:
	sphere = geompy.MakeSphere(x,y,z, r)
	sphere_id = geompy.addToStudy(sphere,"Sphere")
	salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
	gg.createAndDisplayGO(sphere_id)
	gg.setDisplayMode(sphere_id,1) 
	gg.setColor(sphere_id,218,165,31) 
	gg.setTransparency(sphere_id,0.9) 
	salome.sg.FitAll()
	#del ??
    else:
	obj_id= [salome.myStudy.FindObjectByName(i,i1)[0].GetID() for i in obj_name1 for i1 in ["GEOM", "SMESH"]  if salome.myStudy.FindObjectByName(i,i1)!=[] ] 
	print obj_id
	for i in obj_id:salome.sg.Display(i)
	salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
	salome.sg.FitAll()
    if obj_name2!=[]:
	#display the rest unfittet
	obj_id2= [salome.myStudy.FindObjectByName(i,i1)[0].GetID() for i in obj_name2 for i1 in ["GEOM", "SMESH"]  if salome.myStudy.FindObjectByName(i,i1)!=[] ] 
	for i in obj_id2:salome.sg.Display(i)
	salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
	gg.UpdateViewer()
#---------

#complaint="Shape1"
#the8vertices(complaint="Shape1",pause=1) #ok
#visualizes _where are indexed vertexes
def the8vertices(complaint="Shape1",pause=1):
    import salome
    salome.salome_init()
    import GEOM
    import time
    #
    delobjregex(".*phere.*$","t") 
    #
    # zoom
    obj_name1=[complaint] #zoom object
    obj_name2=[] #environment object
    zoomobj(-1,-1,-1,-1,obj_name1,obj_name2,"OCCViewer")# ok
    #
    Shape1=salome.myStudy.FindObjectByName(complaint,"GEOM")[0].GetObject()#.GetID()
    #def:
    VP=(geompy.SubShapeAll(Shape1,geompy.ShapeType["VERTEX"])) #shape 
    for i in range(0,len(VP)):
	sphere = geompy.MakeSpherePntR(VP[i],20)
	sphere_id = geompy.addToStudy(sphere,"Sphere12" +str(i))
	salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
	gg.createAndDisplayGO(sphere_id)
	gg.setDisplayMode(sphere_id,1) 
	gg.setColor(sphere_id,255-255*i/len(VP),165,31) 
	gg.setTransparency(sphere_id,0.01) 
	print "vertex" +str(i)
	time.sleep(pause)


#out[0]list of meshboundary mb nodes, [1]:of edges element in: boundary end points as index in vertex object list of mesh's shape, all boundary elements collection, number of maximal iteration, debug, gimmik
def edge2mbnodes(Pi,VPi1, VPi2, VP, Mesh_1, new_group2,i5end=100, debug=4, complaint='Yes or no, please!'):
    geompy = geomBuilder.New(salome.myStudy)
    mb11point=list(geompy.PointCoordinates(VP[VPi1]))
    mb12point=list(geompy.PointCoordinates(VP[VPi2]))
    if debug!=4:print "mb11point mb12point " + str([mb11point, mb12point])# + mb12node mb11node
    # 
    if debug!=4:print "he"+str(new_group2.GetNodeIDs()) # #debug off, >100 nodes long,list of vertices of shape, mesh, list of mesh's boundary nodes
    mb11node=0; mb12node=0
    for i in new_group2.GetNodeIDs():
	a=Mesh_1.GetNodeXYZ(i)
	if a==mb12point: mb12node=i
	if a==mb11point: mb11node=i
    #boundary points as nodes 
    if debug!=4:print "mb12node mb11node " + str([mb12node, mb11node])# + mb12node mb11node
    #
    #xy repres of Edges
    Vx=[list(geompy.PointCoordinates(i)) for i in VP]
    #
    #Vertexes indices as boundary node list
    Vnodes=[i for i1 in Vx for i in new_group2.GetNodeIDs() if i1==Mesh_1.GetNodeXYZ(i)]
    #[4, 3, 2, 1, 6, 5, 8, 7]
    # 
    #
    # on the neighbour suche
    # Element of mbpoint1
    mesh=Mesh_1
    if debug!=4:mesh.FindElementsByPoint (mb12point[0],mb12point[1],mb12point[2])
    #[119, 134, 920]
    #[133, 134, 842, 860, 920, 945] neughbour does not show up even 
    # lets focus on element 920 
    #Mesh_1.GetElemNodes(920)
    #[8, 119, 133]
    #
    #
    foundpoints0=[mb12node]
    foundpoints=foundpoints0
    if debug!=4:len(foundpoints)
    d=[]
    d0=[]
    resultedge=[]*2
    resultedgeL=[]
    secondbetnode=-1
    lastsecondbetnode=-1
    i5=0
    say="ok"
    # vom ersten boundary eckpunkt, die anliegenden Elemente:b
    a=Mesh_1.GetNodeXYZ(mb12node)
    b=mesh.FindElementsByPoint (a[0],a[1],a[2])
    if debug!=4:print "-ALL_adjacent_Elem_at_start" + str(b) #+"-c1 bound " + str(c1)+"-c " + str(c) + "-d nicht schon " + str(d)
    while list(set(resultedge) & set(foundpoints))==[] and i5<i5end:
	i5=i5+1
	for i in b: #extract neighbor node on boundary line part 1
	    if len(Mesh_1.GetElemNodes(i))>2:
		for i1 in Mesh_1.GetElemNodes(i):	    
		    if i1 == foundpoints[len(foundpoints)-1]:		
			d0=list(set(set(Mesh_1.GetElemNodes(i))) & set(new_group2.GetNodeIDs())- set(foundpoints) -set([secondbetnode])  -set([lastsecondbetnode])-set(d))
			if debug!=4:print "-d EleNodes /foundnotes " + str(d0)# + "-next points  " + str(i1) +"-c1 bound " + str(c1)+"-c " + str(c) + "-d nicht schon " + str(d)
			if d0!=[]: d.append(d0[0])
			if len(d0)==2: d.append(d0[1])
			if len(d0)==3: print "pointed stick??"
			if d0!=[]: break  
	    if debug!=4:print ":for adjEle_b(i) " + str(i) +  ": these nodes " + str(Mesh_1.GetElemNodes(i)) 
	    #d.append(d0[0]) # in the beginning we wait for two
	    #if d!=[]: break #buggy?
    #
	if len(d)>1 and i5==1: #part 2, in the beginning we got two bet, chose one
	    # Debug wait boundary could get loss in the interior at subshape contracts right: more then one boundary node per element:add vertex only
	    e=list(set(Vnodes) & set(d))
	    if e!=[]:foundpoints.append(d[1])
	    else:
		foundpoints.append(d[1]) 
		secondbetnode=d[0]
	if len(d)>1 and i5!=1: #if more then one node add the Vnode
	    f=list(set(Vnodes) & set(d))
	    ##print "the two nodes:" + str(d) + "but:" + str(f) + "is vertex"
	    if f!=[]:foundpoints.append(f[0])	    
    #
	if len(d)==1:
	    foundpoints.append(d[0]) #put best neighbour bet to the collection
    #
	d=[];d0=[] #and go for searching the next
	a=Mesh_1.GetNodeXYZ(foundpoints[len(foundpoints)-1])
	b=mesh.FindElementsByPoint (a[0],a[1],a[2])
	if debug!=4:print "-new found points:" + str(foundpoints) + "new adjElem:" + str(b) + "2.betnode:" + str(secondbetnode)		# 
	#at endnode: out with result, at vertex: out with second bet, new collection list
	if list(set(Vnodes) & set([foundpoints[len(foundpoints)-1]]))!=[]:
	    if foundpoints[len(foundpoints)-1]==mb11node:
		resultedge=foundpoints
		#resultedge.append(foundpoints)
		if debug!=4:print "result case" 
	    else:
		lastsecondbetnode=foundpoints[1]
		foundpoints=[mb12node,secondbetnode]
		secondbetnode=-1
		if debug!=4:print "second bet case" +"-new found points:" + str(foundpoints)
	else:
	    if debug!=4:print "added node no vertex" 
	if debug!=4:print "Durchlauf" + str(i5)
    if debug!=4:print "Durchlauf" + str(i5)
    resultedgeL.append(foundpoints)
    #print resultedgeL
    resultedgeL.append([mesh.FindElementByNodes([foundpoints[i],foundpoints[i+1]]) for i in range(0,len(foundpoints)-1)])
    #print resultedgeL
    #note: afterwards it came out that everything could have been done easier with better APIs, ppssibly everything needs to be rewritten due to performances probs
    #
    #find the elements atjacent to the boundary line and add it to return matrix, yet.
    foundmbelem=[]
    for i in range(0,len(foundpoints)-1):
	#print "i ",i,"  foundpoints[i] ", foundpoints[i]
	pi2=Pi.meshobj.GetNodeXYZ(foundpoints[i])
	#print "pi2 ",pi2
	ei3L=Pi.meshobj.FindElementsByPoint(pi2[0],pi2[1],pi2[2])
	#print "GetElemNodes",ei3L
	#element index 3 is  a list of adjacent element to boundary point
	for ei4 in ei3L:
	    ei4L=Pi.meshobj.GetElemNodes(ei4)
	    #print "FindElementsByPoint",ei4
	    #print "GetElemNodes",ei4L
	    if len(ei4L)>2 and set(ei4L)>=set([foundpoints[i],foundpoints[i+1]]):
		foundmbelem.append(ei4)
	    #print foundmbelem
    resultedgeL.append(foundmbelem)
    return resultedgeL



def brep2shapedirs(Pi,debug=1000000):
    geompy = geomBuilder.New(salome.myStudy)
    #debug=last index 1:activate view occ
    #debug=digit 2:delete obj    
    #debug=digit 4:restoreswitch salome geom module    
    if int(str(debug)[len(str(debug))-4])==1:
	restoresalomeiparm(module='Geometry')   
    if int(str(debug)[len(str(debug))-2])==1:
	delobjregex(complaint="Shape*",s="delete",module='GEOM')
    #instantiate salome kind occ object
    Shape1 = geompy.ImportBREP(Pi.brepfile)
    Pi.brepshapeobj=Shape1
    #debug checksum
    [Xmin1,Xmax1, Ymin1,Ymax1, Zmin1,Zmax1] = geompy.BoundingBox(Shape1)
    d1 = (Xmax1-Xmin1)*(Xmax1-Xmin1) + (Ymax1-Ymin1)*(Ymax1-Ymin1) + (Zmax1-Zmin1)*(Zmax1-Zmin1)
    if int(str(debug)[len(str(debug))-1])==1:print "dd32 some file's fingerprint = ",d1
    studyID = salome.myStudy._get_StudyId()
    salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
    # now it is visible in the obj browser
    # found where: site:docs.salome-platform.org latest geompy_doc Packages  ExtractShapes
    #http://docs.salome-platform.org/7/gui/GEOM/geompy_doc/group__l4__decompose.html
    #def and example
    FACE= geompy.ExtractShapes(Shape1, geompy.ShapeType["FACE"], True)
    #SubFaceList = geompy.SubShapeAll(Shape1, geompy.ShapeType["FACE"])
    #len(SubFaceList)
    #len(FACE)
    listSubShapeIDs = geompy.SubShapeAllIDs(Shape1, geompy.ShapeType["FACE"])
    nf=len(listSubShapeIDs)
    print "number of faces " + str(nf)
    #[2, 12, 19]
    # create a group from the faces of the box
    #solution of the puzzle: linguistic evolution: a group is a face.
    GROUP = [geompy.CreateGroup(Shape1, geompy.ShapeType["FACE"]) for Face in FACE]
    print "number of Groups " + str(len(GROUP))
    #create 1 dir for each of those faces aka groups 
    for i in range(0,nf):
	print listSubShapeIDs[i]
	geompy.UnionIDs(GROUP[i], [listSubShapeIDs[i]])
    #finally represent all in object browser
    geompy.addToStudy( Shape1, 'Shape1' )
    for i in range(0,nf):
	geompy.addToStudyInFather(Shape1, GROUP[i], 'Group' +str(nf)+'_'+str(listSubShapeIDs[i]))
    if salome.sg.hasDesktop():
	salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
    if int(str(debug)[len(str(debug))-1])==1:displaysalomeplease(i5=10110)
    Pi.brepgroupobj=GROUP



def shape2mesh(Pi,debug=1000000):
    import  SMESH, SALOMEDS
    #debug=last index 1:activate vtkviewr
    #debug=digit 2:delete obj    
    #debug=digit 4:restoreswitch salome geom module    
    if int(str(debug)[len(str(debug))-4])==1:
	restoresalomeiparm(module='Mesh')   
    from salome.smesh import smeshBuilder
    if int(str(debug)[len(str(debug))-2])==1:
	delobjregex(complaint="Shape*",s="delete",module='SMESH')
    smesh = smeshBuilder.New(salome.myStudy)
    Mesh_1 = smesh.Mesh(Pi.brepshapeobj)
    isDone = Mesh_1.Compute()
    #
    # from meshbuilder class and Mesh class instance
    # found among Modules..
    NETGEN_2D = Mesh_1.Triangle(algo=smeshBuilder.NETGEN_1D2D)
    #An instance of Mesh_Algorithm sub-class
    #"Creates triangle 2D algorithm for faces.
    #algo = canstants plugin
    NETGEN_2D.GetId()
    #?
    SGROUP = [Mesh_1.GroupOnGeom(group) for group in Pi.brepgroupobj]
    #Returns SMESH_GroupOnGeom
    #?
    for group in Pi.brepgroupobj:
	group.SetColor( SALOMEDS.Color( 1, 0.666667, 0 ))
    NETGEN_2D_Parameters = NETGEN_2D.Parameters()
    NETGEN_2D_Parameters.SetMaxSize(Pi.ng2D.NGParamSetMaxSize ) #18 
    NETGEN_2D_Parameters.SetSecondOrder(Pi.ng2D.NGParamSetSecondOrder )
    NETGEN_2D_Parameters.SetOptimize(Pi.ng2D.NGParamSetOptimize )
    NETGEN_2D_Parameters.SetFineness(Pi.ng2D.NGParamSetFineness ) #5
    NETGEN_2D_Parameters.SetGrowthRate(Pi.ng2D.NGParamSetGrowthRate )
    NETGEN_2D_Parameters.SetNbSegPerEdge(Pi.ng2D.NGParamSetNbSegPerEdge )#15
    NETGEN_2D_Parameters.SetNbSegPerRadius(Pi.ng2D.NGParamSetNbSegPerRadius )#2
    NETGEN_2D_Parameters.SetMinSize(Pi.ng2D.NGParamSetMinSize ) #52
    NETGEN_2D_Parameters.SetUseSurfaceCurvature(Pi.ng2D.NGParamSetUseSurfaceCurvature)# 1 
    NETGEN_2D_Parameters.SetFuseEdges(Pi.ng2D.NGParamSetFuseEdges )#1
    NETGEN_2D_Parameters.SetQuadAllowed(Pi.ng2D.NGParamSetQuadAllowed)# 0 
    isDone = Mesh_1.Compute()
    # sfaces(Groups) in object browser and visible in viewer: 2 cells be face
    if int(str(debug)[len(str(debug))-1])==1:displaysalomeplease(11121, 4,Pi.brepshapeobj.GetName())
    Pi.meshobj=Mesh_1
    print Mesh_1



def mesh2bnd_n_unv(Pi,debug=1000140,maxmbsteps=1300):
    import  SMESH, SALOMEDS
    #debug=last index 1:activate vtkviewr fitall
    #debug=digit 2:4 put off debug noise; level edges, next 5    
    #debug=digit 3:1 delete former objects   
    geompy = geomBuilder.New(salome.myStudy)
    #####
    #interfaces boundaries
    VP=(geompy.SubShapeAll(Pi.brepshapeobj,geompy.ShapeType["VERTEX"])) #shape objects
    #testfunction for visualisation of vertex sequence ##
    mode="test_manual"
    #mode="production_manual"
    #mode="if_man_prod"
    if mode=="test_manual":
	Vp_mb1=[8-1,7-1,8-1,6-1] ##
	#Vp_mb1=[8,7,8,6] #is: line between Vertice 8,7 and between 8,6
	Vp_mb2=[1-1,2-1]# cold?
	new_group2=[None]*len(Vp_mb1+Vp_mb2)
	print "test_manual"
	VpL=[Vp_mb1,Vp_mb2]
    else:VpL=[Pi.Vp_mb1,Pi.Vp_mb2]
    #
    bggroup1L=[]
    mesh=Pi.meshobj ##
    dim= SMESH.BND_1DFROM2D
    Pi.mbedges=[]
    glue_edges=[]
    glue_elements=[]
    glue_points=[]   
    i6=0
    for Vp_mb in VpL: #boundary by boundaryy 
	i6=i6+1
	for i in range(0,len(Vp_mb),2): #boundary line byboundary  line
	    groupName='Group_bd'+''.join(str(Vp_mb[i])+str(Vp_mb[i+1]))				
	    nb2, new_mesh2, new_group2[i] =  mesh.MakeBoundaryElements(dim, groupName)
	    # new_group2[i]:all mesh edge boundary elements of mesh
	    # but as well create new entry in obj browser
	    #nb2, new_mesh2?
	    salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
	    #print new_group2[i].GetListOfID()
	    #print "i6:" +str(i6)
	    debug1=int(str(debug)[len(str(debug))-2])
	    #4
	    #if i6==2:debug1=5
	    mbresult=edge2mbnodes(Pi,Vp_mb[i], Vp_mb[i+1], VP, mesh, new_group2[i],maxmbsteps, debug1, complaint='Yes or no, please!') 
	    #return mbresult=mesh boundary elements of line: mesh edge elements of it unv reqires
	    #max Length 1300
	    ##debug off, >100 nodes long,list of vertices of shape, mesh, list of mesh's boundary nodes
	    ##nbDel = new_group2[i].Remove( new_group2[i].GetListOfID() )
	    ##nbAdd = new_group2[i].Add(  mbresult[1]  )
	    ##delete groups with same name
	    for group, name in zip(mesh.GetGroups(),mesh.GetGroupNames()):
		if name == groupName:
		    mesh.RemoveGroup(group)	
	    #clean object brouwer of single line entry no needed
	    for i1 in mbresult[1]:glue_edges.append(i1)
	    for i1 in mbresult[0]:glue_points.append(i1)
	    for i1 in mbresult[2]:glue_elements.append(i1)
	    #hold lines of same boundary in second part of array
	    #glue groups togehter
	groupName='Group_bd'+str(i6)
	#final boject browsers entries of mesh boundary "group" with found edge as required for export to unv
	for group, name in zip(mesh.GetGroups(),mesh.GetGroupNames()):
	    if name == groupName:
		mesh.RemoveGroup(group)
	nb2, new_mesh2, bggroup1 = mesh.MakeBoundaryElements(dim, groupName)
	nbDel = bggroup1.Remove(bggroup1.GetListOfID())
	nbAdd =  bggroup1.Add(  glue_edges  )
	#
	salome.sg.updateObjBrowser(salome.myStudy._get_StudyId())
	displaysalomeplease(11021, 4,groupName)
	bggroup1L.append(bggroup1)	
	Pi.mbedges.append([glue_edges,glue_elements,glue_points])   
	glue_edges=[]
	glue_elements=[]
	glue_points=[]   	
    # Boundary part end
    ##Expor
    mesh.ExportUNV( Pi.unvfile )
    if int(str(debug)[len(str(debug))-1])==1:
	displaysalomeplease(11111)



def elmerunv2ep(Pi,debug=1000811,debugpath1="" ,debugpath2=""):
    import re
    if debugpath1=="":debugpath1=Pi.fempath
    if debugpath2=="":debugpath2=Pi.gridpath
    os.chdir("%s" % Pi.fempath)
    #debug:Ep-visu last digit 1:1, multidir watch digit 2:1, ElmerGrid 8 2 digit 3:8 ), 
    #debug level print >2: to console >3 elmersolve output digit 4:0 )(T):log only and +
    #(T)autoclean: ep 2* rm mesh 2* if*2 , unv
    #logging, checks, return value -1 ..
    #timing, speed opt, .
    #debug (T) size, position
    if int(str(debug)[len(str(debug))-2])==1:
	stdin, stdout = os.popen2('ps aux|grep xterm|grep -v "grep"|grep watch');
	if stdout.read()=='':
	    a1="ls -rtl "+debugpath1+"|tail;"
	    #
	    a2="ls -rtl "+debugpath2+"|tail;";
	    a0=a1+a2
	    stdin, stdout = os.popen2('ps aux|grep xterm|grep -v "grep"|grep watch||xterm -title "watch" -e sh -c "watch \'%s\'" &' % (a0)); #ok with lost focus
    #debug end
    ##
    #debug breakpoint
    #os.system("xterm -e sh -c 'watch echo  \"ctrl c to continue\"'")
    #debug end breakpoint
    ##
    #file management
    stdin, stdout = os.popen2('rm %s/*' % Pi.grid_templ_path);
    #unv file needs to be in pwd, so:
    stdin, stdout = os.popen2('cp %s .' % Pi.unvfile);
    #
    stdin, stdout = os.popen2('ElmerGrid %s 2 %s' % (str(debug)[len(str(debug))-3],os.path.basename(Pi.unvfile),));a=stdout.read();
    if int(str(debug)[len(str(debug))-4])>3: print a;
    #sync, sleep
    stdin, stdout = os.popen2('sync;sleep 0.1; ls -rtl %s|grep mesh.' % Pi.grid_templ_path);
    #debug
    if int(str(debug)[len(str(debug))-4])>2: 
	print stdout.read()
	print str(debug)[len(str(debug))-3] +" "+Pi.unvfile 	
    a=stdout.read() ## massive sync problems with Elmergrid here:Python popen
    #mesh.boundary mesh.elements mesh.header mesh.namesbmesh.nodes
    #file management
    stdin, stdout = os.popen2('rm mesh*; rm %s; cp %s/mesh* %s' % (Pi.epfile,Pi.grid_templ_path,Pi.gridpath));
    stdin, stdout = os.popen2('rm %s' % Pi.siffile)
    stdin, stdout = os.popen2('cp %s %s' % (Pi.siftemplfile,Pi.siffile));a1=stdout.read()
    #sif manipulation
    # sif preparation body and material bocks generation
    stdin, stdout = os.popen2("grep \"^Body\" %s|wc -l" % Pi.siffile);a1=stdout.read()
    #a1=0 #debug
    for i in range(len(Pi.Bodies)-int(a1)):
	fh=open(Pi.siffile)
	s=fh.read();fh.close()
	print "append Material and Bodyblock"
	#print s
	##Match Material Paragraph
	#
	it=re.findall("\nMaterial.*?\nEnd",s,re.MULTILINE+re.DOTALL)
	#got occurences
	a=[ite.span() for ite in re.finditer("\nMaterial.*?\nEnd",s,re.MULTILINE+re.DOTALL)]
	ind=list(a[len(a)-1])[1]
	#got index of last occurence
	it1= re.sub(r'M(aterial\ )[0-9]+?', r"Material "+"" + str(len(it)+1),it[len(it)-1],flags=re.MULTILINE+re.DOTALL)
	#changed contents: Material number
	it2= re.sub(r'M(aterial)[0-9]+?', r"Material"+"" + str(len(it)+1),it1,flags=re.MULTILINE+re.DOTALL)
	#changed contents: Material Material number 
	s=s[:ind]+"\n"+it2+s[ind:]
	#reglued 
	#print s
	##Match Body Paragraph
	#
	it=re.findall("\nBody.*?\nEnd",s,re.MULTILINE+re.DOTALL)
	#got occurences
	a=[ite.span() for ite in re.finditer("\nBody.*?\nEnd",s,re.MULTILINE+re.DOTALL)]
	ind=list(a[len(a)-1])[1]
	#got index of last occurence
	it1= re.sub(r'(Body\ )[0-9]+?', r"Body "+"" + str(len(it)+1),it[len(it)-1],flags=re.MULTILINE+re.DOTALL)
	#changed contents: Body number
	it2= re.sub(r'(  Target Bodies\(1\) =) [0-9]+?', r"\1 "+"" + str(len(it)+1),it1,flags=re.MULTILINE+re.DOTALL)
	#changed contents: Target Bodies number
	it3= re.sub(r'(Material = )[0-9]+?', r"Material = "+"" + str(len(it)+1),it2,flags=re.MULTILINE+re.DOTALL)
	#changed contents: Body Material number
	it4= re.sub(r'Body[0-9]+?', r"Body"+"" + str(len(it)+1),it3,flags=re.MULTILINE+re.DOTALL)
	#changed contents: Body body number
	s=s[:ind]+"\n"+it4+s[ind:]
	#reglued 
	fh=open(Pi.siffile,"w")
	fh.write(s);fh.close()	
    if int(str(debug)[len(str(debug))-4])>3: print s;
    #
    ##change conductivity of 2.body  to 1.0
    for i in range(len(Pi.Bodies)):
	stdin, stdout = os.popen2("sed -i ':a N;$!ba; s/Conductivity = [0-9]*\.\?[0-9]*/Conductivity = %s/%s' %s" % (str(Pi.Bodies[i].k),str(i+1), Pi.siffile));
	a=stdout.read()
	#debug
	if int(str(debug)[len(str(debug))-4])>3:
	    stdin, stdout = os.popen2('grep Condu flux.sif');print stdout.read()
	    print "i="+str(i)+" body " + str(Pi.Bodies[i].k)
	#debug end
    for i in range(len(Pi.Bnds)):
	tempera_=str(Pi.Bnds[i].T)
	tempera_1=str(i+1)
	stdin, stdout = os.popen2("sed -i ':a N;$!ba; s/Temperature = [0-9]*\.\?[0-9]*/Temperature = %s/%s' %s; cat case.sif| grep Temperature\ =" % (tempera_,tempera_1,Pi.siffile));
	a=stdout.read()
	#debug
    if int(str(debug)[len(str(debug))-4])>2:
	stdin, stdout = os.popen2('grep "Heat Conduct\|Temperature =" %s' % Pi.siffile );
	print stdout.read()
	stdin, stdout = os.popen2('cat %s' %Pi.grid_templ_path+'/mesh.names' );
	print stdout.read()
	
    #manipuate sif end
    #
    stdin, stdout = os.popen2('unset LD_LIBRARY_PATH; ElmerSolver;');a=stdout.read() #popen2 wait until finished - hopefully
    if int(str(debug)[len(str(debug))-4])>3: print a;
    #file management
    stdin, stdout = os.popen2('cp %s %s' % (Pi.eptemplfile,Pi.epfile));a=stdout.read()
    #optionally viewing
    if int(str(debug)[len(str(debug))-1])==1:stdin, stdout = os.popen2('killall ElmerPost; ElmerPost source %s' % Pi.epsourcefile)
#ok


def paraviewvtu2pic(Pi,debug=1000000,debugpath1="" ,debugpath2=""):
    from pvsimple import *
    from time import *
    if int(str(debug)[len(str(debug))-3])==1:t1 = clock()
    #debug:clean vtuO last digit 1 default:0
    # DISPLAY PIC digit 2:1,
    # time keeping digit 3:1,
    #(T) screnn before hover mouse over
    if int(str(debug)[len(str(debug))-1])==0:
	for i in GetSources().values():servermanager.UnRegister(i)
	#source;
	view1=servermanager.ProxyManager().GetProxiesInGroup("representations").values();
	print "reps"+str(len(view1));
	for i in view1:Delete(i)
	view1=servermanager.ProxyManager().GetProxiesInGroup("views").values();
	print "view"+str(len(view1));
	for i in view1:Delete(i)
	#
	print "delete last"
	#case0 = GetActiveSource();Delete(case0);#removes source/reader from pipeline browser
    Pi.vtuobj= XMLUnstructuredGridReader(FileName=[Pi.vtufile] );
    if int(str(debug)[len(str(debug))-3])==1:
	t2 = clock()
	t = t2 - t1
	print('endure delete and load: ', t)
    case=Pi.vtuobj
    #gives a reader which is a source, a class, an object: XMLUnstructuredGridReader, appears ad hoc in pipeline browser but not in canvas = (Paraview viewer)
    #Show(); #shown
    #Render();#?
    view = GetRenderView()
    Pi.vtuobjview= view
    #view = servermanager.CreateRenderView()
    #does update screenshot, but at the mom, cannot do without..
    #print view
    #gets, creates "active" "view" object
    #dp = GetDisplayProperties(case);
    if int(str(debug)[len(str(debug))-3])==1:
	t3 = clock()
	t = t2 - t3
	print('endureGetRenderView(): ', t)    
	# corresponds to display GUI-Dialog
	#got a "display property" class  UnstructuredGridRepresentation
	#of some 240 properties though
	# broadly undocumented!!
    
    #print view
    #dp = servermanager.CreateRepresentation(case, view)
    dp = Show(case, view)    
    Pi.vtuobjdp=dp
    if int(str(debug)[len(str(debug))-3])==1:
	t4 = clock()
	t = t3 - t4
	print('CreateRepresentation: ', t)    
    #dp.ScalarOpacityFunction = [];
    #??
    dp.ColorArrayName = ('POINT_DATA', 'temperature') ;
    #alters "display dialogs" "color by" option
    #bulk color after Render() in canvas
    dp.LookupTable = GetLookupTableForArray( "temperature", 1 ) ;
    #shows gradient color on canvas
    dp.LookupTable.RGBPoints=[Pi.Bnds[0].T, 0.0, 0.0, 1.0, Pi.Bnds[1].T, 1.0, 0.0, 0.0]
    dp.Representation = 'Wireframe' #'Surface' 'Points'
    #Show(); #no effect
    #Render(); # shows points
    #set point size
    dp.PointSize = 2
    #set surface color
    dp.DiffuseColor = [0, 1, 0] #blue
    view.CameraViewUp=[0.0, 1.0, 0.0];
    #Render()
    view.CameraParallelProjection=1;Render()
    #y-axis point upwards
    #set the background color
    view.Background = [1,1,1]  #white
    view.CameraFocalPoint = [0, 0, 0]
    view.CameraViewAngle = 45;
    #Show();Render()
    view.CameraPosition = [0,0,-5];
    #Render()
    view.ResetCamera();
    print "view.CameraPosition" + str(view.CameraPosition)
    #set image size
    viewres=view.ViewSize
    view.ViewSize = [300, 280] #[width, height]
    #rescale to data range how?
    #Render()
    Render() #Fittoframe
    #draw the object
    #Show()
    WriteImage(Pi.pngfile);
    #view.ViewSize=viewres
    #view.ResetCamera();Render() #Fittoframe
    #Writeimagetopath Deprecated..(T)
    if int(str(debug)[len(str(debug))-2])==1:
	stdin, stdout = os.popen2('killall display;display %s' % Pi.pngfile );
    if int(str(debug)[len(str(debug))-3])==1:
	t5 = clock()
	t = t1 - t5
	print('total: ', t)    


def pvsource2point(Pi,debug=1000101,valrep='Wireframe',x=0,    ratva=3.5, selfield='CELL',selelem=[391,392],selpoiname='temperature',selcelname='vtkOriginalCellIds',selcelvis=1,selpoivis=1,gradfield='CELL',i_ele=391,i_x=1,iv=0):
    from pvsimple import *
    from time import *
    #out put to console:
        #gradfield='POINT',
    #gradfield='CELL'
    #i_ele=391#node or cell number
    #i_x=1#vector component of i_ele.th cell,1:y
    #iv=0; #iv'th vertex of cell
    #display be gui selection:
       #selfield='POINT'
    #selfield='CELL'
    #selelem=[391,392];
    #selpoiname='temperature'#'vtkOriginalCellIds';##,'temperature flux'
    ##selpoiname='vtkOriginalPointIds'
    #selcelname='vtkOriginalCellIds';##'temperature'
    #selcelname='temperature flux';##'temperature'
    #selcelvis=1;#
    #selpoivis=1;#
     #zoom level: angle ratio from fitall
    #ratva=0.9   
    #deb  mag:delete last digit 1 default:0
    # 
    # gradient color representation: nodes values else elements digit 3:1,
    #x=4:x oder magni:2 ??
    #(T)rescale:flux
    #zoom ongroup of selected points
    if int(str(debug)[len(str(debug))-1])==1:
	view1=servermanager.ProxyManager().GetProxiesInGroup("sources").values();
	for i in view1:Delete(i)
	view1=servermanager.ProxyManager().GetProxiesInGroup("views").values();
	for i in view1:Delete(i)
	return()
    #view1=servermanager.ProxyManager().GetProxiesInGroup("views").values();
    #for i in view1:Delete(i) 
    case=Pi.vtuobj
    #view=servermanager.ProxyManager().GetProxiesInGroup("views").values()[0]
    print "debug"
    view = Pi.vtuobjview
    #view = GetRenderView()
    print "debug"
    #dp = servermanager.CreateRepresentation(case, view)
    dp = Pi.vtuobjdp
    dp = GetDisplayProperties(case);
    print "debug getdpready"
    #valrep='Surface'#instead of Surface,Wire and such
    #
    #debug=1000100;
    #debug=1000000;x=3
    if int(str(debug)[len(str(debug))-3])==1:
	valstr='POINT_DATA'
	value="temperature"
	maxv=Pi.Bnds[0].T
	minv=Pi.Bnds[1].T    
    else:
	value="temperature flux"
	valstr='CELL_DATA'
	maxv=0.04
	minv=-0.04 #where?
    dp.ColorArrayName = (valstr, value) ;
    #corresponds to display window: "color by" and changes it
    #bulk color
    dp.ColorAttributeType = valstr
    dp.LookupTable = GetLookupTableForArray( value, x ) ;
    #shows gradient color on piece
    dp.LookupTable.RGBPoints=[minv, 0.0, 0.0, 1.0, maxv, 1.0, 0.0, 0.0]
    #Render();  
    #rescale to data range how?
    dp.Representation = valrep 
    dp.CubeAxesVisibility=1
    dp.CubeAxesColor=[0.0, 0.0, 0.0]
    #print "debug"
    #Show(); #nothing
    #Render(); # shows points
    #print "debug shown"
    ##################
    # get values to console
    #print "debug"
    data = servermanager.Fetch(case)
    #print "debug data fetch"
    numPoints=data.GetNumberOfPoints()
    print "data.GetNumberOfPoints()"+str(data.GetNumberOfPoints())
    print "data.GetNumberOfCells()"+str(data.GetNumberOfCells())
    #case.GetPropertyValue('PointArrayInfo')
    #(T)  zoom neighborhood
    if gradfield=='CELL':
	i_n=(data.GetCell(i_ele).GetPointId(iv))
	print "Cell node "+str(i_n)
	ixy=data.GetPoint(i_n);Render()
	print "Cell node coor "+str(ixy)
	#ix.th vertex of cell i_ele	
	print "cell vertices xy "+str(data.GetCell(i_ele).GetBounds())
	print "cell Area "+str(data.GetCell(i_ele).ComputeArea())
	print ".GetReferenceCount() "+str(data.GetCell(i_ele).GetReferenceCount())
	ival=data.GetCellData().GetArray("temperature flux").GetValue(i_ele*3+i_x)
	print "cell flux "+str(ival)
	#0.0038994857
    else:
	#"nodes here"
	ixy=data.GetPoint(i_ele);#Render()
	print "point coord "+str(ixy)
	ival=data.GetPointData().GetArray("temperature").GetValue(i_ele)
	print "Point value "+str(ival)
    #vector
    #(T)  print and find element_s_
    #
    #####
    #pytho selection
    #switch between Points/Fiels
    IDs = []
    for i in selelem:
	IDs.append(0L)
	IDs.append(long(i))
    selectSource = IDSelectionSource()
    selectSource.FieldType=selfield
    selectSource.IDs = IDs 
    case.SetSelectionInput(0,selectSource,0)
    #print "dp.SelectionVisibility"+str(dp.SelectionVisibility)
    #print "dp.SelectionCellLabelVisibility"+str(dp.SelectionCellLabelVisibility)
    #print str(dp.SelectionCellFieldDataArrayName)
    #print str(dp.SelectionPointFieldDataArrayName)
    dp.SelectionVisibility=1
    dp.SelectionCellLabelVisibility=selpoivis
    dp.SelectionPointLabelVisibility=selcelvis
    dp.SelectionPointFieldDataArrayName=selpoiname
    dp.SelectionCellFieldDataArrayName=selcelname
    #print "dp.SelectionCellLabelVisibility"+str(dp.SelectionCellLabelVisibility) 
    ##zoom 
    ##
    if ratva!=0:
	view.ResetCamera();Render()#fitall obj
	view.CameraPosition= [ixy[0], ixy[1], view.CameraPosition[2]];Render()
	view.CameraViewUp=[0.0, 1.0, 0.0];Render()
	#print "view.CameraPosition " + str(view.CameraPosition)
	#print "view.CameraViewUp " + str(view.CameraViewUp)
	#view.ResetCamera();Render()#fitall obj
	#print "view.CameraViewUp " + str(view.CameraViewUp)
	#print "view.CameraPosition " + str(view.CameraPosition)
	#print "view.CameraViewAngle " + str(view.CameraViewAngle)
	#view.CameraFocalPoint=ixy# Focus in first point coor	
	a=view.CameraViewAngle
	view.CameraViewAngle=a/ratva;Render() # get somewhat nearer
	#print "view.CameraViewUp " + str(view.CameraViewUp)
	#print "view.CameraPosition " + str(view.CameraPosition)
	#print "view.CameraViewAngle " + str(view.CameraViewAngle)
	view.CameraFocalPoint=ixy;Render()
	#print "view.CameraViewUp " + str(view.CameraViewUp)
	#print "view.CameraPosition " + str(view.CameraPosition)
	#print "view.CameraViewAngle " + str(view.CameraViewAngle)	
    Render()
    #ok




