''' 
Desired Result for End-Users
----------------------------
I want this easily accessible online. The webpage should be mobile-friendly.
According to the following queries, I want the page to display the results, 
followed by optional excel and pdf downloads.
    1.   Up to three degree programs.
    2.   Up to three minor fields of study.
    3.   Current year of study.
    4.   Willingness to study over summer. 

More Specs
----------
    1.  Limit third-party dependencies. The last thing I want is 90-percent 
        of the code becoming useless when some import updates.
    2.  Keep it local. It's time consuming to keep pulling source code from
        the source. Do it once, then pull from file.

Gathering Data ( * : Incomplete )
---------------------------------
    1. Save the source code locally for each department. 
 *  2. Pull the following data from the source code. 
        a. Course Code (This included a dept prefix)
        b. Course Title
        c. Prerequisites

Fortunately, everything we need is online at the MSU Registrar's Office.

    URL = 'https://reg.msu.edu/Courses/Request.aspx?'
'''
from sys import exit
import html.parser
import re

from bs4 import BeautifulSoup
import requests
import urllib.request as urlreq 
import urllib.parse as urlparse

from functions import *

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
zipped = zip(a,b)
for i in zipped:
    print(i)
        
    # print(line)