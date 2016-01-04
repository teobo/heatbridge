#Writegeo1:
'/tmp/elmermesh1/'
#Pi.fempath'/tmp/elmermesh1/'
Pi=fem2dheatconductiongui.Pi
t=fem2dheatconductiongui.t
stepfile2="/tmp/tmpNO2c.step"
geofile1="/tmp/tmpNO2c.geo"
geofile2="/tmp/tmpNO2c2.geo"
geofile3=Pi.fempath+"tmpNO2c3.geo"
geofile4=Pi.fempath+"tmpNO2c4.geo"
em_headerfile=Pi.fempath+"angle/mesh.header"
gmsh="/usr/bin/gmsh"
gmsh="~/gmsh/gmsh/projects/dg/build/gmsh/gmsh"
#2.11.0
gmshv=" -v 9 -rand 1.e-8 -smooth 400 " #verbosity
#
ElmerSolver="/usr/local/bin/ElmerSolver" #non used yet
#Version: 8.0 (Rev: 4dfe228, Compiled: 2015-11-25)

mshfile=Pi.fempath+"angle.msh"
#ElmerGrid="/usr/bin/ElmerGrid"
ElmerGrid="/usr/local/bin/ElmerGrid"
gmsh_maxsize=""
gmsh_minsize=""
savesalarfile=Pi.fempath+"forces.dat"
logs1=Pi.fempath+"logs1"
logs2=Pi.fempath+"logs2" #Error messages
gmshoutlog=" >>"+logs2 +" 2>&1 "

###prepare geofile 3 for messhing 
gmsh_minsize="0.03"
gmsh_maxsize="0.4"
#gmsh_minsize=  '144.4' 
#gmsh_maxsize='336.6'
#[-1.001260856871
#-1.004264029924

runs=3
reducerate=0.70
#timepL.append(timep)
film=0

result_performance=[]
timepL=[]
timep=[]
import time#ok
##
#gui
import os
import sys
#try:
    #execfile(os.environ["FEMProjScripts"]+"../local/projenv.py")
#except OSError:
    #pass

#fem2dheatconductiongui.MeshGmsh.close(fem2dheatconductiongui.d)
#del sys.modules["pointtopost"]
#del sys.modules["fem2dheatconductiongui"]
#import pointtopost
#import fem2dheatconductiongui

#from fem2dheatconductiongui import Pi
#from fem2dheatconductiongui import Pieces
# no no

import subprocess
#take time

#clear log file
fh=open(logs1,"w")
s=""
fh.write(s);fh.close()	

fh=open(logs2,"w")
s=""
fh.write(s);fh.close()	


timep.append([time.time(),"Step1"])



#geofile juggling
#prepare geofile 1: load step to geo
l1='Merge "'+ stepfile2 +'";'
l2='Coherence;' # no effect
l3='Print "'+ geofile2 +'";'
s=l1+"\n"+l2+"\n"+l3+"\n"
fh=open(geofile1,"w")
fh.write(s);fh.close()	

command= gmsh+ " " + geofile1 + " -"

output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
FreeCAD.Console.PrintMessage(output)
#take time
timep.append([time.time(),round(timep[len(timep)-1][0]-time.time(),2),"Step2#prepare geofile 2: coher geo"])

#prepare geofile 2: coher geo 

fh=open(geofile2)
s=fh.read();fh.close()
l2='Coherence;' #now it has effect
l3='Print "'+ geofile3 +'";'
s=s+l2+"\n"+l3+"\n"
fh=open(geofile2,"w")
fh.write(s);fh.close()	

command= gmsh+ " " + geofile2 + " -"
#
output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
#
FreeCAD.Console.PrintMessage(output)
#ok

#read geolines to array
linesL=[]
pointsL=[]

