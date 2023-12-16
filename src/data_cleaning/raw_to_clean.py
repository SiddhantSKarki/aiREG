import pandas as pd
import numpy as np

def clean_subject(x):
    texts = x.split('\n')
    return texts[0]
def clean_meet(x):
    s = x['MEETING SCHEDULE']
    my_list_1 = list(map(str.strip, s.split('\n')))
    list_2 = []
    if len(my_list_1) > 4:
        if '' in my_list_1:
            ind = my_list_1.index('')
            list_2 = my_list_1[ind + 1:]
            my_list_1 = my_list_1[:ind]
    if len(my_list_1) == 1:
        x['DATE'] = (my_list_1[0],list_2[0] if list_2 else np.NaN)
    for i in range(len(my_list_1)):
        if i == 0:
            x['DAY'] = (my_list_1[i],list_2[i] if list_2 else np.NaN)
        elif i == 1:
            x['TIME'] = (my_list_1[i],list_2[i] if list_2 else np.NaN)
        elif i == 2:
            x['BUILDING'] = (my_list_1[i],list_2[i] if list_2 else np.NaN)
        else:
            x['DATE'] = (my_list_1[i],list_2[i] if list_2 else np.NaN)
    del x['MEETING SCHEDULE']
    return x
def enroll_cap(x):
    text_form = x['ENROLLMENT/CAPACITY'].split('/')
    x['ENROLLMENT'] = int(text_form[0])
    x['CAPACITY'] = int(text_form[1])
    del x['ENROLLMENT/CAPACITY']
    return x



raw_df = pd.read_csv('../../raw_data/TEMP1')
raw_df['SUBJECT'] = raw_df['SUBJECT'].apply(clean_subject)
clean_df = (raw_df.apply(clean_meet, axis=1)).apply(enroll_cap, axis=1)
new_cols = ['CRN', 'TITLE', 'SECTION', 'SUBJECT', 'NUMBER', 'CAMPUS', 'CREDITHOURS', 'BUILDING', 'DATE', 'DAY', 'TIME', 'ENROLLMENT', 'CAPACITY', 'DELIVERY']
clean_df = clean_df[new_cols]
