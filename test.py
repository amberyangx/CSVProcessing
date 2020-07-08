from xml.etree import ElementTree
import csv
import os
import glob
import errno


path = os.getcwd()

configFiles = glob.glob(path+"/*_Config.txt")
for name in configFiles:
    try:
        with open(name) as ConfigFile:
            filename = ConfigFile.read()

        open('temp.xml', 'w').close()

        with open(filename) as f:
            index = 0
            lines = f.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                with open('temp.xml','r+') as f1:
                    f1.write(line)
                    f1.seek(0,0) # when parsing an open and write file, parse will go to next line.
                    #seek() helps to go to any desired line 

                    #get the tree structure
                    tree = ElementTree.parse('temp.xml')
                    root = tree.getroot()

                    #open and write to a temp csv file
                    base = os.path.basename(filename)
                    basefilename = os.path.splitext(base)[0]
                    outfile = open(str(index)+ "_" + basefilename +'_Row_Lane.csv', 'w', newline='')
                    csvwriter = csv.writer(outfile)
                    index += 1


                    #write the header
                    head = ["hour","date",'contractId','vdsId','periodNum','laneNumber', 'validityFlag','failureTypeReason','laneOcc','laneVol','laneSpd','laneLength']
                    csvwriter.writerow(head)

                    #get the date data.
                    date = root.find('date').text

                    #get the period
                    hour = basefilename.split('_')[1]

                    vdsData = root.find('vdsData')
                    if vdsData is None:
                        incRow = []
                        incRow.append(hour)
                        incRow.append(date)
                        incRow += 10*['NONE']
                        csvwriter.writerow(incRow)
                        
                    #get vdsData and append to the row to complete one row each time
                    for vdsData in root.findall('vdsData'):
                        #get date, contractId, vdsId
                        contractId = vdsData.find('contractId')
                        if contractId is not None:         
                            incRow = []
                            
                            incRow.append(hour)
                            incRow.append(date)

                            contractId = vdsData.find('contractId').text
                            incRow.append(contractId)
                            
                            vdsId = vdsData.find('vdsId').text
                            incRow.append(vdsId)
                            periodNum = vdsData.find('periodNum').text
                            incRow.append(periodNum)
                            #get all laneData
                            for laneData in vdsData.findall('laneData'):
                                row=[]
                                row.append(laneData.findtext('laneNumber', default = ''))
                                row.append(laneData.findtext('validityFlag', default = ''))
                                row.append(laneData.findtext('failureTypeReason', default = ''))
                                row.append(laneData.findtext('laneOcc', default = ''))
                                row.append(laneData.findtext('laneVol', default = ''))
                                row.append(laneData.findtext('laneSpd', default = ''))
                                row.append(laneData.findtext('laneLength', default = ''))
                                joinedRow = incRow + row
                                csvwriter.writerow(joinedRow)
                            
                            
                    outfile.close()

                    f1.truncate(0)
                

        os.remove('temp.xml')
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
