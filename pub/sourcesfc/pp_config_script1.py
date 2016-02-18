#Writegeo1:
'/tmp/elmermesh1/'
#Pi.fempath'/tmp/elmermesh1/'
import time#ok
##
#gui
import os
import sys
import re
import math
import ast


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
gmshv=" -rand 1.e-8 -smooth 400 " #verbosity
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
gmshoutlog=" -v 9  >>"+logs2 +" 2>&1 "
elmeroutlog="  >>"+logs2 +" 2>&1 "
###prepare geofile 3 for messhing 
point_beam=1 #flag
nodesbyedge=4 #controll parameter 1.choice
f2LcMinbylc= 6 #controll parameter, 2.choice
report_table=[]
studysubname="quadrangles and treshold mesh size at vertices, direct fem-solving"
studyname="2D heat conduction analysis with elmer-gmsh-python tool chain"
textsnipped="There has been found over mesh size converging plateau. The results are therefore: usable"
reportname="report"
cle=math.sqrt(Pi.compound0.Shape.Area) # char. length edge
cl1=cle/nodesbyedge #char. length elment
f2DistMin = cle*0.0
f2DistMax = cle*0.3

gmsh_minsize=str(cl1/200)
gmsh_maxsize=str(cl1*200)
#gmsh_minsize=  '144.4' 
#gmsh_maxsize='336.6'
#[-1.001260856871
#-1.004264029924
meshmode="threshold_nodes"
runs=1
reducerate=0.7
#timepL.append(timep)
film=1
header_result_performance=["flux-elmer","gmsh-minsize","gmsh-maxsize","nodes-el-bnd" ]
###valitation 1 switches 
Pi.siftemplfile=os.environ["FEM_PROTO_FLUX3_PATH"]+'flux_templ_2bodys_validatationpiece1.sif'
result_performance=[]
header_result_performance=header_result_performance+["T min","T at A","T at b","T at c","T at d","T at e","T at f","T at g","T at h","T at i"]
###valitation 1 switches end

timepL=[]
timep=[]
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


timep.append([time.time(),round(timep[len(timep)-1][0]-time.time(),2),"Step1"])



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
timep.append([time.time(),round(timep[len(timep)-1][0]-time.time(),2),"Step2: coherence geo 2"])

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

hash_topo_geo_linesL=pointtopost.get_hash_topoline_from_geo(Pi.comp_topo_edges,geofile3)
			
[hash_array_geo_surfaceL, pointsL]=  pointtopost.get_hash_topoface_from_geo(Pi.compound1,geofile3)


###prepare geofile 4 for messhing 
timepL.append(timep)
for mstep in range(runs):
    timep=[]
    cl1=str(float(cl1)*reducerate)
    gmsh_minsize=str(float(gmsh_minsize)*reducerate)
    gmsh_maxsize=str(float(gmsh_maxsize)*reducerate)

    timep.append([time.time(),0,"S3prepgeo3"])

    fh=open(geofile3)
    s=fh.read();fh.close()
    for i in range(len(Pi.Bodies)):
	s=s+"Physical Surface("+str(i+1) +") = {"+str(hash_array_geo_surfaceL[i]) +"};\n"
    #for i in range(len(Pi.Bodies)):
	#s=s+"Physical Surface("+str(i+1) +") = {"+str(i+1) +"};\n"

    bias=len(Pi.Bodies)+1
    #project note convention: Boundary enumeration: body 1, 2, 3,| Nullbnd, Pi.Bnd(1), Pi.Bnd(2)
    geo_bnd=[]
    geo_bndL=[]
    i1=0
    for i in Pi.bnd_tegdeL:
	for j in i:
	    i1=i1+1
	    geo_bnd.append(hash_topo_geo_linesL[j])
	geo_bndL.append(geo_bnd)
	geo_bnd=[]

    print geo_bndL

    for i in range(len(geo_bndL)):
	    s=s+"Physical Line("+str(bias+1+i) +") = {"+str(geo_bndL[i]).strip('\]\[') +"};\n"
    
    #todo: beaming points and lines meshes
    #import math
    
    #### 
    if point_beam==1:
	#f1NNodesByEdge	= 10

	s=s+"Field[1] = Attractor;\n"
	s=s+"Field[1].NodesList = {"+', '.join([i[0] for i in pointsL])+"};\n"

	s=s+"Field[2] = Threshold;\n"
	s=s+"Field[2].IField = 1;\n"
	s=s+"Field[2].LcMin = cl__1 / "+str(f2LcMinbylc)+";\n"
	s=s+"Field[2].LcMax = cl__1;\n"
	s=s+"Field[2].DistMin = "+str(f2DistMin)+";\n"
	s=s+"Field[2].DistMax = "+str(f2DistMax)+";\n"
	
	s=s+"Field[7] = Min;\n"
	s=s+"Field[7].FieldsList = {2 };\n"
	s=s+"Background Field = 7;\n"


	subpattern="(Point.*? = .*?,.*?,.*?, ).*?};"
	substitutepattern="\\1" +"cl__1};"
	subpassage=s
	s= re.sub(subpattern,substitutepattern,subpassage,flags=re.MULTILINE+re.DOTALL)

	subpassage=s
	s= re.sub('cl__1 = 1e\+22;',"cl__1 = " + str(cl1)+";",subpassage,flags=re.MULTILINE+re.DOTALL)
	#### point_beam end
    
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
    s=s+"Mesh.RecombineAll = 1;\n"
    s=s+"Recombine Surface \"*\";\n"
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
	pass
	#break
    
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
    s=pointtopost.process_elmer_sif_file(Pi.siffile,Pi.epsourcefile,Pi.fempath,11, elmeroutlog)
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
    result_performance.append([float(linesL[0][0]),gmsh_minsize,gmsh_maxsize,nodes_el_bnd]+linesL[0][1:])
    
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
result_performance.insert(0,header_result_performance)
tb = texttable.Texttable()
tb.set_precision(11)
tb.add_rows(result_performance)
tb.add_rows([[i[0],i[3],i[4]] for i in result_performance])
print tb.draw()

