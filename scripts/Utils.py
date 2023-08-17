import os
import pandas as pd
import datetime as dt
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

today = dt.date.today().strftime("%d_%m_%Y")


def create_csv(csv_name, destination):
        # Construct the filename
    csv_file_path = f'{csv_name}_{today}_Modified_file.csv'
    csv_full_path = os.path.join(destination, csv_file_path)
    return csv_full_path



def csv_parser(df, mod_csv):
    # Filter the input dataframe based on the message_type
    match_str = mod_csv.split("_")[0].split("/")[-1]
    message_category = df[df['message_type'].str.startswith(match_str)]
    
    # Check if mod_csv exists and has data
    if os.path.exists(mod_csv) and os.path.getsize(mod_csv) > 0:
        df_mod = pd.read_csv(mod_csv)
    else:
        # If mod_csv doesn't exist or is empty, create an empty dataframe with the same columns as df
        df_mod = pd.DataFrame(columns=df.columns)
    
    # Append the filtered data from df to df_mod
    df_mod = df_mod.append(message_category, ignore_index=True)
    
    # Save the concatenated data back to mod_csv
    df_mod.to_csv(mod_csv, index=False)


def extract_msg_fields(message):
    with open(message, 'r') as file_3:
        message = file_3.read()


        # Split the message by line
        lines = message.split('\n')
        
        # Define a dictionary to hold the extracted values
        extracted_data = {}
        
        # Extract data from PID segment
        pid_segment = [line for line in lines if line.startswith('PID')]
        if pid_segment:
            pid_fields = pid_segment[0].split('|')
            extracted_data['patient_last_name'] = pid_fields[5].split('^')[0] if len(pid_fields) > 5 else None
            extracted_data['patient_first_name'] = pid_fields[5].split('^')[1] if len(pid_fields) > 5 else None
            extracted_data['patient_middle_name'] = pid_fields[5].split('^')[2] if len(pid_fields) > 5 and len(pid_fields[5].split('^')) > 2 else None
            extracted_data['patient_address'] = pid_fields[11].split('^')[0] if len(pid_fields) > 11 else None
            extracted_data['state'] = pid_fields[11].split('^')[3] if len(pid_fields) > 11 and len(pid_fields[11].split('^')) > 3 else None
            extracted_data['account_number'] = pid_fields[3] if len(pid_fields) > 3 else None
            extracted_data['bill_amount'] = 1234
            extracted_data['date_of_service'] = today
        return extracted_data
    

def name_concat(df):
    df['patient_name'] = df['patient_last_name'] + ', ' + df['patient_first_name'] + ' ' + df['patient_middle_name']
    return df


def sum_bills(df):
    grouped_state_data = df[df['patient_state'].notna() & df['patient_state'].str.strip().ne('')]

    # Calculating the grouped sum
    grouped_sum = grouped_state_data.groupby('patient_state')['bill_amount'].sum()

    # Adding the total sum at the end
    total_sum = grouped_state_data['bill_amount'].sum()
    grouped_sum['Total'] = total_sum

    # Saving the result to a text file
    output_path = "./Archive/Modified/total_bill_sum.txt"
    grouped_sum.to_csv(output_path, header=['bill_amount'], sep='\t')