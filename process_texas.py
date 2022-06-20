from os import listdir
from os.path import isfile, join
from pprint import pprint
import numpy as np
import pandas as pd

DATA_PATH = 'data/'
OUT_PATH = 'output/'


def preprocess_texas():
    path = DATA_PATH
    allDataFiles = [f for f in listdir(path) if (isfile(join(path, f)) and f.endswith('.txt'))]
    df = None
    #print("All data files")
    #print(allDataFiles)
    # go over all files in the data folder
    for file in allDataFiles:
        # Note: The files PUDF_base1q2006_tab.txt, PUDF_base2q2006_tab.txt, PUDF_base3q2006_tab.txt and PUDF_base4q2006_tab.txt
        # can be downloaded from https://www.dshs.texas.gov/THCIC/Hospitals/Download.shtm
        df_ = pd.read_csv(path+"/"+file, sep='\t')
        df_ = df_[['THCIC_ID', 'SEX_CODE', 'TYPE_OF_ADMISSION', 'SOURCE_OF_ADMISSION', 'LENGTH_OF_STAY', 'PAT_AGE', 'PAT_STATUS', 'RACE', 'ETHNICITY', 'TOTAL_CHARGES', 'ADMITTING_DIAGNOSIS', 'PRINC_SURG_PROC_CODE']]
        # concat data in the current file to the aggregated data
        if df is not None:
            df = pd.concat([df, df_], ignore_index=True)
        else:
            df = df_
    
    df.drop_duplicates(inplace=True)
    print(df)
    cat_attrs = ['SEX_CODE', 'TYPE_OF_ADMISSION', 'SOURCE_OF_ADMISSION', 'PAT_STATUS', 'RACE', 'ETHNICITY', 'ADMITTING_DIAGNOSIS', 'PRINC_SURG_PROC_CODE']
    df.loc[df['SEX_CODE'] == 'M', 'SEX_CODE'] = 0
    df.loc[df['SEX_CODE'] == 'F', 'SEX_CODE'] = 1
    df.loc[df['SEX_CODE'] == 'U', 'SEX_CODE'] = None
    for col in cat_attrs:
        df = df[pd.to_numeric(df[col], errors='coerce').notnull()]
        df[col] = df[col].astype('int64')
    df.dropna(inplace=True)
    for col in ['LENGTH_OF_STAY', 'PAT_AGE']:
        df[col] = df[col].astype('int64')
    df['TOTAL_CHARGES'] = df['TOTAL_CHARGES'].astype('float64')
    top_100_surgery = dict(Counter(df['PRINC_SURG_PROC_CODE']))
    top_100_surgery = sorted(top_100_surgery.items(), key=(lambda x: x[1]), reverse=True)[:100]
    top_100_surgery = [surgery[0] for surgery in top_100_surgery]
    for idx in df.index:
        if df['PRINC_SURG_PROC_CODE'][idx] not in top_100_surgery:
            df['PRINC_SURG_PROC_CODE'][idx] = None
    df.dropna(inplace=True)
    df['PRINC_SURG_PROC_CODE'] = df['PRINC_SURG_PROC_CODE'].astype('int64')
    print(df)
    for col in df.columns:
        print(col, len(set(df[col])))
    mapping = {}
    for col in cat_attrs:
        mapping[col] = {b:a for a,b in enumerate(sorted(list(Counter(df[col]).keys())))}
        for key, value in mapping[col].items():
            df.loc[df[col] == key, col] = value
    print(df)
    
    # creating the categorical attribute dictionary
    attribute_dict = {}
    for col in cat_attrs:
        if col == 'SEX_CODE':
            attribute_dict[df.columns.get_loc('SEX_CODE')] = {0: 'Male', 1: 'Female'}
        elif col == 'ETHNICITY':
            attribute_dict[df.columns.get_loc('ETHNICITY')] = {0: 'Hispanic', 1: 'Not Hispanic'}
        elif col == 'RACE':
            # note: Pacific Islander is grouped with Asian in this data set
            attribute_dict[df.columns.get_loc('RACE')] = {0: 'Native American', 1: 'Asian', 2: 'Black', 3: 'White', 4: 'Other'}
        elif col == 'PRINC_SURG_PROC_CODE':
            continue
        else:
            attribute_dict[df.columns.get_loc(col)] = {val: str(val) for val in mapping[col].values()}
    
    attribute_idx = {col: df.columns.get_loc(col) for col in set(cat_attrs).union({'THCIC_ID', 'TOTAL_CHARGES'}) - {'PRINC_SURG_PROC_CODE'}}
    pprint(attribute_idx)
    #pprint(attribute_dict)
    
    y = np.array(df['PRINC_SURG_PROC_CODE'])
    X = np.matrix(df.drop(columns='PRINC_SURG_PROC_CODE'))
    print(X.shape, y.shape)
    
    df.to_csv(OUT_PATH+'texas_100x.csv')
    
    max_attr_vals = np.max(X, axis=0)
    X = X / max_attr_vals
    max_attr_vals = np.squeeze(np.array(max_attr_vals))
    print(max_attr_vals, max_attr_vals.shape)
    
    pickle.dump(X, open(OUT_PATH+'texas_100x_features.p', 'wb'))
    pickle.dump(y, open(OUT_PATH+'texas_100x_labels.p', 'wb'))
    pickle.dump([attribute_idx, attribute_dict, max_attr_vals], open(OUT_PATH+'texas_100x_feature_desc.p', 'wb'))


if __name__ == '__main__':
    preprocess_texas()
