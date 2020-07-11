# step1_function
import sys
import datetime
import pandas as pd


def get_sample_df(
    excel_file, sheet='Sheet1',
    column_dict={},
    project='unkownProject',
    # the fixed patient columns --> used for renaming
    patient_cols=['PatientID', 'LastName', 'FirstName', 'DOB', 'SAP'],
    # the final patient columns --> to make everything similar
    final_patient_cols=['PatientID', 'LastName',
                        'FirstName', 'DOB', 'SAP', 'Clinix'],
    # the repeated sample columns how they appear in table
    data_cols=['Date', 'Type', 'Count', 'N2', 'DNA', 'Note'],
    final_data_cols=['Date', 'Type', 'Count',
                     'N2', 'N2removed', 'DNA', 'Note'],
    sample_type=None,  # if there are no sample_types, this is the default sample type
    time_points=[]
):

    # Load excel_file
    df = pd.read_excel(excel_file, sheet_name=sheet)
    # check columns
    timepoint_count = (len(df.columns) - len(patient_cols)) / len(data_cols)
    if timepoint_count == len(time_points):
        if timepoint_count > 1:
            print(
                f'Detected {timepoint_count} timepoints for samples --> stacking the data')
        else:
            print(
                f"Detected single timepoint --> assign {time_points[0]} for timepoint_descriptor")
    else:
        sys.exit(
            f"Error {len(time_points)} timepoints are given but data fields (length = {len(df.columns) - len(patient_cols)} do not correspond!!")

    # change fixed column names
    df.columns = patient_cols + list(df.columns[len(patient_cols):])

    # STACK THE TIMEPOINTS
    df_multiindexed = stack_df(
        df, patient_cols=patient_cols, data_cols=data_cols, time_points=time_points)

    # expand \n-stacked columns
    df_expanded = expand_cols(
        df_multiindexed, patient_cols=patient_cols + ['Timepoint'], data_cols=data_cols)

    # reset_index
    df = df_expanded.reset_index()

    ############ SAMPLE TYPE ###################
    def infer_sample_type(cellcountstr):
        if cellcountstr != cellcountstr:
            return 'PB?'
        types = []
        if 'KM' in cellcountstr:
            types.append('KM')
        if 'PB' in cellcountstr or 'GR' in cellcountstr or (('MN' in cellcountstr) and not ('KM' in cellcountstr)):
            types.append('PB')

        return '+'.join(types)

    # add sample_type, if not given in data_cols
    if not 'Type' in data_cols:
        # if sample_type is explicitely given
        if sample_type:
            df['Type'] = sample_type
        elif 'PB' in time_points:
            df['Type'] = df['Timepoint']
        else:
            df['Type'] = df['Count'].apply(infer_sample_type)

    #### DATA CONVERSIONS #####################################

    df['DOB'] = convert_date(df['DOB'])
    df['Date'] = convert_date(df['Date'])

    # check PatientID and fillin if missing
    df.loc[df['PatientID'] != df['PatientID'], 'PatientID'] = df['LastName'].str[0] + df['FirstName'].str[0] + \
        "_" + df['DOB'].astype(str).str[8:] + \
        df['DOB'].astype(str).str[5:7] + df['DOB'].astype(str).str[:4]

    if not 'Clinix' in patient_cols:
        df['Clinix'] = 'No Info'

    if not 'N2removed' in data_cols:
        df['N2removed'] = '-'

    # edit data
    df['Project'] = project

    # df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d %H:%M:%S')
    df = df[final_patient_cols + ['Project', 'Timepoint'] + final_data_cols]

    # return df
    # CLEAN SAMPLES
    df_clean = clean_rows(df)

    return df_clean


def stack_df(df, patient_cols=[], data_cols=[], time_points=[]):
    '''
    transform the horizontally stacked timepoints into single data rows
    '''

    df = df.set_index(patient_cols, append=True)
    # create MultiIndex for subsequent stacking
    df.columns = pd.MultiIndex.from_product(
        [time_points, data_cols], names=['Timepoint', None])
    df_multiindexed = df.stack(level=0)
    return df_multiindexed.reset_index().drop(columns='level_0')


def expand_cols(df, data_cols=[], patient_cols=[]):
    '''
    expands all columns that are stacked in one cell using weird \n stacking
    '''

    # set the multiindex
    df = df.set_index(patient_cols, append=True)
    expanded_df_dict = {}
    # place individual expanded dfs into dict for subsequent merging
    for col in data_cols:
        df_expanded = df[col].astype(
            'str').str.extractall(f'(?P<{col}>[^\n$]+)')
        expanded_df_dict[col] = df_expanded

    # init empty df with correct index for looped merging
    expanded_df = pd.DataFrame(index=expanded_df_dict['Date'].index)
    for col in data_cols:
        expanded_df = expanded_df.merge(
            expanded_df_dict[col], how='outer', left_index=True, right_index=True)
    # return expanded_df
    expanded_df = expanded_df.reset_index()
    expanded_df['Timepoint'] = expanded_df.apply(lambda row: row['Timepoint'] + '-' + str(
        row['match']) if row['match'] > 0 else row['Timepoint'], axis=1)
    expanded_df = expanded_df.drop(columns=['match', 'level_0'])
    return expanded_df


