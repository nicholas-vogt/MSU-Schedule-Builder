# MSU-Schedule-Builder
Create a sample 4 year schedule given a degree program.

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

    URL = 'https://reg.msu.edu/Courses/Request.aspx?
