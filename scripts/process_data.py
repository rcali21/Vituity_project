import os
import pandas as pd
import shutil
import datetime as dt
from Utils import create_csv, csv_parser, extract_msg_fields, name_concat, sum_bills


def main():
    today = dt.date.today().strftime("%d_%m_%Y")
    df = pd.read_csv('../sampledata.csv')
    ADT_csv = f'./Archive/Modified/ADT_{today}_Modified_file.csv'
    ORU_csv = f'./Archive/Modified/ORU_{today}_Modified_file.csv'

    orig_files = ['ADT_sample.txt', 'Sample_ORU.txt', 'sampledata.csv']
    dirs_to_make = ['Archive', 'Archive/Original', 'Archive/Modified']
    modified_path = 'Archive/Modified'

    for dir in dirs_to_make:
        if not os.path.exists(dir):
            os.mkdir(dir)

    for file in orig_files:
        if not os.path.exists(file):
            print(f'File {file} does not exist. Ensure all files are present.')
            break
        else:
            print(f'File {file} exists. Copying file to Archive/Original/ folder...')
            shutil.copy(file, '../Archive/Original/')

    create_csv('ADT',modified_path)
    create_csv('ORU',modified_path)

    csv_parser(df, ADT_csv)
    csv_parser(df, ORU_csv)

    df_adt = pd.read_csv(ADT_csv)
    df_oru = pd.read_csv(ORU_csv)

    ORU_message = extract_msg_fields("../Archive/Original/Sample_ORU.txt")
    df_oru = df_oru.append(ORU_message, ignore_index=True)

    ADT_message = extract_msg_fields("../Archive/Original/ADT_sample.txt")
    df_adt = df_adt.append(ADT_message, ignore_index=True)

    name_concat(df_adt)
    name_concat(df_oru)

    sum_bills(df)

if __name__ == "__main__":
    main()

