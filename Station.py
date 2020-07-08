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
    

        open('temp.xml','w').close()

        with open(filename) as f:
            index = 0
            lines = f.readlines()  
            for i in range(0, len(lines)):
                line = lines[i]
                #getthe tree structure
                with open('temp.xml','r+') as f1:
                    f1.write(line)
                    f1.seek(0,0)

                    #with open('temp.xml','r') as infile:
                    tree = ElementTree.parse('temp.xml')
                    root = tree.getroot()

                    #open and write to a temp csv file
                    #filename = "C:/Users/AmberX/Desktop/temp/testcsv/index+'.csv'"
                    base = os.path.basename(filename)
                    basefilename = os.path.splitext(base)[0]
                    outfile = open(str(index)+'_'+basefilename+'_Row_Station.csv', 'w', newline='')
                    csvwriter = csv.writer(outfile)
                    index +=1


                    #write the header
                    head = ["hour","date",'contractId','vdsId','validThisPeriod','periodNum','occ','vol','spd','length']
                    csvwriter.writerow(head)

                    #get the date data.
                    date = root.find('date').text

                    #get the hour
                    hour = basefilename.split('_')[1]

                    vdsData = root.find('vdsData')
                    if vdsData is None:
                        incRow = []
                        incRow.append(hour)
                        incRow.append(date)
                        incRow += 8*['NONE']
                        csvwriter.writerow(incRow)
                    
                    #get vdsData and append to the row to complete one row each time
                    for vdsData in root.findall('vdsData'):
                        contractId = vdsData.find('contractId')
                        if contractId is not None:                            
                            row = []
                            row.append(hour)
                            row.append(date)
                            contractId= vdsData.find('contractId').text
                            row.append(contractId)
                            vdsId = vdsData.find('vdsId').text
                            row.append(vdsId)
                            validThisPeriod = vdsData.find("validThisPeriod").text
                            row.append(validThisPeriod)
                            periodNum = vdsData.find("periodNum").text
                            row.append(periodNum)
                            occ = vdsData.find("occ").text
                            row.append(occ)
                            vol = vdsData.find('vol').text
                            row.append(vol)
                            spd = vdsData.find('spd').text
                            row.append(spd)
                            length = vdsData.find("length").text
                            row.append(length)
                            csvwriter.writerow(row)
                    outfile.close()

                    f1.truncate(0)
            
        os.remove('temp.xml')
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

                                    
                
