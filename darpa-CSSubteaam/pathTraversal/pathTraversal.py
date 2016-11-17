import os, csv, fnmatch
import time
import sys
import re
#==============================================================================
def getFileTypes(fileName):
    if '.png' in fileName or '.jpg' in fileName:
        fileType = 'Image'
    elif '.csv' in fileName:
        fileType = 'CSV'
    elif '.xls' in fileName or '.xlsx' in fileName:
        fileType = 'Excel'
    elif '.txt' in fileName:
        fileType = 'Text'
    else:
        fileType = 'Unidentified'
    return fileType

def getFullFilePath(imFileList, dirName):
    fullFilePath = []
    for fileName in fnmatch.filter(imFileList, '*.*'):
        fullFilePath.append(os.path.join(dirName, fileName))
    return fullFilePath
    
def getCouponName(fileName):
    regex = re.compile("[0-9]{0,}[\\-_][0-9]{0,}[\\-_][0-9]{0,}")
    matchArray = regex.findall(fileName)
    if(matchArray):
        return matchArray[0].replace('_', '-')
    else:
        return ''
        
def getImageAttributes(fileName):
    if '.png' in fileName or '.jpg' in fileName:
        name = fileName.split('.')[0]
        nameTypes = name.split('-')
        series = nameTypes[0]
        panel = nameTypes[1]
        coupon = nameTypes[2]
        attributes = [series, panel, coupon]
        return attributes
    else:
        return []
        
def getSeries(dirName):
    if 'DOE_I/' in dirName or 'DOE_I_' in dirName:
        return 'Series 2'
    elif 'DOE_II/' in dirName or 'DOE_II_' in dirName:
        return 'Series 6'
    elif 'DOE_IV/' in dirName or 'DOE_IV_' in dirName:
        return 'Series 10'
#==============================================================================



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error in arguments passed.\nStandard input format:")
        print("$python3 <filename> <directorypath>")
        sys.exit()
    datetime = time.strftime("%Y%m%d_%H%M%S")
    nameOfCSV = 'graphFilePath_run_'+datetime+'.csv'
    nameOfDirectoryCsv = 'graphDirectory_run_'+datetime+'.csv'
    rootDirectory= sys.argv[1]
    headerSetFlag = False
    cleanedList = []
    couponList = list()
    dirList = list()
    #==============================================================================
    #creating the header row
    
    headerRow = ["FullFilePath","FileTypes", "CurrentDirectoryName","SeriesName",\
                 "AllFileList", "CouponName", "Series","Panel", "Coupon"]
    
    #============================================================================== 
    
    
    #creating the CSV file=========================================================
    with open(nameOfCSV, 'a',newline='') as csvFile:
        w = csv.writer(csvFile)
        w.writerow(headerRow)
        headerforDir = ['currentDirectory','currLabel', 'parentDirectory','PLabel', 'childDirectory', 'CLabel', \
                        'NumOfFilesInside', 'NumofSubDir', 'SubDirLabels', 'FilePathsInsideCurr']
        with open(nameOfDirectoryCsv, 'a',newline='') as csvFileD:
            ww = csv.writer(csvFileD)
            ww.writerow(headerforDir)#write the header row
            for dirName, subDirList, imFileList in os.walk(rootDirectory):
                depth = len(dirName.rstrip(os.path.sep).split(os.path.sep))#find the depth of the curr dir
                currLabel = dirName.rstrip(os.path.sep).split(os.path.sep)[-1]#current directory label 
                fullFilePath = getFullFilePath(imFileList, dirName) #get full path names for files.
                if depth >1:
                    isOfSubDir = (os.path.sep).join((dirName.rstrip(os.path.sep).split(os.path.sep)[:-1])) #the parent directory
                    Plabel = (dirName.rstrip(os.path.sep).split(os.path.sep)[-2])#parent directory label
                else:
                    isOfSubDir = ''
                    Plabel =''
                dirList = [dirName.strip().replace(' ','_'), currLabel.strip().replace(' ','_'),\
                           isOfSubDir.strip().replace(' ','_') ,Plabel.strip().replace(' ','_'),'','',\
                            len(imFileList),len(subDirList),','.join(subDirList).strip().replace(' ','_'),\
                            ','.join(fullFilePath).strip().replace(' ','_')]
                try:
                    ww.writerow(dirList)#write the header of each level          
                except:
                    pass
                
                #for the stuff inside the subdirectories
                for bfsDir in subDirList:
                    depth = len(dirName.rstrip(os.path.sep).split(os.path.sep))
                    currLabel = dirName.rstrip(os.path.sep).split(os.path.sep)[-1]#current directory label
                    filePathForSD = getFullFilePath(imFileList, dirName) #get full path names for files.
                    if depth >1:
                        isOfSubDir = (os.path.sep).join((dirName.rstrip(os.path.sep).split(os.path.sep)[:-1])) #the parent directory
                        Plabel = (dirName.rstrip(os.path.sep).split(os.path.sep)[-2])
                    else:
                        isOfSubDir = ''
                        Plabel = ''

                    Clabel = bfsDir.split(os.path.sep)[-1]
                    dirList = [dirName.strip().replace(' ','_') , currLabel.strip().replace(' ','_'),\
                               isOfSubDir.strip().replace(' ','_'), Plabel.strip().replace(' ','_') ,\
                                 os.path.join(dirName, bfsDir).strip().replace(' ','_') ,Clabel.strip().replace(' ','_'),\
                                 len(imFileList), '','',','.join(filePathForSD).strip().replace(' ' ,'_')]
                    try:
                        ww.writerow(dirList)
                    except:
                        pass
                
                #for individual files
                for fileName in fnmatch.filter(imFileList, '*.*'):
                    filePath = os.path.join(dirName, fileName).strip().replace(' ','_')
                    currentDirName = dirName.rstrip(os.path.sep).split(os.path.sep)[-1].strip().replace(' ','_')
                    couponName = getCouponName(fileName)
                    splitcoupon = couponName.split('-') if len(couponName) != 0 else ['','','']
                    cleanedList = [filePath.strip().replace('\\','/'), getFileTypes(fileName),  dirName.strip().replace('\\','/'),\
                                   getSeries(dirName),fileName.strip().replace(' ','_'), couponName, str(splitcoupon[0]),\
                                    str(splitcoupon[1]), str(splitcoupon[2])]
                    if(len(couponName)>0):             
                        splitcoupon.insert(0,couponName)
                    if (len(cleanedList) != 0):
                        try:    
                            w.writerow(cleanedList)
                        except:
                            pass
                
    #closing the CSV file=========================================================
    csvFile.close()
    csvFileD.close()
print("Conversion done.\nFilenames are --> ")
print("1. For Directory Structure  - {} \n2. For FileStructure Associated with domain knowledge - {}".format(nameOfDirectoryCsv,nameOfCSV))


