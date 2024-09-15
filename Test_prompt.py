import google.generativeai as genai
import os
import re



genai.configure(api_key=os.environ["GOOGLE_API_KEY "])
model = genai.GenerativeModel('gemini-1.5-flash')
#response = model.generate_content("Write a story about an AI and magic")
#print(response.text)

# list all files and remove the previous uploads to save space
for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")
#print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

    file = genai.get_file(name=file.name).delete()

#sample_file = genai.upload_file(path="./downloaded/SI-Glossary-Public-0124.pdf")
sample_file = genai.upload_file(path="EdgarTD.html")
# sample_file = genai.upload_file(path="./downloaded/womk0012_prelim.htm")
#sample_file = genai.upload_file(path="./downloaded/e13650-424b2.htm")
#sample_file1 = genai.upload_file(path="./downloaded/f530238424b2.htm")



#print("Retrieved file https://generativelanguage.googleapis.com/v1beta/files/iozqlnj3mam3")

# Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Prompt the model with text and the previously uploaded image.
#response = model.generate_content([sample_file, "Extract all relevant information in JSON format"])

extraction_prompt = """You are a document entity extraction specialist. Given a document, your task is to extract the text value of the following entities:
{
	"CUSIP": "",
	"Issuer": "",
	"Pricipal Amount": ""
	"Total Equity": ""
	"Estimated Value": ""
	"Trade Date":""
	"Underlying Asset": ""
	"Underlying Stocks": [
	{
	    "Ticker":""
	    "Weightage":""
	}]
	"Summary" :""
}

- The JSON schema must be followed during the extraction.
- If an entity is not found in the document, set the entity value to null.
"""
extraction_prompt1 = """You are a Structured Notes Prospectus document entity extraction specialist. For each document, your task is to extract the text value of the following entities:
doc ={
	"CUSIP": "",
	"Issuer": "",
	"Pricipal Amount": ""
	"Total Equity": ""
	"Estimated Value": ""
	"Trade Date":""
	"Issue Date":""
	"Maturity Date":""
	"Underlying Asset": ""
	"Amount payable at maturity":""
	"Summary" :""
	"File name": ""
}

- The JSON schema must be followed during the extraction. 
- Return a `list[doc]`
- If an entity is not found in the document, set the entity value to null.
- Remove any HTML/XML tags if they are present in the doc
"""

extraction_prompt2 = """You are a document entity extraction specialist. You need to parse the document and capture all the important terminologies listed in the document

- The terminologies can also have other equivalent terminology and will include either the text 'also called as' or 'also known as' or 'also referred as'


- You should add "/" and the equivalent terminology if only if the document explicitly mentions the words 'also called as' or 'also known as' or 'also referred as' in that definition else ignore it and print the next term
- You should not include the words 'also called as' or 'also known as' or 'also referred as' in your repsonse when you print the equivalent terminology
- You should respond with the below output format:
"term/equivalent terminology"

"""

extraction_prompt3= """You are a Structured Notes Prospectus document entity extraction specialist. For each document, your task is to extract the value associated with the following entities in the document :
doc ={
	"CUSIP": "",
	"Issuer": "",
	"Pricipal Amount": ""
	"Total Equity": ""
	"Estimated Value": ""
	"Trade Date":""
	"Issue Date":""
	"Maturity Date":""
	"Underlying Asset": ""
	"Amount payable at maturity":""
	"Summary" :""
	"File name": ""
	"Absolute Return": ""
    "Accrual Coupon": ""
    "Autocall Premium": ""
    "Autocallable/Callable": ""
    "Barrier": ""
    "Buffer Level": ""
    "Buffer Percentage": ""
    "Buffer Rate": ""
    "Bearish": ""
    "Buffer": ""
    "Call Observation Date": ""
    "Callable": ""
    "Cap": ""
    "Contingency": ""
    "Coupon": ""
    "Coupon Contingency": ""
    "Commission": ""
    "Credit Risk/Default risk": ""
    "Current Note or CD Value": ""
    "Cusip": ""
    "Deleveraged Buffer": ""
    "Determination Date": ""
    "Digital Payment": ""
    "Estimated Initial Value": ""
    "Expiration": ""
    "FDIC Insured": ""
    "Final Level": ""
    "Fixed Coupon": ""
    "Fixed Term": ""
    "Floor": ""
    "Geared Buffer": ""
    "Growth Product": ""
    "Hard Buffer": ""
    "Income Product": ""
    "Initial Level": ""
    "Intrinsic Value": ""
    Index Return" : ""
    "Investment Horizon": ""
    "Issuer": ""
    "Issuer Callable": ""
    "Issuer Protected": ""
    "Leverage": ""
    "Market Linked CD": ""
    "Market Linked Note": ""
    "Payment at Maturity": ""
    "Maximum Return": ""
    "Minimum Coupon": ""
    "Non-Call Period": ""
    "Notional Amount/Principal Amount": ""
    "Observation Date": ""
    "Payment Date": ""
    "Performance Coupon": ""
    "Principal Amount/Principal/Notional Amount": ""
    "Prospectus": ""
    "Proximity to Coupon Contingency": ""
    "Proximity to Digital Contingency": ""
    "Proximity to Protection Level": ""
    "Proximity to Current Call Level": ""
    "Risk Tolerance": ""
    "Sales Concession": ""
    "Secondary Market": ""
    "Settlement Amount": ""
    "Settlement Date": ""
    "Structured Investment": ""
    "Tenor/Maturity Date": ""
    "Total Coupons Earned": ""
    "Trade Date": ""
    "Threshold Price": ""
    "Uncapped": ""
    "Underlier": ""
    "Underlier Return": ""
    "Underwriting Discount": ""
    "Unprotected": ""
    "Upside Participation": ""
    "Downside Participation": ""
    "Volatility": ""

}

The following rules need to be followed while generating a respons :
- The JSON schema must be followed during the extraction. 
- For the terms containing "/" in the key of the above JSON format , try to check if either of those terms are present and get its value from the document.
- Do not replace mathematical signs like +  or - or * or / or % in your response with encoded string.
- In your response Replace the text '&times;' with '*' and Replace '&ndash;' replace with '-' and if you see '%2b' replace with '+'.
- Read the terms fully to understand thh context as some terms have detailed explanation in multiple lines. 
- If for any term or its section there are details of how it is calculated for each condition then list down each condition description followed by the complete text of the formula used for that calculation. If multiple caclulations conditions are present for same term , put them inside an array using [] tag containing the list of items in the format ( condition : caclulation ) and replace the '\n' with a space.
- If there is a percentage "%" sign in the entity value then include "%" sign in the value.
- If an entity is not found in the document, set the entity value to null.
- Remove all the HTML tags and XML tags in the generated text.
- Payment at maturity or the investment maturity might be explained in detailed. So include the summary for the same.
- Add a comma after each key value pair in the JSON output.

Also tell me the total principal amount
"""


response = model.generate_content([extraction_prompt3,sample_file])


print(response.text)
