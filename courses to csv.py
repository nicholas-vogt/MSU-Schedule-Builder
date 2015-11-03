''' 
Scrape relevant text from MSU's Registrar and put into csv format with a tab delimiter.

ToDo: Sort info properly by column. Some courses have more parameters than others.
'''
from sys import exit
import html.parser
import re

from bs4 import BeautifulSoup
import requests
import urllib.request as urlreq 
import urllib.parse as urlparse

import functions

URL = 'https://reg.msu.edu/Courses/Request.aspx?SubjectCode=mth&Term=current'
# req = urlreq.Request(URL)
# resp = urlreq.urlopen(req)
# # print(resp.read())
# soup = BeautifulSoup(resp.read(), 'html.parser')
# resp.close()
# print(soup.prettify())

all_data = open('all data.txt', 'r')
for line in all_data:
    # print(line)
    line = [i for i in line if i.isalnum() or i.isspace()]
    line = ''.join(line)
    line = line.replace('xa0', ' ')
    print(line)
all_data.close()

exit()

line = line.split('\t')
a = line[0::2]
b = line[1::2]
zipped = zip(a, b)
for i in zipped:
    print(i)
    # print(line)
