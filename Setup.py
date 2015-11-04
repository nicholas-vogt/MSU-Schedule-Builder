'''
Write html to csv
-----------------
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

class Setup:
    '''Functions to write data files.'''
    def write_pretty_html(FILE_NAME, URL):
        '''
        Write pretty html source code from URL to user-defined FILE_NAME.
        'Pretty' formats the html to make it legible without changing the
        code.

        Returns html string.
        '''
        assert isinstance(FILE_NAME, str)
        if '.' not in FILE_NAME:
            FILE_NAME += '.txt'
        try:
            req = requests.get(URL)
        except requests.exceptions.ConnectionError:
            print('ConnectionError: Internet is not connected. Connect and try again.')
            sys.exit()
        soup = BeautifulSoup(req.content, 'html.parser')
        export = open(FILE_NAME, 'w')
        export.write(soup.prettify())
        export.close()


    def get_dept_prefixes():
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
        dept_names = Setup.get_dept_prefixes()
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
        '''
        Retrieve all information from html files and export to txt
        files with tab '\t' delimiters.

        Parameters
        ----------
        EXPORT_FILE : Name of file to be exported.
        COURSE_FOLDER : Name of folder where course htmls are stored.

        '''
        assert isinstance(EXPORT_FILE, str), \
            TypeError('Export file must be a string')
        assert isinstance(COURSE_FOLDER, str), \
            TypeError('Folder name must be a string')
        if '.' not in EXPORT_FILE:
            EXPORT_FILE += '.txt'
        DIR = [file_name for file_name in os.listdir(COURSE_FOLDER)]
        DIR_SIZE = len(DIR)
        print('Exporting {} files to csv...'.format(DIR_SIZE))
        NOODLES = ['''displaydataheading''', 'tabledata1']
        # TODO: Figure out why regex doesn't capture all escaped chars
        # We don't want flies in our soup...
        FLIES = ('&nbsp', ';', '\t', r'\t', '\r', r'\r', '\n', r'\n', '  ')
        save_file = open(EXPORT_FILE, 'w')
        for dept in DIR:
            html_file = open(COURSE_FOLDER + '/' + dept, 'r')
            html = html_file.read()
            html_file.close()
            soup = BeautifulSoup(html, 'html.parser')
            filtered_soup = soup.find_all(class_=NOODLES)
            for line in filtered_soup:
                text = line.text
                for fly in FLIES:
                    text = text.replace(fly, '')
                # TODO: Figure out why .rstrip isn't working
                try:
                    while not text[0].isalnum():
                        text = text[1:]
                    while not text[-1].isalnum():
                        text = text[:-1]
                except IndexError:
                    print('\t{} was empty.'.format(dept))
                    break
                if text == 'Course': # new list for new course
                    save_file.write('\n')
        save_file.close()


    def setup_everything(FOLDER_NAME=None):
        '''Writes all html files, csvs, etc.'''
        assert isinstance(FOLDER_NAME, str) or FOLDER_NAME == None, \
            TypeError('Input must be string.')
        print('Exporting files to file course data.txt...')
        if FOLDER_NAME:
            Setup.get_courses_html(FOLDER_NAME)
            Setup.write_course_html_to_csv('course data.txt', FOLDER_NAME)
        else:
            Setup.get_courses_html('course htmls')
            Setup.write_course_html_to_csv('course data.txt', 'course htmls')
