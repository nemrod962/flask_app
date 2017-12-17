from bs4 import BeautifulSoup
import urllib2
#import requests


"""
url = raw_input("Enter a website to extract the URL's from: ")
r  = requests.get("http://" +url)
data = r.text
"""


html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

"""
#get source
response = urllib2.urlopen("http://www.numeroalazar.com.ar/")
page_source = response.read()
#print page_source

print "SOUP!"
soup = BeautifulSoup(page_source, "html.parser")

print soup.prettify()

import requests
res = soup.find(id="numeros_generados")
print res
"""

print "GO!"
url = "https://beebotte.com/dash/"
tablaID = "09db3e70-df3a-11e7-bfef-6f68fef5ca14"
fullurl = url+tablaID
print fullurl
response = urllib2.urlopen(fullurl)
page_source = response.read()

soup = BeautifulSoup(page_source, "html.parser")

#print soup.prettify()
asd = tablaID+"_body"
print asd
res = soup.find_all(id=asd)
print res
"""
for link in soup.find_all('a'):
    print(link.get('href'))
"""

"""
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get('http://jokes.cc.com/')
soupFromJokesCC = BeautifulSoup(driver.page_source) #page_source fetches page after rendering is complete
driver.save_screenshot('screen.png') # save a screenshot to disk

driver.quit()
"""
