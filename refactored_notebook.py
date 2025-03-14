"""
    This module process Bureau of Labor Statistics (BLS) data into a function treemap_data_manipulation from the main-project-notebook into 
    the refactored_notebook py file.
"""
import sys
import os
import pandas as pd


# Add custom py file to directory to import functions
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
# Import custom data manipulation helper functions
from data_manipulation import get_short_names, get_df_list_final

def process_data_for_treemap(bls_data_frame,
                                hierarchical_levels=['l4', 'l3', 'l2', 'l1'],
                                filepath_excel_heirarchy='./data/bls_cpsaat39_2011_to_2015.xlsx',
                                target_metric='number_of_workers_all_sum',                                                
                                sheet_name='level_mapping_l0'
                            ):
    """
        This function imports a flat file representation of the Bureau of Labor Statistics (BLS) 
        and reformats into hierachical levels to be consumed by a treemap visual (bokeh preferred).

    """
    # import BLS hierarchy mapping to build treemap block levels.
    df_occupation_level_mapping = pd.read_excel(filepath_excel_heirarchy, sheet_name=sheet_name, header=0)
    df_occupation_level_mapping_distinct = df_occupation_level_mapping[hierarchical_levels].drop_duplicates().reset_index()
    df_occupation_level_mapping_distinct = df_occupation_level_mapping_distinct[hierarchical_levels]
    df_occupation_level_mapping_distinct

    # Define the target metric to build treemap.
    metric = target_metric # metric = 'number_of_workers_all_sum'
    # Extract base metric exclusive of sex to be used by the get_short_names(level, metric) formatting function.
    base_metric = metric.replace('_sum', '').replace('_women', '').replace('_men', '').replace('_all', '')

    # Create level 1 and level 2 dataframes for treemap block data objects.
    l1_grouping = df_level_list[0]
    l2_grouping = df_level_list[1]

    # Merge hiearchny mapping to level 1 block grouping.
    l1_grouping = pd.merge(l1_grouping,
                            df_occupation_level_mapping_distinct[['l1', 'l2']],
                            how='left',
                            left_on=['l1'],
                            right_on=['l1'])

    # Filter out the most recent year for analsyis by target metric.
    l1_grouping = l1_grouping[l1_grouping['year'] == '2015']
    l1_grouping = l1_grouping[['l1','l2', metric]]
    l2_grouping = l2_grouping[l2_grouping['year'] == '2015']
    l2_grouping = l2_grouping[['l2', metric]]

    # Get short name dictionary mapper
    short_name_l2 = get_short_names('l2', base_metric)
    # Transform BLS long name to short name for readability in treemap visual.
    l1_grouping['l2'] = l1_grouping['l2'].apply(lambda x: short_name_l2[x] if x in short_name_l2.keys() else x)
    l2_grouping['l2'] = l2_grouping['l2'].apply(lambda x: short_name_l2[x] if x in short_name_l2.keys() else x)
    # Transform BLS long name to short name for readability in treemap visual.
    short_name_l1 = get_short_names('l1', base_metric)
    l1_grouping['l1'] = l1_grouping['l1'].apply(lambda x: short_name_l1[x] if x in short_name_l1.keys() else x)

    # Compute total metric value to calculate worker percentages by level category.
    total = l2_grouping[metric].sum() # total seems low, validate later on

    # Concat percentage of workers to level labels for visual.
    l1_grouping['l1'] = l1_grouping.apply(lambda x: x['l1'] + ' | ' + str(int(round(x[metric]/total*100, 0))) + '%', axis=1)
    l2_grouping['l2'] = l2_grouping.apply(lambda x: x['l2'] + ' | ' + str(int(round(x[metric]/total*100, 0))) + '%', axis=1)
    l2_lookup = {k: k + " | " + v for k, v in (x.split(" | ") for x in l2_grouping['l2'].to_list())}
    l1_grouping['l2'] = l1_grouping.apply(lambda x: l2_lookup[x['l2']], axis=1)

    # keep only records with non-zero values, otherwise treemap will throw a divide by zero error
    l1_grouping = l1_grouping[l1_grouping[metric] > 0]
    l2_grouping = l2_grouping[l2_grouping[metric] > 0]

    return l1_grouping, l2_grouping



# target_metric='number_of_workers_all_sum'
# l1_grouping, l2_grouping = process_data_for_treemap(target_metric)

df_level_list = get_df_list_final()

print(df_level_list[0].head(5))
print(df_level_list[1].head(5))