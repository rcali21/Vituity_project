import datetime as dt
import warnings
import re

# pandas was complaining about append vs concat and I preferred append so ignoring the deprecation warning for now
warnings.filterwarnings("ignore", category=FutureWarning)

today = dt.date.today().strftime("%d_%m_%Y")


# function that takes in original df and message type 'ADT' or 'ORU' in our case and cross references the column in orig df
def parse_and_save_csv(df, message_type):
    parsed_df = df[df["message_type"].str.contains(message_type, na=False)]
    # ADD date to filename and wrote to csv under modified dir
    parsed_df.to_csv(
        f"./Archive/Modified/{message_type}_{today}_Modified_file.csv", index=False
    )
    return parsed_df


def extract_msg_fields(message):
    with open(message, "r") as file_3:
        message = file_3.read()

        # Split the message by line
        lines = message.split("\n")

        # Define a dictionary to hold future values
        extracted_data = {}

        # Extract data from PID portion
        pid_segment = [line for line in lines if line.startswith("PID")]
        if pid_segment:
            pid_fields = pid_segment[0].split("|")
            ### B. ADD LAST NAME --- see if more than 5 items in pid_fields and if so, split the sixth item [5] by ^
            # If there are 5 or fewer items, set to none
            extracted_data["patient_last_name"] = (
                pid_fields[5].split("^")[0] if len(pid_fields) > 5 else None
            )
            ### ADD FIRST NAME --- see if there are more than 5 items in pid_fields and if so, split the sixth item by ^
            # and take the second part as the patient's first name, else none
            extracted_data["patient_first_name"] = (
                pid_fields[5].split("^")[1] if len(pid_fields) > 5 else None
            )
            ### ADD MIDDLE NAME --- do the same as above but this time take third part else none
            extracted_data["patient_middle_name"] = (
                pid_fields[5].split("^")[2]
                if len(pid_fields) > 5 and len(pid_fields[5].split("^")) > 2
                else None
            )
            ### ADD ADDRESS --- check if there are more than 11 items pid field and split the twelfth item [11] by ^
            # and take the first part as the first line of the patient's address else fewer than 11 items none
            extracted_data["patient_address_1"] = (
                pid_fields[11].split("^")[0] if len(pid_fields) > 11 else None
            )
            ### ADD STATE --- check if there are more than 11 items in pid and if the twelfth item split by ^ has more than 3 parts
            # if so take fourth part as the patient's state else none
            extracted_data["patient_state"] = (
                pid_fields[11].split("^")[3]
                if len(pid_fields) > 11 and len(pid_fields[11].split("^")) > 3
                else None
            )
            ### ADD ACCOUNT NUMBER --- # see if there are more than 3 items in pid and take the fourth item [3] as the account number
            # if 3 or less none
            extracted_data["account_number"] = (
                pid_fields[3] if len(pid_fields) > 3 else None
            )
            ### ADD BILL AMOUNT AS 1234
            extracted_data["bill_amount"] = 1234
            ### C. ADD DATE OF SERVICE
            extracted_data["date_of_service"] = today
            # Extract email using regular expression. This will look for uppercase and lowercase and other characters directly
            # before an @ and directly after but it isn't perfect and will likely fail if an @ appears in a message elsewhere in PID seg
            email = re.search(r"[\w.-]+@[\w.-]+", pid_fields[13])
            # insert email by grouping the entire match if the re works properly
            extracted_data["patient_email_address"] = email.group(0) if email else None

        # Extract data from MSH section
        msh_segment = [line for line in lines if line.startswith("MSH")]
        if msh_segment:
            msh_fields = msh_segment[0].split("|")
            # Extract the desired values (9th field is message type & trigger event in MSH segment)
            message_type = msh_fields[8].split("^")  # Further split this field using ^
            formatted_message = "-".join(
                message_type
            )  # Join the extracted values with '-'
            extracted_data["message_type"] = formatted_message

        # Extract data from GT1 line (this is bonus info)
        gt1_segment = [line for line in lines if line.startswith("GT1")]
        if gt1_segment:
            gt1_fields = gt1_segment[0].split("|")
            # If the  list has more than 3 items, split the fourth item which is index 3 by ^ take the first part otherwise set it to None
            extracted_data["guarantor_first_name"] = (
                gt1_fields[3].split("^")[0] if len(gt1_fields) > 3 else None
            )
            # If more than 3 items and the fourth item when split by ^ has more than 1 part, take the second part otherwise set it to None
            extracted_data["guarantor_last_name"] = (
                gt1_fields[3].split("^")[1]
                if len(gt1_fields) > 3 and len(gt1_fields[3].split("^")) > 1
                else None
            )
            # If more than 3 items and the fourth item has more than 2 parts, take the third part.
            extracted_data["guarantor_middle_name"] = (
                gt1_fields[3].split("^")[2]
                if len(gt1_fields) > 3 and len(gt1_fields[3].split("^")) > 2
                else None
            )
            # If more than 5 items, split the sixth item by ^ take the first part
            extracted_data["guarantor_address_1"] = (
                gt1_fields[5].split("^")[0] if len(gt1_fields) > 5 else None
            )

        return extracted_data


# function for concatenating columns in a dataframe to make a full name
def name_concat(df):
    df["patient_name"] = (
        df["patient_last_name"]
        + ", "
        + df["patient_first_name"]
        + " "
        + df["patient_middle_name"]
    )


# function to sum the bills by state in the orig dataframe and then create a .txt file with bills by state and the total bill amount. NOTE: this ignores any rows where the state is null or empty.
def sum_bills(df):
    # not na and not empty sub dataframe
    grouped_state_data = df[
        df["patient_state"].notna() & df["patient_state"].str.strip().ne("")
    ]

    # summate the bills grouped by the patient_state
    grouped_sum = grouped_state_data.groupby("patient_state")["bill_amount"].sum()

    # Add a total sum at the end
    total_sum = grouped_state_data["bill_amount"].sum()
    grouped_sum["Total"] = total_sum

    # Save the result to .txt file this time
    output_path = "./Archive/Modified/total_bill_sum.txt"
    grouped_sum.to_csv(output_path, header=["bill_amount"], sep="\t")
