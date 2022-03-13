**This folder contains our process of data analysis after getting detailed information of every alumni from LinkedIn.**
1. '1. match industry.ipynb' is the code for matching company (we scraped from LinkedIn) with industry and NAICS code.
2. '2. match salary.ipynb' is the code for matching sector-level NAICS code, and then matching NAICS code with industry average annual salary.
3. '3. match fips-code.ipynb' is the code for matching location with fips.
4. '4. fix fips-code.ipynb' is the code for cleaning fips.
5. 'Raw OES data from U.S. BUREAU OF LABOR STATISTICS' is the industry average annual salary datasource.
6. 'industry_code_with_salary.csv' is a matching table where each industry is matched with NAICS code and industry average annual salary from above steps.
7. 'fips2county.tsv' is the data source of fips.
8. 'data' folder contains: \
   (1) 'linkedin_html' where alumni lists are downloaded from LinkedIn; \
   (2) finished alumni information of each university after implementing above data analysis codes;\
   (3) 'complete.csv' combines finished alumni information of every university into one file.