#### report project interface writing start

### snipped report_table assignment
#sources:
#1.timepL
#2.result_performance
#3.text
#4.options
#header_result_performanc
#5. Pi.bnd
#6 Pi.bodies
# first 3 element reserve convention
#
studysubname="quadrangles and treshold mesh size at vertices"
studyname="2D heat conduction analysis with elmer-gmsh-python tool chain"
#heuristic take a best bet mesh run
#up
best_bet_mesh_run=0
#take 2. take: there is a convergence plate after 500 Nodes usually
#heuristic end
report_table=[]
report_table.append([studyname,""])
report_table.append([studysubname,""])
report_table.append([textsnipped,""])
report_table.append(["",""])# project convention
##results: overall consuption in watts, Temperature at points, temperature at coldest points
report_table.append([str(result_performance[0]),str(result_performance[best_bet_mesh_run+1])])
#
##Boundary conditions
report_table=report_table+[["Kelvin Boundary 1-2 ", 
str(Pi.Bnds[0].T) +" - "+str(Pi.Bnds[1].T)], ["Rsi,e  Km²/W",  str(Pi.Bnds[0].Rs) +" - "+str(Pi.Bnds[1].Rs)],["[lambda, material] /body  ", str([[i.k,i.name] for i in Pi.Bodies])]]
#
#sample 2 all time measures from array timepL
report_table=report_table+[[i[2],i[1]] for i in timepL[best_bet_mesh_run+1]]
report_table

#test print table
len(report_table)
t1b = texttable.Texttable()
t1b.set_precision(11)
t1b.add_rows(report_table)
print t1b.draw()


## snippes report_table assignment end

###filename generation report interface writing
latexrun=1
##testdata
#latexrun=2#testdata
##testdataend
stem="_data_"+reportname+"_piece"+str(fem2dheatconductiongui.Pieces.index(Pi))+"_valid_direct_tex_"+".txt"
texfile1_1="table_"+ str(latexrun)+stem
texfile1_2="graph_"+ str(latexrun)+stem
##filename generation report interface writing

###sequentialize report data into named data files
##testdata for second tex files
#report_table=[['2D heat conduction analysis with elmer-gmsh-python tool chain', ''], ['Triangle and tplan mesh size at vertices', ''], ['There has been found over mesh size converging plateau. The results are therefore: usable', ''], ['', ''], ['S3prepgeo3', 0], ['S4msh', -0.0], ['S4.1cert', "testdata"], ['S5solv', -0.037], ['S6rdsavesc', -0.35], ['s7end', -0.0006]]
#result_performance=[['flux-elmer', 'gmsh_minsize', 'gmsh_maxsize', 'nodes_el_bnd'], [-1.014125896996, '0.000634846556315', '5.3938622526', '279    271    52   '], [-1.010308773898, '9.43925894205e-05', '3.77570357682', '344    327    68   '], [-1.000960007704, '6.60748125943e-05', '2.64299250377', '713    552    98   '], [-1.0014506662, '4.6252368816e-05', '1.85009475264', '1064   947    138  ']]
##testdata
s=str(report_table)
fh=open(texfile1_1,"w")
fh.write(s);fh.close()	

s=str(result_performance)
fh=open(texfile1_2,"w")
fh.write(s);fh.close()	
###sequentialize report data into named data files

### report project interface writing finished

### report project interface 
#reading start
#read from file
  #which files are there?
pattern="_data_"+reportname
texpots=sorted([f for f in os.listdir(Pi.fempath) if re.search(pattern, f)])

