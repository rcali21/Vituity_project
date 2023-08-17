import os
import pandas as pd
import shutil
import datetime as dt
from Utils import parse_and_save_csv, extract_msg_fields, name_concat, sum_bills

def main():
    today = dt.date.today().strftime("%d_%m_%Y")
    directory = os.chdir('../')
    df = pd.read_csv('sampledata.csv')
    target_files = ['ADT_sample.txt', 'Sample_ORU.txt', 'sampledata.csv']
    dirs_to_make = ['Archive', 'Archive/Original', 'Archive/Modified']


    for dir in dirs_to_make:
        if not os.path.exists(dir):
            os.mkdir(dir)
    for file in target_files:
        if not os.path.exists(file):
            print(f'File {file} does not exist. Ensure all files are present.')
            break
        else:
            print(f'File {file} exists. Copying file to Archive/Original/ folder...')
            shutil.copy(file, './Archive/Original/')

    
    
    adt_df = parse_and_save_csv(df, 'ADT')
    oru_df = parse_and_save_csv(df, 'ORU')

    adt_parsed = extract_msg_fields('./Archive/Original/ADT_sample.txt')

    oru_parsed = extract_msg_fields('./Archive/Original/Sample_ORU.txt')

    adt_df_from_txt = pd.concat([adt_df, pd.DataFrame([adt_parsed])], ignore_index=True)
    oru_df_from_txt = pd.concat([oru_df, pd.DataFrame([oru_parsed])], ignore_index=True)

    name_concat(adt_df_from_txt)
    name_concat(oru_df_from_txt)

    adt_df_from_txt.to_csv(f'./Archive/Modified/ADT_{today}_Modified_file.csv', index=False)
    oru_df_from_txt.to_csv(f'./Archive/Modified/ORU_{today}_Modified_file.csv', index=False)

    sum_bills(df)



if __name__ == "__main__":
    main()

