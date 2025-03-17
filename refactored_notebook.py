"""
    This module process Bureau of Labor Statistics (BLS) data into a function 
    treemap_data_manipulation from the main-project-notebook into the 
    refactored_notebook py file.

    The data this module operates on is a flat representation of an occupational hierarchical.
    Ex.   Total
            Management, professional, and related
                Professional and related occupations
                    Computer and mathematical occupations
                        Mechanical Engineer
                        Archictect
                        Computer Engineer
                        etc...
"""
import sys
import os
import pandas as pd
from data_manipulation import get_short_names, get_df_list_final

def get_distinct_hierarchical_mappings(hierarchical_levels,
                                        filepath_excel_heirarchy,
                                        sheet_name):
    """
        Create a dataframe of the BLS hierarchy mapping to build treemap block levels.
        :param List<string> hierarchical_levels ->  List of levels you want to select.
        :param string filepath_excel_heirarchy -> Filepath to BLS excel file
        :param string sheet_name -> Name of the sheet were BLS levels are stored.
        :return Dataframe -> BLS Occupational Hierarchy
    """
    df_occupation_level_mapping = pd.read_excel(
                                    filepath_excel_heirarchy,
                                    sheet_name=sheet_name,
                                    header=0)
    df_occupation_level_mapping_distinct =\
          df_occupation_level_mapping[hierarchical_levels].drop_duplicates().reset_index()
    df_occupation_level_mapping_distinct =\
          df_occupation_level_mapping_distinct[hierarchical_levels]

    return df_occupation_level_mapping_distinct

def create_treemap_levels(df_level_data,
                          df_hierarchical_map,
                          level_names):
    """
        Create groupings for treemap block levels. This function only allows for 
        2 levels deep.
        :param Dataframe df_level_data -> Transactional BLS level data.
        :param Dataframe df_hierarchical_map -> BLS Hieracrchy map.
        :param List<string> level_names -> List of selected level names.
        :return Dataframe, Dataframe -> Groupings for teemap blocks
    """
    # Create level 1 and level 2 dataframes for treemap block data objects.
    l1_grouping = df_level_data[0]
    l2_grouping = df_level_data[1]

    # Merge hiearchny mapping to level 1 block grouping.
    l1_grouping = pd.merge(l1_grouping,
                            df_hierarchical_map[level_names],
                            how='left',
                            left_on=[level_names[0]],
                            right_on=[level_names[0]])

    return l1_grouping, l2_grouping

def filter_by_year_and_metric(l1_grouping,
                              l2_grouping,
                              level_names,
                              year,
                              metric):
    """
        Filter out the most recent year for analsyis by target metric.
        :param Dataframe l1_grouping -> treemap block 1 df
        :param Dataframe l1_grouping -> treemap block 2 df
        :param List<string> level_names -> List of selected level names.
        :param string year -> Filter by year
        :param string metric -> Selected metric
        :return Dataframe, Dataframe -> Filtered groupings for teemap blocks
    """
    l1_grouping = l1_grouping[l1_grouping['year'] == str(year)]
    l1_grouping = l1_grouping[level_names + [metric]]
    l2_grouping = l2_grouping[l2_grouping['year'] == str(year)]
    l2_grouping = l2_grouping[[level_names[1]] + [metric]]

    return l1_grouping, l2_grouping

def apply_short_names(l1_grouping,
                      l2_grouping,
                      level_names,
                      metric):
    """
        Swaps out the original occupational name assigned by the BLS to short hand name
        for readabiility inside the treemap visual.
        :param Dataframe l1_grouping -> treemap block 1 df
        :param Dataframe l1_grouping -> treemap block 2 df
        :param List<string> level_names -> List of selected level names.
        :param string metric -> Selected metric
        :return Dataframe, Dataframe -> Short name groupings for teemap blocks
    """
    l1 = level_names[0]
    l2 = level_names[1]
     # Extract base metric exclusive of sex to be used by the
     # get_short_names(level, metric) formatting function.
    base_metric = metric.replace('_sum', '').replace('_women', '').\
        replace('_men', '').replace('_all', '')
    # Get short name dictionary mapper
    short_name_l2 = get_short_names(l2, base_metric)
    # Transform BLS long name to short name for readability in treemap visual.
    l1_grouping[l2] = l1_grouping[l2].\
        apply(lambda x: short_name_l2[x] if x in short_name_l2.keys() else x)
    l2_grouping[l2] = l2_grouping[l2].\
        apply(lambda x: short_name_l2[x] if x in short_name_l2.keys() else x)
    # Transform BLS long name to short name for readability in treemap visual.
    short_name_l1 = get_short_names(l1, base_metric)
    l1_grouping[l1] = l1_grouping[l1].\
        apply(lambda x: short_name_l1[x] if x in short_name_l1.keys() else x)

    return l1_grouping, l2_grouping

