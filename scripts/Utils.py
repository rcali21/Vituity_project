import os
import pandas as pd
import datetime as dt
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

today = dt.date.today().strftime("%d_%m_%Y")


def parse_and_save_csv(df, message_type):
    parsed_df = df[df['message_type'].str.contains(message_type, na=False)]
    parsed_df.to_csv(f'./Archive/Modified/{message_type}_{today}_Modified_file.csv', index=False)
    return parsed_df



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
            ### B. ADD LAST NAME
            extracted_data['patient_last_name'] = pid_fields[5].split('^')[0] if len(pid_fields) > 5 else None
            ### ADD FIRST NAME
            extracted_data['patient_first_name'] = pid_fields[5].split('^')[1] if len(pid_fields) > 5 else None
            ### ADD MIDDLE NAME
            extracted_data['patient_middle_name'] = pid_fields[5].split('^')[2] if len(pid_fields) > 5 and len(pid_fields[5].split('^')) > 2 else None
            ### ADD ADDRESS
            extracted_data['patient_address_1'] = pid_fields[11].split('^')[0] if len(pid_fields) > 11 else None
            ### ADD STATE
            extracted_data['patient_state'] = pid_fields[11].split('^')[3] if len(pid_fields) > 11 and len(pid_fields[11].split('^')) > 3 else None
            ### ADD ACCOUNT NUMBER
            extracted_data['account_number'] = pid_fields[3] if len(pid_fields) > 3 else None
            ### ADD BILL AMOUNT AS 1234
            extracted_data['bill_amount'] = 1234
            ### C. ADD DATE OF SERVICE
            extracted_data['date_of_service'] = today
        # Extract data from GT1 segment (Guarantor information)
        gt1_segment = [line for line in lines if line.startswith('GT1')]
        if gt1_segment:
            gt1_fields = gt1_segment[0].split('|')
            extracted_data['guarantor_first_name'] = gt1_fields[3].split('^')[0] if len(gt1_fields) > 3 else None
            extracted_data['guarantor_last_name'] = gt1_fields[3].split('^')[1] if len(gt1_fields) > 3 and len(gt1_fields[3].split('^')) > 1 else None
            extracted_data['guarantor_middle_name'] = gt1_fields[3].split('^')[2] if len(gt1_fields) > 3 and len(gt1_fields[3].split('^')) > 2 else None
            extracted_data['guarantor_address_1'] = gt1_fields[5].split('^')[0] if len(gt1_fields) > 5 else None

        return extracted_data
    
def name_concat(df):
    df['patient_name'] = df['patient_last_name'] + ', ' + df['patient_first_name'] + ' ' + df['patient_middle_name']
    


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
    



    



