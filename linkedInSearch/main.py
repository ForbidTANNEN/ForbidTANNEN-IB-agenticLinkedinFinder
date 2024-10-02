import os
import pandas as pd
from linkedin_lookup_agent import lookup
from tools.tools import get_profile_url_tavily
import linkedin_lookup_agent


def safe_str(value):
    return "" if value is None else str(value)

def process_row(row):
    name = safe_str(row["First Name"]) + " " + safe_str(row["Last Name"])
    print(name)
    company = safe_str(row["Company Name"])
    emailDomain = safe_str(row["Email Domain"])
    prompt = safe_str("Linkedin") + " " + safe_str(name) + " " + safe_str(company) + " "
    if safe_str(company) == "":
        prompt += emailDomain
    print(prompt)
    linkedin_url = get_profile_url_tavily(prompt)[0]["url"]
    print(linkedin_url)
    if ("linkedin" in linkedin_url and "/in/" in linkedin_url):
        return linkedin_url
    else:
        return "CHECK " + lookup(name, company, emailDomain)

def process_in_chunks(df, chunk_size=10):
    # DataFrame to hold accumulated results
    accumulated_df = pd.DataFrame()

    # Number of chunks
    num_chunks = (len(df) + chunk_size - 1) // chunk_size

    for i in range(num_chunks):
        # Determine the slice of the DataFrame to process
        start_idx = i * chunk_size
        end_idx = min(start_idx + chunk_size, len(df))  # Adjust end index to avoid going out of bounds
        temp_df = df[start_idx:end_idx]



        # Process each row in the chunk
        temp_df['Linkedin Profile'] = temp_df.apply(process_row, axis=1)

        # Accumulate this chunk's results
        accumulated_df = pd.concat([accumulated_df, temp_df])

        # Output to a separate spreadsheet including all previous data
        output_file = f'output/output_{i+1}.xlsx'
        accumulated_df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Processed and wrote rows 0 to {end_idx} to {output_file}")
    accumulated_df.to_excel("FINAL.xlsx", index=False, engine='openpyxl')
def main():
    # Load the Excel file
    file_path = 'spreadsheets/5.xlsx'
    df = pd.read_excel(file_path)

    # Process the DataFrame in chunks
    process_in_chunks(df)

if __name__ == '__main__':
    main()
