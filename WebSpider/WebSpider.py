from bs4 import BeautifulSoup
import urllib2,urllib
import os
import os.path
import wget
import sys
import shutil
import re

saveToFolder = ''
if(len(sys.argv) == 2):
    saveToFolder = sys.argv[1]
    if(not os.path.exists(saveToFolder)):
        os.mkdir(saveToFolder)

if(not os.path.isfile("base.page")):
    print 'file base.page dosen\'t exit...'
    exit(0)

file = open("base.page","r")
baseUrl = file.readline().replace('\n','')
startUrl  = file.readline()
if((len(startUrl)<10) or (len(baseUrl)<10)):
    print 'Settings in base.page invalid...'

basePage = urllib2.urlopen(startUrl).read()
soup = BeautifulSoup(basePage)
content = soup.find_all('a',href=True)

allDownloadedFiles = []
for tag in content:
    for attr in tag.attrs:
        if (('title' in attr) and ('.jpg' in tag.attrs[attr])):
            saveFile = unicode(tag.attrs['title'].replace('File:',''))
            imageUrl = baseUrl + tag.attrs['href']
            imagePage = urllib2.urlopen(imageUrl).read()
            imageSoup = BeautifulSoup(imagePage)
            bigImageUrl = ''
            for imTag in imageSoup.find_all('a',href=True):
                tagString = imTag.string
                if(not tagString):
                    continue
                if((('x' in tagString) and ('pixels' in tagString)) or ('Original file' in tagString)):
                    bigImageUrl = imTag.attrs['href']
            if(len(bigImageUrl)>0):
                currFileName = wget.download(bigImageUrl)
                if(len(saveToFolder)>0):
                    destFile = os.path.join(saveToFolder,saveFile)
                    index = 1
                    while(os.path.exists(destFile)):
                        destFile = destFile.replace('.jpg',str(index)+'.jpg')
                        index = index + 1
                    destFile = re.sub('[*?"<>|]', '_',destFile)
                    shutil.copyfile(currFileName.decode('utf8'),destFile)
                    #os.remove(currFileName)
                allDownloadedFiles.append(currFileName)
                    
            
    tagString = unicode(tag.string)