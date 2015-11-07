'''
Use get_all() to write all data to current working directory

There are two main URLs to read from. The first displays all course
information, including course code, semester offered, etc.
    https://reg.msu.edu/Courses/Request.aspx?

The second displays degree requirements.
    https://reg.msu.edu/academicprograms/Programs.aspx?PType=UN

The functions in this file read the source code to these URLs and create
ordered csv files with tab delimiter.
'''
import os
import re
import requests

from bs4 import BeautifulSoup

class Setup:
    '''Writes all '''
    def write_html(url, file_name):
        '''Write html source code from url to user-defined file_name.
        '''
        assert isinstance(file_name, str), \
            TypeError('file name must be a string')
        if '.' not in file_name:
            index = file_name.find('/') + 1
            print('{0} rewritten to {0}.txt'.format(file_name[index:]))
            file_name += '.txt'
        try:
            req = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            print('Your internet may be disconnected.')
            raise e
        soup = BeautifulSoup(req.content, 'html.parser')
        export = open(file_name, 'w')
        export.write(soup.prettify())
        export.close()


    def get_dept_prefixes():
        '''Get dept prefixes'''
        try:
            #txt file will empty if we don't assign save_file
            save_file = open('course htmls/!course homepage.txt', 'r')
        except FileNotFoundError:
            Setup.write_html('https://reg.msu.edu/Courses/Search.aspx',
                             'course htmls/!course homepage.txt')
            save_file = open('course htmls/!course homepage.txt', 'r')
        html = save_file.read()
        save_file.close()
        # All department info is of the form value="MTH"
        dept_prefixes = re.findall(r'value="([A-Z]+)"', html)
        return dept_prefixes


    def get_course_htmls():
        '''
        Retrieves course source code by department. Writes raw source code to
        file according to department prefix. e.g. html files/MTH.txt.

        All MSU course codes have a department prefix. The form on MSU's
        course search includes a list of all department acronyms since 2000.
        '''
        folder = 'course htmls'
        dept_prefixes = Setup.get_dept_prefixes()
        url = 'https://reg.msu.edu/Courses/Request.aspx'
        if not os.path.exists(folder):
            os.makedirs(folder)
        for dept_code in dept_prefixes:
            course_path = folder + '/' + dept_code + '.txt'
            if os.path.exists(course_path):
                continue
            print('\tGathering {} courses...'.format(dept_code))
            tag = '?Term=current&SubjectCode=' + dept_code
            dept_url = url + tag
            Setup.write_html(dept_url,
                             'course htmls/{}.txt'.format(dept_code))


    def write_course_csv():
        '''
        Retrieve all information from html files and export to txt
        files with tab '\t' delimiters.
        '''
        csv = 'course data.txt'
        folder='course htmls/'
        Setup.get_course_htmls()
        if os.path.exists(csv):
            print('{} already exists. CSV was not created.'.format(csv))
            return None

        DIR = [file_name for file_name in os.listdir(folder)]
        DIR_SIZE = len(DIR)
        print('Exporting {} files to csv...'.format(DIR_SIZE))
        save_file = open(csv, 'w')
        for i, dept in enumerate(DIR):
            if i % (len(DIR) // 10) == 0:
                print('\t{} percent completed...'.format(i*10 // (len(DIR) // 10)))
            html_file = open(folder + dept, 'r')
            html = html_file.read()
            html_file.close()
            soup = BeautifulSoup(html, 'html.parser')
            filtered_soup = soup.find_all(class_=['displaydataheading',
                                                  'tabledata1'])
            for line in filtered_soup:
                text = line.text
                text = re.sub(r'\W+', ' ', text).strip()
                if text == 'Course': # new list for new course
                    save_file.write('\n')
        save_file.close()


    def get_program_htmls():
        '''Get academic program htmls'''
        folder='program htmls/'
        try:
            homepage = open('program htmls/!program homepage.txt', 'r')
        except FileNotFoundError:
            url = 'https://reg.msu.edu/academicprograms/Programs.aspx?PType=UN'
            Setup.write_html(url, 'program htmls/!program homepage.txt')
            homepage = open('program htmls/!program homepage.txt', 'r')
        finally:
            html = homepage.read()
            homepage.close()
        if not os.path.exists(folder):
            os.makedirs(folder)
        print('Retrieving program HTML files...')
        soup = BeautifulSoup(html, 'html.parser').find_all(class_='text')
        for tag in soup:
            link = tag.get('href')
            if link == None:
                continue
            link = 'https://reg.msu.edu/academicprograms/' + link
            program = tag.text
            program = re.sub(r'\W+', ' ', program).strip()
            program = folder + program + '.txt'
            if os.path.exists(program):
                continue
            print('\tGathering {} program...'.format(program[14:-4]))
            Setup.write_html(link, program)


    def get_all():
        '''Writes all html files, csvs, etc.'''
        Setup.write_course_csv()
        Setup.get_program_htmls()