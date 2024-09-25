import google.generativeai as genai
import os
import enum
import glob
from pathlib import Path

import typing_extensions as typing
	
class tickers(typing.TypedDict):
	    ticker:str
	    weightage:float

class Notes(typing.TypedDict):
  cik:str
  cusip: str
  notional_amount:float
  notional_amount_wofees:float
  contingent_int_rate:float
  trigger_value:float
  redemption_option: str
  guarantor:str
  payoff_underlying:str
  maturity_date:str
  strike_date:str
  payment_frequency_months:int
  underwriting_fees:float
  underwriting_fees_total:str
  summary:str
  underlying_product:str
  underlying_asset:list[tickers]
  file_name: str
  file_description: str
  asset_type:str
  issue_date:str
  call_dates:list[str]
  coupon_dates:list[str]
  estimated_value:float
  is_preliminary:bool
  isin:str
  payoff_name:str
  issuer:str
  trade_date:str
  payoff_type:str

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model1 = genai.GenerativeModel(model_name="gemini-1.5-flash")
model2 = genai.GenerativeModel('gemini-1.5-flash',
                              # Set the `response_mime_type` to output JSON response_schema=list[Recipe]
                              # Pass the schema object to the `response_schema` field
                              generation_config={"response_mime_type": "application/json",
                                                 "response_schema":Notes})
                                                 
#sample_file1 = genai.upload_file(path="/Users/sachinmistry/snotesproject/ea167766_424b2.htm")
#sample_file2 = genai.upload_file(path="/Users/sachinmistry/snotesproject/ea167798_424b2.html")
#sample_file3 = genai.upload_file(path="/Users/sachinmistry/snotesproject/ea168071_424b2.htm")
#sample_file4 = genai.upload_file(path="/Users/sachinmistry/snotesproject/jpmc.htm")
#sample_file5 = genai.upload_file(path="/Users/sachinmistry/snotesproject/ubs_424b2-13429.htm")



html_folder=Path('/Users/anujwalia/PycharmProjects/snotesproject/Anuj/Anuj_Downloads/Anuj')
for child in p.iterdir(): child
file_list=html_folder
print(len(file_list), "files found in",html_path)

# Upload all files to genai cloud
#for file in file_list:
#    genai.upload_file(path=file)
    
print(len(file_list), "files uploaded")

prompt1 = """You are a Structured Notes Prospectus document entity extraction specialist. For each document, your task is to extract the text value of the following entities:
doc ={
	"cik":"cik is the 10 digit issue identifier with leading zeroes."
	"price_per_note":" Price per Stuctured note - float datatype"
	"cusip": "cusip is the unique identifier of the Structured notes.",
	"notional_amount": "notional_amount is the principal amount of the Structured Notes Issued including fees - float datatype"
	"notional_amount_wofees": "notional_amount_wofees is the principal amount of the Structured Notes Issued without fees. - float datatype"
	"contingent_int_rate": "contingent_int_rate is the contingent Interest Rate of the Structured Notes issued - float datatype",
	"trigger_value":"is the  Interest Barrier or the Trigger Value  of the Structured Notes issued - float datatype",
	"redemption_option":"Redemption Option is Structured Notes issued be redeemed early before actual maturity, Return the name of the feature that allows this early redemption and possible values are Issuer Callable or Auto Callable",
	"guarantor":"is the guarantor of the Structured Notes Issued",
	"payoff_underlying":"is for the performance of the index within payoff.",
	"maturity_date":"is the maturity date of theStructured Notes issued - in mm/DD/yyyy format"
	"strike_date":"is the date on which underlying products were priced."
	"payment_frequency_months":"is the coupon payment frequency in months of the Structured Notes issued - integer datatype"
	"underwriting_fees":"is the amount for underwriting fees and commissions of each Structured Notes, set it to null if not found. - float datatype"
	"underwriting_fees_total":"is total amount for underwriting fees and commissions of the Structured Notes, set it to null if not found. - float datatype"
	"summary" :"short summary include payoff structure of the note, underlying, call structure and return."
	"underlying_product": ""
	"underlying_asset Asset": [
	{
	    "ticker":"Underlying ticker."
	    "weightage":"Underlying ticker weightage - float datatype"
	}]
	"file_name": "The name of the file."
	"file_description": "The description of the file"
	"asset_type": "is the financial asset class of the Underlying Product based on which the Structured Notes are issued and possible values are Equites or Rates"
	"issue_date":"the issue date of the Structured Notes in mm/DD/yyyy format"
	"call_dates": ["list of call dates of the Structured Notes in mm/DD/yyyy format"]
	"coupon_dates": ["the list of coupon dates in mm/DD/yyyy format"]
	"Coupon Frequency":"the list of coupon dates of the Structured Notes."
	"estimated_value": "is the estimated value of the Structured Notes Issued. - float datatype"
	"is_preliminary" :"is true if the document is prelilmary otherwise false - datatype boolean"
	"isin" :"the ISIN of the Structured notes."
	"payoff_name" :"Payoff name with the name of the underlying, assest class and maturity date from the heading, use mm/DD/yyyy format for the date"
	"issuer": "issuer is the name of the Issuer."
	"trade_date":"trade date of the underlying asset in mm/DD/yyyy format"
	"payoff_type":"is the type of payoff."
}

- The JSON schema must be followed during the extraction. 
- Summary to include payoff structure of the note and give the main attributes of the note like underlying, call structure and return.
- Redemption Option is Structured Notes issued be redeemed early before actual maturity, Return the name of the feature that allows this early redemption and possible values are Issuer Callable or Auto Callable
- If an entity is not found in the document, set the entity value to null.
"""

