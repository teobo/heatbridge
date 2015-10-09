#environment variables definition
#fem solver
import os
from re import search
for key in os.environ.keys():
   if not search("FEM_PROTO_PATH1", key):
      os.environ["FEM_PROTO_PATH1"]=os.environ["FEMProjScripts"]+"testbed1/salome_erste2D/"

for key in os.environ.keys():
   if not search("FEM_PROTO_FLUX3_PATH", key):
      os.environ["FEM_PROTO_FLUX3_PATH"]=os.environ["FEMProjScripts"]+"testbed2/fluxsolver3/"
      
for key in os.environ.keys():
   if not search("FEM_UNVFILE1", key):
      os.environ["FEM_UNVFILE1"]=os.environ["FEM_PROTO_PATH1"]+"Elmer_Mesh_tutoria150915.2D.unv"

for key in os.environ.keys():
   if not search("FEM_SIF_TEMPL_FILE1", key):
      os.environ["FEM_SIF_TEMPL_FILE1"]=os.environ["FEM_PROTO_PATH1"]+"case.sif_template"

for key in os.environ.keys():
   if not search("FEM_SIF_FILE1", key):
      os.environ["FEM_SIF_FILE1"]=os.environ["FEM_PROTO_PATH1"]+"case.sif"

for key in os.environ.keys():
   if not search("FEM_ElMER_GRID_TEMPL_PATH1", key):
      os.environ["FEM_ElMER_GRID_TEMPL_PATH1"]=os.environ["FEM_PROTO_PATH1"]+"Elmer_Mesh_tutoria150915.2D"

for key in os.environ.keys():
   if not search("FEM_ElMER_GRID_PATH1", key):
      os.environ["FEM_ElMER_GRID_PATH1"]=os.environ["FEM_PROTO_PATH1"]+""


for key in os.environ.keys():
   if not search("FEM_ElMER_EP_FILE1", key):
      os.environ["FEM_ElMER_EP_FILE1"]=os.environ["FEM_PROTO_PATH1"]+"case.ep"

for key in os.environ.keys():
   if not search("FEM_ElMER_EP_TEMPL_FILE1", key):
      os.environ["FEM_ElMER_EP_TEMPL_FILE1"]=os.environ["FEM_ElMER_GRID_PATH1"]+"case.ep"

for key in os.environ.keys():
   if not search("FEM_ElMERPOST_SOURCE1", key):
      os.environ["FEM_ElMERPOST_SOURCE1"]=os.environ["FEM_PROTO_PATH1"]+"cmd1.txt"
