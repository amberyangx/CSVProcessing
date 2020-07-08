import shutil
import glob
from pathlib import Path
import subprocess
import os

#subprocess.call("Station.py", shell = True)

path = os.getcwd()
allFiles = glob.glob(path+"/*_Row_Station.csv")

with open('tempStation.csv','wb') as outfile:
    for i, fname in enumerate(allFiles):
        with open(fname, 'rb') as infile:
            if i != 0:
                infile.readline()

            shutil.copyfileobj(infile, outfile)
            
for p in Path('.').glob("*_Row_Station.csv"):
    p.unlink()
