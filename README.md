# Career Outlook
##### Find your alumni
##### Ocean's 4 (Jiehan Liu, Peihan Gao, Ning Tang, Sushan Zhao)


### Goals of the project: 
Job seekers may find it hard to assess the feasibility of their career goal. One of the many excellent resources college graduates have access to is the alumni. With similar educational background and experience, alumni association can be used as job seeker’s career assessment tool.  Our project attempts to create a web-application that assist job hunters to evaluate their career goal through alumni’s information. Based on users’ input of education backgrounds, ideal occupation position, expected salaries, our interactive web-application will match users input with alumni’s information, and visualize matching alumni’s current occupation, location of employment, career path, as a reference for users’ self-assessment.

### Git repository structure:
1. school list: process of selecting target universities
2. web scrapping:  includes LinkedIn web scraping codes 
3. data processing:  process of data analysis after getting detailed information of every alumni from LinkedIn
4. data: all the data we scraped and used in this project
5. web application - career outlook: interactive web-application code
6. notebooks: draft codes



### Main source of data:
1. Individual profiles from LinkedIn: 
  - LinkedIn: https://www.linkedin.com/
2. Occupational Wage Statistics:
  - Bureau of Labor Statistics  https://www.bls.gov/oes/current/oes_research_estimates.htm (May 2020)
3. Industry NAICS Code:
  - Bureau of Labor Statistics https://www.bls.gov/oes/2020/may/oessrci.htm
4. Company Inforamtion:
  - EBSCO Industries https://www.ebscoind.com/
5. Geographical Data:
  - Nominatim https://nominatim.org/ 
  - U.S. DEPARTMENT OF AGRICULTURE https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697

### How to run the interactive web-application 
1. Git clone the whole project to local machine 
2. Open terminal in the web application - career outlook folder 
3. Type 'python3 app.py' and enter 

### Required Python Libraries:
|Package|Version|Guideline|
|------|-------|----------|
|`numpy`|1.22.0|fundamental package for data processing|
|`pandas`|1.4.1|fundamental package for data processing and analysis|
|`geopy`|2.2.0|locates the coordinates of addresses, cities, countries, and landmarks across the globe|
|`selenium`|4.0.0|webdriver implementation for web scraping and information crawling|
|`glob`|3.10.0|finds all the pathnames matching a specified pattern |
|`os`|3.10.0|operating system for reading path and autoload files|
|`pyautogui`|0.9.53|controls the mouse and keyboard to automate interactions with other applications|
|`beautifulSoup`|4.9.0|pull data out of HTML and XML files. |
|`requests`|2.27.1|HTTP library for python to scrap and get urls|
|`time`|3.10.2|provides various time-related functions and supports for scraping|
|`random`|3.10.2|implements pseudo-random number generators for various distributions.|
|`plotly`|5.6.0|an interactive, open-source, and browser-based graphing library, visualize industries and maps|
|`dash`|2.2.0|gives a point-&-click interface to models written in Python|
|`pywebcopy`|6.3.0|supports for web scraping and archiving tool in any online website|
|`urllib`|1.26.8|collects several modules for working with URLs|
|`pickle`|0.0.12|inmplements binary protocols for serializing and de-serializing|
|`copy`|3.10.2|change one copy without changing the other|
|`datetime`|3.10.2|supplies classes for manipulating dates and times|
|`math`|3.10.2|provides access to the mathematical functions|
|`flask`|2.0.0|lightweight WSGI web application helps to complete our application|
|`json`|3.10.2|converts JSON documents|
|`matplotlib`|3.5.1|Python plotting package|


