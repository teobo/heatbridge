# -*- coding: iso-8859-1 -*-

###
### This file is generated automatically by SALOME v7.4.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/kubuntu/salome/appli_V7_4_0/salomedumpscripts')

import iparameters
ipar = iparameters.IParameters(salome.myStudy.GetCommonParameters("Interface Applicative", 1), True)

#Set up visual properties:
ipar.setProperty("AP_ACTIVE_VIEW", "ParaView_0_0")
ipar.setProperty("AP_WORKSTACK_INFO", "00000001000000000000000201000000020000014a000002e9000000040000000100000001000000080000001a00560054004b005600690065007700650072005f0030005f00300000000102000000040000000200000001000000080000001a004f00430043005600690065007700650072005f0030005f00300000000002000000080000001800500061007200610056006900650077005f0030005f00300000000102")
ipar.setProperty("AP_ACTIVE_MODULE", "ParaViS")
ipar.setProperty("AP_SAVEPOINT_NAME", "GUI state: 1")
#Set up lists:
# fill list AP_VIEWERS_LIST
ipar.append("AP_VIEWERS_LIST", "VTKViewer_1")
ipar.append("AP_VIEWERS_LIST", "OCCViewer_2")
ipar.append("AP_VIEWERS_LIST", "ParaView_3")
# fill list VTKViewer_1
ipar.append("VTKViewer_1", "VTK scene:20 - viewer:1")
ipar.append("VTKViewer_1", """<?xml version="1.0"?>
<ViewState>
    <Position X="738.968" Y="-738.968" Z="738.968"/>
    <FocalPoint X="0" Y="0" Z="0"/>
    <ViewUp X="0" Y="0" Z="1"/>
    <ViewScale Parallel="439.643" X="1" Y="1" Z="1"/>
    <DisplayCubeAxis Show="0"/>
    <GraduatedAxis Axis="X">
        <Title isVisible="1" Text="X" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="1" G="0" B="0"/>
        </Title>
        <Labels isVisible="1" Number="3" Offset="2" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="1" G="0" B="0"/>
        </Labels>
        <TickMarks isVisible="1" Length="5"/>
    </GraduatedAxis>
    <GraduatedAxis Axis="Y">
        <Title isVisible="1" Text="Y" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="0" G="1" B="0"/>
        </Title>
        <Labels isVisible="1" Number="3" Offset="2" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="0" G="1" B="0"/>
        </Labels>
        <TickMarks isVisible="1" Length="5"/>
    </GraduatedAxis>
    <GraduatedAxis Axis="Z">
        <Title isVisible="1" Text="Z" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="0" G="0" B="1"/>
        </Title>
        <Labels isVisible="1" Number="3" Offset="2" Font="0" Bold="0" Italic="0" Shadow="0">
            <Color R="0" G="0" B="1"/>
        </Labels>
        <TickMarks isVisible="1" Length="5"/>
    </GraduatedAxis>
    <Trihedron isShown="1" Size="100"/>
    <Background Value="bt=1;fn=;tm=0;ts=false;c1=#000000;c2=#000000;gt=-1;gr="/>
</ViewState>
""")
# fill list OCCViewer_2
ipar.append("OCCViewer_2", "OCC scene:20 - viewer:1")
ipar.append("OCCViewer_2", "999|-1|scale=1.000000000000e+00*centerX=0.000000000000e+00*centerY=0.000000000000e+00*projX=5.773502588272e-01*projY=-5.773502588272e-01*projZ=5.773502588272e-01*twist=0.000000000000e+00*atX=0.000000000000e+00*atY=0.000000000000e+00*atZ=0.000000000000e+00*eyeX=2.886751294136e+02*eyeY=-2.886751294136e+02*eyeZ=2.886751294136e+02*scaleX=1.000000000000e+00*scaleY=1.000000000000e+00*scaleZ=1.000000000000e+00*isVisible=1*size=100.00*gtIsVisible=0*gtDrawNameX=1*gtDrawNameY=1*gtDrawNameZ=1*gtNameX=X*gtNameY=Y*gtNameZ=Z*gtNameColorRX=255*gtNameColorGX=0*gtNameColorBX=0*gtNameColorRY=0*gtNameColorGY=255*gtNameColorBY=0*gtNameColorRZ=0*gtNameColorGZ=0*gtNameColorBZ=255*gtDrawValuesX=1*gtDrawValuesY=1*gtDrawValuesZ=1*gtNbValuesX=3*gtNbValuesY=3*gtNbValuesZ=3*gtOffsetX=2*gtOffsetY=2*gtOffsetZ=2*gtColorRX=255*gtColorGX=0*gtColorBX=0*gtColorRY=0*gtColorGY=255*gtColorBY=0*gtColorRZ=0*gtColorGZ=0*gtColorBZ=255*gtDrawTickmarksX=1*gtDrawTickmarksY=1*gtDrawTickmarksZ=1*gtTickmarkLengthX=5*gtTickmarkLengthY=5*gtTickmarkLengthZ=5*background=bt$2;fn$;tm$0;ts$false;c1$#cddbff;c2$#698fff;gt$1;gr$")
# fill list ParaView_3
ipar.append("ParaView_3", "ParaView scene:2 - viewer:1")
ipar.append("ParaView_3", "empty")
# fill list AP_MODULES_LIST
ipar.append("AP_MODULES_LIST", "Geometry")
ipar.append("AP_MODULES_LIST", "Mesh")
ipar.append("AP_MODULES_LIST", "ParaViS")


###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

#O = geompy.MakeVertex(0, 0, 0)
#OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
#OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
#OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
#geompy.addToStudy( O, 'O' )
#geompy.addToStudy( OX, 'OX' )
#geompy.addToStudy( OY, 'OY' )
#geompy.addToStudy( OZ, 'OZ' )

### Store presentation parameters of displayed objects
import iparameters
ipar = iparameters.IParameters(theStudy.GetModuleParameters("Interface Applicative", "GEOM", 1))


###
### PARAVIS component
###

try: pvsimple
except:
  import pvsimple
  from pvsimple import *
pvsimple._DisableFirstRenderCameraReset()

RenderView1 = GetRenderView()

Render()

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
  iparameters.getSession().restoreVisualState(1)
import os
#load environment project variables
execfile(os.environ["FEMProjScripts"]+"../local/projenv.py")
# load system function definitions
sys.path.insert(0,os.environ["FEMProjScripts"]+"sources/")
from salome_breptovtu import *