import re
frd_file = open(geofile3, "r")
str_frd_file=frd_file.readlines()
n_str_frd_file=len(str_frd_file)
for line in str_frd_file:
    #check if we found header section
    if re.search('Line\(',line)!=None:
	lline=[i for i in re.split('[A-Za-z]|\n|\ |[:;_=(){},]',line) if i]##(22) = {22, 23}
	linesL.append(lline)
	#for line in str_frd_file:
	    #if re.search('Point(',line)!=None:
		#pline=[i for i in re.split('\n|\ |:',line)  if i]
		#if pline[0]== lline[2]:=P1 =[pline[2,4]
		#if pline[0]== lline[3]:=P2 =[pline[2,4]
		#if P1=[] and P2!=[]:
		    #lline.append([p1][P2])
		    #break
    if re.search('Point\(',line)!=None:
	pline=[i for i in re.split('[A-Za-z]|\n|\ |[:;_=(){},]',line) if i]##(22) = {22, 23}
	pointsL.append(pline)

print pointsL
print linesL

Pi=fem2dheatconductiongui.Pi
Pi.bnd_tegdeL

pt0=Pi.comp_topo_edges.Links[1].Shape.Vertexes[0].Point

pt1=Pi.comp_topo_edges.Links[1].Shape.Vertexes[1].Point
linesL[1][1]

p1_ind=int(linesL[1][1])
p1x=int(pointsL[p1_ind][1])
bnds=[]
bnd=[]
for i in Pi.bnd_tegdeL:
    for j in i:
	pt0=Pi.comp_topo_edges.Links[j].Shape.Vertexes[0].Point
	pt1=Pi.comp_topo_edges.Links[j].Shape.Vertexes[1].Point
	#print j, pt0, pt1

	ptm=[pt1.x-(pt1.x-pt0.x)/2,pt1.y-(pt1.y-pt0.y)/2,pt1.z-(pt1.z-pt0.z)/2]
	#get middelpoint
	for j1 in linesL:
	    #Line(23) = {24, 10};
	    #Point(24) = {50, 4.75, 0, 1e+22};
	    #print j1
	    p0_ind=[i[0] for i in pointsL].index(j1[1])
	    p0x=float(pointsL[p0_ind][1])
	    #Point(24) = {50, 4.75, 0, cl__1};
	    p0y=float(pointsL[p0_ind][2])
	    p0z=float(pointsL[p0_ind][3])
	    p1_ind=[i[0] for i in pointsL].index(j1[2])
	    p1x=float(pointsL[p1_ind][1])
	    p1y=float(pointsL[p1_ind][2])
	    p1z=float(pointsL[p1_ind][3])
	    pm=[p1x-(p1x-p0x)/2,p1y-(p1y-p0y)/2,p1z-(p1z-p0z)/2]
	    #print " p1 p0,"+str(p1x) +" "+str(p1y) +" "+str(p1z)  +" "+str(p0x) +" "+str(p0y) +" "+str(p0z) 

	    if pm==ptm:
		print "tedgedind:"+ str(j) +" geo lineindex "+str(j1)
		print "pt1, pt0" +str(pt1) +str(pt0)
		print "j1" +str(j1)
		print "j" +str(j)
		print " p1 p0,"+str(p1x) +" "+str(p1y) +" "+str(p1z)  +" "+str(p0x) +" "+str(p0y) +" "+str(p0z) 
		bnd.append(j1[0])
		continue	    
    bnds.append(bnd)
    bnd=[]


