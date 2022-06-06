import scrapy
import requests
import re
import lxml.html
#from selectolax.parser import HTMLParser

from bs4 import BeautifulSoup
def extratBs(txt):
    lst = []
    s = BeautifulSoup(txt, 'lxml')
    for tag in s.find_all('a', href=True):
        lst.append(tag['href'])
    return lst

def extractLinkRegEx(txt):
    tgs = re.compile(r'<a[^<>]+?href=([\'\"])(.*?)\1', re.IGNORECASE)
    return [match[1] for match in tgs.findall(txt)]

def extractLinkxml(txt):
    lst = []
    dom = lxml.html.fromstring(txt)
    for l in dom.xpath('//a/@href'):
        lst.append(l)
    return lst

def printList(lst):
    for l in lst:
        print('level 1 ->' + l)

r = requests.get('https://edfreitas.me')
#print(extractLinkRegEx(r.text))
#printList(extractLinkRegEx(r.text))
#print(extractLinkxml(r.text))
printList(extratBs(r.text))