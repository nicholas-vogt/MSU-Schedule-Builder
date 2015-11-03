'''
Functions for reading source code
---------------------------------
There are two main URLs to read from. The first displays all course
information, including course code, semester offered, etc. 
    https://reg.msu.edu/Courses/Request.aspx?

The second displays degree requirements. 
    ***URL GOES HERE***

The functions in this file read the source code to these URLs and create
ordered csv files with tab delimiter.
'''
import os
import re
import requests
import sys

from bs4 import BeautifulSoup
import urllib.parse as urlparse
import urllib.request as urlreq

class Setup:
    '''Functions to write data files.'''
    def write_pretty_html(FILE_NAME, URL):
        '''
        Write pretty html source code from URL to user-defined FILE_NAME.
        'Pretty' formats the html to make it legible without changing the
        code. 
        '''
        assert isinstance(FILE_NAME, str)
        assert '.' in FILE_NAME, Exception('Please designate file type.')
        try:
            req = requests.get(URL)
        except requests.exceptions.ConnectionError:
            print('ConnectionError: Internet is not connected. Connect and try again.')
            sys.exit()
        soup = BeautifulSoup(req.content, 'html.parser')
        export = open(FILE_NAME, 'w')
        export.write(soup.prettify())
        export.close()


    def get_dept_names():
        '''Get dept prefixes'''
        print('Retrieving department prefixes...')
        try:
            #txt file will empty if we don't assign save_file
            save_file = open('homepage html.txt', 'r')
        except FileNotFoundError:
            print('FileNotFoundError: Gathering source code.')
            Setup.write_pretty_html('homepage html.txt', 
                              'https://reg.msu.edu/Courses/Search.aspx')
            save_file = open('homepage html.txt', 'r')
        data = save_file.read()
        save_file.close()
        # All department info is of the form value="MTH"
        dept_names = re.findall(r'value="([A-Z]+)"', data)
        return dept_names


    def get_courses_html(FOLDER):
        '''
        Retrieves course source code by department. Writes raw source code to 
        file according to department prefix. e.g. html files/MTH.txt.

        All MSU course codes have a department prefix. The form on MSU's 
        course search includes a list of all department acronyms since 2000.
        '''
        assert isinstance(FOLDER, str), TypeError('Input must be string.')
        print('Retrieving course HTML files...')
        dept_names = Setup.get_dept_names()
        URL = 'https://reg.msu.edu/Courses/Request.aspx'
        if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)
        for dept_code in dept_names:
            course_path = FOLDER + '/' + dept_code + '.txt'
            if not os.path.exists(course_path):
                print('Gathering {} courses...'.format(dept_code))
                tag = '?Term=current&SubjectCode=' + dept_code
                dept_url = URL + tag
                Setup.write_pretty_html('course files/{}.txt'.format(dept_code), dept_url)


    def write_course_html_to_csv(EXPORT_FILE, COURSE_FOLDER):
        '''Retrieve all information from pretty.txt files and export to txt
        files with tab '\t' delimiters.
        '''
        print('Writing courses to csv...')
        TXT_FILES = [file_name for file_name in os.listdir(COURSE_FOLDER)]
        CLASS_FILTER = ['''displaydataheading''', 'tabledata1']
        TEXT_FILTER = ('&nbsp', ';', '\t', r'\t', '\r', r'\r', '\n', r'\n', '  ')
        all_courses = []
        for file_name in TXT_FILES: #index 121 is MTH
            ''' Get html and filter out unwanted tags.'''
            html_file = open(COURSE_FOLDER + '/' + file_name, 'r')
            html = html_file.read()
            html_file.close()
            soup = BeautifulSoup(html, 'html.parser')
            filtered_soup = soup.find_all(class_ = CLASS_FILTER)
            ''' Order a list with three levels
                1. all_courses is a list of depts
                2. dept is a list of courses
                3. course is a list of course info
            '''
            dept_info, course_info = [], []
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
                    print('{} was empty.'.format(file_name))
                    continue
                '''New list for new course'''
                if content == 'Course':
                    dept_info.append(course_info)
                    course_info = []
                course_info.append(content)
            dept_info.append(course_info)
            all_courses.append(dept_info)

        '''Write to file'''
        save_file = open(EXPORT_FILE, 'w')
        for i, dept in enumerate(all_courses):
            for j, course in enumerate(dept):
                save_file.write('\t'.join(course) + '\n')    
        save_file.close()

    def setup_everything(FOLDER_NAME=None):
        '''Writes all html files, csvs, etc.'''
        if FOLDER_NAME == None:
            Setup.get_courses_html('course htmls')
            Setup.write_course_html_to_csv('course data.txt', 'course htmls' )
        else:
            assert isinstance(FOLDER_NAME, str), TypeError('Input must be string.')
            Setup.get_courses_html(FOLDER_NAME)
            Setup.write_course_html_to_csv('course data.txt', FOLDER_NAME)