prompt2 = """You are a document entity extraction specialist. Given a document, your task is to return `Notes`. Use below additional information about entities required to be extracted. 	
    cik is the 10 digit issue identifier with leading zeroes.
    cusip is the unique identifier of the Structured notes.
	notional_amount is the principal amount of the Structured Notes Issued including fees.
	notional_amount_wofees is the principal amount of the Structured Notes Issued without fees.
	contingent_int_rate is the contingent Interest Rate of the Structured Notes issued.
	trigger_value is the  Interest Barrier or the Trigger Value  of the Structured Notes issued.
	redemption_option is Structured Notes issued be redeemed early before actual maturity, Return the name of the feature that allows this early redemption in not more than 3 words.
	guarantor is the guarantor of the Structured Notes Issued.
	payoff_underlying is for the performance of the index within payoff.
    maturity_date is the maturity date of theStructured Notes issued.
    strike_date is the date on which underlying products were priced.
    payment_frequency_months is the coupon payment frequency in months of the Structured Notes issued.
    underwriting_fees is the amount for underwriting fees and commissions of each Structured Notes, set it to null if not found.
    underwriting_fees_total is total amount for underwriting fees and commissions of the Structured Notes, set it to null if not found.
    summary is the short summary of the Structured notes.
    tickers is the unique list of Underlying ticker.
    file_name is the name of the file.
    file_description is the description of the file.
    asset_type is the financial asset class of the Underlying Product based on which the Structured Notes are issued.
    issue_date is the issue date of the Structured Notes.
    call_dates is the list of call dates of the Structured Notes.
    coupon_dates is the list of coupon dates of the Structured Notes.
    estimated_value is the estimated value of the Structured Notes Issued.
    is_preliminary is true if the document is prelilmary other wise false.
    isin is the ISIN of the Structured notes.
    payoff_name is the name of the underlying, asset class.
    issuer is the name of the Issuer.
    trade_date is the trade of the underlying asset
    payoff_type is the type of payoff.
	- If an entity is not found in the document, set the entity value to null.

	"""

for file in genai.list_files():
    #print(f"{file.display_name}, URI: {file.uri}")
    response1 = model1.generate_content([prompt1,file])
    print(response1.text)
    #response2 = model2.generate_content([prompt2,response1.text])
    #print(response2.text)
    
    
#    underlying_product is Underlying product in one sentence.

#
#```json
#{
#  "cik": "0000789019",
#  "price_per_note": null,
#  "cusip": "26054MEH0",
#  "notional_amount": 63000.0,
#  "notional_amount_wofees": null,
#  "contingent_int_rate": null,
#  "trigger_value": null,
#  "redemption_option": "Callable",
#  "guarantor": null,
#  "payoff_underlying": null,
#  "maturity_date": "02/15/2029",
#  "strike_date": null,
#  "payment_frequency_months": 6,
#  "underwriting_fees": 1.25,
#  "underwriting_fees_total": null,
#  "summary": "The Dow Chemical Company InterNotes are senior unsecured notes with a principal amount of $63,000.00. They have a coupon rate of 4.650% and are payable semi-annually. The #notes mature on 02/15/2029 and are callable at 100.000% on 8/15/2024 and any time thereafter.",
#  "underlying_product": null,
#  "underlying_asset Asset": [],
#  "file_name": "d766322d424b3.htm",
#  "file_description": "424B3",
#  "asset_type": null,
#  "issue_date": null,
#  "call_dates": [
#    "08/15/2024"
#  ],
#  "coupon_dates": [
#    "08/15/2024"
#  ],
#  "Coupon Frequency": "Semi-Annual",
#  "estimated_value": null,
#  "is_preliminary": false,
#  "isin": null,
#  "payoff_name": null,
#  "issuer": "The Dow Chemical Company",
#  "trade_date": "02/20/2024",
#  "payoff_type": null
#}
#```
#```json
#{
#    "cik": null,
#    "price_per_note": null,
#    "cusip": "34540TF72",
#    "notional_amount": 3000000000.0,
#    "notional_amount_wofees": 23990000.0,
#    "contingent_int_rate": null,
#    "trigger_value": null,
#    "redemption_option": "Callable",
#    "guarantor": null,
#    "payoff_underlying": null,
#    "maturity_date": "11/20/2026",
#    "strike_date": null,
#    "payment_frequency_months": 6,
#    "underwriting_fees": null,
#    "underwriting_fees_total": null,
#    "summary": "This is a Ford Credit Notes Series B note with a notional amount of $3 billion, a coupon rate of 6.65%, and a maturity date of November 20, 2026. It is callable at 100% on #11/20/2024 and Semi-Annually thereafter with 30 Calendar Days' Notice.",
#    "underlying_product": null,
#    "underlying_asset Asset": [],
#    "file_name": "tm2329422d6_424b2.htm",
#    "file_description": "424B2",
#    "asset_type": null,
#    "issue_date": null,
#    "call_dates": [
#        "11/20/2024"
#    ],
#    "coupon_dates": [
#        "05/20/2024"
#    ],
#    "Coupon Frequency": "Semi-Annual",
#    "estimated_value": null,
#    "is_preliminary": false,
#    "isin": null,
#    "payoff_name": null,
#    "issuer": "Ford Motor Credit Company LLC",
#    "trade_date": "11/20/2023",
#    "payoff_type": null
#}
#```