def create_labels_for_treemap(l1_grouping,
                              l2_grouping,
                              level_names,
                              metric):
    """
        Creates treemap lables as "occupational_name | percentage_of_all_occupations" 
        and values as total number of workers.
        :param Dataframe l1_grouping -> treemap block 1 df
        :param Dataframe l1_grouping -> treemap block 2 df
        :param List<string> level_names -> List of selected level names.
        :param string metric -> Selected metric
        :return Dataframe, Dataframe -> Labeled groupings for teemap blocks        
    """
    l1 = level_names[0]
    l2 = level_names[1]
    total = l2_grouping[metric].sum() # total seems low, validate later on
    # Concat percentage of workers to level labels for visual.
    l1_grouping[l1] = l1_grouping.\
        apply(lambda x: x[l1] + ' | ' + str(int(round(x[metric]/total*100, 0))) + '%', axis=1)
    l2_grouping[l2] = l2_grouping.\
        apply(lambda x: x[l2] + ' | ' + str(int(round(x[metric]/total*100, 0))) + '%', axis=1)
    l2_lookup = {k: k + " | " + v for k, v in (x.split(" | ") for x in l2_grouping[l2].to_list())}
    l1_grouping[l2] = l1_grouping.apply(lambda x: l2_lookup[x[l2]], axis=1)
    # keep only records with non-zero values, otherwise treemap will throw a divide by zero error
    l1_grouping = l1_grouping[l1_grouping[metric] > 0]
    l2_grouping = l2_grouping[l2_grouping[metric] > 0]

    return l1_grouping, l2_grouping

if __name__ == '__main__':
    import argparse
    # Add custom py file to directory to import functions
    module_path = os.path.abspath(os.path.join('.'))
    if module_path not in sys.path:
        sys.path.append(module_path)

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='The name of the BLS excel data file.')
    parser.add_argument('sheet_name', type=str, help='The the name of the sheet to '
    '                    extract the BLS hierarchy.')
    args = parser.parse_args()

    levels = ['l4', 'l3', 'l2', 'l1']
    hierarchical_map = get_distinct_hierarchical_mappings(
                            hierarchical_levels=levels,
                            filepath_excel_heirarchy='./data/' + args.file,
                            sheet_name=args.sheet_name)

    target_levels = ['l1', 'l2']
    df_data = get_df_list_final()
    tgt_l1_grouping, tgt_l2_grouping = create_treemap_levels(
                                            df_level_data=df_data,
                                            df_hierarchical_map=hierarchical_map,
                                            level_names=target_levels)

    TARGET_METRIC = 'number_of_workers_all_sum'

    l1_grouping_filtered, l2_grouping_filtered = filter_by_year_and_metric(
                                                    l1_grouping=tgt_l1_grouping,
                                                    l2_grouping=tgt_l2_grouping,
                                                    level_names=target_levels,
                                                    year=2015,
                                                    metric=TARGET_METRIC)

    l1_grouping_short, l2_grouping_short = apply_short_names(
                                            l1_grouping=l1_grouping_filtered,
                                            l2_grouping=l2_grouping_filtered,
                                            level_names=target_levels,
                                            metric=TARGET_METRIC)

    l1_grouping_treemap, l2_grouping_treemap = create_labels_for_treemap(
                                                l1_grouping=l1_grouping_short,
                                                l2_grouping=l2_grouping_short,
                                                level_names=target_levels,
                                                metric=TARGET_METRIC)

    # Print treemap hierarchical blocks to be used in treemap visual
    print('l1_grouping_treemap:', l1_grouping_treemap)
    print('l2_grouping_treemap', l2_grouping_treemap)
