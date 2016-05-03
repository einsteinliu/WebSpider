from bs4 import BeautifulSoup
import urllib2,urllib
import os
import os.path

if(not os.path.isfile("base.page")):
    print 'file base.page dosen\'t exit...'

file = open("base.page","r")
baseUrl = file.readline()
if(len(baseUrl)<10):
    print 'Settings in base.page invalid...'


