'''Functions for the schedule builder project'''
import os
import re
import requests

from bs4 import BeautifulSoup
import urllib.parse as urlparse
import urllib.request as urlreq

def save_resp_data_to_file(resp_data, file_name):
    '''Saves resp_data to file_name'''
    assert isinstance(file_name, str), TypeError
    assert '.' in file_name, 'Please designate file type.'
    save_file = open(file_name, 'w')
    save_file.write(str(resp_data))
    save_file.close()

def get_source_code(URL, var_dict = None):
    ''' Get HTML source code from user-defined URL'''
    if var_dict == None:
        req = urlreq.Request(URL)
        resp = urlreq.urlopen(req)
    else:        
        resp_data = urlparse.urlencode(var_dict) 
        resp_data = resp_data.encode('utf-8') 
        req = urlreq.Request(URL, resp_data) 
        resp = urlreq.urlopen(req)
    return resp

def write_pretty_file(FILE_NAME, URL):
    '''Write pretty html source code from URL to user-defined FILE_NAME'''
    assert isinstance(FILE_NAME, str)
    export = open(FILE_NAME + ' pretty.txt', 'w')
    req = requests.get(URL)
    soup = BeautifulSoup(req.content, 'html.parser')
    export.write(soup.prettify())
    export.close()


def get_dept_codes():
    '''Retrieve all department prefixes from MSU Courses homepage'''
    save_file = open('homepage html.txt', 'r')
    data = save_file.read()
    save_file.close()
    dept = re.findall(r'value="([A-Z]+)"', data)
    return dept
    URL = 'https://reg.msu.edu/Courses/Request.aspx?'
    for code in dept:
        print('Gathering {} courses...'.format(code))
        tag = 'Term=current&SubjectCode=' + code
        # print(tag)
        req = urlreq.Request(URL + tag)
        resp = urlreq.urlopen(req)
        FILE_NAME = 'html files/{}.txt'.format(code)
        save_to_file(resp.read(), FILE_NAME)

def get_pretty_html_files():
    '''Update pretty files for each department'''
    URL = 'https://reg.msu.edu/Courses/Request.aspx?Term=current&SubjectCode='
    dept_codes = get_dept_codes()
    for dept in dept_codes:
        write_pretty_file('html files/' + dept, URL + dept)

def the_prototype(file_name, DEPT):
    '''No longer necessary for anything else.'''
    save_file = open(file_name, 'r')
    html = save_file.read()
    save_file.close()
    instances = re.findall(DEPT.upper() + r'''.{100}''', html)
    cleaned = []
    for substr in instances:
        '''Remove unnecessary characters'''
        chars = r'<|/|>|\r|\n| |\t|\w|td'
        substr = substr.strip(chars)
        substr = substr.replace(r'&nbsp;', ' ')
        substr = substr.replace(r'&nbsp', ' ')
        '''Remove non-course titles'''
        upper = any(letter.isupper() for letter in substr[8:])
        period = any(letter == '.' for letter in substr)
        and_or = any(word == 'or' or word == 'and' for word in substr.split())
        if upper and not period and not and_or:
            cleaned.append(substr.split('  '))
    for i in cleaned:
        i[0] = i[0].replace(' ', '')
        if len(i) != 2:
            i.pop()
        print(i)
    return cleaned


def return_file_as_string(FILE_NAME):
    '''Return file contents as string.'''
    import_ = open(FILE_NAME, 'r')
    string = import_.read()
    import_.close()
    return string

def write_course_info_to_csv(FILE_NAME):
    '''Retrieve all information from pretty.txt files and export to txt
    files with tab '\t' delimiters.
    '''
    '''Get names of files'''
    FOLDER_PATH = 'C:\Python34\schedule builder project\html files'
    TXT_FILES = [file_name for file_name in os.listdir(FOLDER_PATH)]
    CLASS_FILTER = ['''displaydataheading''', 'tabledata1']
    TEXT_FILTER = ('&nbsp', ';', '\t', r'\t', '\r', r'\r', '\n', r'\n', '  ')
    all_courses = []
    for file_name in TXT_FILES: #index 121 is MTH
        ''' Get html and filter out unwanted tags.'''
        print(file_name)
        html = return_file_as_string(FOLDER_PATH + '\\' + file_name)
        soup = BeautifulSoup(html, 'html.parser')
        filtered_soup = soup.find_all(class_ = CLASS_FILTER)
        ''' Order a list with three levels
            1. [All courses]
            2. [dept]
            3. [course]
        '''
        dept_info, course_info, pair = [], [], []
        '''For each department, go through courses'''
        for i, line in enumerate(filtered_soup):
            content = line.text
            for i, string in enumerate(TEXT_FILTER):
                content = content.replace(string, '')
            '''TODO: Figure out why .rstrip isn't working'''
            try:
                while not content[0].isalnum():
                    content = content[1:]
                while not content[-1].isalnum():
                    content = content[:-1]
            except IndexError:
                print('Found empty content')
                continue
            '''New list for new course'''
            if content == 'Course':
                dept_info.append(course_info)
                course_info = []
            course_info.append(content)
        dept_info.append(course_info)
        all_courses.append(dept_info)

    '''Write to file'''
    save_file = open(FILE_NAME, 'w')
    for i, dept in enumerate(all_courses):
        for j, course in enumerate(dept):
            save_file.write('\t'.join(course) + '\n')    
    save_file.close()

def get_csv(FILE_NAME):
    get_pretty_html_files()
    write_course_info_to_csv()