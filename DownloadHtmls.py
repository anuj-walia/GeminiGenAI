from shutil import Error

import requests
import urllib3
import pandas as pd
from numpy.distutils.conv_template import header

DEFAULT_METADATA_FILE_TYPE = 'csv'

ARCHIVES_EDGAR_DATA = "https://www.sec.gov/Archives/edgar/data"
urllib3.disable_warnings()
PROCESSED_RECORDS_LOG= open('processed_records.csv', 'wt+')
NOT_PROCESSED_RECORDS_LOG= open('not_processed_records.csv', 'wt+')
def download(url:str):
    """
    Extracts indicative information from a prospectus using fuzzy search and Gemini AI.

    Args:
        url (str): URL of the prospectus.
    Returns:
        None
    """


    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        "User-Agent": "anujwalia.itm@gmail.com"

    }  # Add a User-Agent header to mimic a browser
    downloaded_file_name = "_".join(url.split("/")[-3:])
    try:
        response = requests.get(url, headers=headers,verify=False)
        response.raise_for_status()

        f=open(f'downloads/vignesh/{downloaded_file_name}', 'wb')
        f.write(response.content)
        f.close()
        PROCESSED_RECORDS_LOG.write(downloaded_file_name+"\n")
    except:
        NOT_PROCESSED_RECORDS_LOG.write(downloaded_file_name + "\n")

    # print(response.text)

def read_metadata_file(uri:str, file_type=DEFAULT_METADATA_FILE_TYPE,delimiter=','):
    df=pd.DataFrame()
    match file_type:
        case 'csv':
            df=pd.read_csv(uri,delimiter=delimiter,header=0,dtype=str)
        case 'excel':
            df=pd.read_excel(uri,header=0,dtype=str)
        case _:
            print('UNKNOWN FILE TYPE!! ** DATAFRAME WILL BE EMPTY **')
    return df
def process_row(row):
    print (row)
    download("%s/%s/%s/%s" % (ARCHIVES_EDGAR_DATA, row['cik'], row['some_identifier'], row['document_name']))

def validate_data_frame(dataframe:pd.DataFrame):
    if len(dataframe.columns)>=3:
        print(f'column count in metadata dataframe {len(dataframe.columns)}')
        return True
    raise Error("The metadata file is incompatible")
    return False

def main():
    # metadata_df=read_metadata_file('data/Anuj_Metadata.csv')
    metadata_df=read_metadata_file('/Users/anujwalia/PycharmProjects/snotesproject/424filenames.csv')
    if validate_data_frame(metadata_df):
        metadata_df.rename(columns={metadata_df.columns[0]: "cik"}, inplace=True)
        metadata_df.rename(columns={metadata_df.columns[1]: "some_identifier"}, inplace=True)
        metadata_df.rename(columns={metadata_df.columns[2]: "document_name"}, inplace=True)

        metadata_df.apply(process_row,axis=1)
        PROCESSED_RECORDS_LOG.close()
        NOT_PROCESSED_RECORDS_LOG.close()
        print('finish')

# cik = "947263"
# some_identifier = "000114036124031123"
# document_name = "ef20031597_424b2.htm"
# download("%s/%s/%s/%s" % (ARCHIVES_EDGAR_DATA, cik, some_identifier, document_name))
# # extracted_info = extract_information("./EdgarTD.html", target_keywords)


if __name__ == "__main__":
         main()