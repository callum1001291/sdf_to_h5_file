from openbabel import pybel as pb
from openbabel import openbabel as ob
import h5py
import numpy as np
import os, sys
#imports the functions from the data packer used to put the data read from the 0509.sdf
#file into the h5py file format
from torchani.data._pyanitools import datapacker

#script takes an sdf file as argument
count = 0
outputFile = datapacker(sys.argv[2])
goodElements = set([1,6,7,8,9,16,17])

for mymol in pb.readfile("sdf", sys.argv[1]): #loops to get all molucules in the sdf file
 a = mymol.atoms
 mymolElements = set([a.atomicnum for a in mymol.atoms])
 if bool(mymolElements - goodElements) == False :
  coordinates = np.array([a.coords for a in mymol.atoms])
  species = [ob.GetSymbol(a.atomicnum) for a in mymol.atoms]
  smiles = mymol.write().split()[0]
  outputFile.store_data('%s_%d'%(mymol.title,count),coordinates=[coordinates], species=species,smiles=list(smiles),energies=[0])
  count += 1

#cleanup
outputFile.cleanup()
print('molecule count = ' + str(count))