def clean_rows(df):
    '''
    clean N2 and Count for consumption by tubeconverter
    '''

    df['CountOrg'] = df['Count']
    df['N2org'] = df['N2']

    ######## COUNT ########################
    #######################################
    # missing info
    df.loc[:, 'Count'] = df['Count'].str.replace(r'^[-?/]$', '').str.replace(
        r'^-+', '').str.replace(r'^keine', '').str.replace(r'^nicht.*', '')

    # remove space
    df.loc[:, 'Count'] = df['Count'].str.replace(r'[ _:]', '')
    # contract ??? --> ?
    df.loc[:, 'Count'] = df['Count'].str.replace(r'\?+', '?')
    # remove leading /
    df.loc[:, 'Count'] = df['Count'].str.replace(r'^/', '')
    # remove ,;._ if not before digits
    df.loc[:, 'Count'] = df['Count'].str.replace(r'[,;.:/]([^0-9])', r'\1')

    ############### REPLACE ####################
    # Monozyten --> MN, Granulozyten --> GR
    df.loc[:, 'Count'] = df['Count'].str.replace(
        r'G[rR]a?n?u?l?o?z?y?t?e?n?', 'GR')
    df.loc[:, 'Count'] = df['Count'].str.replace('Monoz?y?t?e?n?', 'MN')
    df.loc[:, 'Count'] = df['Count'].str.replace('CAR-TCells', 'CAR-TC')
    df.loc[:, 'Count'] = df['Count'].str.replace(r'Plasma', 'Pl')
    # put MN at beginning
    df.loc[:, 'Count'] = df['Count'].str.replace('^\(?([0-9]+)', r'MN\1')

    # 2,3x10E6 --> 2,3E6
    df.loc[:, 'Count'] = df['Count'].str.replace(
        r'([0-9])[xX*](10)?[Ee]?([0-9])', r'\1E\3')
    # 2.3 --> 2,3
    df.loc[:, 'Count'] = df['Count'].str.replace(
        r'([0-9])[,;:.]([0-9])', r'\1,\2')

    # MN(5)4,4E4 --> MN4,4E4(4)
    # repl = lambda m: f"{m.group(1)}{m.group(3)}{m.group(2)}"
    df.loc[:, 'Count'] = df['Count'].str.replace(
        r'([MNKN]+)(\([1-9]+\))([0-9],?[0-9]*E[1-9])', r'\1\3\2')
    df.loc[:, 'Count'] = df['Count'].str.replace(
        r'([MNKN]+)(\([1-9]+\))\?', r'\1?\2')

    # KM PB
    # remove redundant MN
    df.loc[:, 'Count'] = df['Count'].str.replace(r'(MN[^MN]+)\(MN\)', r'\1')
    df.loc[:, 'Count'] = df['Count'].str.replace('\(?PB\)?-?', '')
    df.loc[:, 'Count'] = df['Count'].str.replace(r'\(?KM\)?-?MN', 'KM')
    df.loc[:, 'Count'] = df['Count'].str.replace(r'\(([GRKM]+)\)', 'KM')
    #df.loc[:,'Count'] = df['Count'].str.replace(r'\(PB\) ?MN', 'PB/MN')
    # (2+) --> (2)
    df.loc[:, 'Count'] = df['Count'].str.replace(r'\(?([1-9])x\)?', r'(\1)')

    df.loc[:, 'Count'] = df['Count'].str.replace(r'\nTank/', ';').astype('str')

    #######################################
    ####### CLEAN N2 ######################
    # missing info
    df.loc[:, 'N2'] = df['N2'].str.replace(r'^[-?/]$', '').str.replace(
        r'^keine', '').str.replace(r'^-+', '').str.replace(r'^nicht.*', '')
    #  -80° Freezer in GI/MM Box --> TankFreezer80BoxGMMM
    df.loc[:, 'N2'] = df['N2'].str.replace(
        '-80° Freezer in GI/MM Box', 'TankFreezer80')

    # change 99 100 to 99, 100  before space strip
    df.loc[:, 'N2'] = df['N2'].str.replace(r'([0-9]+)[ \.]+([0-9]+)', r'\1,\2')
    # remove space
    df.loc[:, 'N2'] = df['N2'].str.replace(' ', '')

    ###### REPLACE #######################

    df.loc[:, 'N2'] = df['N2'].str.replace(r'([0-9],?Box)', r'\1/Box')
    df.loc[:, 'N2'] = df['N2'].str.replace(r'([0-9],?Turm)', r'\1/Turm')
    # Tank / --> TankTW

    df.loc[:, 'N2'] = df['N2'].str.replace(r'Tank/', 'TankTW/')
    # TW/ --> TankTW
    df.loc[:, 'N2'] = df['N2'].str.replace(r'^TW/', 'TankTW/')
    # Rack --> Turm
    df.loc[:, 'N2'] = df['N2'].str.replace('Rack', 'Turm')
    # MK --> KM
    df.loc[:, 'N2'] = df['N2'].str.replace('MK', 'KM')
    # BP --> PB
    df.loc[:, 'N2'] = df['N2'].str.replace('BP', 'PB')
    # pos --> Pos
    df.loc[:, 'N2'] = df['N2'].str.replace('pos', 'Pos')

    ############## CHARS ##################
    # remove char after Pos
    df.loc[:, 'N2'] = df['N2'].str.replace(r'Pos[:,.]', 'Pos')
    # remove duplicate ,,
    df.loc[:, 'N2'] = df['N2'].str.replace(r',+', r',')

    # /N vials --> Pos ?,?,?..
    def repl(m): return f"Pos {','.join('?' *int(m.group(1)))}"
    df.loc[:, 'N2'] = df['N2'].str.replace(r'/([0-9]+)vials?', repl)
    # strip final (strings)
    df.loc[:, 'N2'] = df['N2'].str.replace(r'[^()0-9?,]+$', '')
    # remove char that is not between numbers
    df.loc[:, 'N2'] = df['N2'].str.replace(r'([0-9])[,;:]([^?\-0-9])', r'\1\2')
    df.loc[:, 'N2'] = df['N2'].str.replace(r'([^\-?0-9])[,;:]([0-9])', r'\1\2')
    df.loc[:, 'N2'] = df['N2'].str.replace(
        r'([^\-?0-9])[,;:]([^\-?0-9])', r'\1\2')

    # df.loc[:,'N2'] = df['N2'].str.replace(r'\([^(0-9].+\)$','')

    ##### POS ###########################
    # 2.3 --> 2,3
    df.loc[:, 'N2'] = df['N2'].str.replace(r'([0-9])\.([0-9])', r'\1,\2')
    # insert missing Pos
    # Box4/1,2,3 --> Box4/Pos
    df.loc[:, 'N2'] = df['N2'].str.replace(
        r'Box([0-9]+)[/:]([1-9])', r'Box\1/Pos\2')
    # Pos1-4 --> Pos1,2,3,4
    def repl(
        m): return f"Pos{','.join([str(i) for i in range(int(m.group(1)),int(m.group(2))+1)])}"
    df.loc[:, 'N2'] = df['N2'].str.replace('Pos([0-9]+)-([0-9]+)', repl)

    # (PB/MN) --> (MN)
    df.loc[:, 'N2'] = df['N2'].str.replace(r'\(PB[/-]?M?N?\)', '(MN)')
    # (PB/GR) --> (GR)
    df.loc[:, 'N2'] = df['N2'].str.replace(r'\(PB[/-]GR\)', '(GR)')
    # (MK/MN) --> (KM)
    df.loc[:, 'N2'] = df['N2'].str.replace(r'\(KM[/-]MN\)', '(KM)')
    # KM( --> (KM)
    df.loc[:, 'N2'] = df['N2'].str.replace(r'[^(]KM[^)]\(?', '(KM)')
    # (Plasma) --> (Pl)
    df.loc[:, 'N2'] = df['N2'].str.replace(r'\(Pla?s?m?a?\)', r'(Pl)')

    # remove the (MN) (Plasma) (GR) inserts
    df.loc[:, 'N2'] = df['N2'].str.replace(r'\([^0-9)]+\)', ' ')

    # rearrange cols
    cols = list(df.columns)
    new_cols = cols[:10] + ['CountOrg', 'Count', 'N2org', 'N2'] + cols[12:-2]
    # new_cols = ['PatientID', 'Project', 'N2org', 'N2']
    return df[new_cols]


def convert_date(dates):
    # convert to str and strip 00:00:00

    date_str = dates.astype(str).str.replace(
        '00:00:00', '').str.replace(' ', '')
    date_str = date_str.str.replace(
        r'.*([0-9][0-9])\.([0-9][0-9])\.([12]?[0-9]?[0-9][0-9]).*', r'\1.\2.\3')
    date_str = date_str.str.replace(
        r'.*([0-9][0-9])/([0-9][0-9])/([12]?[0-9]?[0-9][0-9]).*', r'\2.\1.\3')
    date_str = date_str.str.replace(
        r'.*([12][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9]).*', r'\3.\2.\1')
    date = pd.to_datetime(date_str, format="%d.%m.%Y",
                          exact=False, errors='coerce')
    # date = pd.to_datetime(date_str, format="%d.%m.%Y", exact=False, errors='ignore')
    return date
