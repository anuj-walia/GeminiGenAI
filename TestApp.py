import google.generativeai as genai
import os
import requests

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
print(GOOGLE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
sample_file = genai.upload_file(path="EdgarTD.html",

                                display_name="EdgarTDTest.html")

# print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
#
# file = genai.get_file(name=sample_file.name)
# print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

# response = model.generate_content([sample_file, "As a structured Notes trader, find all indicative financial "
#                                                 "data for the newly issued structured note mentioned in the given document and write in csv format"])


response_with_uploaded_docs = model.generate_content(["As a structured Notes trader, find all indicative financial "
                                                "data for the newly issued structured note mentioned "
                                                 "in the given document and write in csv format",
                                                 sample_file,sample_file,sample_file])

response_with_passing_doc_content= model.generate_content("As a structured Notes trader, find all indicative financial "
                                                "data for the newly issued structured note mentioned "
                                                 "in the given document and write in csv format")
print(response_with_uploaded_docs.text)
print(response_with_uploaded_docs.text)

def get_web_content(url):
    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        "User-Agent": "anujwalia.itm@gmail.com"

    }  # Add a User-Agent header to mimic a browser
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text
