from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox
import subprocess
import os
import zipfile 
from zipfile import ZipInfo
import collections
from datetime import datetime

root = Tk()
    
def station():
    subprocess.call('collectAllStation.py', shell = True)
    if tkinter.messagebox.askyesno(title="Collection Done", message='Click Yes to save, click No to remove'):
        file_save_station()
        if tkinter.messagebox.askokcancel(title="Open", message='Do you wish to open the file?'):
            os.startfile(station_filename)
    else:
        os.remove('tempStation.csv')

def lane():
    #start collection
    subprocess.call('collectAllLane.py', shell = True)
    if tkinter.messagebox.askyesno(title="Collection Done", message='Click Yes to save, click No to remove'):
        file_save_lane()
        if tkinter.messagebox.askokcancel(title="Open", message='Do you wish to open the file?'):
            os.startfile(lane_filename)
        '''
        label2toopen = Label(root, text = "   Click to open the file    >>>>>")
        label2toopen.place(x = 180, y = 102)
        b2 = Button(root, text = 'Open csv file', command=openLane)
        b2.place(x = 420, y = 100)

        '''
    else:
        os.remove('tempLane.csv')

def remove():     ### remove all the files end with txt
    path = os.getcwd()
    currentDir = os.listdir(path)
    for item in currentDir:
        if item.endswith('.txt'):
            os.remove(os.path.join(path,item))

def file_save_lane(): ### ask the user to input the file name for saving
    '''
    for FTM prefix only
    FTM = []
    prefix = ''
    global lane_filename
    for i in nameList:
        FTM.append(i.split('-')[0])
    prefix = '+'.join(list(set(FTM))) ### i.e. FTM1+FTM2
    '''
    global lane_filename
    prefix = nameList[0]
    prefix = prefix+"_Lane_"+datetime.today().strftime('%Y%m%d%H%M%S')+".csv" ### i.e. 'FTM1+FTM2_Lane_2020-03-03-15:02:59.csv'
    files = [('CSV Files','*.csv*')]
    lane_filename = filedialog.asksaveasfilename(parent = root,initialdir=os.getcwd(),title="Save As ...",initialfile= prefix,filetypes=files, defaultextension='.csv')
    lane()
    os.rename('tempLane.csv',lane_filename)


def file_save_station(): ### ask the user to input the file name for saving
    FTM = []
    prefix = ''
    global station_filename
    for i in nameList:
        FTM.append(i.split('-')[0])
    prefix = '+'.join(list(set(FTM))) ### i.e. FTM1+FTM2
    prefix = prefix+"_Station_"+datetime.today().strftime('%Y%m%d%H%M%S')+".csv" ### i.e. 'FTM1+FTM2_Station_2020-03-03-15:02:59.csv'
    files = [('CSV Files','*.csv*')]
    station_filename = filedialog.asksaveasfilename(parent = root,initialdir=os.getcwd(),title="Save As ...",initialfile= prefix,filetypes=files, defaultextension='.csv')
    os.rename('tempStation.csv',station_filename)

'''       
def popupmsg(msg):
    popup = tkinter.Tk()
    popup.wm_title("Important!")
    label = ttk.Label(popup, text = msg)
    label.pack(side = "top", fill = 'x', pady=10)
    B1 = ttk.Button(popup, text = "Remove", command = popup.destroy)
    B1.pack()
    B2 = ttk.Button(popup, text = "Cancel", command = popup.destroy)
    B2.pack()
'''
    
def checkSize(zipfileName):
    alltxt = ''
    for i in zipfileName:
        zip_ref = zipfile.ZipFile(i) # create zipfile object
        for info in zip_ref.infolist():
            txt = info.filename + '\n\tCompressed:\t' + str(info.compress_size) +' bytes' +'\n\tUncompressed:\t' + str(info.file_size)+' bytes \n'
            alltxt += txt
    if tkinter.messagebox.askokcancel("Click Ok to continue",alltxt):
        return True
    
  
def openzippedfile():
    global nameList  
    nameList = []
    zipfileName = filedialog.askopenfilenames(parent = root, title = "Choose your file")
    if zipfileName:
        checkSize(zipfileName)
        for i in zipfileName:
            zip_ref = zipfile.ZipFile(i) # create zipfile object
            extracted = zip_ref.namelist() # get upzipped the file name
            path = os.getcwd() #get current working dir
            unzippedFile = zip_ref.extractall(path) # extract file to working dir
            name = os.path.basename(zip_ref.filename) #get the entire zipped file name
            extracted_file = os.path.join(path,extracted[0]) # get the full path of extracted txt
            namebase = os.path.splitext(name)[0]
            nameList.append(namebase)
            try:
                os.rename(extracted_file, path+'/' + namebase+'.txt')
            except FileExistsError:
                os.remove(namebase+'.txt')
                os.rename(extracted_file, path+'/'+namebase+'.txt')
            reName = os.path.join(path, namebase+'.txt')
            zip_ref.close() #close file
            os.chdir(path)
            f = open(namebase+'_Config.txt','w')
            f.write(reName)
            f.close()
    print(nameList)
    return nameList


def main():
    root.geometry('600x350')
    root.title("Raw 20-sec Data Extractor")

    uploadBtn = Button(root, text = "Upload your file", command = openzippedfile)
    uploadBtn.pack()

    stationBtn = Button(root, text = "Collect Station Data", command = station)
    stationBtn.place(x = 30, y = 50)

    laneBtn = Button(root, text = "Collect Lane Data", command = lane)
    laneBtn.place(x = 30, y = 100)

    var = StringVar()
    label = Message(root, textvariable=var, width = 1000)
    var.set("IMPORTANT: Must press this button before starting a new collection -->")
    label.place(x =25, y = 152)
    
    removeBtn = Button(root, text = "Remove .txt Files", command = remove)
    removeBtn.place(x = 420, y =150)
    
    txt = Text(root,height = 6,width=65)
    txt.pack()
    txt.place(x = 40,y=200)
    txt.insert(END, "Instructions:\n1. Please upload your zip file first.\n2. Data collecting requires some time.\n3. 'Open csv file' button will show up when collecting is done.\n4. Must remove all txt files.")

    
    frame = Frame(root)
    frame.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