pattern="pic_[0-9]*_"+reportname
texpics=sorted([f for f in os.listdir(Pi.fempath) if re.search(pattern, f)])

report_table_tex=[]
report_graph_tex=[]
for i in range(len(texpots)/2):
    fh=open(texpots[i],"r")
    s=fh.read();fh.close()
    a=ast.literal_eval(s)
    report_graph_tex.append(a)
    #
    print "hi"
    fh=open(texpots[len(texpots)/2+i],"r")
    s=fh.read();fh.close()
    a=ast.literal_eval(s)
    report_table_tex.append(a)
    #

#generation of gnuplot plt file
s=""
s=s+"set terminal epslatex color solid size 4in, 3in"+"\n"
i=0 
s=s+"set output  'tmp_graph_"+str(i+1)+".eps'"+"\n"
s=s+"set title 'simulation 1: red   2 grey'"+"\n"
s=s+"set style data linespoints"+"\n"
s=s+'set xlabel "Nodes (n)"'+"\n"
s=s+'set ylabel "Temperatur(T)"'+"\n"
#for i in report_graph_tex: # todo: to implement: color scale
#generate 1 file plt.data per simulation
sline=""
for k in range(0,len(report_graph_tex)):
    j=report_graph_tex[k]
    print j
    sline=""
    for i in range(1,len(j)):
	print i, j[i] ,j[i][0]
	#for k in range(1,len(j[i])):
	sline=sline+str(j[i][0])+" "+str(j[i][3])+"\n"
	fh=open("tmp_graph"+str(k+1)+".plt","w")
	fh.write(sline);fh.close()	

s=s+"plot 'tmp_graph" +str(1)+".plt'"+" u 2:1 t '',"
s=s+"'tmp_graph" +str(2)+".plt'"+" u 2:1 lt 0 t ''"+"\n"#
    
i=0    
plt_file=Pi.fempath+"f"+str(i+1)+".plt"
fh=open(plt_file,"w")
fh.write(s);fh.close()	

##execute gnuplot
command= "gnuplot "+plt_file +" --persist " 
output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
FreeCAD.Console.PrintMessage(output)

s=""
s=s+"\documentclass[12]{article}\n"
s=s+"\usepackage{graphicx}\n"
s=s+"\usepackage{caption}\n"
s=s+r"\begin{document}"+"\n"
s=s+r"\tableofcontents"+"\n"
# %\chapter{First chapterrr}
s=s+r" \section{"+report_table_tex[0][0][0]+"}"+"\n"
i=0
s=s+r"\begin{center}"+"\n"
s=s+r"    \input{graph_"+str(i+1)+".tex}"+"\n"
s=s+r"	  \captionof{figure}{Diagramm}"+"\n"

s=s+r"\end{center}"+"\n"

for i1 in range(len (report_table_tex)):
    s=s+r"\subsection{"+report_table_tex[i1][1][0]+"}"+"\n"
    s=s+r"\paragraph{"+report_table_tex[i1][2][0]+r"\\}"+"\n"
    #s=s+r" \\   \\ "+"\n"
    s=s+r"\begin{center}"+"\n"
    s=s+r"  \begin{tabular}{ | p{7cm} | p{7cm} |}"+"\n"
    s=s+r"     \hline"+"\n"
    s=s+r"    \multicolumn{2}{|c|}{resuls-options} \\ \hline"+"\n"
    for i2 in range(4,len (report_table_tex[i1])):
	s=s+str(report_table_tex[i1][i2 ][1])+"& "+str(report_table_tex[i1][i2 ][0]) +"\n"
	s=s+r"\\ \hline"+"\n"   
    
    s=s+r"    \end{tabular}"+"\n"
    s=s+r"  \end{center}"+"\n";
    #
    s=s+r"\begin{center}"+"\n"
    #s=s+r"\begin{figure}[hp]"+"\n"
    #s=s+r"\centering"+"\n"
    s=s+r"\includegraphics[width=0.4\textwidth]{pic_"+str(i1+1)+"_report_piece1_valid_direct_complete.png}"+"\n"
    s=s+r"\captionof{figure}{fem warmth flow}"+"\n"
    #s=s+r"\caption{Awesome Image}"+"\n"
    #s=s+r"\label{fig:awesome_image}"+"\n"
    #s=s+r"\end{figure}"+"\n"
    s=s+r"  \end{center}"+"\n";

s=s+r"\end{document}"+"\n"

i=0    
cumulativetex_file=Pi.fempath+"cumulative"+str(i+1)+".tex"
fh=open(cumulativetex_file,"w")
fh.write(s);fh.close()	

##execute gnuplot
command= "/usr/bin/pdflatex -file-line-error -halt-on-error "+cumulativetex_file #+";xpdf cumulative1.pdf &"
output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
FreeCAD.Console.PrintMessage(output)

