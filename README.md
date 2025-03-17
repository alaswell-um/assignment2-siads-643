# assignment2-siads-643


This project refactors the function treemap_data_manipulation from the main-project-notebook into 
the refactored_notebook py file.

Install project dependencies -> pip install -r requirements.txt

Containerized environment -> docker-compose up -d (Jupyter Notebook docker container enviroment) 

Run -> python refactored_notebook.py bls_cpsaat39_2011_to_2015.xlsx level_mapping_l0

Data
    - Sourced from Bureau of Labor Statistics (BLS)
    - Aggregated into an single excel file labeled bls_cpsaat09_2002_to_2015.xslx
    - Data is flat representation of an occupational hierarchical
    - Sheets 2003 - 2015 are tabular represenations of total workers per occupation by
        gender and age category.  


