# assignment2-siads-643


This project refactors the function treemap_data_manipulation from the main-project-notebook into 
the refactored_notebook py file.

Install project dependencies -> pip install -r requirements.txt

Containerized environment -> docker-compose up -d (Jupyter Notebook docker container enviroment) 

Data
    - Sourced from Bureau of Labor Statistics (BLS)
    - Aggregated into an single excel file labeled bls_cpsaat09_2002_to_2015.xslx
    - Data is flat representation of an occupational hierarchical
        Ex.   Total
                Management, professional, and related 
                    Professional and related occupations
                        Computer and mathematical occupations
                            Mechanical Engineer
                            Archictect
                            Computer Engineer
                            etc...
    - Sheets 2003 - 2015 are tabular represenations of total workers per occupation by
        gender and age category.  


