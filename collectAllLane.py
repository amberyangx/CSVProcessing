import shutil
import glob
from pathlib import Path
import subprocess
import os



#subprocess.call("Lane.py", shell = True)

path = os.getcwd()
allFiles = glob.glob(path+"/*_Row_Lane.csv")


with open('tempLane.csv','wb') as outfile:
    for i, fname in enumerate(allFiles):
        with open(fname, 'rb') as infile:
            if i != 0:
                infile.readline()

            shutil.copyfileobj(infile, outfile)
            
for p in Path('.').glob("*_Row_Lane.csv"):
    p.unlink()