bnds
###prepare geofile 3 for messhing 
timepL.append(timep)
for mstep in range(runs):
    timep=[]
    gmsh_minsize=str(float(gmsh_minsize)*reducerate)
    gmsh_maxsize=str(float(gmsh_maxsize)*reducerate)

    timep.append([time.time(),0,"S3prepgeo3"])

    fh=open(geofile3)
    s=fh.read();fh.close()
    for i in range(len(Pi.Bodies)):
	s=s+"Physical Surface("+str(i+1) +") = {"+str(i+1) +"};\n"

    bias=len(Pi.Bodies)+1
    #project note convention: Boundary enumeration: body 1, 2, 3,| Nullbnd, Pi.Bnd(1), Pi.Bnd(2)
    for i in range(len(bnds)):
	s=s+"Physical Line("+str(bias+1+i) +") = {"+', '.join(bnds[i]) +"};\n"

    s=s+"//Mesh.CharacteristicLengthExtendFromBoundary = 0;\n"

    s=s+"//Mesh.CharacteristicLengthFactor = 0.01;\n"
    s=s+"Mesh.CharacteristicLengthMin = "+gmsh_minsize+";\n"
    s=s+"Mesh.CharacteristicLengthMax = "+gmsh_maxsize+";\n"
    s=s+"//Mesh.CharacteristicLengthFromCurvature = 0;\n"
    s=s+"//Mesh.CharacteristicLengthFromPoints = 1;\n"
    s=s+"Mesh.Format = 1;\n"
    s=s+"Mesh.SaveElementTagType = 2;\n"
    s=s+"Mesh.SaveGroupsOfNodes = 1;\n"
    s=s+"Mesh.SaveAll = 0;\n"
    s=s+"Mesh  2;\n"
    s=s+"Save \'" +str(mshfile)+"\';\n"
    s=s+"//Print 'femmesh.geo';\n"
    s=s+"//Print 'femmesh.unv';\n"

    fh=open(geofile4,"w")
    fh.write(s);fh.close()	
    #
    timep.append([time.time(),round(timep[len(timep)-1][0]-time.time(),2),"S4msh"])

    command= gmsh+gmshv+ " " + geofile4 + " -" +gmshoutlog
    print command
    try:
	output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
    except BaseException:
	#pass
	break
    
    #if logs2!="":
	#fh=open(logs2,"a")
	#fh.write(logs2);fh.close()
    #else:
	#FreeCAD.Console.PrintMessage(output)

    timep.append([time.time(),round(timep[len(timep)-1][0]-time.time(),3),"S4.1cert"])

    command=ElmerGrid+ " " + "  14 2 " + mshfile+gmshoutlog
    #
    output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
    #
    FreeCAD.Console.PrintMessage(output)

    #write siffile
    s=pointtopost.write_elmer_sif_file(Pi.siftemplfile,Pi.siffile,Pi.Bodies,Pi.Bnds,film)

    timep.append([time.time(),round(timep[len(timep)-1][0]-time.time(),3),"S5solv"])

    #t=fem2dheatconductiongui.t
    #t.gui_point2post("11101111")#
    s=pointtopost.process_elmer_sif_file(Pi.siffile,Pi.epsourcefile,Pi.fempath,11, gmshoutlog)
    if logs2!="":
	fh=open(logs2,"a")
	fh.write(str(s));fh.close()	


    timep.append([time.time(),round(timep[len(timep)-1][0]-time.time(),2),"S6rdsavesc"])
    #read savescalar:Temperature Load
    linesL=[]
    
    #read number of nodes
    frd_file = open(em_headerfile, "r")
    nodes_el_bnd=frd_file.readline()
    nodes_el_bnd=nodes_el_bnd[:len(nodes_el_bnd)-2]
    frd_file.close()
    
    frd_file = open(savesalarfile, "r")
    str_frd_file=frd_file.readlines()
    n_str_frd_file=len(str_frd_file)
    for line in str_frd_file:
	if re.search('E',line)!=None:
	    lline=[i for i in re.split('\ |\n',line) if i]
	    linesL.append(lline)
    frd_file.close()

    print line
    result_performance.append([float(linesL[0][0]),gmsh_minsize,gmsh_maxsize,nodes_el_bnd])
    timep.append([time.time(),round(timep[len(timep)-1][0]-time.time(),4),"s7end"])
    print timep
    print time.time()
    timepL.append(timep)
    #log result
    fh=open(logs1,"a")
    s=str(timep)+"\n"+str(result_performance)+"\n"
    fh.write(s);fh.close()	
    #



#read savescalar:Temperature Load end
for i in range(runs): 
    print [i1[1:] for i1 in timepL[i+1]]
    print result_performance[i]

#humanreadable table
import texttable
header_result_performance=["flux-elmer","gmsh_minsize","gmsh_maxsize","nodes_el_bnd"]
result_performance.insert(0,header_result_performance)
tb = texttable.Texttable()
tb.set_precision(11)
tb.add_rows(result_performance)
print tb.draw()

